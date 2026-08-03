"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useEventState } from "@/hooks/use-event-state";
import { eventChannel, sendBroadcast } from "@/lib/realtime";
import { CheckinForm } from "./checkin-form";
import { CountdownOverlay } from "./countdown-overlay";
import { FinishScreen } from "./finish-screen";
import { RaceScreen } from "@/components/race/race-screen";
import { WebcamPublisher } from "@/components/monitor/webcam";
import {
  acquireWebcam,
  startWebcamRecording,
  uploadRecording,
  type WebcamRecording,
} from "@/lib/webcam-recorder";
import type { BroadcastMsg, Lang, Problem, RunResult, StationRole } from "@/lib/types";
import { summarizeRun, type RunSummary } from "@/lib/tourist";
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
  const [uploading, setUploading] = useState(0);
  const [uploadProgress, setUploadProgress] = useState(0);
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
  const replayBuffer = useRef<
    {
      t: number;
      code: string;
      lang: Lang;
      kind?: "run" | "run_result" | "tab" | "scroll";
      payload?: RunSummary | { tab: string } | { frac: number };
    }[]
  >([]);
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
          lastEditorRef.current = pending;
          sendBroadcast(chRef.current, { type: "editor", station, ...pending });
        }
        const rec = recorderRef.current;
        if (pending && rec) {
          // Clamp countdown-time snapshots to t=0 so the replay isn't empty
          // before the first post-start edit.
          const t = Math.max(0, serverNowRef.current() - rec.startMs);
          replayBuffer.current.push({ t, code: pending.code, lang: pending.lang });
        }
      }, 300);
    };
  }, [station]);

  // Record "ran samples" moments as replay timeline markers.
  const recordRun = useCallback((lang: Lang) => {
    const rec = recorderRef.current;
    if (!rec) return;
    const t = serverNowRef.current() - rec.startMs;
    if (t >= 0) replayBuffer.current.push({ t, code: "", lang, kind: "run" });
  }, []);

  const recordRunResult = useCallback(
    (result: RunResult, target: "samples" | "custom", lang: Lang) => {
      const rec = recorderRef.current;
      if (!rec) return;
      const t = Math.max(0, serverNowRef.current() - rec.startMs);
      replayBuffer.current.push({
        t,
        code: "",
        lang,
        kind: "run_result",
        payload: summarizeRun(result, target),
      });
    },
    []
  );

  const recordTab = useCallback((tab: string, lang: Lang) => {
    const rec = recorderRef.current;
    if (!rec) return;
    const t = Math.max(0, serverNowRef.current() - rec.startMs);
    replayBuffer.current.push({ t, code: "", lang, kind: "tab", payload: { tab } });
  }, []);

  const recordScroll = useCallback((frac: number, lang: Lang) => {
    const rec = recorderRef.current;
    if (!rec) return;
    const t = Math.max(0, serverNowRef.current() - rec.startMs);
    replayBuffer.current.push({ t, code: "", lang, kind: "scroll", payload: { frac } });
  }, []);

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
  useEffect(() => {
    const stopAndUpload = (entry: NonNullable<typeof webcamRec.current>) => {
      void entry.rec.stop().then(async (blob) => {
        entry.stream.getTracks().forEach((t) => t.stop());
        if (blob) {
          setUploading((n) => n + 1);
          setUploadProgress(0);
          await uploadRecording(
            blob,
            {
              eventId,
              raceId: entry.raceId,
              station,
              offsetMs: String(entry.offsetMs),
            },
            setUploadProgress
          );
          setUploading((n) => n - 1);
        }
      });
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
        const rec = startWebcamRecording(stream);
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

  // Leaving mid-upload would lose the webcam recording — warn first.
  useEffect(() => {
    if (uploading === 0) return;
    const warn = (e: BeforeUnloadEvent) => {
      e.preventDefault();
      e.returnValue = "";
    };
    window.addEventListener("beforeunload", warn);
    return () => window.removeEventListener("beforeunload", warn);
  }, [uploading]);

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

  const webcam = (
    <>
      <WebcamPublisher eventId={eventId} identity={station} />
      {uploading > 0 && (
        <div className="fixed bottom-4 right-4 z-50 w-64 space-y-1.5 rounded-lg border border-border/60 bg-background/95 p-3 shadow-lg backdrop-blur">
          <p className="font-mono text-xs text-foreground">
            Uploading webcam recording… {Math.round(uploadProgress * 100)}%
          </p>
          <div className="h-1.5 w-full overflow-hidden rounded-full bg-muted">
            <div
              className="h-full rounded-full bg-primary transition-[width] duration-200"
              style={{ width: `${Math.round(uploadProgress * 100)}%` }}
            />
          </div>
          <p className="text-[10px] text-muted-foreground">
            Don&apos;t close this tab until it finishes.
          </p>
        </div>
      )}
    </>
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
