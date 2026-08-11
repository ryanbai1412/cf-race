"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import confetti from "canvas-confetti";
import { CodeMirror } from "./code-mirror";
import { WebcamView } from "./webcam";
import { ReplayEditor } from "@/components/replay/replay-editor";
import { TouristPlayer, type TouristEvent } from "@/lib/tourist";
import { formatMs, formatMsPrecise } from "@/lib/templates";
import { flagEmoji } from "@/lib/countries";
import { cn } from "@/lib/utils";
import type { Lang } from "@/lib/types";

export type RacerStatus = "working" | "ac" | "timeup" | "resting";

export type LogEntry = {
  t: number;
  label: string;
  tone: "neutral" | "green" | "red";
};

export function StatusChip({
  status,
  solveMs,
}: {
  status: RacerStatus;
  solveMs: number | null;
}) {
  if (status === "resting") return null;
  return (
    <span
      className={cn(
        "ml-auto rounded px-2.5 py-1 font-mono text-lg font-bold tabular-nums",
        status === "ac"
          ? "bg-green-500/20 text-green-400"
          : status === "timeup"
            ? "bg-muted text-muted-foreground"
            : "bg-amber-500/15 text-amber-400"
      )}
    >
      {status === "ac" && solveMs !== null
        ? `AC ${formatMsPrecise(solveMs)}`
        : status === "timeup"
          ? "TIME UP"
          : "WORKING"}
    </span>
  );
}

/** "tourist" in Codeforces Legendary Grandmaster styling. */
export function TouristName({ className }: { className?: string }) {
  return (
    <span className={cn("font-bold", className)}>
      <span className="text-foreground">t</span>
      <span className="text-[#ff0000]">ourist</span>
    </span>
  );
}

function SubmissionLog({ entries }: { entries: LogEntry[] }) {
  return (
    <div className="flex min-h-0 flex-1 flex-col gap-1 overflow-hidden px-3 py-2">
      {entries.length === 0 ? (
        <p className="font-mono text-sm text-muted-foreground/60">
          no runs yet
        </p>
      ) : (
        entries.slice(0, 6).map((e, i) => (
          <p
            key={`${e.t}-${i}`}
            className={cn(
              "truncate font-mono text-sm",
              i === 0 ? "" : "opacity-60",
              e.tone === "green"
                ? "text-green-400"
                : e.tone === "red"
                  ? "text-red-400"
                  : "text-muted-foreground"
            )}
          >
            <span className="tabular-nums">{formatMs(Math.max(0, e.t))}</span>{" "}
            {e.label}
          </p>
        ))
      )}
    </div>
  );
}

function useColumnConfetti(fireKey: string | null) {
  const firedRef = useRef<string | null>(null);
  const hostRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!fireKey || firedRef.current === fireKey) return;
    firedRef.current = fireKey;
    const host = hostRef.current;
    const x = host
      ? (host.getBoundingClientRect().left + host.getBoundingClientRect().width / 2) /
        window.innerWidth
      : 0.5;
    confetti({ particleCount: 180, spread: 80, origin: { x, y: 0.4 } });
  }, [fireKey]);
  return hostRef;
}

/** A live contestant column: streamed webcam, broadcast editor mirror, submissions. */
export function LiveRacerColumn({
  eventId,
  monitorId,
  station,
  name,
  country,
  status,
  solveMs,
  code,
  lang,
  logEntries,
  confettiKey,
}: {
  eventId: string;
  monitorId: string;
  station: string;
  name: string | null;
  country: string | null;
  status: RacerStatus;
  solveMs: number | null;
  code: string;
  lang: Lang;
  logEntries: LogEntry[];
  confettiKey: string | null;
}) {
  const hostRef = useColumnConfetti(status === "ac" ? confettiKey : null);
  return (
    <div ref={hostRef} className="flex min-h-0 min-w-0 flex-1 flex-col border-r border-border/60 last:border-r-0">
      <div className="flex items-center gap-2 border-b border-border/60 bg-card/40 px-3 py-2">
        <span className="text-2xl">{country ? flagEmoji(country) : "🏳️"}</span>
        <span className="truncate text-xl font-bold">
          {name ?? (station === "station1" ? "Contestant A" : "Contestant B")}
        </span>
        <StatusChip status={status} solveMs={solveMs} />
      </div>
      <div className="flex h-40 shrink-0 border-b border-border/60">
        <div className="relative aspect-[4/3] h-full shrink-0 bg-black/60">
          <WebcamView
            eventId={eventId}
            identity={`${monitorId}-${station}`}
            publisherIdentity={station}
            wrapperClassName="absolute inset-0"
            className="h-full w-full object-cover"
          />
        </div>
        <SubmissionLog entries={logEntries} />
      </div>
      <div className="min-h-0 flex-1">
        <CodeMirror code={code} lang={lang} fontSize={13} />
      </div>
    </div>
  );
}

/** Build submission-log entries from a tourist-format event log up to `clockMs`. */
export function logFromEvents(events: TouristEvent[], clockMs: number): LogEntry[] {
  const out: LogEntry[] = [];
  for (const ev of events) {
    if (ev.t > clockMs) break;
    if (ev.type === "run") out.push({ t: ev.t, label: "ran samples…", tone: "neutral" });
    else if (ev.type === "run_result")
      out.push({
        t: ev.t,
        label:
          ev.result.verdict === "AC" ? "samples passed ✓" : "samples failed",
        tone: ev.result.verdict === "AC" ? "green" : "red",
      });
    else if (ev.type === "submit")
      out.push({ t: ev.t, label: "submitted…", tone: "neutral" });
    else if (ev.type === "verdict")
      out.push({
        t: ev.t,
        label: `submission ${ev.verdict}`,
        tone: ev.verdict === "AC" ? "green" : "red",
      });
  }
  return out.reverse();
}

/** The Genna ghost column: replayed code, log and webcam from his session. */
export function GennaRacerColumn({
  clockMs,
  raceId,
  log,
  loading,
}: {
  clockMs: number; // race clock, negative during countdown
  raceId: string | null;
  log: {
    events: TouristEvent[];
    lang: Lang;
    solveMs: number | null;
    recordingUrl: string | null;
    recordingOffsetMs: number;
  } | null;
  loading: boolean;
}) {
  const player = useMemo(
    () => (log ? new TouristPlayer(log.events) : null),
    [log]
  );
  const solveMs = log?.solveMs ?? null;
  const solved = solveMs !== null && clockMs >= solveMs;
  const status: RacerStatus =
    raceId === null
      ? "resting"
      : solved
        ? "ac"
        : "working";
  const hostRef = useColumnConfetti(
    solved && raceId ? `${raceId}:genna` : null
  );
  const entries = useMemo(
    () => (log ? logFromEvents(log.events, Math.max(0, clockMs)) : []),
    [log, clockMs]
  );

  return (
    <div ref={hostRef} className="flex min-h-0 min-w-0 flex-1 flex-col">
      <div className="flex items-center gap-2 border-b border-border/60 bg-card/40 px-3 py-2">
        <TouristName className="truncate text-xl" />
        <StatusChip status={status} solveMs={solveMs} />
      </div>
      <div className="flex h-40 shrink-0 border-b border-border/60">
        <div className="relative aspect-[4/3] h-full shrink-0 bg-black/60">
          {log?.recordingUrl ? (
            <GennaWebcam
              src={log.recordingUrl}
              offsetMs={log.recordingOffsetMs}
              clockMs={clockMs}
            />
          ) : (
            <div className="flex h-full w-full items-center justify-center">
              <TouristName className="text-lg" />
            </div>
          )}
        </div>
        <SubmissionLog entries={entries} />
      </div>
      <div className="min-h-0 flex-1">
        {player && log ? (
          <ReplayEditor
            player={player}
            clockMs={Math.max(0, clockMs)}
            fallbackLang={log.lang}
            fontSize={13}
          />
        ) : (
          <div className="flex h-full items-center justify-center">
            <p className="animate-pulse font-mono text-sm text-muted-foreground">
              {loading ? "Loading ghost…" : ""}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

/** Genna's recorded webcam, kept seeked to the race clock. */
function GennaWebcam({
  src,
  offsetMs,
  clockMs,
}: {
  src: string;
  offsetMs: number;
  clockMs: number;
}) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const video = videoRef.current;
    if (!video || !ready) return;
    const target = (clockMs - offsetMs) / 1000;
    if (target < 0 || target > video.duration) {
      video.pause();
      return;
    }
    if (Math.abs(video.currentTime - target) > 0.5) {
      video.currentTime = target;
    }
    if (video.paused) void video.play().catch(() => {});
    // Re-sync every render tick (parent ticks the clock).
  }, [clockMs, offsetMs, ready]);

  return (
    <video
      ref={videoRef}
      src={src}
      muted
      playsInline
      preload="auto"
      onLoadedMetadata={() => setReady(true)}
      className="h-full w-full object-cover"
    />
  );
}
