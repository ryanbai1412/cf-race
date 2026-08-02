"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useEventState } from "@/hooks/use-event-state";
import { eventChannel, sendBroadcast } from "@/lib/realtime";
import { CheckinForm } from "./checkin-form";
import { CountdownOverlay } from "./countdown-overlay";
import { FinishScreen } from "./finish-screen";
import { RaceScreen } from "@/components/race/race-screen";
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
      }, 300);
    };
  }, [station]);

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

  const contestant = state.contestants[station];
  const rivalRole: StationRole = station === "station1" ? "station2" : "station1";
  const rival = state.contestants[rivalRole];
  const race = state.race;

  if (!contestant) {
    return (
      <CheckinForm
        eventId={eventId}
        eventName={state.event.name}
        station={station}
        rival={rival}
        onCheckedIn={refetch}
      />
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
    />
  );
}
