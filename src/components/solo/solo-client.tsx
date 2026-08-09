"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import confetti from "canvas-confetti";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CountdownOverlay } from "@/components/station/countdown-overlay";
import { RaceScreen } from "@/components/race/race-screen";
import { Eyebrow } from "@/components/shell/page";
import { Segmented } from "@/components/ui/segmented";
import { formatMsPrecise } from "@/lib/templates";
import { loadSoloHistory, upsertSoloHistory, bestSolve } from "@/lib/solo";
import { preferredLang, setPreferredLang } from "@/lib/lang-preference";
import {
  acquireWebcam,
  startWebcamRecording,
  type WebcamRecording,
} from "@/lib/webcam-recorder";
import type { Contestant, Lang, Problem } from "@/lib/types";
import { useReplayRecorder } from "@/hooks/use-replay-recorder";
import {
  Camera,
  CameraOff,
  Loader2,
  Play,
  RotateCcw,
  Video,
} from "lucide-react";
import { StarRating } from "@/components/problems/star-rating";

const SOLO_CONTESTANT: Contestant = {
  id: "solo",
  event_id: "solo",
  station_role: "station1",
  name: "Solo run",
  country: null,
  retired_at: null,
};

type Phase = "idle" | "racing" | "finished";
type Session = { sessionId: string; startAtMs: number; timerSec: number };

const ACTIVE_KEY = "cfr-solo-active";

export function SoloClient({
  problem,
  problemIds,
  signedIn = false,
}: {
  problem: Problem;
  problemIds: string[];
  signedIn?: boolean;
}) {
  const [phase, setPhase] = useState<Phase>("idle");
  const [session, setSession] = useState<Session | null>(null);
  const [result, setResult] = useState<{
    outcome: "solved" | "timeout";
    solveMs: number | null;
  } | null>(null);
  const [camState, setCamState] = useState<"pending" | "ready" | "none">("pending");
  const [camEnabled, setCamEnabled] = useState(true);
  const [uploadState, setUploadState] = useState<
    "none" | "uploading" | "done" | "failed"
  >("none");
  const [uploadProgress, setUploadProgress] = useState(0);
  const [starting, setStarting] = useState(false);
  // Language chosen before the run starts, so the race opens on the right
  // buffer and template.
  const [lang, setLang] = useState<Lang>("cpp");

  useEffect(() => {
    const saved = preferredLang();
    if (saved) setLang(saved);
  }, []);

  // Server clock offset (serverNow − Date.now()), set when the session starts.
  const clockOffset = useRef(0);
  const serverNow = useCallback(() => Date.now() + clockOffset.current, []);

  const streamRef = useRef<MediaStream | null>(null);
  const previewRef = useRef<HTMLVideoElement | null>(null);
  const recordingRef = useRef<WebcamRecording | null>(null);
  const sessionRef = useRef<Session | null>(null);
  sessionRef.current = session;

  // Webcam preview (recording is optional — everything works without it).
  useEffect(() => {
    if (!camEnabled) {
      streamRef.current?.getTracks().forEach((t) => t.stop());
      streamRef.current = null;
      setCamState("none");
      return;
    }
    let cancelled = false;
    setCamState("pending");
    void acquireWebcam().then((stream) => {
      if (cancelled) {
        stream?.getTracks().forEach((t) => t.stop());
        return;
      }
      streamRef.current = stream;
      setCamState(stream ? "ready" : "none");
    });
    return () => {
      cancelled = true;
      streamRef.current?.getTracks().forEach((t) => t.stop());
      streamRef.current = null;
    };
  }, [camEnabled]);

  useEffect(() => {
    if (camState === "ready" && previewRef.current && streamRef.current) {
      previewRef.current.srcObject = streamRef.current;
    }
  }, [camState, phase]);

  // Per-keystroke editor recorder: deltas + periodic keyframes. Clamps
  // countdown-time events to t=0 so the replay isn't empty before the start.
  const {
    editorRecorder,
    recordRun,
    recordRunResult,
    recordTab,
    recordScroll,
    flush: flushEvents,
  } = useReplayRecorder({
    now: () => {
      const s = sessionRef.current;
      if (!s) return null;
      return Date.now() + clockOffset.current - s.startAtMs;
    },
    send: (events) => {
      const s = sessionRef.current;
      if (!s) return false;
      void fetch("/api/solo/events", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ sessionId: s.sessionId, events }),
        keepalive: true,
      }).catch(() => {});
      return true;
    },
    autoFlush: phase === "racing",
  });

  // Mark abandoned runs if the tab closes mid-race.
  useEffect(() => {
    if (phase !== "racing") return;
    const onUnload = () => {
      flushEvents();
      const s = sessionRef.current;
      if (s) {
        navigator.sendBeacon(
          "/api/solo/finish",
          JSON.stringify({ sessionId: s.sessionId, outcome: "abandoned" })
        );
      }
    };
    window.addEventListener("beforeunload", onUnload);
    return () => window.removeEventListener("beforeunload", onUnload);
  }, [phase, flushEvents]);

  const finish = useCallback(
    (outcome: "solved" | "timeout", solveMs: number | null) => {
      setPhase((p) => {
        if (p !== "racing") return p;
        setResult({ outcome, solveMs });
        return "finished";
      });
    },
    []
  );

  // Side effects of finishing: flush events, stop + upload the recording.
  useEffect(() => {
    if (phase !== "finished" || !session || !result) return;
    sessionStorage.removeItem(ACTIVE_KEY);
    flushEvents();
    upsertSoloHistory({
      sessionId: session.sessionId,
      problemId: problem.id,
      startedAt: session.startAtMs,
      outcome: result.outcome,
      solveMs: result.solveMs,
    });
    if (result.outcome === "timeout") {
      void fetch("/api/solo/finish", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ sessionId: session.sessionId, outcome: "timeout" }),
      }).catch(() => {});
    } else {
      confetti({ particleCount: 160, spread: 80, origin: { y: 0.6 } });
    }
    const rec = recordingRef.current;
    recordingRef.current = null;
    if (rec) {
      setUploadState("uploading");
      setUploadProgress(0);
      // Keep recording 5s past the end to capture the reaction. Chunks have
      // been streaming up during the run; this finalizes the recording (and
      // survives a closed tab: resumed from IndexedDB on the next visit).
      void rec
        .stopAndUpload({
          tailMs: 5000,
          query: {
            sessionId: session.sessionId,
            offsetMs: String(
              rec.startedAtMs + clockOffset.current - session.startAtMs
            ),
          },
          onProgress: setUploadProgress,
        })
        .then((ok) => setUploadState(ok ? "done" : "failed"));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [phase]);

  // Leaving mid-upload would lose the webcam recording — warn first.
  useEffect(() => {
    if (uploadState !== "uploading") return;
    const warn = (e: BeforeUnloadEvent) => {
      e.preventDefault();
      e.returnValue = "";
    };
    window.addEventListener("beforeunload", warn);
    return () => window.removeEventListener("beforeunload", warn);
  }, [uploadState]);

  // Timer watchdog → timeout finish.
  useEffect(() => {
    if (phase !== "racing" || !session) return;
    const endMs = session.startAtMs + session.timerSec * 1000;
    const iv = setInterval(() => {
      if (serverNow() > endMs) finish("timeout", null);
    }, 250);
    return () => clearInterval(iv);
  }, [phase, session, serverNow, finish]);

  // Resume an in-progress run after a reload (webcam recording doesn't survive).
  useEffect(() => {
    try {
      const raw = sessionStorage.getItem(ACTIVE_KEY);
      if (!raw) return;
      const saved = JSON.parse(raw) as Session & { problemId: string };
      if (saved.problemId !== problem.id) return;
      if (Date.now() < saved.startAtMs + saved.timerSec * 1000) {
        setSession(saved);
        setPhase("racing");
      } else {
        sessionStorage.removeItem(ACTIVE_KEY);
      }
    } catch {}
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const start = useCallback(async () => {
    if (starting) return;
    setStarting(true);
    try {
      const res = await fetch("/api/solo/session", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ problemId: problem.id }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? "Failed to start");
      clockOffset.current = data.serverNow - Date.now();
      const s: Session = {
        sessionId: data.sessionId,
        startAtMs: data.startAtMs,
        timerSec: data.timerSec,
      };
      sessionStorage.setItem(
        ACTIVE_KEY,
        JSON.stringify({ ...s, problemId: problem.id })
      );
      upsertSoloHistory({
        sessionId: s.sessionId,
        problemId: problem.id,
        startedAt: s.startAtMs,
        outcome: "pending",
        solveMs: null,
      });
      if (streamRef.current) {
        recordingRef.current = startWebcamRecording(streamRef.current, {
          sessionId: s.sessionId,
        });
      }
      setResult(null);
      setUploadState("none");
      setSession(s);
      setPhase("racing");
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed to start");
    } finally {
      setStarting(false);
    }
  }, [starting, problem.id]);

  // The server's solveMs is measured from the submission timestamp; the local
  // clock here would measure from the judge verdict instead.
  const onSolved = useCallback(
    (solveMs: number | null) => {
      const s = sessionRef.current;
      finish(
        "solved",
        solveMs ??
          (s ? Date.now() + clockOffset.current - s.startAtMs : null)
      );
    },
    [finish]
  );

  const nextProblemId = useMemo(() => {
    const history = typeof window !== "undefined" ? loadSoloHistory() : [];
    const others = problemIds.filter((id) => id !== problem.id);
    const unsolved = others.filter((id) => !bestSolve(history, id));
    const pool = unsolved.length > 0 ? unsolved : others;
    return pool[Math.floor(Math.random() * pool.length)] ?? null;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [problemIds, problem.id, phase]);

  // ── Racing ────────────────────────────────────────────────────────────────
  if (phase === "racing" && session) {
    const endAtMs = session.startAtMs + session.timerSec * 1000;
    return (
      <>
        {serverNow() < session.startAtMs && (
          <CountdownOverlay startAtMs={session.startAtMs} serverNow={serverNow} />
        )}
        <RaceScreen
          eventId=""
          problem={problem}
          contestant={SOLO_CONTESTANT}
          raceId={session.sessionId}
          endAtMs={endAtMs}
          serverNow={serverNow}
          warmup={false}
          solo
          initialLang={lang}
          onEditorDelta={editorRecorder.delta}
          onEditorSnapshot={editorRecorder.snapshot}
          onRun={recordRun}
          onRunResult={recordRunResult}
          onTabChange={recordTab}
          onStatementScroll={recordScroll}
          onSubmitAccepted={onSolved}
        />
      </>
    );
  }

  // ── Finished ─────────────────────────────────────────────────────────────
  if (phase === "finished" && session && result) {
    const solved = result.outcome === "solved";
    const touristDelta =
      solved && result.solveMs !== null && problem.tourist_time_ms !== null
        ? result.solveMs - problem.tourist_time_ms
        : null;
    return (
      <main className="flex min-h-screen items-center justify-center px-6">
        <Card className="w-full max-w-lg border-border/60 bg-card/60 text-center">
          <CardHeader>
            <CardTitle
              className={`font-mono text-4xl font-black ${
                solved ? "text-green-400" : ""
              }`}
            >
              {solved ? "ACCEPTED" : "TIME'S UP"}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-5">
            {solved && result.solveMs !== null && (
              <p className="font-mono text-6xl font-bold tabular-nums">
                {formatMsPrecise(result.solveMs)}
              </p>
            )}
            {touristDelta !== null && problem.tourist_time_ms !== null && (
              <p className="font-mono text-sm text-muted-foreground">
                tourist{" "}
                <span className="text-foreground tabular-nums">
                  {formatMsPrecise(problem.tourist_time_ms)}
                </span>{" "}
                ·{" "}
                <span
                  className={
                    touristDelta <= 0 ? "text-green-400" : "text-red-400"
                  }
                >
                  {touristDelta <= 0 ? "−" : "+"}
                  {formatMsPrecise(Math.abs(touristDelta))}
                </span>
              </p>
            )}
            {!solved && (
              <p className="text-sm text-muted-foreground">
                No AC this time — replay it and see where the seconds went.
              </p>
            )}
            {uploadState === "uploading" && (
              <div className="mx-auto w-full max-w-xs space-y-1">
                <p className="font-mono text-xs text-muted-foreground">
                  Uploading webcam recording… {Math.round(uploadProgress * 100)}%
                </p>
                <div className="h-1.5 w-full overflow-hidden rounded-full bg-muted">
                  <div
                    className="h-full rounded-full bg-primary transition-[width] duration-200"
                    style={{ width: `${Math.round(uploadProgress * 100)}%` }}
                  />
                </div>
              </div>
            )}
            <p className="font-mono text-xs text-muted-foreground">
              {uploadState === "done" && "Webcam recording saved."}
              {uploadState === "failed" &&
                "Webcam recording saved locally — upload will retry automatically."}
              {uploadState === "none" &&
                camState === "none" &&
                "No camera — this run was recorded without video."}
            </p>
            {signedIn && (
              <div className="flex items-center justify-center gap-2">
                <span className="font-mono text-xs text-muted-foreground">
                  Rate this problem:
                </span>
                <StarRating problemId={problem.id} initial={null} />
              </div>
            )}
            <div className="flex flex-wrap justify-center gap-2">
              <Button asChild>
                <Link href={`/replay/${session.sessionId}`}>
                  <Video className="mr-1.5 h-4 w-4" />
                  Watch replay
                </Link>
              </Button>
              <Button variant="secondary" onClick={() => setPhase("idle")}>
                <RotateCcw className="mr-1.5 h-4 w-4" />
                Run again
              </Button>
              {nextProblemId && (
                <Button asChild variant="secondary">
                  <Link href={`/problems/${nextProblemId}/solve`}>
                    Random unsolved problem →
                  </Link>
                </Button>
              )}
              <Button asChild variant="ghost">
                <Link href="/problems">Back to list</Link>
              </Button>
            </div>
          </CardContent>
        </Card>
      </main>
    );
  }

  // ── Pre-race ─────────────────────────────────────────────────────────────
  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden px-6">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(99,102,241,0.12),transparent_60%)]" />
      <Card className="relative w-full max-w-lg border-border/60 bg-card/60">
        <CardHeader>
          <Eyebrow>Solo practice</Eyebrow>
          <CardTitle className="flex items-center gap-2 text-2xl">
            <span className="font-mono text-primary">{problem.id}</span>
            {problem.name}
            {problem.rating !== null && (
              <Badge variant="outline" className="ml-auto font-mono">
                {problem.rating}
              </Badge>
            )}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-5">
          <p className="text-sm text-muted-foreground">
            3:00 on the clock · 50 submissions · Your editor and webcam are
            recorded for replay.
          </p>
          <div className="flex items-center gap-2">
            <span className="font-mono text-xs uppercase tracking-widest text-muted-foreground">
              Language
            </span>
            <Segmented
              options={["cpp", "py"] as Lang[]}
              value={lang}
              onChange={(l) => {
                setLang(l);
                setPreferredLang(l);
              }}
              labelFor={(l) => (l === "cpp" ? "C++" : "Python")}
            />
          </div>
          <div className="overflow-hidden rounded-lg border border-border/60 bg-black/50">
            {camState === "ready" ? (
              <video
                ref={previewRef}
                autoPlay
                muted
                playsInline
                className="aspect-video w-full object-cover"
              />
            ) : (
              <div className="flex aspect-video w-full items-center justify-center">
                {camState === "pending" ? (
                  <p className="flex items-center gap-2 font-mono text-sm text-muted-foreground">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Requesting camera…
                  </p>
                ) : (
                  <p className="flex items-center gap-2 font-mono text-sm text-amber-400">
                    <CameraOff className="h-4 w-4" />
                    {camEnabled
                      ? "No camera — run will be recorded without video"
                      : "Webcam off — run will be recorded without video"}
                  </p>
                )}
              </div>
            )}
          </div>
          <div className="flex items-center justify-between">
            {camState === "ready" ? (
              <p className="flex items-center gap-1.5 font-mono text-xs text-green-400">
                <Camera className="h-3.5 w-3.5" /> Camera ready
              </p>
            ) : (
              <span />
            )}
            <button
              type="button"
              onClick={() => setCamEnabled((v) => !v)}
              className="flex items-center gap-1.5 font-mono text-xs text-muted-foreground hover:text-foreground"
            >
              {camEnabled ? (
                <>
                  <CameraOff className="h-3.5 w-3.5" /> Turn webcam off
                </>
              ) : (
                <>
                  <Camera className="h-3.5 w-3.5" /> Turn webcam on
                </>
              )}
            </button>
          </div>
          <div className="flex items-center gap-2">
            <Button className="flex-1" onClick={start} disabled={starting}>
              <Play className="mr-2 h-4 w-4" />
              {starting ? "Starting…" : "Start run"}
            </Button>
            <Button asChild variant="ghost">
              <Link href="/problems">Back</Link>
            </Button>
          </div>
        </CardContent>
      </Card>
    </main>
  );
}
