"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useEventState } from "@/hooks/use-event-state";
import { useReplayRecorder } from "@/hooks/use-replay-recorder";
import { eventChannel, sendBroadcast } from "@/lib/realtime";
import { CheckinForm } from "./checkin-form";
import { CountdownOverlay } from "./countdown-overlay";
import { FinishScreen } from "./finish-screen";
import { RaceScreen } from "@/components/race/race-screen";
import { WebcamPublisher } from "@/components/monitor/webcam";
import {
  acquireWebcam,
  startWebcamRecording,
  type WebcamRecording,
} from "@/lib/webcam-recorder";
import type { BroadcastMsg, Lang, Problem, StationRole } from "@/lib/types";
import type { RealtimeChannel } from "@supabase/supabase-js";

export function StationClient({
  eventId,
  station,
}: {
  eventId: string;
  station: StationRole;
}) {
  const lastEditorRef = useRef<{
    code: string;
    lang: Lang;
    cursorLine: number;
  } | null>(null);

  // Re-send the latest editor snapshot when a monitor asks for it (it lost
  // the mirror state, e.g. after a page refresh).
  const onMessage = useCallback(
    (msg: BroadcastMsg) => {
      if (msg.type === "request_editor" && msg.station === station) {
        const last = lastEditorRef.current;
        if (last && chRef.current) {
          sendBroadcast(chRef.current, { type: "editor", station, ...last });
        }
      }
    },
    [station]
  );

  const { state, refetch, serverNow } = useEventState(eventId, onMessage);
  const [warmupProblem, setWarmupProblem] = useState<Problem | null>(null);
  const [ready, setReady] = useState(false);
  const [switchingContestant, setSwitchingContestant] = useState(false);
  const [camReady, setCamReady] = useState(false);
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
  const serverNowRef = useRef(serverNow);
  serverNowRef.current = serverNow;

  // Per-keystroke replay recorder: deltas + periodic keyframes. Clamps
  // countdown-time events to t=0 so the replay isn't empty before the start.
  const { editorRecorder, recordRun, recordRunResult, recordTab, recordScroll } =
    useReplayRecorder({
      now: () => {
        const rec = recorderRef.current;
        if (!rec) return null;
        return serverNowRef.current() - rec.startMs;
      },
      send: (events) => {
        const rec = recorderRef.current;
        if (!rec) return false;
        void fetch("/api/replay", {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ eventId, raceId: rec.raceId, station, events }),
          keepalive: true,
        }).catch(() => {});
        return true;
      },
      autoFlush: true,
    });

  const broadcastEditor = useMemo(() => {
    let timeout: ReturnType<typeof setTimeout> | null = null;
    let pending: { code: string; lang: Lang; cursorLine: number } | null = null;
    return (code: string, lang: Lang, cursorLine: number) => {
      pending = { code, lang, cursorLine };
      if (timeout) return;
      timeout = setTimeout(() => {
        timeout = null;
        if (pending && chRef.current) {
          lastEditorRef.current = pending;
          sendBroadcast(chRef.current, { type: "editor", station, ...pending });
        }
      }, 300);
    };
  }, [station]);

  const race0 = state?.race;
  useEffect(() => {
    // Races stay in "countdown" state in the DB; the recorder itself only
    // keeps snapshots with t >= 0, i.e. after the actual start moment.
    recorderRef.current =
      race0 && race0.state !== "finished" && race0.started_at
        ? { raceId: race0.id, startMs: new Date(race0.started_at).getTime() }
        : null;
  }, [race0]);

  // Webcam recording during races: capture from countdown, stop + upload when
  // this station's race ends (AC, timer expiry, or reset). Keyed by race id.
  const webcamRec = useRef<{
    raceId: string;
    rec: WebcamRecording;
    stream: MediaStream;
    offsetMs: number;
  } | null>(null);
  const activeRecRaceId =
    race0 && race0.state !== "finished" && race0.started_at ? race0.id : null;
  const activeRecStartMs = race0?.started_at
    ? new Date(race0.started_at).getTime()
    : null;
  // Problem name for the upload toast, read at recorder start.
  const raceProblemRef = useRef<string | undefined>(undefined);
  raceProblemRef.current = race0?.problem?.name;
  useEffect(() => {
    // Keep recording 5s past the end to capture the contestant's reaction.
    // Chunks stream up during the race; this finalizes the recording (and
    // survives a closed tab: resumed from IndexedDB on the next visit).
    const stopAndUpload = (entry: NonNullable<typeof webcamRec.current>) => {
      void entry.rec
        .stopAndUpload({
          tailMs: 5000,
          query: {
            eventId,
            raceId: entry.raceId,
            station,
            offsetMs: String(entry.offsetMs),
          },
        })
        .finally(() => entry.stream.getTracks().forEach((t) => t.stop()));
    };

    const cur = webcamRec.current;
    if (activeRecRaceId && activeRecStartMs !== null) {
      if (cur && cur.raceId === activeRecRaceId) return;
      if (cur) {
        webcamRec.current = null;
        stopAndUpload(cur);
      }
      let cancelled = false;
      void acquireWebcam().then((stream) => {
        if (!stream) return;
        if (cancelled || webcamRec.current) {
          stream.getTracks().forEach((t) => t.stop());
          return;
        }
        const rec = startWebcamRecording(
          stream,
          { eventId, raceId: activeRecRaceId, station },
          raceProblemRef.current
        );
        if (!rec) {
          stream.getTracks().forEach((t) => t.stop());
          return;
        }
        const clockSkew = serverNowRef.current() - Date.now();
        webcamRec.current = {
          raceId: activeRecRaceId,
          rec,
          stream,
          offsetMs: rec.startedAtMs + clockSkew - activeRecStartMs,
        };
      });
      return () => {
        cancelled = true;
      };
    }
    if (cur) {
      webcamRec.current = null;
      stopAndUpload(cur);
    }
  }, [activeRecRaceId, activeRecStartMs, eventId, station]);

  const markReady = useCallback(() => {
    setReady((r) => !r);
    void refetch();
  }, [refetch]);

  if (!state) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <p className="animate-pulse font-mono text-sm text-muted-foreground">
          Connecting…
        </p>
      </main>
    );
  }

  // Upload progress toast + leave-warning come from the layout-mounted
  // RecordingUploadManager, which also retries pending uploads from IndexedDB.
  const webcam = (
    <WebcamPublisher
      eventId={eventId}
      identity={station}
      onPublishState={setCamReady}
    />
  );
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
        {startMs !== null && now < startMs && (
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
          onEditorDelta={editorRecorder.delta}
          onEditorSnapshot={editorRecorder.snapshot}
          onRun={recordRun}
          onRunResult={recordRunResult}
          onTabChange={recordTab}
          onStatementScroll={recordScroll}
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
        <p className="animate-pulse font-mono text-sm text-muted-foreground">
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
        readyBlockedReason={
          state.event.requireWebcam && !camReady
            ? "This event requires a webcam — allow camera access to ready up"
            : null
        }
        onEditorChange={broadcastEditor}
        onSwitchContestant={() => setSwitchingContestant(true)}
      />
    </>
  );
}
