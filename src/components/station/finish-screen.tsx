"use client";

import { useEffect } from "react";
import confetti from "canvas-confetti";
import { LeaderboardTable } from "@/components/leaderboard-table";
import { formatMsPrecise } from "@/lib/templates";
import { flagEmoji } from "@/lib/countries";
import type { Contestant, Problem } from "@/lib/types";
import { cn } from "@/lib/utils";

export function FinishScreen({
  eventId,
  problem,
  contestant,
  solveMs,
  rival,
  rivalSolveMs,
  rivalStillRacing,
}: {
  eventId: string;
  problem: Problem;
  contestant: Contestant;
  solveMs: number | null; // null = DNF
  rival: Contestant | undefined;
  rivalSolveMs: number | null;
  rivalStillRacing: boolean;
}) {
  const solved = solveMs !== null;

  useEffect(() => {
    if (!solved) return;
    const burst = (x: number) =>
      confetti({ particleCount: 120, spread: 75, origin: { x, y: 0.6 } });
    burst(0.3);
    burst(0.7);
    const t = setTimeout(() => burst(0.5), 400);
    return () => clearTimeout(t);
  }, [solved]);

  const rivalDelta =
    solveMs !== null && rivalSolveMs !== null ? solveMs - rivalSolveMs : null;
  const touristDelta =
    solveMs !== null && problem.tourist_time_ms != null
      ? solveMs - problem.tourist_time_ms
      : null;

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-8 px-6 py-10">
      <div className="text-center">
        <h1
          className={cn(
            "font-mono text-6xl font-black tracking-tight",
            solved ? "text-green-400" : "text-muted-foreground"
          )}
        >
          {solved ? "ACCEPTED" : "TIME'S UP"}
        </h1>
        {solved && (
          <p className="mt-4 font-mono text-7xl font-bold tabular-nums">
            {formatMsPrecise(solveMs)}
          </p>
        )}
        <div className="mt-4 flex items-center justify-center gap-6 font-mono text-lg">
          {rival && (
            <span>
              vs {rival.name} {rival.country ? flagEmoji(rival.country) : ""}:{" "}
              {rivalStillRacing ? (
                <span className="text-amber-400">still racing…</span>
              ) : rivalDelta === null ? (
                solved ? (
                  <span className="text-green-400">you solved it, they didn&apos;t</span>
                ) : rivalSolveMs !== null ? (
                  <span className="text-red-400">
                    solved in {formatMsPrecise(rivalSolveMs)}
                  </span>
                ) : (
                  <span className="text-muted-foreground">
                    didn&apos;t solve it either
                  </span>
                )
              ) : (
                <span className={rivalDelta <= 0 ? "text-green-400" : "text-red-400"}>
                  {rivalDelta <= 0 ? "−" : "+"}
                  {formatMsPrecise(Math.abs(rivalDelta))}
                </span>
              )}
            </span>
          )}
          {touristDelta !== null && problem.tourist_time_ms != null && (
            <span className="text-muted-foreground">
              tourist 🇧🇾 {" "}
              <span className="text-foreground tabular-nums">
                {formatMsPrecise(problem.tourist_time_ms)}
              </span>{" "}
              ·{" "}
              <span className={touristDelta <= 0 ? "text-green-400" : "text-red-400"}>
                {touristDelta <= 0 ? "−" : "+"}
                {formatMsPrecise(Math.abs(touristDelta))}
              </span>
            </span>
          )}
        </div>
      </div>

      <div className="w-full max-w-xl">
        <h2 className="mb-2 text-center font-mono text-xs uppercase tracking-widest text-muted-foreground">
          Fastest solves — {problem.name}
        </h2>
        <LeaderboardTable
          eventId={eventId}
          problemId={problem.id}
          touristTimeMs={problem.tourist_time_ms}
          highlightContestantId={contestant.id}
        />
      </div>
      <p className="font-mono text-sm text-muted-foreground">
        Next racers — see the staff!
      </p>
    </main>
  );
}
