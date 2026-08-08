"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ReplayCore, ReplayBadges } from "@/components/replay/replay-player";
import { Button } from "@/components/ui/button";
import { formatMsPrecise } from "@/lib/templates";
import { cn } from "@/lib/utils";
import type { SessionReplayResponse } from "@/lib/session-log";
import { Download, Upload } from "lucide-react";
import { toast } from "sonner";

export function SoloReplay({
  sessionId,
  showExport,
}: {
  sessionId: string;
  showExport: boolean;
}) {
  const [log, setLog] = useState<SessionReplayResponse | null | undefined>(undefined);
  const [promoting, setPromoting] = useState(false);

  useEffect(() => {
    fetch(`/api/solo/replay?sessionId=${sessionId}`, { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : null))
      .then(setLog)
      .catch(() => setLog(null));
  }, [sessionId]);

  if (log === undefined) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <p className="animate-pulse font-mono text-muted-foreground">Loading replay…</p>
      </main>
    );
  }
  if (log === null) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <p className="font-mono text-muted-foreground">No replay found for this run.</p>
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

  const promote = async () => {
    if (
      !confirm(
        `Promote this run to the tourist ghost for ${log.problemId}? This overwrites the ghost the monitors play.`
      )
    )
      return;
    setPromoting(true);
    try {
      const res = await fetch("/api/solo/promote", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ sessionId }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? "Promote failed");
      toast.success(`Uploaded tourist ghost: ${data.path}`);
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Promote failed");
    } finally {
      setPromoting(false);
    }
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
            solo replay ·{" "}
            {log.outcome === "solved"
              ? "AC"
              : log.outcome === "timeout"
                ? "DNF"
                : (log.outcome ?? "in progress")}
          </span>
          <Button asChild size="sm" variant="ghost" className="font-mono text-xs">
            <Link href="/solo">← gauntlet</Link>
          </Button>
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
        showExport ? (
          <div className="flex gap-1">
            <Button size="sm" variant="ghost" onClick={downloadTouristJson}>
              <Download className="mr-1.5 h-3.5 w-3.5" />
              Tourist JSON
            </Button>
            <Button
              size="sm"
              variant="ghost"
              onClick={promote}
              disabled={promoting || log.outcome !== "solved"}
            >
              <Upload className="mr-1.5 h-3.5 w-3.5" />
              {promoting ? "Promoting…" : "Promote to tourist"}
            </Button>
          </div>
        ) : undefined
      }
    />
  );
}
