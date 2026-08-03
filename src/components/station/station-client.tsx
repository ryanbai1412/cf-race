"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useEventState } from "@/hooks/use-event-state";
import { eventChannel, sendBroadcast } from "@/lib/realtime";
import { CheckinForm } from "./checkin-form";
import { CountdownOverlay } from "./countdown-overlay";
import { FinishScreen } from "./finish-screen";
import { RaceScreen } from "@/components/race/race-screen";
import { WebcamPublisher } from "@/components/monitor/webcam";
import type { Lang, Problem, StationRole } from "@/lib/types";
import type { RealtimeChannel } from "@supabase/supabase-js";

export function StationClient({
  eventId,
  station,
}: {
  eventId: string;
  station: StationRole;
}) {
  const { state, refetch, serverNow } = useEventState(eventId);
  const [warmupProblem, setWarmupProblem] = useState<Problem | null>(null);
  const [ready, setReady] = useState(false);
  const [switchingContestant, setSwitchingContestant] = useState(false);
  const chRef = useRef<RealtimeChannel | null>(null);

  useEffect(() => {
    const ch = eventChannel(eventId);
    ch.subscribe();
    chRef.current = ch;
    return () => {
      void ch.unsubscribe();
      chRef.current = null;
    };
  }, [eventId]);

  useEffect(() => {
    fetch(`/api/problems/warmup-sum?eventId=${eventId}`, { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => d && setWarmupProblem(d.problem))
      .catch(() => {});
  }, [eventId]);

  // Active race context for the replay recorder (kept in a ref so the
  // debounced editor callback always sees the current race).
  const recorderRef = useRef<{ raceId: string; startMs: number } | null>(null);
  const replayBuffer = useRef<{ t: number; code: string; lang: Lang }[]>([]);
  const serverNowRef = useRef(serverNow);
  serverNowRef.current = serverNow;

  const broadcastEditor = useMemo(() => {
    let timeout: ReturnType<typeof setTimeout> | null = null;
    let pending: { code: string; lang: Lang; cursorLine: number } | null = null;
    return (code: string, lang: Lang, cursorLine: number) => {
      pending = { code, lang, cursorLine };
      if (timeout) return;
      timeout = setTimeout(() => {
        timeout = null;
        if (pending && chRef.current) {
          sendBroadcast(chRef.current, { type: "editor", station, ...pending });
        }
        const rec = recorderRef.current;
        if (pending && rec) {
          const t = serverNowRef.current() - rec.startMs;
          if (t >= 0) {
            replayBuffer.current.push({ t, code: pending.code, lang: pending.lang });
          }
        }
      }, 300);
    };
  }, [station]);

  // Flush recorded editor snapshots to the replay store every few seconds.
  useEffect(() => {
    const flush = () => {
      const rec = recorderRef.current;
      const events = replayBuffer.current;
      if (!rec || events.length === 0) return;
      replayBuffer.current = [];
      void fetch("/api/replay", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ eventId, raceId: rec.raceId, station, events }),
        keepalive: true,
      }).catch(() => {});
    };
    const id = setInterval(flush, 5000);
    window.addEventListener("beforeunload", flush);
    return () => {
      clearInterval(id);
      window.removeEventListener("beforeunload", flush);
      flush();
    };
  }, [eventId, station]);

  const race0 = state?.race;
  useEffect(() => {
    // Races stay in "countdown" state in the DB; the recorder itself only
    // keeps snapshots with t >= 0, i.e. after the actual start moment.
    recorderRef.current =
      race0 && race0.state !== "finished" && race0.started_at
        ? { raceId: race0.id, startMs: new Date(race0.started_at).getTime() }
        : null;
  }, [race0]);

  const markReady = useCallback(() => {
    setReady((r) => !r);
    void refetch();
  }, [refetch]);

  if (!state) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <p className="animate-pulse font-mono text-muted-foreground">Connecting…</p>
      </main>
    );
  }

  const webcam = <WebcamPublisher eventId={eventId} identity={station} />;
  const contestant = state.contestants[station];
  const rivalRole: StationRole = station === "station1" ? "station2" : "station1";
  const rival = state.contestants[rivalRole];
  const race = state.race;

  if (!contestant || (switchingContestant && !race)) {
    return (
      <>
        {webcam}
        <CheckinForm
          eventId={eventId}
          eventName={state.event.name}
          station={station}
          rival={rival}
          onCheckedIn={() => {
            setSwitchingContestant(false);
            void refetch();
          }}
        />
      </>
    );
  }

  // Active race involving this contestant?
  const myParticipant = race?.participants.find(
    (p) => p.contestant_id === contestant.id
  );

  if (race && myParticipant) {
    const startMs = race.started_at ? new Date(race.started_at).getTime() : null;
    const now = serverNow();
    const endMs = startMs !== null ? startMs + race.timer_sec * 1000 : null;

    const rivalParticipant = race.participants.find(
      (p) => p.station_role === rivalRole
    );
    const solveMs =
      myParticipant.first_ac_at && startMs !== null
        ? new Date(myParticipant.first_ac_at).getTime() - startMs
        : null;
    const rivalSolveMs =
      rivalParticipant?.first_ac_at && startMs !== null
        ? new Date(rivalParticipant.first_ac_at).getTime() - startMs
        : null;
    const raceOver = endMs !== null && now > endMs;
    const rivalStillRacing = Boolean(
      rivalParticipant && !rivalParticipant.first_ac_at && !rivalParticipant.dq && !raceOver
    );

    // Finished (AC) or race fully over → finish screen.
    if (solveMs !== null || raceOver) {
      return (
        <FinishScreen
          eventId={eventId}
          problem={race.problem}
          contestant={contestant}
          solveMs={solveMs}
          rival={rival}
          rivalSolveMs={rivalSolveMs}
          rivalStillRacing={rivalStillRacing}
        />
      );
    }

    // Countdown or racing.
    return (
      <>
        {webcam}
        {startMs !== null && now < startMs + 1200 && (
          <CountdownOverlay startAtMs={startMs} serverNow={serverNow} />
        )}
        <RaceScreen
          eventId={eventId}
          problem={race.problem}
          contestant={contestant}
          raceId={race.id}
          endAtMs={endMs}
          serverNow={serverNow}
          warmup={false}
          onEditorChange={broadcastEditor}
          onSubmitAccepted={refetch}
          rivalName={rival?.name}
          rivalSolveMs={rivalSolveMs}
        />
      </>
    );
  }

  // No active race → warm-up sandbox.
  if (!warmupProblem) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <p className="animate-pulse font-mono text-muted-foreground">
          Loading warm-up…
        </p>
      </main>
    );
  }
  return (
    <>
      {webcam}
      <RaceScreen
        eventId={eventId}
        problem={warmupProblem}
        contestant={contestant}
        raceId={null}
        endAtMs={null}
        serverNow={serverNow}
        warmup
        ready={ready}
        onReady={markReady}
        onEditorChange={broadcastEditor}
        onSwitchContestant={() => setSwitchingContestant(true)}
      />
    </>
  );
}
