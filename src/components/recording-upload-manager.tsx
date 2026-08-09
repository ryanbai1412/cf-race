"use client";

import { useEffect, useState } from "react";
import {
  retryPendingRecordings,
  subscribeUploads,
  type UploadStatus,
} from "@/lib/upload-manager";

const RETRY_INTERVAL_MS = 30_000;

/**
 * Site-wide recording upload manager (mounted in the root layout). Retries
 * IndexedDB-persisted recordings on load and periodically, shows a bottom-right
 * progress toast for in-flight uploads, and warns before leaving mid-upload.
 */
export function RecordingUploadManager() {
  const [uploads, setUploads] = useState<UploadStatus[]>([]);

  useEffect(() => subscribeUploads(setUploads), []);

  useEffect(() => {
    void retryPendingRecordings();
    const iv = setInterval(() => void retryPendingRecordings(), RETRY_INTERVAL_MS);
    return () => clearInterval(iv);
  }, []);

  // Leaving mid-upload would delay the recording until the next visit — warn.
  const uploading = uploads.some((u) => u.state === "uploading");
  useEffect(() => {
    if (!uploading) return;
    const warn = (e: BeforeUnloadEvent) => {
      e.preventDefault();
      e.returnValue = "";
    };
    window.addEventListener("beforeunload", warn);
    return () => window.removeEventListener("beforeunload", warn);
  }, [uploading]);

  if (uploads.length === 0) return null;
  return (
    <div className="fixed bottom-4 right-4 z-50 w-64 space-y-2">
      {uploads.map((u) => (
        <div
          key={u.id}
          className="space-y-1.5 rounded-lg border border-border/60 bg-background/95 p-3 shadow-lg backdrop-blur"
        >
          {u.state === "uploading" ? (
            <>
              <p className="font-mono text-xs text-foreground">
                Uploading webcam recording… {Math.round(u.progress * 100)}%
              </p>
              <div className="h-1.5 w-full overflow-hidden rounded-full bg-muted">
                <div
                  className="h-full rounded-full bg-primary transition-[width] duration-200"
                  style={{ width: `${Math.round(u.progress * 100)}%` }}
                />
              </div>
              <p className="font-mono text-xs text-muted-foreground">
                Don&apos;t close this tab until it finishes.
              </p>
            </>
          ) : (
            <p className="font-mono text-xs text-amber-400">
              Recording upload failed — will retry automatically.
            </p>
          )}
        </div>
      ))}
    </div>
  );
}
