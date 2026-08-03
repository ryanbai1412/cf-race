"use client";

import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { VerdictChip } from "./verdict-chip";
import type { RunResult, Submission } from "@/lib/types";
import { ChevronDown, ChevronRight } from "lucide-react";

export type ConsoleTab = "samples" | "custom" | "submissions";

function OutputBlock({
  label,
  text,
  truncated,
}: {
  label: string;
  text: string;
  truncated?: boolean;
}) {
  if (!text) return null;
  return (
    <div>
      <p className="mb-0.5 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
        {label}
        {truncated && " (truncated)"}
      </p>
      <pre className="max-h-40 overflow-auto rounded bg-black/40 p-2 font-mono text-xs">
        {text}
      </pre>
    </div>
  );
}

function SampleRow({
  r,
  input,
  expected,
}: {
  r: RunResult["results"][number];
  input?: string;
  expected?: string;
}) {
  const [open, setOpen] = useState(r.verdict !== "AC");
  return (
    <div className="rounded-md border border-border/60">
      <button
        className="flex w-full items-center gap-2 px-3 py-2 text-left"
        onClick={() => setOpen((o) => !o)}
      >
        {open ? <ChevronDown className="h-3.5 w-3.5" /> : <ChevronRight className="h-3.5 w-3.5" />}
        <span className="font-mono text-sm">{r.name}</span>
        <VerdictChip verdict={r.verdict} />
        <span className="ml-auto font-mono text-xs text-muted-foreground">
          {r.timeMs}ms
        </span>
      </button>
      {open && (
        <div className="space-y-2 border-t border-border/60 p-3">
          {r.checkerNote && (
            <p className="font-mono text-xs text-amber-400">{r.checkerNote}</p>
          )}
          <OutputBlock label="Input" text={input ?? ""} />
          <OutputBlock label="Expected" text={expected ?? ""} />
          <OutputBlock
            label="Your output (stdout)"
            text={r.stdout}
            truncated={r.stdoutTruncated}
          />
          <OutputBlock label="stderr" text={r.stderr} truncated={r.stderrTruncated} />
        </div>
      )}
    </div>
  );
}

export function ConsolePanel({
  runResult,
  runBusy,
  runError,
  checkerWarning,
  sampleInputs,
  customInput,
  setCustomInput,
  customResult,
  customBusy,
  onRunCustom,
  submissions,
  submissionsUsed,
  maxSubmissions,
  tab,
  onTabChange,
}: {
  runResult: RunResult | null;
  runBusy: boolean;
  runError: string | null;
  checkerWarning: boolean;
  sampleInputs: { input: string; output: string }[];
  customInput: string;
  setCustomInput: (v: string) => void;
  customResult: RunResult | null;
  customBusy: boolean;
  onRunCustom: () => void;
  submissions: Submission[];
  submissionsUsed: number;
  maxSubmissions: number;
  tab: ConsoleTab;
  onTabChange: (tab: ConsoleTab) => void;
}) {
  return (
    <Tabs
      value={tab}
      onValueChange={(v) => onTabChange(v as ConsoleTab)}
      className="flex h-full flex-col"
    >
      <TabsList className="mx-3 mt-2 w-fit">
        <TabsTrigger value="samples">Samples</TabsTrigger>
        <TabsTrigger value="custom">Custom test</TabsTrigger>
        <TabsTrigger value="submissions">
          Submissions{" "}
          <span className="ml-1.5 font-mono text-xs text-muted-foreground">
            {submissionsUsed}/{maxSubmissions}
          </span>
        </TabsTrigger>
      </TabsList>

      <TabsContent value="samples" className="flex-1 space-y-2 overflow-y-auto px-3 pb-3">
        {checkerWarning && (
          <p className="rounded border border-amber-500/40 bg-amber-500/10 p-2 text-xs text-amber-400">
            This problem may accept multiple answers — sample checking here can
            report false WA.
          </p>
        )}
        {runError && <p className="text-sm text-destructive">{runError}</p>}
        {runBusy && <p className="animate-pulse text-sm text-muted-foreground">Running…</p>}
        {runResult && !runResult.compile.ok && (
          <div>
            <VerdictChip verdict="CE" />
            <pre className="mt-2 max-h-48 overflow-auto rounded bg-black/40 p-2 font-mono text-xs text-red-300">
              {runResult.compile.stderr}
            </pre>
          </div>
        )}
        {runResult?.compile.ok &&
          runResult.results.map((r, i) => (
            <SampleRow
              key={r.name}
              r={r}
              input={sampleInputs[i]?.input}
              expected={sampleInputs[i]?.output}
            />
          ))}
        {!runResult && !runBusy && !runError && (
          <p className="pt-2 text-sm text-muted-foreground">
            Press <kbd className="rounded border px-1 font-mono">Ctrl+Enter</kbd> to run
            your code on the sample tests.
          </p>
        )}
      </TabsContent>

      <TabsContent value="custom" className="flex-1 space-y-2 overflow-y-auto px-3 pb-3">
        <textarea
          className="h-24 w-full resize-y rounded-md border border-border bg-black/30 p-2 font-mono text-xs outline-none focus:ring-1 focus:ring-primary"
          placeholder="Custom input…"
          value={customInput}
          onChange={(e) => setCustomInput(e.target.value)}
        />
        <Button size="sm" onClick={onRunCustom} disabled={customBusy}>
          {customBusy ? "Running…" : "Run custom input"}
        </Button>
        {customResult && !customResult.compile.ok && (
          <pre className="max-h-48 overflow-auto rounded bg-black/40 p-2 font-mono text-xs text-red-300">
            {customResult.compile.stderr}
          </pre>
        )}
        {customResult?.compile.ok &&
          customResult.results.map((r) => (
            <div key={r.name} className="space-y-2">
              <div className="flex items-center gap-2">
                <span className="font-mono text-xs text-muted-foreground">
                  {r.timeMs}ms
                </span>
                {r.verdict !== "AC" && r.verdict !== "WA" && <VerdictChip verdict={r.verdict} />}
              </div>
              <OutputBlock label="stdout" text={r.stdout} truncated={r.stdoutTruncated} />
              <OutputBlock label="stderr" text={r.stderr} truncated={r.stderrTruncated} />
              {!r.stdout && !r.stderr && (
                <p className="text-xs text-muted-foreground">(no output)</p>
              )}
            </div>
          ))}
      </TabsContent>

      <TabsContent value="submissions" className="flex-1 space-y-2 overflow-y-auto px-3 pb-3">
        {submissions.length === 0 && (
          <p className="pt-2 text-sm text-muted-foreground">
            No submissions yet. <kbd className="rounded border px-1 font-mono">Ctrl+Shift+Enter</kbd>{" "}
            submits against the full test set.
          </p>
        )}
        {submissions.map((s) => (
          <div key={s.id} className="rounded-md border border-border/60 px-3 py-2">
            <div className="flex items-center gap-3">
              <VerdictChip verdict={s.verdict ?? "PENDING"} />
              <span className="font-mono text-xs uppercase text-muted-foreground">
                {s.lang}
              </span>
              {s.details?.failedTest && (
                <span className="font-mono text-xs text-muted-foreground">
                  failed on {s.details.failedTest}
                </span>
              )}
              {typeof s.details?.passedCount === "number" && (
                <span className="font-mono text-xs text-muted-foreground">
                  {s.details.passedCount}/{s.details.totalCount} passed
                </span>
              )}
              <span className="ml-auto font-mono text-xs text-muted-foreground">
                {new Date(s.submitted_at).toLocaleTimeString()}
              </span>
            </div>
            {s.details?.compileError && (
              <pre className="mt-2 max-h-40 overflow-auto rounded bg-black/40 p-2 font-mono text-xs text-red-300">
                {s.details.compileError}
              </pre>
            )}
          </div>
        ))}
      </TabsContent>
    </Tabs>
  );
}
