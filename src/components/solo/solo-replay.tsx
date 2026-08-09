"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ReplayCore, ReplayBadges } from "@/components/replay/replay-player";
import { ShareButton } from "@/components/shell/share-button";
import { Button } from "@/components/ui/button";
import { formatMsPrecise } from "@/lib/templates";
import { cn } from "@/lib/utils";
import type { SessionReplayResponse } from "@/lib/session-log";
import { Download } from "lucide-react";

export function SoloReplay({
  sessionId,
  showExport = false,
  apiUrl,
  readOnly = false,
}: {
  sessionId?: string;
  showExport?: boolean;
  /** Override the replay data endpoint (e.g. public share tokens). */
  apiUrl?: string;
  /** Public share view: no share/export controls. */
  readOnly?: boolean;
}) {
  const [log, setLog] = useState<SessionReplayResponse | null | undefined>(undefined);

  const url = apiUrl ?? `/api/solo/replay?sessionId=${sessionId}`;
  useEffect(() => {
    fetch(url, { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : null))
      .then(setLog)
      .catch(() => setLog(null));
  }, [url]);

  if (log === undefined) {
    return (
      <main className="flex h-full items-center justify-center">
        <p className="animate-pulse font-mono text-sm text-muted-foreground">
          Loading replay…
        </p>
      </main>
    );
  }
  if (log === null) {
    return (
      <main className="flex h-full flex-col items-center justify-center gap-3">
        <p className="font-mono text-sm text-muted-foreground">
          No replay found for this run.
        </p>
        {!readOnly && (
          <Button asChild size="sm" variant="secondary">
            <Link href="/sessions">Back to sessions</Link>
          </Button>
        )}
      </main>
    );
  }

  const downloadTouristJson = () => {
    const data = {
      problemId: log.problemId,
      lang: log.lang,
      solveMs: log.solveMs,
      events: log.events,
    };
    const blob = new Blob([JSON.stringify(data)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${log.problemId}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <ReplayCore
      log={log}
      videoUrl={log.recordingUrl}
      videoOffsetMs={log.recordingOffsetMs}
      problem={log.problem}
      header={(clockMs, solved) => (
        <header
          className={cn(
            "flex items-center gap-3 border-b border-border/60 px-5 py-3",
            solved ? "bg-green-500/15" : "bg-primary/10"
          )}
        >
          <span className="text-lg font-bold">
            <span className="font-mono text-primary">{log.problemId}</span>{" "}
            {log.problemName}
          </span>
          <span className="font-mono text-sm text-muted-foreground">
            {readOnly ? "shared replay" : "replay"} ·{" "}
            {log.outcome === "solved"
              ? "AC"
              : log.outcome === "timeout"
                ? "DNF"
                : (log.outcome ?? "in progress")}
          </span>
          {!readOnly && sessionId && <ShareButton sessionId={sessionId} />}
          <span className="ml-auto">
            <ReplayBadges log={log} clockMs={clockMs} />
          </span>
          <span className="font-mono text-xl tabular-nums">
            {solved && log.solveMs !== null ? (
              <span className="font-bold text-green-400">
                AC {formatMsPrecise(log.solveMs)}
              </span>
            ) : (
              formatMsPrecise(clockMs)
            )}
          </span>
        </header>
      )}
      footerExtra={
        showExport && !readOnly ? (
          <div className="flex gap-1">
            <Button size="sm" variant="ghost" onClick={downloadTouristJson}>
              <Download className="mr-1.5 h-3.5 w-3.5" />
              Tourist JSON
            </Button>
          </div>
        ) : undefined
      }
    />
  );
}
