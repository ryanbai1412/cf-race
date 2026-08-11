"use client";

import { useEffect, useState } from "react";
import { useEventState } from "@/hooks/use-event-state";
import { TouristName } from "./racer-column";
import { StatementPane } from "@/components/race/statement-pane";
import { formatMsPrecise } from "@/lib/templates";
import { flagEmoji } from "@/lib/countries";
import { cn } from "@/lib/utils";
import type { GennaLeaderboardRow } from "@/app/api/leaderboard/genna/route";
import type { Problem } from "@/lib/types";

/**
 * The left monitor: RACE tourist leaderboard (best deltas vs Genna) on the
 * left half, the active/last problem statement on the right half.
 */
export function LeftMonitor({ eventId }: { eventId: string }) {
  const { state, serverNow } = useEventState(eventId);
  const [rows, setRows] = useState<GennaLeaderboardRow[]>([]);
  const [, forceTick] = useState(0);

  useEffect(() => {
    const iv = setInterval(() => forceTick((n) => n + 1), 500);
    return () => clearInterval(iv);
  }, []);

  useEffect(() => {
    let cancelled = false;
    const load = () =>
      fetch(`/api/leaderboard/genna?eventId=${eventId}`, { cache: "no-store" })
        .then((r) => (r.ok ? r.json() : null))
        .then((d) => !cancelled && d && setRows(d.rows))
        .catch(() => {});
    void load();
    const iv = setInterval(load, 10000);
    return () => {
      cancelled = true;
      clearInterval(iv);
    };
  }, [eventId]);

  if (!state) {
    return (
      <main className="flex h-screen items-center justify-center">
        <p className="animate-pulse font-mono text-sm text-muted-foreground">
          Connecting…
        </p>
      </main>
    );
  }

  const race = state.race;
  const startMs = race?.started_at ? new Date(race.started_at).getTime() : null;
  // Fairness: keep the statement hidden until the race clock hits zero.
  const countdown = startMs !== null && serverNow() < startMs;
  const problem: Problem | null = race?.problem ?? state.lastRace?.problem ?? null;
  const reviewing = !race && state.lastRace;

  return (
    <main className="grid h-screen grid-cols-2 bg-background">
      <section className="flex min-h-0 flex-col border-r border-border/60">
        <header className="border-b border-border/60 bg-card/50 px-8 py-5">
          <h1 className="font-mono text-5xl font-black tracking-tight">
            RACE <TouristName />
          </h1>
          <p className="mt-1 font-mono text-sm uppercase tracking-[0.3em] text-muted-foreground">
            best solve times vs a legendary competitive programmer
          </p>
        </header>
        <div className="min-h-0 flex-1 overflow-hidden px-6 py-4">
          {rows.length === 0 ? (
            <div className="flex h-full flex-col items-center justify-center gap-2 text-center">
              <p className="text-2xl font-bold text-muted-foreground">
                No one has beaten <TouristName /> yet.
              </p>
              <p className="text-xl text-muted-foreground/70">Be the first.</p>
            </div>
          ) : (
            <div className="space-y-1.5">
              <div className="flex items-center gap-4 px-4 font-mono text-xs uppercase tracking-widest text-muted-foreground">
                <span className="w-8">#</span>
                <span className="flex-1">contestant</span>
                <span className="w-20">problem</span>
                <span className="w-24 text-right">time</span>
                <span className="w-24 text-right">tourist</span>
                <span className="w-24 text-right">delta</span>
              </div>
              {rows.slice(0, 12).map((r, i) => (
                <div
                  key={`${r.contestant_id}:${r.problem_id}`}
                  className={cn(
                    "flex items-center gap-4 rounded-md px-4 py-2.5",
                    r.delta_ms <= 0 && "bg-green-500/10"
                  )}
                >
                  <span className="w-8 font-mono text-lg text-muted-foreground">
                    {i + 1}
                  </span>
                  <span className="flex flex-1 items-center gap-3 truncate">
                    <span className="text-2xl">
                      {r.country ? flagEmoji(r.country) : "🏳️"}
                    </span>
                    <span className="truncate text-xl font-bold">{r.name}</span>
                  </span>
                  <span className="w-20 font-mono text-lg text-primary">
                    {r.problem_id}
                  </span>
                  <span className="w-24 text-right font-mono text-lg tabular-nums">
                    {formatMsPrecise(r.solve_ms)}
                  </span>
                  <span className="w-24 text-right font-mono text-lg tabular-nums text-muted-foreground">
                    {formatMsPrecise(r.genna_ms)}
                  </span>
                  <span
                    className={cn(
                      "w-24 text-right font-mono text-lg font-bold tabular-nums",
                      r.delta_ms <= 0 ? "text-green-400" : "text-red-400"
                    )}
                  >
                    {r.delta_ms <= 0 ? "−" : "+"}
                    {formatMsPrecise(Math.abs(r.delta_ms))}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      <section className="relative flex min-h-0 flex-col">
        {problem ? (
          <>
            <header className="flex items-center gap-3 border-b border-border/60 bg-card/50 px-6 py-3">
              <span className="font-mono text-2xl font-black text-primary">
                {problem.id}
              </span>
              <span className="truncate text-lg font-bold">{problem.name}</span>
              {reviewing && (
                <span className="ml-auto rounded bg-muted px-2 py-0.5 font-mono text-xs uppercase tracking-widest text-muted-foreground">
                  last race
                </span>
              )}
            </header>
            <div className="min-h-0 flex-1">
              <StatementPane problem={problem} />
            </div>
            {countdown && (
              <div className="absolute inset-0 z-10 flex items-center justify-center bg-background/95 backdrop-blur">
                <p className="font-mono text-4xl font-black text-muted-foreground">
                  statement revealed at GO
                </p>
              </div>
            )}
          </>
        ) : (
          <div className="flex h-full items-center justify-center">
            <p className="font-mono text-xl text-muted-foreground">
              Waiting for the first race…
            </p>
          </div>
        )}
      </section>
    </main>
  );
}
