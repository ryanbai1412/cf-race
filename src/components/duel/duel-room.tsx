"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import confetti from "canvas-confetti";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { CountdownOverlay } from "@/components/station/countdown-overlay";
import { RaceScreen } from "@/components/race/race-screen";
import { SoloAuthButton, useSoloAuth } from "@/components/solo/auth-button";
import { formatMsPrecise } from "@/lib/templates";
import {
  duelChannel,
  sendDuelBroadcast,
  type DuelBroadcast,
} from "@/lib/realtime";
import {
  acquireWebcam,
  startWebcamRecording,
  uploadRecording,
  type WebcamRecording,
} from "@/lib/webcam-recorder";
import type { Contestant, Lang, Problem, RunResult } from "@/lib/types";
import { summarizeRun } from "@/lib/tourist";
import {
  createEditorRecorder,
  type RecordedEditorEvent,
} from "@/lib/replay-recorder";
import type { RealtimeChannel } from "@supabase/supabase-js";
import {
  Camera,
  CameraOff,
  Check,
  Copy,
  Loader2,
  Swords,
  Video,
} from "lucide-react";
import { toast } from "sonner";

type StatePlayer = {
  userId: string;
  name: string;
  avatarUrl: string | null;
  ready: boolean;
};

type MatchPlayer = {
  userId: string;
  sessionId: string;
  outcome: "solved" | "timeout" | "abandoned" | null;
  solveMs: number | null;
};

type RoomState = {
  serverNow: number;
  userId: string;
  room: {
    id: string;
    status: "lobby" | "racing" | "done";
    totalTimeSec: number | null;
    graceAfterAcSec: number | null;
    createdBy: string;
  };
  players: StatePlayer[];
  match: {
    id: string;
    startAtMs: number;
    totalTimeSec: number | null;
    graceAfterAcSec: number | null;
    firstAcAtMs: number | null;
    finishedAtMs: number | null;
    winnerUserId: string | null;
    yourSessionId: string | null;
    problem: Problem | null;
    players: MatchPlayer[];
  } | null;
};

const DUEL_CONTESTANT: Contestant = {
  id: "duel",
  event_id: "duel",
  station_role: "station1",
  name: "Duel",
  country: null,
  retired_at: null,
};

export function DuelRoom({ roomId }: { roomId: string }) {
  const auth = useSoloAuth();
  const { user, loading } = auth;
  const [state, setState] = useState<RoomState | null>(null);
  const [notFound, setNotFound] = useState(false);
  const [joining, setJoining] = useState(false);
  const [readyBusy, setReadyBusy] = useState(false);
  const [camState, setCamState] = useState<"pending" | "ready" | "none">("pending");
  const [uploadState, setUploadState] = useState<
    "none" | "uploading" | "done" | "failed"
  >("none");
  const [uploadProgress, setUploadProgress] = useState(0);
  const [copied, setCopied] = useState(false);
  // The session id I raced under; kept after the match ends so the finish
  // screen survives the room flipping back to lobby.
  const [racedSessionId, setRacedSessionId] = useState<string | null>(null);
  const [finishedLocal, setFinishedLocal] = useState<{
    outcome: "solved" | "timeout";
    solveMs: number | null;
    matchId: string;
  } | null>(null);

  const clockOffset = useRef(0);
  const serverNow = useCallback(() => Date.now() + clockOffset.current, []);

  const streamRef = useRef<MediaStream | null>(null);
  const previewRef = useRef<HTMLVideoElement | null>(null);
  const recordingRef = useRef<WebcamRecording | null>(null);
  const channelRef = useRef<RealtimeChannel | null>(null);
  const stateRef = useRef<RoomState | null>(null);
  stateRef.current = state;

  const refresh = useCallback(async () => {
    try {
      const res = await fetch(`/api/duel/state?roomId=${roomId}`, {
        cache: "no-store",
      });
      if (res.status === 404) {
        setNotFound(true);
        return;
      }
      if (!res.ok) return;
      const d: RoomState = await res.json();
      clockOffset.current = d.serverNow - Date.now();
      setState(d);
    } catch {}
  }, [roomId]);

  useEffect(() => {
    if (!user) return;
    void refresh();
    const iv = setInterval(refresh, 2500);
    return () => clearInterval(iv);
  }, [user, refresh]);

  // Realtime: lobby sync nudges + opponent AC notifications.
  useEffect(() => {
    if (!user) return;
    const ch = duelChannel(roomId);
    channelRef.current = ch;
    ch.on("broadcast", { event: "duel" }, ({ payload }) => {
      const msg = payload as DuelBroadcast;
      if (msg.type === "ac" && msg.userId !== user.id) {
        toast(`${msg.name} got AC in ${formatMsPrecise(msg.solveMs)}!`, {
          description: "Grace window — finish your solve to still count.",
        });
      }
      void refresh();
    });
    ch.subscribe();
    return () => {
      void ch.unsubscribe();
      channelRef.current = null;
    };
  }, [user, roomId, refresh]);

  const nudge = useCallback(() => {
    const ch = channelRef.current;
    if (ch) sendDuelBroadcast(ch, { type: "sync" });
  }, []);

  const me = state?.players.find((p) => p.userId === state.userId) ?? null;
  const opponent = state?.players.find((p) => p.userId !== state?.userId) ?? null;
  const isMember = me !== null;
  const match = state?.match ?? null;
  const mySessionId = match?.yourSessionId ?? null;
  const myMatchPlayer =
    match?.players.find((p) => p.userId === state?.userId) ?? null;
  const oppMatchPlayer =
    match?.players.find((p) => p.userId !== state?.userId) ?? null;

  // Racing when there is a live match I'm part of and I'm not decided yet.
  const racing =
    match !== null &&
    mySessionId !== null &&
    match.finishedAtMs === null &&
    finishedLocal?.matchId !== match.id &&
    myMatchPlayer?.outcome === null;

  // Webcam (members only; preview + recording).
  useEffect(() => {
    if (!isMember) return;
    let cancelled = false;
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
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isMember]);

  useEffect(() => {
    if (camState === "ready" && previewRef.current && streamRef.current) {
      previewRef.current.srcObject = streamRef.current;
    }
  });

  // Start the webcam recording as soon as my match session exists (countdown).
  useEffect(() => {
    if (!mySessionId || racedSessionId === mySessionId) return;
    setRacedSessionId(mySessionId);
    setFinishedLocal(null);
    setUploadState("none");
    if (streamRef.current && !recordingRef.current) {
      recordingRef.current = startWebcamRecording(streamRef.current);
    }
  }, [mySessionId, racedSessionId]);

  // Editor event recorder (deltas + keyframes), flushed to /api/duel/events.
  const matchStartRef = useRef<number | null>(null);
  matchStartRef.current = match?.startAtMs ?? matchStartRef.current;
  const sessionIdRef = useRef<string | null>(null);
  sessionIdRef.current = mySessionId ?? racedSessionId;

  const buffer = useRef<RecordedEditorEvent[]>([]);
  const editorRecorder = useMemo(
    () =>
      createEditorRecorder({
        now: () => {
          const startAt = matchStartRef.current;
          if (startAt === null) return null;
          return Math.max(0, Date.now() + clockOffset.current - startAt);
        },
        push: (ev) => buffer.current.push(ev),
      }),
    []
  );

  const tNow = useCallback(() => {
    const startAt = matchStartRef.current;
    if (startAt === null) return 0;
    return Math.max(0, Date.now() + clockOffset.current - startAt);
  }, []);

  const recordRun = useCallback(
    (lang: Lang) => {
      buffer.current.push({ t: tNow(), code: "", lang, kind: "run" });
    },
    [tNow]
  );
  const recordRunResult = useCallback(
    (result: RunResult, target: "samples" | "custom", lang: Lang) => {
      buffer.current.push({
        t: tNow(),
        code: "",
        lang,
        kind: "run_result",
        payload: summarizeRun(result, target),
      });
    },
    [tNow]
  );
  const recordTab = useCallback(
    (tab: string, lang: Lang) => {
      buffer.current.push({ t: tNow(), code: "", lang, kind: "tab", payload: { tab } });
    },
    [tNow]
  );
  const recordScroll = useCallback(
    (frac: number, lang: Lang) => {
      buffer.current.push({
        t: tNow(),
        code: "",
        lang,
        kind: "scroll",
        payload: { frac },
      });
    },
    [tNow]
  );

  const flushEvents = useCallback(() => {
    const sid = sessionIdRef.current;
    const events = buffer.current;
    if (!sid || events.length === 0) return;
    buffer.current = [];
    void fetch("/api/duel/events", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ sessionId: sid, events }),
      keepalive: true,
    }).catch(() => {});
  }, []);

  useEffect(() => {
    if (!racing) return;
    const id = setInterval(flushEvents, 5000);
    return () => clearInterval(id);
  }, [racing, flushEvents]);

  // Mark abandoned if the tab closes mid-race.
  useEffect(() => {
    if (!racing) return;
    const onUnload = () => {
      flushEvents();
      const sid = sessionIdRef.current;
      if (sid) {
        navigator.sendBeacon(
          "/api/duel/finish",
          JSON.stringify({ sessionId: sid, outcome: "abandoned" })
        );
      }
    };
    window.addEventListener("beforeunload", onUnload);
    return () => window.removeEventListener("beforeunload", onUnload);
  }, [racing, flushEvents]);

  const finishLocal = useCallback(
    (outcome: "solved" | "timeout", solveMs: number | null) => {
      const m = stateRef.current?.match;
      if (!m) return;
      setFinishedLocal((prev) =>
        prev?.matchId === m.id ? prev : { outcome, solveMs, matchId: m.id }
      );
    },
    []
  );

  // Effective end of the race for me: total cutoff and/or grace after 1st AC.
  const endAtMs = useMemo(() => {
    if (!match) return null;
    let end: number | null = null;
    if (match.totalTimeSec) end = match.startAtMs + match.totalTimeSec * 1000;
    if (match.firstAcAtMs !== null && match.graceAfterAcSec !== null) {
      const graceEnd = match.firstAcAtMs + match.graceAfterAcSec * 1000;
      end = end === null ? graceEnd : Math.min(end, graceEnd);
    }
    return end;
  }, [match]);

  // Timer watchdog → timeout finish.
  useEffect(() => {
    if (!racing || endAtMs === null) return;
    const iv = setInterval(() => {
      if (serverNow() > endAtMs) {
        const sid = sessionIdRef.current;
        if (sid) {
          void fetch("/api/duel/finish", {
            method: "POST",
            headers: { "content-type": "application/json" },
            body: JSON.stringify({ sessionId: sid, outcome: "timeout" }),
          }).catch(() => {});
        }
        finishLocal("timeout", null);
      }
    }, 250);
    return () => clearInterval(iv);
  }, [racing, endAtMs, serverNow, finishLocal]);

  // Side effects of finishing: flush events, stop + upload the recording.
  const finished = finishedLocal !== null || myMatchPlayer?.outcome != null;
  useEffect(() => {
    if (!finished || !racedSessionId) return;
    flushEvents();
    if (finishedLocal?.outcome === "solved") {
      confetti({ particleCount: 160, spread: 80, origin: { y: 0.6 } });
    }
    const rec = recordingRef.current;
    recordingRef.current = null;
    if (rec) {
      setUploadState("uploading");
      setUploadProgress(0);
      void rec.stop().then(async (blob) => {
        if (!blob) {
          setUploadState("failed");
          return;
        }
        const startAt = matchStartRef.current ?? rec.startedAtMs;
        const ok = await uploadRecording(
          blob,
          {
            sessionId: racedSessionId,
            offsetMs: String(rec.startedAtMs + clockOffset.current - startAt),
          },
          setUploadProgress
        );
        setUploadState(ok ? "done" : "failed");
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [finished]);

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

  const onSolved = useCallback(() => {
    const startAt = matchStartRef.current;
    const solveMs =
      startAt !== null ? Date.now() + clockOffset.current - startAt : null;
    const ch = channelRef.current;
    const st = stateRef.current;
    if (ch && st && solveMs !== null) {
      const meName =
        st.players.find((p) => p.userId === st.userId)?.name ?? "Opponent";
      sendDuelBroadcast(ch, {
        type: "ac",
        userId: st.userId,
        name: meName,
        solveMs,
      });
    }
    finishLocal("solved", solveMs);
    void refresh();
  }, [finishLocal, refresh]);

  const join = useCallback(async () => {
    setJoining(true);
    try {
      const res = await fetch("/api/duel/join", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ roomId }),
      });
      const d = await res.json();
      if (!res.ok) throw new Error(d.error ?? "Failed to join");
      await refresh();
      nudge();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed to join");
    } finally {
      setJoining(false);
    }
  }, [roomId, refresh, nudge]);

  const setReady = useCallback(
    async (ready: boolean) => {
      setReadyBusy(true);
      try {
        const res = await fetch("/api/duel/ready", {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ roomId, ready }),
        });
        const d = await res.json();
        if (!res.ok) throw new Error(d.error ?? "Failed");
        await refresh();
        nudge();
      } catch (e) {
        toast.error(e instanceof Error ? e.message : "Failed");
      } finally {
        setReadyBusy(false);
      }
    },
    [roomId, refresh, nudge]
  );

  const saveSettings = useCallback(
    async (patch: { totalTimeSec?: number | null; graceAfterAcSec?: number | null }) => {
      try {
        const res = await fetch("/api/duel/settings", {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ roomId, ...patch }),
        });
        if (!res.ok) {
          const d = await res.json();
          throw new Error(d.error ?? "Failed to save settings");
        }
        await refresh();
        nudge();
      } catch (e) {
        toast.error(e instanceof Error ? e.message : "Failed to save settings");
      }
    },
    [roomId, refresh, nudge]
  );

  const copyLink = useCallback(() => {
    void navigator.clipboard.writeText(window.location.href).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    });
  }, []);

  // ── Gates ─────────────────────────────────────────────────────────────────
  if (loading || (user && !state && !notFound)) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <p className="animate-pulse font-mono text-muted-foreground">Loading…</p>
      </main>
    );
  }

  if (!user) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center gap-4 px-6">
        <p className="font-mono text-xs uppercase tracking-[0.3em] text-primary">
          1v1 Duel
        </p>
        <p className="text-sm text-muted-foreground">
          Sign in with Google to join this duel room.
        </p>
        <SoloAuthButton {...auth} next={`/duel/room/${roomId}`} />
      </main>
    );
  }

  if (notFound || !state) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center gap-3 px-6">
        <p className="text-lg font-semibold">Room not found</p>
        <Button asChild variant="secondary">
          <Link href="/duel">Back to duels</Link>
        </Button>
      </main>
    );
  }

  // Full room (2 players, I'm not one of them).
  if (!isMember && state.players.length >= 2) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center gap-4 px-6">
        <Card className="w-full max-w-md border-border/60 bg-card/70 text-center">
          <CardHeader>
            <CardTitle>Room is full</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-sm text-muted-foreground">
              {state.players.map((p) => p.name).join(" vs ")} are already dueling
              here. There is no spectator mode — ask for the review link after
              the match.
            </p>
            <Button asChild variant="secondary">
              <Link href="/duel">Back to duels</Link>
            </Button>
          </CardContent>
        </Card>
      </main>
    );
  }

  // ── Racing (countdown + race screen) ─────────────────────────────────────
  if (racing && match) {
    if (serverNow() < match.startAtMs || !match.problem) {
      return (
        <main className="flex min-h-screen items-center justify-center">
          <CountdownOverlay startAtMs={match.startAtMs} serverNow={serverNow} />
          <p className="animate-pulse font-mono text-muted-foreground">
            Problem revealed at GO…
          </p>
        </main>
      );
    }
    return (
      <>
        {serverNow() < match.startAtMs + 1200 && (
          <CountdownOverlay startAtMs={match.startAtMs} serverNow={serverNow} />
        )}
        <RaceScreen
          eventId=""
          problem={match.problem}
          contestant={{ ...DUEL_CONTESTANT, name: me?.name ?? "You" }}
          raceId={mySessionId}
          endAtMs={endAtMs}
          serverNow={serverNow}
          warmup={false}
          solo
          apiBase="/api/duel"
          label="Duel"
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

  // ── Post-race (upload + result) ──────────────────────────────────────────
  const showFinish =
    racedSessionId !== null &&
    (finishedLocal !== null ||
      (match !== null && match.yourSessionId === racedSessionId));
  if (showFinish && (finishedLocal || myMatchPlayer)) {
    const myOutcome = finishedLocal?.outcome ?? myMatchPlayer?.outcome ?? null;
    const mySolveMs = finishedLocal?.solveMs ?? myMatchPlayer?.solveMs ?? null;
    const solved = myOutcome === "solved";
    const matchDone = match?.finishedAtMs != null;
    const iWon = matchDone && match?.winnerUserId === state.userId;
    const uploading = uploadState === "uploading";
    const reviewMatchId = finishedLocal?.matchId ?? match?.id ?? null;
    return (
      <main className="relative flex min-h-screen items-center justify-center px-6">
        {uploading && (
          <div className="absolute inset-0 z-40 flex items-center justify-center bg-background/80 backdrop-blur-sm">
            <Card className="w-full max-w-sm border-border/60 bg-card text-center">
              <CardContent className="space-y-3 pt-6">
                <Loader2 className="mx-auto h-6 w-6 animate-spin text-primary" />
                <p className="text-sm font-medium">
                  Uploading webcam recording… {Math.round(uploadProgress * 100)}%
                </p>
                <div className="h-1.5 w-full overflow-hidden rounded-full bg-muted">
                  <div
                    className="h-full rounded-full bg-primary transition-[width] duration-200"
                    style={{ width: `${Math.round(uploadProgress * 100)}%` }}
                  />
                </div>
                <p className="text-xs text-muted-foreground">
                  Don&apos;t close this tab — the recording is part of the match
                  review.
                </p>
              </CardContent>
            </Card>
          </div>
        )}
        <Card className="w-full max-w-lg border-border/60 bg-card/70 text-center">
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
            {solved && mySolveMs !== null && (
              <p className="font-mono text-6xl font-bold tabular-nums">
                {formatMsPrecise(mySolveMs)}
              </p>
            )}
            {!matchDone ? (
              <p className="animate-pulse font-mono text-sm text-muted-foreground">
                Waiting for {opponent?.name ?? "opponent"} to finish…
              </p>
            ) : (
              <p
                className={`font-mono text-lg font-bold ${
                  iWon
                    ? "text-green-400"
                    : match?.winnerUserId
                      ? "text-red-400"
                      : "text-muted-foreground"
                }`}
              >
                {iWon
                  ? "You won the duel!"
                  : match?.winnerUserId
                    ? `${opponent?.name ?? "Opponent"} won`
                    : "Both DNF"}
              </p>
            )}
            {matchDone && oppMatchPlayer?.outcome === "solved" &&
              oppMatchPlayer.solveMs !== null && (
                <p className="font-mono text-sm text-muted-foreground">
                  {opponent?.name ?? "Opponent"}: AC{" "}
                  {formatMsPrecise(oppMatchPlayer.solveMs)}
                </p>
              )}
            <p className="font-mono text-xs text-muted-foreground">
              {uploadState === "done" && "Webcam recording saved."}
              {uploadState === "failed" &&
                "Webcam recording could not be saved — the editor replay still works."}
              {uploadState === "none" &&
                camState === "none" &&
                "No camera — this run was recorded without video."}
            </p>
            <div className="flex flex-wrap justify-center gap-2">
              {reviewMatchId && (
                <Button asChild disabled={uploading}>
                  <Link
                    href={`/duel/review/${reviewMatchId}`}
                    aria-disabled={uploading}
                    className={uploading ? "pointer-events-none opacity-50" : ""}
                  >
                    <Video className="mr-1.5 h-4 w-4" />
                    {uploading ? "Review (uploading…)" : "Watch review"}
                  </Link>
                </Button>
              )}
              <Button
                variant="secondary"
                disabled={uploading}
                onClick={() => {
                  setRacedSessionId(null);
                  setFinishedLocal(null);
                  setUploadState("none");
                  void refresh();
                }}
              >
                Back to lobby
              </Button>
            </div>
          </CardContent>
        </Card>
      </main>
    );
  }

  // ── Lobby ─────────────────────────────────────────────────────────────────
  const lastMatch = match;
  return (
    <main className="relative min-h-screen overflow-hidden px-6 py-10">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(99,102,241,0.12),transparent_60%)]" />
      <div className="relative mx-auto max-w-2xl space-y-6">
        <header className="flex items-center gap-3">
          <div>
            <p className="font-mono text-xs uppercase tracking-[0.3em] text-primary">
              Duel lobby
            </p>
            <h1 className="text-2xl font-bold">
              {state.players.map((p) => p.name).join(" vs ") || "Empty room"}
            </h1>
          </div>
          <div className="ml-auto">
            <Button size="sm" variant="secondary" onClick={copyLink}>
              {copied ? (
                <Check className="mr-1.5 h-3.5 w-3.5" />
              ) : (
                <Copy className="mr-1.5 h-3.5 w-3.5" />
              )}
              {copied ? "Copied" : "Copy invite link"}
            </Button>
          </div>
        </header>

        <Card className="border-border/60 bg-card/70">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <Swords className="h-4 w-4 text-primary" /> Players
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {state.players.map((p) => (
              <div
                key={p.userId}
                className="flex items-center gap-3 rounded-md border border-border/60 px-3 py-2"
              >
                {p.avatarUrl ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img
                    src={p.avatarUrl}
                    alt=""
                    className="h-8 w-8 rounded-full"
                    referrerPolicy="no-referrer"
                  />
                ) : (
                  <span className="flex h-8 w-8 items-center justify-center rounded-full bg-muted font-mono text-xs">
                    {p.name.slice(0, 2).toUpperCase()}
                  </span>
                )}
                <span className="text-sm font-medium">
                  {p.name}
                  {p.userId === state.userId && (
                    <span className="text-muted-foreground"> (you)</span>
                  )}
                </span>
                <Badge
                  variant="outline"
                  className={`ml-auto font-mono ${
                    p.ready
                      ? "border-green-500/50 text-green-400"
                      : "text-muted-foreground"
                  }`}
                >
                  {p.ready ? "ready" : "not ready"}
                </Badge>
              </div>
            ))}
            {state.players.length < 2 && (
              <p className="text-sm text-muted-foreground">
                Waiting for an opponent — send them the invite link.
              </p>
            )}
            {!isMember && (
              <Button className="w-full" onClick={join} disabled={joining}>
                {joining ? "Joining…" : "Join duel"}
              </Button>
            )}
          </CardContent>
        </Card>

        {isMember && (
          <>
            <Card className="border-border/60 bg-card/70">
              <CardHeader>
                <CardTitle className="text-lg">Timers</CardTitle>
              </CardHeader>
              <CardContent className="grid gap-4 sm:grid-cols-2">
                <div className="space-y-1.5">
                  <label className="font-mono text-xs text-muted-foreground">
                    Total time (minutes, empty = no limit)
                  </label>
                  <Input
                    type="number"
                    min={1}
                    defaultValue={
                      state.room.totalTimeSec
                        ? Math.round(state.room.totalTimeSec / 60)
                        : ""
                    }
                    key={`total-${state.room.totalTimeSec}`}
                    disabled={me?.ready}
                    onBlur={(e) => {
                      const v = e.target.value.trim();
                      void saveSettings({
                        totalTimeSec: v === "" ? null : Number(v) * 60,
                      });
                    }}
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="font-mono text-xs text-muted-foreground">
                    Time after first AC (seconds, empty = none)
                  </label>
                  <Input
                    type="number"
                    min={5}
                    defaultValue={state.room.graceAfterAcSec ?? ""}
                    key={`grace-${state.room.graceAfterAcSec}`}
                    disabled={me?.ready}
                    onBlur={(e) => {
                      const v = e.target.value.trim();
                      void saveSettings({
                        graceAfterAcSec: v === "" ? null : Number(v),
                      });
                    }}
                  />
                </div>
              </CardContent>
            </Card>

            <Card className="border-border/60 bg-card/70">
              <CardContent className="space-y-4 pt-6">
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
                        <p className="animate-pulse font-mono text-sm text-muted-foreground">
                          Requesting camera…
                        </p>
                      ) : (
                        <p className="flex items-center gap-2 font-mono text-sm text-amber-400">
                          <CameraOff className="h-4 w-4" />
                          No camera — the duel will be recorded without video
                        </p>
                      )}
                    </div>
                  )}
                </div>
                {camState === "ready" && (
                  <p className="flex items-center gap-1.5 font-mono text-xs text-green-400">
                    <Camera className="h-3.5 w-3.5" /> Camera ready
                  </p>
                )}
                <Button
                  className="w-full"
                  size="lg"
                  variant={me?.ready ? "secondary" : "default"}
                  disabled={readyBusy || state.players.length < 2}
                  onClick={() => void setReady(!me?.ready)}
                >
                  {me?.ready ? "Un-ready" : "Ready up"}
                </Button>
                {state.players.length < 2 ? (
                  <p className="text-center font-mono text-xs text-muted-foreground">
                    Need two players to start.
                  </p>
                ) : (
                  <p className="text-center font-mono text-xs text-muted-foreground">
                    Race starts when both players are ready. Problem is picked at
                    random — neither of you has solved it.
                  </p>
                )}
              </CardContent>
            </Card>
          </>
        )}

        {lastMatch?.finishedAtMs != null && (
          <Card className="border-border/60 bg-card/70">
            <CardContent className="flex items-center gap-3 pt-6">
              <span className="font-mono text-sm text-primary">
                {lastMatch.problem?.id ?? "Last match"}
              </span>
              <span className="text-sm text-muted-foreground">
                {lastMatch.winnerUserId
                  ? `${
                      state.players.find((p) => p.userId === lastMatch.winnerUserId)
                        ?.name ?? "Opponent"
                    } won`
                  : "Both DNF"}
              </span>
              <Button asChild size="sm" variant="ghost" className="ml-auto">
                <Link href={`/duel/review/${lastMatch.id}`}>
                  <Video className="mr-1.5 h-3.5 w-3.5" />
                  Review
                </Link>
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </main>
  );
}
