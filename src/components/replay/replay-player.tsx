"use client";

import { useEffect, useRef, useState } from "react";
import { CodeMirror } from "@/components/monitor/code-mirror";
import { touristStateAt, TouristLog } from "@/lib/tourist";
import { formatMsPrecise } from "@/lib/templates";
import { flagEmoji } from "@/lib/countries";
import { Button } from "@/components/ui/button";
import { Pause, Play, RotateCcw } from "lucide-react";
import { cn } from "@/lib/utils";

type ReplayLog = TouristLog & {
  contestant: { name: string; country: string | null } | null;
  timerSec: number;
};

const SPEEDS = [1, 2, 4, 8];

export function ReplayPlayer({
  eventId,
  raceId,
  station,
}: {
  eventId: string;
  raceId: string;
  station: string;
}) {
  const [log, setLog] = useState<ReplayLog | null | undefined>(undefined);
  const [clockMs, setClockMs] = useState(0);
  const [playing, setPlaying] = useState(true);
  const [speed, setSpeed] = useState(1);
  const raf = useRef<number>();
  const last = useRef<number>(0);

  useEffect(() => {
    fetch(`/api/replay?eventId=${eventId}&raceId=${raceId}&station=${station}`, {
      cache: "no-store",
    })
      .then((r) => (r.ok ? r.json() : null))
      .then(setLog)
      .catch(() => setLog(null));
  }, [eventId, raceId, station]);

  const durationMs = log
    ? Math.max(
        log.solveMs ?? 0,
        log.events.length ? log.events[log.events.length - 1].t : 0,
        1000
      )
    : 0;

  useEffect(() => {
    if (!playing || !log) return;
    last.current = performance.now();
    const tick = (now: number) => {
      const dt = (now - last.current) * speed;
      last.current = now;
      setClockMs((c) => {
        const next = c + dt;
        if (next >= durationMs) {
          setPlaying(false);
          return durationMs;
        }
        return next;
      });
      raf.current = requestAnimationFrame(tick);
    };
    raf.current = requestAnimationFrame(tick);
    return () => {
      if (raf.current) cancelAnimationFrame(raf.current);
    };
  }, [playing, speed, durationMs, log]);

  if (log === undefined) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <p className="animate-pulse font-mono text-muted-foreground">Loading replay…</p>
      </main>
    );
  }
  if (log === null) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <p className="font-mono text-muted-foreground">No replay found for this race.</p>
      </main>
    );
  }

  const state = touristStateAt(log, clockMs);
  const solved = log.solveMs !== null && clockMs >= log.solveMs;
  let lastVerdict: string | null = null;
  let pendingSubmit = false;
  for (const ev of log.events) {
    if (ev.t > clockMs) break;
    if (ev.type === "submit") {
      pendingSubmit = true;
      lastVerdict = null;
    } else if (ev.type === "verdict") {
      pendingSubmit = false;
      lastVerdict = ev.verdict;
    }
  }
  const markers = log.events.filter((ev) => ev.type !== "snapshot");

  return (
    <main className="flex h-screen flex-col bg-background">
      <header
        className={cn(
          "flex items-center gap-3 border-b border-border/60 px-5 py-3",
          solved ? "bg-green-500/15" : "bg-primary/10"
        )}
      >
        {log.contestant?.country && (
          <span className="text-2xl">{flagEmoji(log.contestant.country)}</span>
        )}
        <span className="text-lg font-bold">
          {log.contestant?.name ?? station}
        </span>
        <span className="font-mono text-sm text-muted-foreground">
          {log.problemId} · replay
        </span>
        <span className="ml-auto flex items-center gap-3">
          {pendingSubmit && (
            <span className="animate-pulse rounded bg-amber-500/20 px-2 py-0.5 font-mono text-xs text-amber-400">
              Judging…
            </span>
          )}
          {lastVerdict && (
            <span
              className={cn(
                "rounded px-2 py-0.5 font-mono text-xs",
                lastVerdict === "AC"
                  ? "bg-green-500/20 text-green-400"
                  : "bg-red-500/20 text-red-400"
              )}
            >
              {lastVerdict}
            </span>
          )}
        </span>
        <span className="font-mono text-xl tabular-nums">
          {solved && log.solveMs !== null ? (
            <span className="font-bold text-green-400">
              AC {formatMsPrecise(log.solveMs)}
            </span>
          ) : (
            formatMsPrecise(clockMs)
          )}
        </span>
      </header>

      <div className="min-h-0 flex-1">
        <CodeMirror code={state.code} lang={log.lang} />
      </div>

      <footer className="flex items-center gap-3 border-t border-border/60 px-5 py-3">
        <Button
          size="icon"
          variant="secondary"
          onClick={() => {
            if (clockMs >= durationMs) setClockMs(0);
            setPlaying((p) => !p);
          }}
        >
          {playing ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
        </Button>
        <Button
          size="icon"
          variant="ghost"
          onClick={() => {
            setClockMs(0);
            setPlaying(true);
          }}
        >
          <RotateCcw className="h-4 w-4" />
        </Button>
        <div className="relative flex-1">
          <input
            type="range"
            className="w-full accent-primary"
            value={clockMs}
            min={0}
            max={durationMs}
            step={100}
            onChange={(e) => setClockMs(Number(e.target.value))}
          />
          {markers.map((ev, i) => (
            <span
              key={i}
              title={
                ev.type === "submit"
                  ? `Submitted ${formatMsPrecise(ev.t)}`
                  : `${ev.verdict} ${formatMsPrecise(ev.t)}`
              }
              className={cn(
                "pointer-events-auto absolute top-0 h-1.5 w-1.5 -translate-x-1/2 rounded-full",
                ev.type === "submit"
                  ? "bg-amber-400"
                  : ev.verdict === "AC"
                    ? "bg-green-400"
                    : "bg-red-400"
              )}
              style={{ left: `${(ev.t / durationMs) * 100}%` }}
            />
          ))}
        </div>
        <div className="flex gap-1">
          {SPEEDS.map((s) => (
            <Button
              key={s}
              size="sm"
              variant={speed === s ? "default" : "ghost"}
              className="font-mono"
              onClick={() => setSpeed(s)}
            >
              {s}×
            </Button>
          ))}
        </div>
      </footer>
    </main>
  );
}
