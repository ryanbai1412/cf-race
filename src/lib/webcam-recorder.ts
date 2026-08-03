"use client";

import { supabase } from "./realtime";

/**
 * Reusable webcam recording: MediaRecorder → webm blob → POST /api/recordings.
 * Used by the solo practice run and the event station race recorder.
 */

export async function acquireWebcam(): Promise<MediaStream | null> {
  if (typeof navigator === "undefined" || !navigator.mediaDevices) return null;
  try {
    return await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
  } catch {
    try {
      return await navigator.mediaDevices.getUserMedia({ video: true });
    } catch {
      return null;
    }
  }
}

export type WebcamRecording = {
  /** Epoch ms when the recorder actually started capturing. */
  startedAtMs: number;
  /** Stop capture and get the final blob (null if nothing was recorded). */
  stop: () => Promise<Blob | null>;
};

export function startWebcamRecording(stream: MediaStream): WebcamRecording | null {
  if (typeof MediaRecorder === "undefined") return null;
  const mimeType = ["video/webm;codecs=vp8,opus", "video/webm"].find((t) =>
    MediaRecorder.isTypeSupported(t)
  );
  let recorder: MediaRecorder;
  try {
    recorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
  } catch {
    return null;
  }
  const chunks: Blob[] = [];
  recorder.ondataavailable = (e) => {
    if (e.data.size > 0) chunks.push(e.data);
  };
  recorder.start(1000);
  const startedAtMs = Date.now();

  return {
    startedAtMs,
    stop: () =>
      new Promise((resolve) => {
        if (recorder.state === "inactive") {
          resolve(chunks.length ? new Blob(chunks, { type: "video/webm" }) : null);
          return;
        }
        recorder.onstop = () =>
          resolve(chunks.length ? new Blob(chunks, { type: "video/webm" }) : null);
        recorder.stop();
      }),
  };
}

/**
 * Upload a finished recording; query identifies the solo session or race.
 * The webm goes straight to Supabase Storage via a signed upload URL
 * (serverless request-body limits are too small to proxy video), then the
 * API records the path in the DB.
 */
export async function uploadRecording(
  blob: Blob,
  query: Record<string, string>,
  onProgress?: (frac: number) => void
): Promise<boolean> {
  const qs = new URLSearchParams(query).toString();
  try {
    const signRes = await fetch(`/api/recordings?${qs}&step=sign`, {
      method: "POST",
    });
    if (!signRes.ok) return false;
    const { path, token, signedUrl } = (await signRes.json()) as {
      path: string;
      token: string;
      signedUrl?: string;
    };
    if (signedUrl && typeof XMLHttpRequest !== "undefined") {
      const ok = await putWithProgress(signedUrl, blob, onProgress);
      if (!ok) return false;
    } else {
      const { error } = await supabase()
        .storage.from("recordings")
        .uploadToSignedUrl(path, token, blob, { contentType: "video/webm" });
      if (error) return false;
      onProgress?.(1);
    }
    const confirmRes = await fetch(`/api/recordings?${qs}&step=confirm`, {
      method: "POST",
    });
    return confirmRes.ok;
  } catch {
    return false;
  }
}

/** PUT to a Supabase signed upload URL via XHR so we get upload progress. */
function putWithProgress(
  url: string,
  blob: Blob,
  onProgress?: (frac: number) => void
): Promise<boolean> {
  return new Promise((resolve) => {
    const xhr = new XMLHttpRequest();
    xhr.open("PUT", url);
    xhr.setRequestHeader("content-type", "video/webm");
    xhr.setRequestHeader("x-upsert", "true");
    xhr.upload.onprogress = (e) => {
      if (e.lengthComputable && e.total > 0) onProgress?.(e.loaded / e.total);
    };
    xhr.onload = () => resolve(xhr.status >= 200 && xhr.status < 300);
    xhr.onerror = () => resolve(false);
    xhr.send(blob);
  });
}
