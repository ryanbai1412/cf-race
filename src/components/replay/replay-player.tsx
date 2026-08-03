"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { CodeMirror } from "@/components/monitor/code-mirror";
import { touristStateAt, TouristLog, type RunSummary } from "@/lib/tourist";
import { formatMsPrecise } from "@/lib/templates";
import { flagEmoji } from "@/lib/countries";
import { Button } from "@/components/ui/button";
import { ChevronDown, ChevronRight, Pause, Play, RotateCcw } from "lucide-react";
import { cn } from "@/lib/utils";

/** TouristLog with a possibly-null solve time (DNF runs/races). */
export type ReplayableLog = Omit<TouristLog, "solveMs"> & {
  solveMs: number | null;
};

type ReplayLog = ReplayableLog & {
  contestant: { name: string; country: string | null } | null;
  timerSec: number;
};

const SPEEDS = [1, 2, 4, 8];

/** One run/compile/submission moment shown in the replay activity list. */
type ActivityItem = {
  t: number;
  label: string;
  verdict: string;
  verdictT?: number; // when the verdict became known (submissions)
  run?: RunSummary;
};

function verdictColor(verdict: string): string {
  if (verdict === "AC") return "bg-green-500/20 text-green-400";
  if (verdict === "PENDING") return "bg-amber-500/20 text-amber-400";
  return "bg-red-500/20 text-red-400";
}

function buildActivity(events: TouristLog["events"]): ActivityItem[] {
  const items: ActivityItem[] = [];
  let pendingSubmitT: number | null = null;
  for (const ev of events) {
    if (ev.type === "run_result") {
      items.push({
        t: ev.t,
        label:
          ev.result.target === "custom"
            ? "Custom run"
            : ev.result.compiled
              ? "Ran samples"
              : "Compile",
        verdict: ev.result.verdict,
        run: ev.result,
      });
    } else if (ev.type === "submit") {
      pendingSubmitT = ev.t;
    } else if (ev.type === "verdict") {
      items.push({
        t: pendingSubmitT ?? ev.t,
        label: "Submission",
        verdict: ev.verdict,
        verdictT: ev.t,
      });
      pendingSubmitT = null;
    }
  }
  if (pendingSubmitT !== null) {
    items.push({ t: pendingSubmitT, label: "Submission", verdict: "PENDING" });
  }
  return items;
}

function ActivityRow({
  item,
  reached,
  onJump,
}: {
  item: ActivityItem;
  reached: boolean;
  onJump: () => void;
}) {
  const [open, setOpen] = useState(false);
  const expandable =
    !!item.run && (item.run.tests?.length || item.run.compileStderr);
  return (
    <div
      className={cn(
        "rounded-md border border-border/60",
        !reached && "opacity-40"
      )}
    >
      <div className="flex w-full items-center gap-2 px-2 py-1.5">
        {expandable ? (
          <button onClick={() => setOpen((o) => !o)} className="shrink-0">
            {open ? (
              <ChevronDown className="h-3 w-3" />
            ) : (
              <ChevronRight className="h-3 w-3" />
            )}
          </button>
        ) : (
          <span className="w-3 shrink-0" />
        )}
        <span className="truncate text-xs">{item.label}</span>
        <span
          className={cn(
            "rounded px-1.5 py-0.5 font-mono text-[10px]",
            verdictColor(item.verdict)
          )}
        >
          {item.verdict}
        </span>
        {item.run && item.run.compiled && (
          <span className="font-mono text-[10px] text-muted-foreground">
            {item.run.passed}/{item.run.total}
          </span>
        )}
        <button
          onClick={onJump}
          title="Jump to this moment"
          className="ml-auto shrink-0 rounded px-1.5 py-0.5 font-mono text-[10px] text-primary hover:bg-primary/10"
        >
          {formatMsPrecise(item.t)}
        </button>
      </div>
      {open && item.run && (
        <div className="space-y-1 border-t border-border/60 p-2">
          {item.run.compileStderr && (
            <pre className="max-h-28 overflow-auto rounded bg-black/40 p-1.5 font-mono text-[10px] text-red-300">
              {item.run.compileStderr}
            </pre>
          )}
          {item.run.tests?.map((tst) => (
            <div
              key={tst.name}
              className="flex items-center gap-2 font-mono text-[10px]"
            >
              <span>{tst.name}</span>
              <span
                className={cn(
                  "rounded px-1 py-px",
                  verdictColor(tst.verdict)
                )}
              >
                {tst.verdict}
              </span>
              <span className="ml-auto text-muted-foreground">{tst.timeMs}ms</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

/**
 * Re-render of the console the contestant saw at the current replay moment:
 * the tab they were viewing, with the latest run/custom/submission results
 * known at that point in the timeline.
 */
function ReplayConsole({
  events,
  activity,
  clockMs,
}: {
  events: TouristLog["events"];
  activity: ActivityItem[];
  clockMs: number;
}) {
  let activeTab = "samples";
  let running = false;
  for (const ev of events) {
    if (ev.t > clockMs) break;
    if (ev.type === "tab") activeTab = ev.tab;
    else if (ev.type === "run") running = true;
    else if (ev.type === "run_result") running = false;
  }
  let samplesRun: RunSummary | null = null;
  let customRun: RunSummary | null = null;
  const submissions: ActivityItem[] = [];
  for (const item of activity) {
    if (item.t > clockMs) break;
    if (item.run) {
      if (item.run.target === "custom") customRun = item.run;
      else samplesRun = item.run;
    } else {
      submissions.push(item);
    }
  }

  const renderRun = (run: RunSummary | null, busy: boolean) => {
    if (busy)
      return (
        <p className="animate-pulse p-2 font-mono text-xs text-amber-400">
          Running…
        </p>
      );
    if (!run)
      return (
        <p className="p-2 text-xs text-muted-foreground">No runs yet.</p>
      );
    if (!run.compiled)
      return (
        <pre className="m-2 max-h-full overflow-auto rounded bg-black/40 p-2 font-mono text-[11px] text-red-300">
          {run.compileStderr || "Compilation failed"}
        </pre>
      );
    return (
      <div className="flex flex-wrap gap-1.5 p-2">
        {run.tests?.map((tst) => (
          <span
            key={tst.name}
            className={cn(
              "flex items-center gap-1.5 rounded border border-border/60 px-2 py-1 font-mono text-[11px]",
              verdictColor(tst.verdict)
            )}
          >
            {tst.name} · {tst.verdict} · {tst.timeMs}ms
          </span>
        ))}
      </div>
    );
  };

  return (
    <div className="flex h-44 shrink-0 flex-col border-t border-border/60 bg-card/40">
      <div className="flex items-center gap-1 border-b border-border/60 px-2 pt-1">
        {[
          ["samples", "Samples"],
          ["custom", "Custom input"],
          ["submissions", "Submissions"],
        ].map(([key, label]) => (
          <span
            key={key}
            className={cn(
              "rounded-t px-3 py-1 font-mono text-[11px]",
              activeTab === key
                ? "border border-b-0 border-border/60 bg-background text-foreground"
                : "text-muted-foreground"
            )}
          >
            {label}
          </span>
        ))}
        <span className="ml-auto pb-1 font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
          console · as viewed
        </span>
      </div>
      <div className="min-h-0 flex-1 overflow-y-auto">
        {activeTab === "samples" && renderRun(samplesRun, running)}
        {activeTab === "custom" && renderRun(customRun, false)}
        {activeTab === "submissions" &&
          (submissions.length === 0 ? (
            <p className="p-2 text-xs text-muted-foreground">
              No submissions yet.
            </p>
          ) : (
            <div className="space-y-1 p-2">
              {[...submissions].reverse().map((sub, i) => (
                <div
                  key={i}
                  className="flex items-center gap-2 rounded border border-border/60 px-2 py-1 font-mono text-[11px]"
                >
                  <span>Submission</span>
                  <span
                    className={cn(
                      "rounded px-1.5 py-px text-[10px]",
                      sub.verdict === "PENDING" ||
                        (sub.verdictT !== undefined && clockMs < sub.verdictT)
                        ? "animate-pulse bg-amber-500/20 text-amber-400"
                        : verdictColor(sub.verdict)
                    )}
                  >
                    {sub.verdictT !== undefined && clockMs < sub.verdictT
                      ? "JUDGING"
                      : sub.verdict}
                  </span>
                  <span className="ml-auto text-muted-foreground">
                    {formatMsPrecise(sub.t)}
                  </span>
                </div>
              ))}
            </div>
          ))}
      </div>
    </div>
  );
}

/** Judging/verdict status badges for the current replay clock. */
export function ReplayBadges({
  log,
  clockMs,
}: {
  log: ReplayableLog;
  clockMs: number;
}) {
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
  return (
    <span className="flex items-center gap-3">
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
  );
}

/**
 * Shared replay engine: plays a tourist-format event log through the read-only
 * editor, with transport controls, timeline markers, and an optional webcam
 * video synced to the same clock (video time = clock − offset).
 */
export function ReplayCore({
  log,
  header,
  videoUrl,
  videoOffsetMs = 0,
  footerExtra,
}: {
  log: ReplayableLog;
  header: (clockMs: number, solved: boolean) => React.ReactNode;
  videoUrl?: string | null;
  videoOffsetMs?: number;
  footerExtra?: React.ReactNode;
}) {
  const [clockMs, setClockMs] = useState(0);
  const [playing, setPlaying] = useState(true);
  const [speed, setSpeed] = useState(1);
  const raf = useRef<number>();
  const last = useRef<number>(0);
  const videoRef = useRef<HTMLVideoElement | null>(null);

  const durationMs = Math.max(
    log.solveMs ?? 0,
    log.events.length ? log.events[log.events.length - 1].t : 0,
    1000
  );

  useEffect(() => {
    if (!playing) return;
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
  }, [playing, speed, durationMs]);

  // Keep the webcam video locked to the replay clock.
  useEffect(() => {
    const v = videoRef.current;
    if (!v) return;
    v.playbackRate = speed;
    if (playing) void v.play().catch(() => {});
    else v.pause();
  }, [playing, speed, videoUrl]);

  useEffect(() => {
    const v = videoRef.current;
    if (!v) return;
    const target = (clockMs - videoOffsetMs) / 1000;
    if (target < 0) {
      if (v.currentTime !== 0) v.currentTime = 0;
      return;
    }
    // Only hard-seek when drifted (scrubs, speed changes); let playback flow.
    if (Math.abs(v.currentTime - target) > 0.4) v.currentTime = target;
  }, [clockMs, videoOffsetMs]);

  const state = touristStateAt(log, clockMs);
  const solved = log.solveMs !== null && clockMs >= log.solveMs;
  const markers = log.events.filter(
    (ev) => ev.type !== "snapshot" && ev.type !== "tab" && ev.type !== "run_result"
  );
  const activity = useMemo(() => buildActivity(log.events), [log.events]);

  return (
    <main className="flex h-screen flex-col bg-background">
      {header(clockMs, solved)}

      <div className="flex min-h-0 flex-1">
        <div className="flex min-h-0 min-w-0 flex-1 flex-col">
          <div className="min-h-0 flex-1">
            <CodeMirror code={state.code} lang={state.lang ?? log.lang} />
          </div>
          <ReplayConsole
            events={log.events}
            activity={activity}
            clockMs={clockMs}
          />
        </div>
        {(videoUrl || activity.length > 0) && (
          <div className="flex w-[28%] min-w-[240px] flex-col border-l border-border/60 bg-black/40">
            {videoUrl && (
              <>
                <video
                  ref={videoRef}
                  src={videoUrl}
                  muted
                  playsInline
                  preload="auto"
                  className="aspect-video w-full object-cover"
                />
                <p className="px-3 py-1.5 font-mono text-[11px] uppercase tracking-widest text-muted-foreground">
                  Webcam · synced
                </p>
              </>
            )}
            <p className="border-t border-border/60 px-3 py-1.5 font-mono text-[11px] uppercase tracking-widest text-muted-foreground">
              Runs & submissions
            </p>
            <div className="min-h-0 flex-1 space-y-1.5 overflow-y-auto px-2 pb-2">
              {activity.length === 0 && (
                <p className="px-1 pt-1 text-xs text-muted-foreground">
                  No runs or submissions in this replay.
                </p>
              )}
              {activity.map((item, i) => (
                <ActivityRow
                  key={i}
                  item={item}
                  reached={item.t <= clockMs}
                  onJump={() => setClockMs(item.t)}
                />
              ))}
            </div>
          </div>
        )}
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
                  : ev.type === "run"
                    ? `Ran samples ${formatMsPrecise(ev.t)}`
                    : `${ev.verdict} ${formatMsPrecise(ev.t)}`
              }
              className={cn(
                "pointer-events-auto absolute top-0 h-1.5 w-1.5 -translate-x-1/2 rounded-full",
                ev.type === "submit"
                  ? "bg-amber-400"
                  : ev.type === "run"
                    ? "bg-sky-400"
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
        {footerExtra}
      </footer>
    </main>
  );
}

/** Event-race replay: loads one station's log and plays it back. */
export function ReplayPlayer({
  eventId,
  raceId,
  station,
}: {
  eventId: string;
  raceId: string;
  station: string;
}) {
  const [log, setLog] = useState<
    | (ReplayLog & { recordingUrl?: string | null; recordingOffsetMs?: number })
    | null
    | undefined
  >(undefined);

  useEffect(() => {
    fetch(`/api/replay?eventId=${eventId}&raceId=${raceId}&station=${station}`, {
      cache: "no-store",
    })
      .then((r) => (r.ok ? r.json() : null))
      .then(setLog)
      .catch(() => setLog(null));
  }, [eventId, raceId, station]);

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

  return (
    <ReplayCore
      log={log}
      videoUrl={log.recordingUrl}
      videoOffsetMs={log.recordingOffsetMs ?? 0}
      header={(clockMs, solved) => (
        <header
          className={cn(
            "flex items-center gap-3 border-b border-border/60 px-5 py-3",
            solved ? "bg-green-500/15" : "bg-primary/10"
          )}
        >
          {log.contestant?.country && (
            <span className="text-2xl">{flagEmoji(log.contestant.country)}</span>
          )}
          <span className="text-lg font-bold">{log.contestant?.name ?? station}</span>
          <span className="font-mono text-sm text-muted-foreground">
            {log.problemId} · replay
          </span>
          <span className="ml-auto">
            <ReplayBadges log={log} clockMs={clockMs} />
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
      )}
    />
  );
}
