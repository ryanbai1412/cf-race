"use client";

import { createStreamingUpload, enqueueRecording, type StreamingUpload } from "./upload-manager";
import type { RecordingQuery } from "./recording-upload";

/**
 * Reusable webcam recording: MediaRecorder → chunked upload → /api/recordings.
 * Used by the solo practice run, the duel room and the event station recorder.
 *
 * Chunks are uploaded while the recording is still running (see
 * upload-manager), so a crash or a closed tab loses at most the current
 * timeslice instead of the whole video.
 */

/** MediaRecorder timeslice: how much video a single upload chunk holds. */
const CHUNK_MS = 5000;

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
  /** Whether chunks are being uploaded as they're produced. */
  streaming: boolean;
  /**
   * Stop capture and upload the recording. `tailMs` keeps recording that much
   * longer before stopping, so the video captures the moment after the run
   * ends (e.g. the player's reaction). `query` overrides/completes the params
   * the recording started with (e.g. a corrected offsetMs). Resolves true once
   * the server has confirmed the finished recording.
   */
  /**
   * Merge params (typically offsetMs) into the upload query as soon as they
   * are known, so a recording resumed after a reload keeps them.
   */
  setQuery: (query: RecordingQuery) => void;
  stopAndUpload: (opts?: {
    tailMs?: number;
    query?: RecordingQuery;
    onProgress?: (frac: number) => void;
  }) => Promise<boolean>;
};

/**
 * Start recording `stream`. `query` identifies the target recording
 * (?sessionId=… for solo/duel runs, ?eventId=&raceId=&station=… for races)
 * and is used for the streamed chunk uploads. `label` (the problem name) is
 * shown in the upload progress toast, and `onProgress` reports uploaded
 * bytes from the very first chunk, so progress bars don't sit at 0% during
 * the run and then jump when the recording stops.
 */
export function startWebcamRecording(
  stream: MediaStream,
  query: RecordingQuery,
  {
    label,
    problemId,
    onProgress,
  }: {
    label?: string;
    problemId?: string;
    onProgress?: (frac: number) => void;
  } = {}
): WebcamRecording | null {
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

  // Chunks are handed to the streaming upload as they arrive; until it is
  // ready (IndexedDB open) they're buffered here, and they're kept as a
  // whole-blob fallback for browsers where streaming isn't available.
  const buffered: Blob[] = [];
  let upload: StreamingUpload | null = null;
  let streamingFailed = false;
  let pump: Promise<void> = Promise.resolve();
  const uploadReady = createStreamingUpload(query, { label, problemId, onProgress })
    .then((u) => {
      upload = u;
      if (!u) streamingFailed = true;
    })
    .catch(() => {
      streamingFailed = true;
    });

  recorder.ondataavailable = (e) => {
    if (e.data.size === 0) return;
    buffered.push(e.data);
    const chunk = e.data;
    pump = pump.then(async () => {
      await uploadReady;
      if (upload) await upload.addChunk(chunk);
    });
  };
  recorder.start(CHUNK_MS);
  const startedAtMs = Date.now();

  const stopped = new Promise<void>((resolve) => {
    recorder.onstop = () => resolve();
  });

  return {
    startedAtMs,
    get streaming() {
      return !streamingFailed;
    },
    setQuery: (extra) => {
      void uploadReady.then(() => upload?.setQuery(extra));
    },
    stopAndUpload: async ({
      tailMs = 0,
      query: finalQuery,
      onProgress: finalProgress,
    } = {}) => {
      if (recorder.state !== "inactive") {
        if (tailMs > 0) await new Promise((r) => setTimeout(r, tailMs));
        recorder.stop();
        await stopped;
      }
      await pump;
      await uploadReady;
      if (upload) {
        return upload.finish(finalQuery, finalProgress ?? onProgress);
      }
      if (buffered.length === 0) return false;
      return enqueueRecording(
        new Blob(buffered, { type: "video/webm" }),
        { ...query, ...finalQuery },
        finalProgress ?? onProgress,
        label,
        problemId
      );
    },
  };
}
