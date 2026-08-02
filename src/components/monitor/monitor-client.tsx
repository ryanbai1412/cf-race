"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import confetti from "canvas-confetti";
import { useEventState } from "@/hooks/use-event-state";
import { CodeMirror } from "./code-mirror";
import { TouristPane } from "./tourist-pane";
import { WebcamView } from "./webcam";
import { CountdownOverlay } from "@/components/station/countdown-overlay";
import { LeaderboardTable } from "@/components/leaderboard-table";
import { STARTER_TEMPLATES, formatMs, formatMsPrecise } from "@/lib/templates";
import { flagEmoji } from "@/lib/countries";
import { cn } from "@/lib/utils";
import type { BroadcastMsg, Lang, StationRole } from "@/lib/types";

const IDLE_SLIDE_MS = 12000;

export function MonitorClient({
  eventId,
  monitor,
}: {
  eventId: string;
  monitor: "a" | "b";
}) {
  const station: StationRole = monitor === "a" ? "station1" : "station2";
  const [mirror, setMirror] = useState<{ code: string; lang: Lang }>({
    code: STARTER_TEMPLATES.cpp,
    lang: "cpp",
  });
  const lastEditorAt = useRef(0);
  const [slide, setSlide] = useState(0);
  const [, forceTick] = useState(0);

  const onMessage = useCallback(
    (msg: BroadcastMsg) => {
      if (msg.type === "editor" && msg.station === station) {
        lastEditorAt.current = Date.now();
        setMirror({ code: msg.code, lang: msg.lang });
      } else if (msg.type === "confetti" && msg.station === station) {
        confetti({ particleCount: 250, spread: 110, origin: { y: 0.5 } });
      }
    },
    [station]
  );

  const { state, serverNow } = useEventState(eventId, onMessage);

  useEffect(() => {
    const iv = setInterval(() => forceTick((n) => n + 1), 200);
    return () => clearInterval(iv);
  }, []);

  useEffect(() => {
    const iv = setInterval(() => setSlide((s) => s + 1), IDLE_SLIDE_MS);
    return () => clearInterval(iv);
  }, []);

  if (!state) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <p className="animate-pulse font-mono text-muted-foreground">Connecting…</p>
      </main>
    );
  }

  const contestant = state.contestants[station];
  const race = state.race;
  const participant = race?.participants.find((p) => p.station_role === station);

  // ---------- Race mode ----------
  if (race && participant && race.started_at) {
    const startMs = new Date(race.started_at).getTime();
    const now = serverNow();
    const clockMs = now - startMs;
    const endMs = startMs + race.timer_sec * 1000;
    const solveMs = participant.first_ac_at
      ? new Date(participant.first_ac_at).getTime() - startMs
      : null;
    const remaining = endMs - now;

    return (
      <main className="flex h-screen flex-col bg-background">
        {clockMs < 1200 && (
          <CountdownOverlay startAtMs={startMs} serverNow={serverNow} />
        )}
        <header className="flex items-center gap-4 border-b border-border/60 bg-card/50 px-6 py-3">
          <span className="font-mono text-xs uppercase tracking-[0.3em] text-primary">
            {state.event.name}
          </span>
          <span className="truncate text-lg font-bold">{race.problem.name}</span>
          <span
            className={cn(
              "ml-auto font-mono text-4xl font-black tabular-nums",
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
        <div className="grid min-h-0 flex-1 grid-cols-[60%_40%]">
          <div className="relative flex min-h-0 flex-col">
            <div className="flex items-center gap-2 border-b border-border/60 px-4 py-2">
              <span className="text-xl">
                {contestant?.country ? flagEmoji(contestant.country) : "🏳️"}
              </span>
              <span className="text-lg font-bold">{contestant?.name ?? "—"}</span>
              {solveMs !== null && (
                <span className="ml-auto font-mono text-xl font-bold text-green-400">
                  AC {formatMsPrecise(solveMs)}
                </span>
              )}
            </div>
            <div className="min-h-0 flex-1">
              <CodeMirror code={mirror.code} lang={mirror.lang} />
            </div>
            {contestant && (
              <div className="absolute bottom-4 right-4 z-10 overflow-hidden rounded-lg border border-border/60 shadow-lg">
                <WebcamView
                  eventId={eventId}
                  identity={`monitor-${monitor}`}
                  publisherIdentity={station}
                  className="h-36 w-48 bg-black object-cover"
                />
              </div>
            )}
            {solveMs !== null && (
              <div className="absolute inset-0 z-20 flex flex-col items-center justify-center gap-2 bg-background/80 backdrop-blur-sm">
                <p className="font-mono text-6xl font-black text-green-400">
                  {contestant?.name.toUpperCase()} SOLVED IT
                </p>
                <p className="font-mono text-4xl font-bold tabular-nums">
                  {formatMsPrecise(solveMs)}
                </p>
              </div>
            )}
          </div>
          <TouristPane
            eventId={eventId}
            problemId={race.problem_id}
            touristTimeMs={race.problem.tourist_time_ms}
            clockMs={clockMs}
          />
        </div>
      </main>
    );
  }

  // ---------- Idle mode ----------
  const warmingUp =
    contestant && Date.now() - lastEditorAt.current < 15000;
  const mode = warmingUp ? 2 : slide % 2;

  return (
    <main className="relative flex h-screen flex-col items-center justify-center overflow-hidden bg-background">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(99,102,241,0.15),transparent_60%)]" />
      {mode === 0 && (
        <div className="z-10 space-y-6 px-8 text-center">
          <p className="font-mono text-sm uppercase tracking-[0.4em] text-primary">
            {state.event.name}
          </p>
          <h1 className="max-w-3xl text-6xl font-extrabold tracking-tight">
            Race a Codeforces problem.
          </h1>
          <p className="text-3xl font-bold text-muted-foreground">
            Beat your rival. Beat <span className="text-primary">tourist</span>.
          </p>
          <p className="text-xl text-muted-foreground">
            Ask the booth staff to jump in — all skill levels welcome.
          </p>
        </div>
      )}
      {mode === 1 && (
        <div className="z-10 w-full max-w-2xl px-8">
          <h2 className="mb-4 text-center font-mono text-sm uppercase tracking-[0.4em] text-primary">
            Fastest solves
          </h2>
          <LeaderboardTable eventId={eventId} limit={10} />
        </div>
      )}
      {mode === 2 && contestant && (
        <div className="z-10 flex h-full w-full flex-col">
          <div className="flex items-center gap-2 border-b border-border/60 px-4 py-2">
            <span className="text-xl">
              {contestant.country ? flagEmoji(contestant.country) : "🏳️"}
            </span>
            <span className="text-lg font-bold">{contestant.name}</span>
            <span className="ml-auto font-mono text-sm text-amber-400">
              warming up…
            </span>
          </div>
          <div className="min-h-0 flex-1">
            <CodeMirror code={mirror.code} lang={mirror.lang} />
          </div>
        </div>
      )}
    </main>
  );
}
