"use client";

import { useEffect, useState } from "react";
import { CodeMirror } from "./code-mirror";
import { touristStateAt, TouristLog } from "@/lib/tourist";
import { formatMsPrecise } from "@/lib/templates";
import { cn } from "@/lib/utils";

export function TouristPane({
  eventId,
  problemId,
  touristTimeMs,
  clockMs,
}: {
  eventId: string;
  problemId: string;
  touristTimeMs: number | null;
  clockMs: number; // race clock; negative during countdown
}) {
  const [log, setLog] = useState<TouristLog | null | undefined>(undefined);

  useEffect(() => {
    let cancelled = false;
    fetch(`/api/tourist/${problemId}?eventId=${eventId}`, { cache: "force-cache" })
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => !cancelled && setLog(d))
      .catch(() => !cancelled && setLog(null));
    return () => {
      cancelled = true;
    };
  }, [eventId, problemId]);

  const solveMs = log?.solveMs ?? touristTimeMs;
  const ghost = log ? touristStateAt(log, clockMs) : null;
  const solved = solveMs !== null && clockMs >= solveMs;

  return (
    <div className="flex h-full flex-col border-l border-border/60">
      <div
        className={cn(
          "flex items-center gap-2 border-b border-border/60 px-4 py-2",
          solved ? "bg-green-500/15" : "bg-primary/10"
        )}
      >
        <span className="text-lg">🇧🇾</span>
        <span className="font-bold">tourist</span>
        <span className="ml-auto font-mono text-lg tabular-nums">
          {solved && solveMs !== null ? (
            <span className="font-bold text-green-400">
              AC {formatMsPrecise(solveMs)}
            </span>
          ) : clockMs < 0 ? (
            "at the start line…"
          ) : solveMs !== null ? (
            formatMsPrecise(Math.min(clockMs, solveMs))
          ) : (
            "—"
          )}
        </span>
      </div>
      <div className="min-h-0 flex-1">
        {log && ghost ? (
          <CodeMirror code={ghost.code} lang={ghost.lang ?? log.lang} fontSize={14} />
        ) : (
          <div className="flex h-full flex-col items-center justify-center gap-2 p-6 text-center">
            {log === undefined ? (
              <p className="animate-pulse text-muted-foreground">Loading ghost…</p>
            ) : solveMs !== null ? (
              <>
                <p className="font-mono text-5xl font-black tabular-nums">
                  {solved ? "SOLVED" : formatMsPrecise(Math.max(0, solveMs - Math.max(0, clockMs)))}
                </p>
                <p className="text-muted-foreground">
                  {solved
                    ? `tourist finished in ${formatMsPrecise(solveMs)}`
                    : "until tourist finishes this problem"}
                </p>
              </>
            ) : (
              <p className="text-muted-foreground">No tourist data for this problem.</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
