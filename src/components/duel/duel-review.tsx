"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { ReplayEditor } from "@/components/replay/replay-editor";
import { ReplayBadges } from "@/components/replay/replay-player";
import { Button } from "@/components/ui/button";
import { formatMsPrecise } from "@/lib/templates";
import { TouristPlayer, type TouristLog, type TouristEvent } from "@/lib/tourist";
import type { SessionReplayResponse } from "@/lib/session-log";
import { cn } from "@/lib/utils";
import { Ban, Pause, Play, RotateCcw, Trophy } from "lucide-react";
import { toast } from "sonner";

const SPEEDS = [1, 2, 4, 8];

type ReviewPlayer = {
  userId: string;
  sessionId: string;
  name: string;
  avatarUrl: string | null;
  isWinner: boolean;
  replay: SessionReplayResponse | null;
};

type ReviewData = {
  match: {
    id: string;
    roomId: string;
    problemId: string;
    startedAt: string;
    finishedAt: string | null;
    winnerUserId: string | null;
    totalTimeSec: number | null;
    graceAfterAcSec: number | null;
  };
  invalidated: boolean;
  invalidReason: string | null;
  players: ReviewPlayer[];
};

/** One player's synced pane: webcam + replay editor + verdict badges. */
function ReviewPane({
  player,
  clockMs,
  playing,
  speed,
}: {
  player: ReviewPlayer;
  clockMs: number;
  playing: boolean;
  speed: number;
}) {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const replay = player.replay;
  const log: TouristLog | null = useMemo(
    () =>
      replay
        ? {
            problemId: replay.problemId,
            lang: replay.lang,
            solveMs: replay.solveMs ?? 0,
            events: replay.events as TouristEvent[],
          }
        : null,
    [replay]
  );
  const touristPlayer = useMemo(
    () => (log ? new TouristPlayer(log.events) : null),
    [log]
  );

  const offsetMs = replay?.recordingOffsetMs ?? 0;
  useEffect(() => {
    const v = videoRef.current;
    if (!v) return;
    v.playbackRate = speed;
    if (playing) void v.play().catch(() => {});
    else v.pause();
  }, [playing, speed, replay?.recordingUrl]);

  useEffect(() => {
    const v = videoRef.current;
    if (!v) return;
    const target = (clockMs - offsetMs) / 1000;
    if (target < 0) {
      if (v.currentTime !== 0) v.currentTime = 0;
      return;
    }
    if (Math.abs(v.currentTime - target) > 0.4) v.currentTime = target;
  }, [clockMs, offsetMs]);

  const solved =
    replay?.solveMs != null && replay.solveMs !== 0 && clockMs >= replay.solveMs;

  return (
    <div className="flex min-h-0 min-w-0 flex-1 flex-col border-r border-border/60 last:border-r-0">
      <div
        className={cn(
          "flex items-center gap-2 border-b border-border/60 px-3 py-2",
          player.isWinner ? "bg-green-500/10" : "bg-card/40"
        )}
      >
        {player.avatarUrl ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={player.avatarUrl}
            alt=""
            className="h-6 w-6 rounded-full"
            referrerPolicy="no-referrer"
          />
        ) : null}
        <span className="text-sm font-semibold">{player.name}</span>
        {player.isWinner && <Trophy className="h-3.5 w-3.5 text-amber-400" />}
        {log && <ReplayBadges log={{ ...log, solveMs: replay?.solveMs ?? null }} clockMs={clockMs} />}
        <span className="ml-auto font-mono text-xs tabular-nums">
          {replay?.solveMs != null && solved ? (
            <span className="font-bold text-green-400">
              AC {formatMsPrecise(replay.solveMs)}
            </span>
          ) : replay?.outcome ? (
            <span className="text-muted-foreground">{replay.outcome}</span>
          ) : null}
        </span>
      </div>
      {replay?.recordingUrl ? (
        <video
          ref={videoRef}
          src={replay.recordingUrl}
          muted
          playsInline
          preload="auto"
          className="aspect-video w-full shrink-0 border-b border-border/60 bg-black object-cover"
        />
      ) : (
        <div className="flex aspect-video w-full shrink-0 items-center justify-center border-b border-border/60 bg-black/50">
          <p className="font-mono text-xs text-muted-foreground">
            No webcam recording
          </p>
        </div>
      )}
      <div className="min-h-0 flex-1">
        {touristPlayer && log ? (
          <ReplayEditor
            player={touristPlayer}
            clockMs={clockMs}
            fallbackLang={log.lang}
          />
        ) : (
          <div className="flex h-full items-center justify-center">
            <p className="font-mono text-xs text-muted-foreground">
              No replay data
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

/**
 * Side-by-side duel review: both players' editor replays and webcams driven
 * by ONE shared clock/scrubber with play/pause, speeds, and jump-to-event.
 */
export function DuelReview({ matchId }: { matchId: string }) {
  const [data, setData] = useState<ReviewData | null | undefined>(undefined);
  const [clockMs, setClockMs] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [speed, setSpeed] = useState(1);
  const [invalidating, setInvalidating] = useState(false);
  const raf = useRef<number>();
  const last = useRef<number>(0);

  const refresh = useCallback(() => {
    fetch(`/api/duel/review?matchId=${matchId}`, { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : null))
      .then(setData)
      .catch(() => setData(null));
  }, [matchId]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  // Autoplay once the replay data is actually loaded (not against the
  // placeholder duration).
  const startedRef = useRef(false);
  useEffect(() => {
    if (data && !startedRef.current) {
      startedRef.current = true;
      setPlaying(true);
    }
  }, [data]);

  const durationMs = useMemo(() => {
    if (!data) return 1000;
    let max = 1000;
    for (const p of data.players) {
      if (!p.replay) continue;
      if (p.replay.solveMs != null) max = Math.max(max, p.replay.solveMs);
      const evs = p.replay.events;
      if (evs.length > 0) max = Math.max(max, evs[evs.length - 1].t);
    }
    return max;
  }, [data]);

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

  // Shared jump-to-event markers: submits/verdicts/ACs from both players.
  const markers = useMemo(() => {
    if (!data) return [];
    const items: { t: number; label: string; color: string }[] = [];
    for (const p of data.players) {
      if (!p.replay) continue;
      for (const ev of p.replay.events) {
        if (ev.type === "submit") {
          items.push({
            t: ev.t,
            label: `${p.name} submitted`,
            color: "bg-amber-400",
          });
        } else if (ev.type === "verdict") {
          items.push({
            t: ev.t,
            label: `${p.name}: ${ev.verdict}`,
            color: ev.verdict === "AC" ? "bg-green-400" : "bg-red-400",
          });
        } else if (ev.type === "run") {
          items.push({
            t: ev.t,
            label: `${p.name} ran samples`,
            color: "bg-sky-400",
          });
        }
      }
    }
    return items.sort((a, b) => a.t - b.t);
  }, [data]);

  const toggleInvalid = async () => {
    if (!data) return;
    setInvalidating(true);
    try {
      let reason: string | null = null;
      if (!data.invalidated) {
        reason = window.prompt("Reason for invalidating (optional):") ?? null;
      }
      const res = await fetch("/api/duel/invalidate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(
          data.invalidated
            ? { problemId: data.match.problemId, revoke: true }
            : { problemId: data.match.problemId, reason }
        ),
      });
      const d = await res.json();
      if (!res.ok) throw new Error(d.error ?? "Failed");
      refresh();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed");
    } finally {
      setInvalidating(false);
    }
  };

  if (data === undefined) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <p className="animate-pulse font-mono text-muted-foreground">
          Loading review…
        </p>
      </main>
    );
  }
  if (data === null) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center gap-3">
        <p className="font-mono text-muted-foreground">Match not found.</p>
        <Button asChild variant="secondary">
          <Link href="/duel">Back to duels</Link>
        </Button>
      </main>
    );
  }

  const winner = data.players.find((p) => p.isWinner) ?? null;

  return (
    <main className="flex h-screen flex-col bg-background">
      <header className="flex flex-wrap items-center gap-3 border-b border-border/60 px-5 py-3">
        <Link href="/duel" className="font-mono text-xs text-primary hover:underline">
          ← duels
        </Link>
        <span className="font-mono text-sm text-primary">
          {data.match.problemId}
        </span>
        <span className="text-sm font-semibold">
          {data.players.map((p) => p.name).join(" vs ")}
        </span>
        {data.invalidated ? (
          <span className="rounded bg-red-500/20 px-2 py-0.5 font-mono text-xs text-red-400">
            problem invalidated{data.invalidReason ? `: ${data.invalidReason}` : ""}
            {" — result void"}
          </span>
        ) : winner ? (
          <span className="flex items-center gap-1.5 rounded bg-green-500/15 px-2 py-0.5 font-mono text-xs text-green-400">
            <Trophy className="h-3 w-3 text-amber-400" />
            {winner.name} won
            {winner.replay?.solveMs != null &&
              ` · ${formatMsPrecise(winner.replay.solveMs)}`}
          </span>
        ) : (
          <span className="rounded bg-muted px-2 py-0.5 font-mono text-xs text-muted-foreground">
            both DNF
          </span>
        )}
        <span className="ml-auto flex items-center gap-2">
          <Button
            size="sm"
            variant="ghost"
            disabled={invalidating}
            onClick={() => void toggleInvalid()}
          >
            {data.invalidated ? (
              <>
                <RotateCcw className="mr-1.5 h-3.5 w-3.5" />
                Restore problem
              </>
            ) : (
              <>
                <Ban className="mr-1.5 h-3.5 w-3.5" />
                Invalidate problem
              </>
            )}
          </Button>
          <span className="font-mono text-xl tabular-nums">
            {formatMsPrecise(clockMs)}
          </span>
        </span>
      </header>

      <div className="flex min-h-0 flex-1">
        {data.players.map((p) => (
          <ReviewPane
            key={p.sessionId}
            player={p}
            clockMs={clockMs}
            playing={playing}
            speed={speed}
          />
        ))}
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
          {markers.map((m, i) => (
            <button
              key={i}
              title={`${m.label} · ${formatMsPrecise(m.t)}`}
              onClick={() => setClockMs(m.t)}
              className={cn(
                "absolute top-0 h-1.5 w-1.5 -translate-x-1/2 rounded-full",
                m.color
              )}
              style={{ left: `${(m.t / durationMs) * 100}%` }}
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
