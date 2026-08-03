"use client";

import { useEffect, useState } from "react";
import { flagEmoji } from "@/lib/countries";
import { formatMsPrecise } from "@/lib/templates";
import { cn } from "@/lib/utils";

export type LeaderboardRow = {
  contestant_id: string;
  name: string;
  country: string | null;
  solve_ms: number;
  problem_id: string;
};

export function LeaderboardTable({
  eventId,
  problemId,
  touristTimeMs,
  highlightContestantId,
  limit = 10,
  refreshKey,
  size = "default",
}: {
  eventId: string;
  problemId?: string;
  touristTimeMs?: number | null;
  highlightContestantId?: string;
  limit?: number;
  refreshKey?: unknown;
  size?: "default" | "lg";
}) {
  const [rows, setRows] = useState<LeaderboardRow[]>([]);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      const qs = new URLSearchParams({ eventId });
      if (problemId) qs.set("problemId", problemId);
      const res = await fetch(`/api/leaderboard?${qs}`, { cache: "no-store" });
      if (res.ok && !cancelled) setRows((await res.json()).rows);
    }
    void load();
    const iv = setInterval(load, 10000);
    return () => {
      cancelled = true;
      clearInterval(iv);
    };
  }, [eventId, problemId, refreshKey]);

  type Entry = LeaderboardRow & { tourist?: boolean };
  const entries: Entry[] = [...rows];
  if (touristTimeMs != null) {
    const ghost: Entry = {
      contestant_id: "__tourist__",
      name: "tourist",
      country: "BY",
      solve_ms: touristTimeMs,
      problem_id: problemId ?? "",
      tourist: true,
    };
    entries.push(ghost);
    entries.sort((a, b) => a.solve_ms - b.solve_ms);
  }

  const highlightIdx = entries.findIndex(
    (e) => e.contestant_id === highlightContestantId
  );
  const top = entries.slice(0, limit);
  const showAppended = highlightIdx >= limit;

  const lg = size === "lg";

  function Row({ e, rank }: { e: Entry; rank: number }) {
    const delta = touristTimeMs != null && !e.tourist ? e.solve_ms - touristTimeMs : null;
    return (
      <div
        className={cn(
          "flex items-center gap-3 rounded-md px-3 py-2",
          lg && "gap-4 px-4 py-3",
          e.tourist && "bg-primary/10 text-primary",
          e.contestant_id === highlightContestantId &&
            "bg-green-500/10 ring-1 ring-green-500/40"
        )}
      >
        <span className={cn("w-8 font-mono text-sm text-muted-foreground", lg && "w-12 text-xl")}>
          #{rank}
        </span>
        <span className={cn("text-lg", lg && "text-3xl")}>
          {e.country ? flagEmoji(e.country) : "🏳️"}
        </span>
        <span className={cn("truncate font-medium", e.tourist && "font-bold", lg && "text-2xl")}>
          {e.name}
        </span>
        <span className={cn("ml-auto font-mono tabular-nums", lg && "text-2xl")}>
          {formatMsPrecise(e.solve_ms)}
        </span>
        {delta !== null && (
          <span
            className={cn(
              lg ? "w-24 text-right font-mono text-base tabular-nums" : "w-16 text-right font-mono text-xs tabular-nums",
              delta <= 0 ? "text-green-400" : "text-red-400"
            )}
          >
            {delta <= 0 ? "−" : "+"}
            {formatMsPrecise(Math.abs(delta))}
          </span>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-1">
      {top.map((e, i) => (
        <Row key={e.contestant_id} e={e} rank={i + 1} />
      ))}
      {showAppended && (
        <>
          <p className="px-3 py-1 font-mono text-xs text-muted-foreground">⋯</p>
          <Row e={entries[highlightIdx]} rank={highlightIdx + 1} />
        </>
      )}
      {entries.length === 0 && (
        <p className="px-3 py-2 text-sm text-muted-foreground">No solves yet — be the first!</p>
      )}
    </div>
  );
}
