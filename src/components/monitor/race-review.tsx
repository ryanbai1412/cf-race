"use client";

import { LeaderboardTable } from "@/components/leaderboard-table";
import { TouristName } from "./racer-column";
import { formatMsPrecise } from "@/lib/templates";
import { flagEmoji } from "@/lib/countries";
import { cn } from "@/lib/utils";
import type { ClientState } from "@/lib/types";

type ReviewRace = NonNullable<ClientState["lastRace"]>;

type RankedRacer = {
  key: string;
  name: React.ReactNode;
  flag: string | null;
  solveMs: number | null;
};

/** Rank the three racers of a finished race: AC by time, DNFs last. */
export function rankRacers(race: ReviewRace): RankedRacer[] {
  const startMs = race.started_at ? new Date(race.started_at).getTime() : 0;
  const racers: RankedRacer[] = race.participants.map((p) => {
    const info = race.contestants[p.contestant_id];
    return {
      key: p.contestant_id,
      name: info?.name ?? (p.station_role === "station1" ? "Contestant A" : "Contestant B"),
      flag: info?.country ? flagEmoji(info.country) : "🏳️",
      solveMs: p.first_ac_at ? new Date(p.first_ac_at).getTime() - startMs : null,
    };
  });
  racers.push({
    key: "genna",
    name: <TouristName />,
    flag: null,
    solveMs: race.gennaSolveMs,
  });
  return racers.sort((a, b) => {
    if (a.solveMs === null && b.solveMs === null) return 0;
    if (a.solveMs === null) return 1;
    if (b.solveMs === null) return -1;
    return a.solveMs - b.solveMs;
  });
}

const MEDALS = ["🥇", "🥈", "🥉"];

/**
 * GAME OVER review: this race's ranking on the left, all-time best times
 * for the problem on the right. Shared by the right monitor and stations.
 */
export function RaceReview({
  eventId,
  race,
  size = "default",
}: {
  eventId: string;
  race: ReviewRace;
  size?: "default" | "lg";
}) {
  const ranked = rankRacers(race);
  const lg = size === "lg";
  return (
    <div className="flex min-h-0 flex-1 flex-col">
      <header className="border-b border-border/60 bg-card/50 px-8 py-4 text-center">
        <p className={cn("font-mono font-black tracking-tight", lg ? "text-6xl" : "text-4xl")}>
          GAME OVER
        </p>
        <p className="mt-1 font-mono text-lg text-muted-foreground">
          <span className="font-bold text-primary">{race.problem_id}</span>{" "}
          {race.problem.name}
        </p>
      </header>
      <div className="grid min-h-0 flex-1 grid-cols-2">
        <div className="flex flex-col justify-center gap-4 border-r border-border/60 px-10">
          {ranked.map((r, i) => (
            <div
              key={r.key}
              className={cn(
                "flex items-center gap-4 rounded-lg border border-border/60 px-6 py-4",
                i === 0 && r.solveMs !== null && "border-green-500/40 bg-green-500/10"
              )}
            >
              <span className={lg ? "text-5xl" : "text-3xl"}>{MEDALS[i] ?? ""}</span>
              {r.flag && <span className={lg ? "text-4xl" : "text-2xl"}>{r.flag}</span>}
              <span className={cn("truncate font-bold", lg ? "text-3xl" : "text-xl")}>
                {r.name}
              </span>
              <span
                className={cn(
                  "ml-auto font-mono font-bold tabular-nums",
                  lg ? "text-3xl" : "text-xl",
                  r.solveMs === null && "text-muted-foreground"
                )}
              >
                {r.solveMs !== null ? formatMsPrecise(r.solveMs) : "—"}
              </span>
              {r.key !== "genna" &&
                r.solveMs !== null &&
                race.gennaSolveMs !== null && (
                  <span
                    className={cn(
                      "font-mono tabular-nums",
                      lg ? "text-xl" : "text-sm",
                      r.solveMs - race.gennaSolveMs <= 0
                        ? "text-green-400"
                        : "text-red-400"
                    )}
                  >
                    {r.solveMs - race.gennaSolveMs <= 0 ? "−" : "+"}
                    {formatMsPrecise(Math.abs(r.solveMs - race.gennaSolveMs))}
                  </span>
                )}
            </div>
          ))}
        </div>
        <div className="flex flex-col justify-center px-10">
          <h2 className="mb-4 text-center font-mono text-sm uppercase tracking-[0.4em] text-muted-foreground">
            All-time fastest — {race.problem_id}
          </h2>
          <LeaderboardTable
            eventId={eventId}
            problemId={race.problem_id}
            touristTimeMs={race.gennaSolveMs}
            limit={8}
            size={size}
          />
        </div>
      </div>
    </div>
  );
}
