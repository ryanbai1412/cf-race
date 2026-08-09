"use client";

import { supabase } from "./realtime";

/**
 * Low-level HTTP for webcam recording uploads (see src/app/api/recordings).
 * Two shapes are supported: the legacy single-blob upload and the streamed
 * chunk upload used while the recording is still running.
 */

export type RecordingQuery = Record<string, string>;

export type ChunkManifestEntry = { index: number; size: number };

function qs(query: RecordingQuery, extra: RecordingQuery): string {
  return new URLSearchParams({ ...query, ...extra }).toString();
}

/** PUT to a Supabase signed upload URL via XHR so we get upload progress. */
function putWithProgress(
  url: string,
  blob: Blob,
  onProgress?: (loaded: number, total: number) => void
): Promise<boolean> {
  return new Promise((resolve) => {
    const xhr = new XMLHttpRequest();
    xhr.open("PUT", url);
    xhr.setRequestHeader("content-type", "video/webm");
    xhr.setRequestHeader("x-upsert", "true");
    xhr.upload.onprogress = (e) => {
      if (e.lengthComputable && e.total > 0) onProgress?.(e.loaded, e.total);
    };
    xhr.onload = () => resolve(xhr.status >= 200 && xhr.status < 300);
    xhr.onerror = () => resolve(false);
    xhr.send(blob);
  });
}

async function sign(
  query: RecordingQuery,
  extra: RecordingQuery = {}
): Promise<{ path: string; token: string; signedUrl?: string } | null> {
  const res = await fetch(`/api/recordings?${qs(query, { ...extra, step: "sign" })}`, {
    method: "POST",
  });
  if (!res.ok) return null;
  return (await res.json()) as { path: string; token: string; signedUrl?: string };
}

async function putSigned(
  signed: { path: string; token: string; signedUrl?: string },
  blob: Blob,
  onProgress?: (loaded: number, total: number) => void
): Promise<boolean> {
  if (signed.signedUrl && typeof XMLHttpRequest !== "undefined") {
    return putWithProgress(signed.signedUrl, blob, onProgress);
  }
  const { error } = await supabase()
    .storage.from("recordings")
    .uploadToSignedUrl(signed.path, signed.token, blob, {
      contentType: "video/webm",
    });
  if (error) return false;
  onProgress?.(blob.size, blob.size);
  return true;
}

/**
 * Upload one numbered chunk of a streamed recording and have the server
 * verify it landed with the expected byte size. Chunks are immutable objects
 * under `<recording path without .webm>/chunks/NNNNNN.webm`.
 */
export async function uploadChunk(
  query: RecordingQuery,
  index: number,
  blob: Blob,
  onProgress?: (loaded: number, total: number) => void
): Promise<boolean> {
  try {
    const signed = await sign(query, { chunk: String(index) });
    if (!signed) return false;
    if (!(await putSigned(signed, blob, onProgress))) return false;
    const res = await fetch(
      `/api/recordings?${qs(query, {
        step: "chunk-confirm",
        chunk: String(index),
        size: String(blob.size),
      })}`,
      { method: "POST" }
    );
    return res.ok;
  } catch {
    return false;
  }
}

/**
 * Ask the server to stitch the uploaded chunks into the final recording
 * object and record it in the DB. Only a matching manifest is accepted.
 */
export async function finalizeRecording(
  query: RecordingQuery,
  chunks: ChunkManifestEntry[]
): Promise<boolean> {
  try {
    const res = await fetch(`/api/recordings?${qs(query, { step: "finalize" })}`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ chunks }),
    });
    return res.ok;
  } catch {
    return false;
  }
}

/**
 * Legacy/fallback path: upload a finished recording as one blob. Used when
 * streamed chunking isn't available (no IndexedDB / no MediaRecorder
 * timeslice support) and for recordings queued by older page loads.
 */
export async function uploadRecording(
  blob: Blob,
  query: RecordingQuery,
  onProgress?: (frac: number) => void
): Promise<boolean> {
  try {
    const signed = await sign(query);
    if (!signed) return false;
    const ok = await putSigned(signed, blob, (loaded, total) => {
      // Cap at 99% — 100% only after the server confirms the save.
      if (total > 0) onProgress?.(Math.min(loaded / total, 0.99));
    });
    if (!ok) return false;
    const confirmRes = await fetch(
      `/api/recordings?${qs(query, { step: "confirm" })}`,
      { method: "POST" }
    );
    if (!confirmRes.ok) return false;
    onProgress?.(1);
    return true;
  } catch {
    return false;
  }
}
