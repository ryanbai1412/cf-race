"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import dynamic from "next/dynamic";
import { Button } from "@/components/ui/button";
import { StatementPane } from "./statement-pane";
import { ConsolePanel } from "./console-panel";
import { STARTER_TEMPLATES, formatMs, formatMsPrecise } from "@/lib/templates";
import { flagEmoji } from "@/lib/countries";
import { cn } from "@/lib/utils";
import type {
  Contestant,
  Lang,
  Problem,
  RunResult,
  Submission,
} from "@/lib/types";
import { Play, Send } from "lucide-react";

const MonacoEditor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

const MAX_SUBMISSIONS = 10;

export function RaceScreen({
  eventId,
  problem,
  contestant,
  raceId,
  endAtMs,
  serverNow,
  warmup,
  onReady,
  ready,
  onEditorChange,
  onSubmitAccepted,
  rivalName,
  rivalSolveMs,
  onSwitchContestant,
}: {
  eventId: string;
  problem: Problem;
  contestant: Contestant;
  raceId: string | null; // null during warm-up
  endAtMs: number | null; // null during warm-up
  serverNow: () => number;
  warmup: boolean;
  onReady?: () => void;
  ready?: boolean;
  onEditorChange?: (code: string, lang: Lang, cursorLine: number) => void;
  onSubmitAccepted?: () => void;
  rivalName?: string;
  rivalSolveMs?: number | null;
  onSwitchContestant?: () => void;
}) {
  const storageKey = `cfr-code-${raceId ?? "warmup"}-${contestant.station_role}`;
  const [lang, setLang] = useState<Lang>("cpp");
  const [code, setCode] = useState<string>(STARTER_TEMPLATES.cpp);
  const touched = useRef(false);
  const [remaining, setRemaining] = useState<number | null>(null);

  const [runResult, setRunResult] = useState<RunResult | null>(null);
  const [runBusy, setRunBusy] = useState(false);
  const [runError, setRunError] = useState<string | null>(null);
  const [customInput, setCustomInput] = useState("");
  const [customResult, setCustomResult] = useState<RunResult | null>(null);
  const [customBusy, setCustomBusy] = useState(false);
  const [submissions, setSubmissions] = useState<Submission[]>([]);
  const [submitBusy, setSubmitBusy] = useState(false);

  // Restore code from localStorage on mount.
  useEffect(() => {
    const saved = localStorage.getItem(storageKey);
    if (saved) {
      try {
        const { code: c, lang: l } = JSON.parse(saved);
        if (typeof c === "string" && (l === "cpp" || l === "py")) {
          setCode(c);
          setLang(l);
          touched.current = true;
        }
      } catch {}
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [storageKey]);

  // Timer.
  useEffect(() => {
    if (endAtMs === null) return;
    const iv = setInterval(() => setRemaining(endAtMs - serverNow()), 200);
    return () => clearInterval(iv);
  }, [endAtMs, serverNow]);

  const timeUp = remaining !== null && remaining <= 0;

  function updateCode(v: string | undefined) {
    const next = v ?? "";
    touched.current = true;
    setCode(next);
    localStorage.setItem(storageKey, JSON.stringify({ code: next, lang }));
    onEditorChange?.(next, lang, 0);
  }

  function switchLang(next: Lang) {
    setLang(next);
    if (!touched.current) setCode(STARTER_TEMPLATES[next]);
    localStorage.setItem(
      storageKey,
      JSON.stringify({ code: touched.current ? code : STARTER_TEMPLATES[next], lang: next })
    );
  }

  const runSamples = useCallback(async () => {
    if (runBusy || timeUp) return;
    setRunBusy(true);
    setRunError(null);
    setRunResult(null);
    try {
      const res = await fetch("/api/judge/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ eventId, lang, source: code, problemId: problem.id }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? "Run failed");
      setRunResult(data);
    } catch (e) {
      setRunError(e instanceof Error ? e.message : "Run failed");
    } finally {
      setRunBusy(false);
    }
  }, [runBusy, timeUp, eventId, lang, code, problem.id]);

  const runCustom = useCallback(async () => {
    if (customBusy || timeUp) return;
    setCustomBusy(true);
    setCustomResult(null);
    try {
      const res = await fetch("/api/judge/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          eventId,
          lang,
          source: code,
          problemId: problem.id,
          customInput,
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? "Run failed");
      setCustomResult(data);
    } catch (e) {
      setCustomResult({
        runId: "",
        compile: { ok: false, stderr: e instanceof Error ? e.message : "Run failed" },
        results: [],
      });
    } finally {
      setCustomBusy(false);
    }
  }, [customBusy, timeUp, eventId, lang, code, problem.id, customInput]);

  const refreshSubmissions = useCallback(async () => {
    if (!raceId) return;
    const res = await fetch(
      `/api/submissions?eventId=${eventId}&raceId=${raceId}&contestantId=${contestant.id}`,
      { cache: "no-store" }
    );
    if (res.ok) setSubmissions((await res.json()).submissions);
  }, [eventId, raceId, contestant.id]);

  useEffect(() => {
    void refreshSubmissions();
  }, [refreshSubmissions]);

  const submit = useCallback(async () => {
    if (warmup || !raceId || submitBusy || timeUp) return;
    setSubmitBusy(true);
    try {
      const res = await fetch("/api/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          eventId,
          raceId,
          contestantId: contestant.id,
          lang,
          source: code,
        }),
      });
      const data = await res.json();
      await refreshSubmissions();
      if (res.ok && data.verdict === "AC") onSubmitAccepted?.();
    } finally {
      setSubmitBusy(false);
    }
  }, [
    warmup, raceId, submitBusy, timeUp, eventId, contestant.id, lang, code,
    refreshSubmissions, onSubmitAccepted,
  ]);

  // Keyboard shortcuts.
  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.ctrlKey && e.key === "Enter") {
        e.preventDefault();
        if (e.shiftKey) void submit();
        else void runSamples();
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [runSamples, submit]);

  const submissionsUsed = submissions.length;

  return (
    <div className="flex h-screen flex-col">
      {/* Top bar */}
      <header className="flex items-center gap-4 border-b border-border/60 bg-card/50 px-4 py-2">
        <span className="font-mono text-xs uppercase tracking-widest text-primary">
          {warmup ? "Warm-up" : "Race"}
        </span>
        <span className="truncate font-semibold">{problem.name}</span>
        <div className="ml-auto flex items-center gap-4">
          {remaining !== null && (
            <span
              className={cn(
                "font-mono text-2xl font-bold tabular-nums",
                remaining < 15000
                  ? "animate-pulse text-red-400"
                  : remaining < 60000
                    ? "text-amber-400"
                    : "text-foreground"
              )}
            >
              {formatMs(remaining)}
            </span>
          )}
          {!warmup && rivalName && (
            <span className="font-mono text-sm">
              {rivalSolveMs != null ? (
                <span className="text-green-400">
                  {rivalName} ✓ AC {formatMsPrecise(rivalSolveMs)}
                </span>
              ) : (
                <span className="text-muted-foreground">
                  vs {rivalName} — racing…
                </span>
              )}
            </span>
          )}
          <span className="text-sm text-muted-foreground">
            {contestant.name} {contestant.country ? flagEmoji(contestant.country) : ""}
          </span>
          <div className="flex overflow-hidden rounded-md border border-border">
            {(["cpp", "py"] as Lang[]).map((l) => (
              <button
                key={l}
                className={cn(
                  "px-3 py-1 font-mono text-xs",
                  lang === l ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:bg-accent"
                )}
                onClick={() => switchLang(l)}
              >
                {l === "cpp" ? "C++" : "Python"}
              </button>
            ))}
          </div>
        </div>
      </header>

      {/* Warm-up banner */}
      {warmup && (
        <div className="flex items-center justify-between border-b border-primary/30 bg-primary/10 px-4 py-1.5 text-sm">
          <span>
            Warm-up — get comfortable. The real race starts when the countdown hits
            zero.
          </span>
          <div className="flex items-center gap-2">
            {onSwitchContestant && (
              <Button size="sm" variant="ghost" onClick={onSwitchContestant}>
                Not {contestant.name}? Switch player
              </Button>
            )}
            {onReady && (
              <Button size="sm" variant={ready ? "secondary" : "default"} onClick={onReady}>
                {ready ? "Ready ✓ (waiting for start)" : "I'm ready"}
              </Button>
            )}
          </div>
        </div>
      )}

      {/* Main panes */}
      <div className="grid min-h-0 flex-1 grid-cols-[45%_55%]">
        <StatementPane problem={problem} />
        <div className="flex min-h-0 flex-col">
          <div className="min-h-0 flex-[3]">
            <MonacoEditor
              height="100%"
              theme="vs-dark"
              language={lang === "cpp" ? "cpp" : "python"}
              value={code}
              onChange={updateCode}
              options={{
                fontSize: 15,
                fontFamily: "var(--font-geist-mono), 'JetBrains Mono', monospace",
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                tabSize: 4,
                automaticLayout: true,
                readOnly: timeUp && !warmup,
              }}
            />
          </div>
          <div className="flex items-center gap-2 border-y border-border/60 bg-card/50 px-3 py-2">
            <Button size="sm" onClick={runSamples} disabled={runBusy || (timeUp && !warmup)}>
              <Play className="mr-1.5 h-3.5 w-3.5" />
              {runBusy ? "Running…" : "Run samples"}
              <kbd className="ml-2 rounded border border-primary-foreground/30 px-1 font-mono text-[10px]">
                Ctrl+↵
              </kbd>
            </Button>
            {!warmup && (
              <Button
                size="sm"
                variant="secondary"
                className="bg-green-600 text-white hover:bg-green-700"
                onClick={submit}
                disabled={submitBusy || timeUp || submissionsUsed >= MAX_SUBMISSIONS}
              >
                <Send className="mr-1.5 h-3.5 w-3.5" />
                {submitBusy ? "Judging…" : "Submit"}
                <kbd className="ml-2 rounded border border-white/30 px-1 font-mono text-[10px]">
                  Ctrl+⇧+↵
                </kbd>
              </Button>
            )}
            {lang === "cpp" && (
              <span className="ml-auto text-xs text-muted-foreground">
                Runs use ASan/UBSan (slower, catches UB); submits use -O2
              </span>
            )}
          </div>
          <div className="min-h-0 flex-[2] overflow-hidden">
            <ConsolePanel
              runResult={runResult}
              runBusy={runBusy}
              runError={runError}
              checkerWarning={problem.special_judge}
              sampleInputs={problem.samples}
              customInput={customInput}
              setCustomInput={setCustomInput}
              customResult={customResult}
              customBusy={customBusy}
              onRunCustom={runCustom}
              submissions={submissions}
              submissionsUsed={submissionsUsed}
              maxSubmissions={MAX_SUBMISSIONS}
            />
          </div>
        </div>
      </div>

      {/* Time's up overlay */}
      {timeUp && !warmup && (
        <div className="fixed inset-0 z-40 flex flex-col items-center justify-center gap-3 bg-background/90 backdrop-blur">
          <h2 className="font-mono text-6xl font-black">TIME&apos;S UP</h2>
          <p className="text-muted-foreground">Great effort — check the leaderboard!</p>
        </div>
      )}
    </div>
  );
}
