"use client";

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

/** Upload a finished recording; query identifies the solo session or race. */
export async function uploadRecording(
  blob: Blob,
  query: Record<string, string>
): Promise<boolean> {
  const qs = new URLSearchParams(query).toString();
  try {
    const res = await fetch(`/api/recordings?${qs}`, {
      method: "POST",
      headers: { "Content-Type": "video/webm" },
      body: blob,
    });
    return res.ok;
  } catch {
    return false;
  }
}
