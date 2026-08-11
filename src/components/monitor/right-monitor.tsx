"use client";

import { useCallback, useEffect, useState } from "react";
import { useEventState } from "@/hooks/use-event-state";
import { sendBroadcast } from "@/lib/realtime";
import {
  GennaRacerColumn,
  LiveRacerColumn,
  TouristName,
  type LogEntry,
  type RacerStatus,
} from "./racer-column";
import { RaceReview } from "./race-review";
import { CountdownOverlay } from "@/components/station/countdown-overlay";
import { STARTER_TEMPLATES, formatMs } from "@/lib/templates";
import { cn } from "@/lib/utils";
import type { TouristEvent } from "@/lib/tourist";
import type {
  BroadcastMsg,
  Lang,
  StationRole,
  Submission,
  Verdict,
} from "@/lib/types";
import type { RealtimeChannel } from "@supabase/supabase-js";

const STATIONS: StationRole[] = ["station1", "station2"];

type GennaLog = {
  events: TouristEvent[];
  lang: Lang;
  solveMs: number | null;
  recordingUrl: string | null;
  recordingOffsetMs: number;
};

/** The right monitor: header timer + three racer columns (A, B, tourist). */
export function RightMonitor({ eventId }: { eventId: string }) {
  const [mirrors, setMirrors] = useState<
    Record<StationRole, { code: string; lang: Lang }>
  >({
    station1: { code: STARTER_TEMPLATES.cpp, lang: "cpp" },
    station2: { code: STARTER_TEMPLATES.cpp, lang: "cpp" },
  });
  const [, forceTick] = useState(0);

  const onMessage = useCallback((msg: BroadcastMsg) => {
    if (msg.type === "editor") {
      setMirrors((m) => ({
        ...m,
        [msg.station]: { code: msg.code, lang: msg.lang },
      }));
    }
  }, []);

  const onSubscribed = useCallback((ch: RealtimeChannel) => {
    for (const station of STATIONS) {
      sendBroadcast(ch, { type: "request_editor", station });
    }
  }, []);

  const { state, serverNow } = useEventState(eventId, onMessage, onSubscribed);

  useEffect(() => {
    const iv = setInterval(() => forceTick((n) => n + 1), 200);
    return () => clearInterval(iv);
  }, []);

  const race = state?.race ?? null;
  const problemId = race?.problem_id ?? null;

  // Genna reference replay for the active problem.
  const [genna, setGenna] = useState<{ problemId: string; log: GennaLog | null } | null>(
    null
  );
  useEffect(() => {
    if (!problemId) return;
    if (genna?.problemId === problemId) return;
    let cancelled = false;
    setGenna({ problemId, log: null });
    fetch(`/api/genna/replay?eventId=${eventId}&problemId=${problemId}`, {
      cache: "no-store",
    })
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => !cancelled && setGenna({ problemId, log: d }))
      .catch(() => !cancelled && setGenna({ problemId, log: null }));
    return () => {
      cancelled = true;
    };
  }, [eventId, problemId, genna?.problemId]);

  // Poll official submissions for the active race (feeds the per-column log).
  const [submissions, setSubmissions] = useState<Submission[]>([]);
  const raceId = race?.id ?? null;
  useEffect(() => {
    if (!raceId) {
      setSubmissions([]);
      return;
    }
    let cancelled = false;
    const load = () =>
      fetch(`/api/submissions?eventId=${eventId}&raceId=${raceId}`, {
        cache: "no-store",
      })
        .then((r) => (r.ok ? r.json() : null))
        .then((d) => !cancelled && d && setSubmissions(d.submissions))
        .catch(() => {});
    void load();
    const iv = setInterval(load, 3000);
    return () => {
      cancelled = true;
      clearInterval(iv);
    };
  }, [eventId, raceId]);

  if (!state) {
    return (
      <main className="flex h-screen items-center justify-center">
        <p className="animate-pulse font-mono text-sm text-muted-foreground">
          Connecting…
        </p>
      </main>
    );
  }

  // ---------- REVIEWING ----------
  if (!race || !race.started_at) {
    if (state.lastRace) {
      return (
        <main className="flex h-screen flex-col bg-background">
          <RaceReview eventId={eventId} race={state.lastRace} size="lg" />
        </main>
      );
    }
    return (
      <main className="relative flex h-screen flex-col items-center justify-center overflow-hidden bg-background">
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(99,102,241,0.15),transparent_60%)]" />
        <div className="z-10 space-y-6 px-8 text-center">
          <p className="font-mono text-sm uppercase tracking-[0.4em] text-primary">
            {state.event.name}
          </p>
          <h1 className="max-w-4xl text-6xl font-extrabold tracking-tight">
            Race <TouristName /> on a Codeforces problem.
          </h1>
          <p className="text-2xl text-muted-foreground">
            Waiting for contestants — ask the booth staff to jump in.
          </p>
        </div>
      </main>
    );
  }

  // ---------- RACING ----------
  const startMs = new Date(race.started_at).getTime();
  const now = serverNow();
  const clockMs = now - startMs;
  const endMs = startMs + race.timer_sec * 1000;
  const remaining = Math.max(0, endMs - now);
  const timeUp = now > endMs;

  const columnFor = (station: StationRole) => {
    const contestant = state.contestants[station];
    const participant = race.participants.find((p) => p.station_role === station);
    const solveMs =
      participant?.first_ac_at != null
        ? new Date(participant.first_ac_at).getTime() - startMs
        : null;
    const status: RacerStatus = !participant
      ? "resting"
      : solveMs !== null
        ? "ac"
        : timeUp
          ? "timeup"
          : "working";
    const entries: LogEntry[] = submissions
      .filter((s) => s.contestant_id === participant?.contestant_id)
      .map((s) => submissionLogEntry(s, startMs))
      .sort((a, b) => b.t - a.t);
    return (
      <LiveRacerColumn
        key={station}
        eventId={eventId}
        monitorId="monitor-right"
        station={station}
        name={contestant?.name ?? null}
        country={contestant?.country ?? null}
        status={status}
        solveMs={solveMs}
        code={mirrors[station].code}
        lang={mirrors[station].lang}
        logEntries={entries}
        confettiKey={solveMs !== null ? `${race.id}:${station}` : null}
      />
    );
  };

  return (
    <main className="flex h-screen flex-col bg-background">
      {clockMs < 0 && <CountdownOverlay startAtMs={startMs} serverNow={serverNow} />}
      <header className="flex items-center gap-6 border-b border-border/60 bg-card/50 px-8 py-3">
        <span className="font-mono text-3xl font-black tracking-tight text-primary">
          {race.problem_id}
        </span>
        <span className="truncate text-xl font-bold text-muted-foreground">
          {race.problem.name}
        </span>
        <span
          className={cn(
            "ml-auto font-mono text-6xl font-black tabular-nums leading-none",
            remaining < 15000
              ? "animate-pulse text-red-400"
              : remaining < 60000
                ? "text-amber-400"
                : ""
          )}
        >
          {formatMs(remaining)}
        </span>
      </header>
      <div className="flex min-h-0 flex-1">
        {STATIONS.map(columnFor)}
        <GennaRacerColumn
          clockMs={clockMs}
          raceId={race.id}
          log={genna?.problemId === race.problem_id ? genna.log : null}
          loading={genna?.problemId === race.problem_id && genna.log === null}
        />
      </div>
    </main>
  );
}

function submissionLogEntry(s: Submission, startMs: number): LogEntry {
  const t = new Date(s.submitted_at).getTime() - startMs;
  const verdict = s.verdict as Verdict | null;
  if (!verdict || verdict === "PENDING") {
    return { t, label: "submitted…", tone: "neutral" };
  }
  return {
    t,
    label: `submission ${verdict}`,
    tone: verdict === "AC" ? "green" : "red",
  };
}
