"use client";

import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import {
  retryPendingRecordings,
  subscribeUploads,
  type UploadStatus,
} from "@/lib/upload-manager";
import { RecordingUploadProgress } from "@/components/recording-upload-progress";

const RETRY_INTERVAL_MS = 30_000;

/**
 * Pages where a run is happening or being watched. The progress toast would
 * sit on top of the thing the user is concentrating on, so it stays hidden
 * there — uploading itself is unaffected.
 */
const FOCUSED_PAGES = [
  /^\/problems\/[^/]+\/solve/,
  /^\/solo\//,
  /^\/replay\//,
  /^\/r\//,
  /^\/duel\/(room|review)\//,
  /^\/e\//,
];

/**
 * Site-wide recording upload manager (mounted in the root layout). Retries
 * IndexedDB-persisted recordings on load and periodically, shows a bottom-right
 * progress toast for in-flight uploads, and warns before leaving mid-upload.
 */
export function RecordingUploadManager() {
  const [uploads, setUploads] = useState<UploadStatus[]>([]);
  const pathname = usePathname();
  const focused = FOCUSED_PAGES.some((re) => re.test(pathname ?? ""));

  useEffect(() => subscribeUploads(setUploads), []);

  useEffect(() => {
    void retryPendingRecordings();
    const iv = setInterval(() => void retryPendingRecordings(), RETRY_INTERVAL_MS);
    return () => clearInterval(iv);
  }, []);

  // Leaving mid-upload would delay the recording until the next visit — warn.
  const uploading = uploads.some((u) => u.state !== "failed");
  useEffect(() => {
    if (!uploading) return;
    const warn = (e: BeforeUnloadEvent) => {
      e.preventDefault();
      e.returnValue = "";
    };
    window.addEventListener("beforeunload", warn);
    return () => window.removeEventListener("beforeunload", warn);
  }, [uploading]);

  if (uploads.length === 0 || focused) return null;
  return (
    <div className="fixed bottom-4 right-4 z-50 w-64 space-y-2">
      {uploads.map((u) => (
        <div
          key={u.id}
          className="space-y-1.5 rounded-lg border border-border/60 bg-background/95 p-3 shadow-lg backdrop-blur"
        >
          <RecordingUploadProgress status={u} />
          {u.state !== "failed" && (
            <p className="font-mono text-xs text-muted-foreground">
              Don&apos;t close this tab until it finishes.
            </p>
          )}
        </div>
      ))}
    </div>
  );
}
