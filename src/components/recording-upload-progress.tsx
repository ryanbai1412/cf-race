"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import {
  retryUpload,
  subscribeUploads,
  type UploadStatus,
} from "@/lib/upload-manager";

/**
 * Shared UI for webcam recording uploads. Every page that wants to show
 * upload progress uses these instead of its own state: the upload manager is
 * the single source of truth, so the bar keeps working across reloads and
 * shows the same phases everywhere (chunk upload 0–90%, stitching 90–100%).
 */

/** Live status of one recording's upload, or null when there's nothing to show. */
export function useRecordingUpload(key: string | null | undefined): UploadStatus | null {
  const [uploads, setUploads] = useState<UploadStatus[]>([]);
  useEffect(() => subscribeUploads(setUploads), []);
  if (!key) return null;
  return uploads.find((u) => u.key === key) ?? null;
}

/** "1335A — Bicycle Race", linking to the problem page when we know the id. */
function ProblemLabel({ status }: { status: UploadStatus }) {
  if (!status.label && !status.problemId) return null;
  const text = [status.problemId, status.label].filter(Boolean).join(" — ");
  if (!status.problemId) return <span>{text}</span>;
  return (
    <Link
      href={`/problems/${status.problemId}`}
      className="underline underline-offset-2 hover:text-foreground"
    >
      {text}
    </Link>
  );
}

function verb(status: UploadStatus): string {
  const pct = Math.round(status.progress * 100);
  if (status.state === "failed") return "Webcam recording upload failed";
  if (status.state === "stitching") return `Saving webcam recording… ${pct}%`;
  return `Uploading webcam recording… ${pct}%`;
}

/** Progress bar + message for a single recording upload. */
export function RecordingUploadProgress({
  status,
  className = "",
}: {
  status: UploadStatus | null;
  className?: string;
}) {
  if (!status) return null;
  const label = <ProblemLabel status={status} />;
  if (status.state === "failed") {
    return (
      <div className={`space-y-1.5 ${className}`}>
        <p className="font-mono text-xs text-amber-400">
          {verb(status)}
          {label ? <> for {label}</> : null}.
        </p>
        <Button
          size="sm"
          variant="outline"
          className="h-7 text-xs"
          onClick={() => void retryUpload(status.id)}
        >
          Retry
        </Button>
      </div>
    );
  }
  const pct = Math.round(status.progress * 100);
  return (
    <div className={`space-y-1 ${className}`}>
      <p className="font-mono text-xs text-muted-foreground">
        {verb(status)}
        {label ? <> for {label}</> : null}
      </p>
      <div className="h-1.5 w-full overflow-hidden rounded-full bg-muted">
        <div
          className="h-full rounded-full bg-primary transition-[width] duration-200"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
