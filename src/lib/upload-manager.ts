"use client";

import {
  finalizeRecording,
  uploadChunk,
  uploadRecording,
  type ChunkManifestEntry,
  type RecordingQuery,
} from "./recording-upload";

/**
 * Resilient webcam-recording uploads.
 *
 * Streaming path (default): MediaRecorder emits a chunk every few seconds;
 * each chunk is written to IndexedDB, uploaded as its own immutable storage
 * object, and deleted locally only once the server confirms it exists with
 * the right byte size. When the recording stops, the remaining chunks go up
 * and a finalize call stitches them into the final recording object. A tab
 * that dies mid-recording leaves its chunks and manifest in IndexedDB, so the
 * layout-mounted manager finishes the recording on the next page load.
 *
 * Fallback path: whole finished blobs (browsers without IndexedDB, or entries
 * queued by an older build) are retried the same way against the legacy
 * single-blob endpoint.
 */

const DB_NAME = "cfr-recordings";
const DB_VERSION = 2;
const STORE = "pending";
const UPLOADS = "uploads";
const CHUNKS = "chunks";

type PendingRecording = {
  id: string;
  blob: Blob;
  /** Query params for /api/recordings (identifies the solo session or race). */
  query: RecordingQuery;
  /** Human label for the progress toast, e.g. the problem name. */
  label?: string;
  createdAt: number;
};

/** A streamed recording: manifest of every chunk MediaRecorder produced. */
type UploadRecord = {
  id: string;
  query: RecordingQuery;
  /** Human label for the progress toast, e.g. the problem name. */
  label?: string;
  chunks: ChunkManifestEntry[];
  /** True once the recorder stopped and the manifest is complete. */
  closed: boolean;
  createdAt: number;
};

type ChunkRecord = {
  /** `${uploadId}:${index padded}` so chunks of one upload sort in order. */
  id: string;
  uploadId: string;
  index: number;
  blob: Blob;
};

export type UploadStatus = {
  id: string;
  progress: number;
  state: "uploading" | "failed";
  /** What the recording is of (problem name), when known. */
  label?: string;
};

function openDb(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    if (typeof indexedDB === "undefined") {
      reject(new Error("indexedDB unavailable"));
      return;
    }
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains(STORE)) {
        db.createObjectStore(STORE, { keyPath: "id" });
      }
      if (!db.objectStoreNames.contains(UPLOADS)) {
        db.createObjectStore(UPLOADS, { keyPath: "id" });
      }
      if (!db.objectStoreNames.contains(CHUNKS)) {
        db.createObjectStore(CHUNKS, { keyPath: "id" }).createIndex(
          "uploadId",
          "uploadId"
        );
      }
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function withStore<T>(
  store: string,
  mode: IDBTransactionMode,
  run: (s: IDBObjectStore) => IDBRequest | null
): Promise<T | undefined> {
  const db = await openDb();
  try {
    return await new Promise<T | undefined>((resolve, reject) => {
      const tx = db.transaction(store, mode);
      const req = run(tx.objectStore(store));
      let result: T | undefined;
      if (req) req.onsuccess = () => (result = req.result as T);
      tx.oncomplete = () => resolve(result);
      tx.onerror = () => reject(tx.error);
    });
  } finally {
    db.close();
  }
}

const idbPut = (store: string, value: unknown) =>
  withStore<void>(store, "readwrite", (s) => s.put(value));
const idbDelete = (store: string, key: string) =>
  withStore<void>(store, "readwrite", (s) => s.delete(key));
const idbAll = <T>(store: string) =>
  withStore<T[]>(store, "readonly", (s) => s.getAll());

async function chunksOf(uploadId: string): Promise<ChunkRecord[]> {
  const db = await openDb();
  try {
    return await new Promise<ChunkRecord[]>((resolve, reject) => {
      const req = db
        .transaction(CHUNKS, "readonly")
        .objectStore(CHUNKS)
        .index("uploadId")
        .getAll(IDBKeyRange.only(uploadId));
      req.onsuccess = () => resolve(req.result as ChunkRecord[]);
      req.onerror = () => reject(req.error);
    });
  } finally {
    db.close();
  }
}

const chunkKey = (uploadId: string, index: number) =>
  `${uploadId}:${String(index).padStart(6, "0")}`;

function newId(): string {
  return typeof crypto !== "undefined" && "randomUUID" in crypto
    ? crypto.randomUUID()
    : `${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

// ── In-memory upload state (shared across the page via module singleton) ────

const active = new Set<string>();
let statuses: UploadStatus[] = [];
const listeners = new Set<(s: UploadStatus[]) => void>();

function emit() {
  for (const cb of listeners) cb(statuses);
}

function setStatus(id: string, patch: Partial<UploadStatus> | null) {
  if (patch === null) {
    statuses = statuses.filter((s) => s.id !== id);
  } else {
    const existing = statuses.find((s) => s.id === id);
    statuses = existing
      ? statuses.map((s) => (s.id === id ? { ...s, ...patch } : s))
      : [...statuses, { id, progress: 0, state: "uploading", ...patch }];
  }
  emit();
}

/** Subscribe to upload progress/state; immediately called with current state. */
export function subscribeUploads(cb: (s: UploadStatus[]) => void): () => void {
  listeners.add(cb);
  cb(statuses);
  return () => {
    listeners.delete(cb);
  };
}

// ── Streamed chunk uploads ──────────────────────────────────────────────────

export type StreamingUpload = {
  id: string;
  /** Persist + upload one MediaRecorder chunk (in emission order). */
  addChunk: (blob: Blob) => Promise<void>;
  /**
   * Mark the manifest complete, flush any unconfirmed chunks and finalize.
   * `query` overrides the params the upload started with (e.g. a corrected
   * offsetMs). Resolves true once the server confirmed the finished recording.
   */
  finish: (
    query?: RecordingQuery,
    onProgress?: (frac: number) => void
  ) => Promise<boolean>;
};

/** Uploads created by this page load — they are still being recorded into. */
const liveUploads = new Set<string>();

/**
 * Begin a streamed recording upload. Returns null when IndexedDB is
 * unavailable, so callers can fall back to the single-blob path.
 */
export async function createStreamingUpload(
  query: RecordingQuery,
  label?: string
): Promise<StreamingUpload | null> {
  const record: UploadRecord = {
    id: newId(),
    query,
    label,
    chunks: [],
    closed: false,
    createdAt: Date.now(),
  };
  try {
    await idbPut(UPLOADS, record);
  } catch {
    return null;
  }
  liveUploads.add(record.id);
  setStatus(record.id, { state: "uploading", progress: 0, label });

  let queue: Promise<void> = Promise.resolve();
  let uploadedBytes = 0;
  let totalBytes = 0;
  let onProgress: ((frac: number) => void) | undefined;
  // Chunks whose upload failed stay in IndexedDB and are retried at finish
  // (or by the background manager after a reload).
  const pending = new Map<number, Blob>();

  const report = () => {
    // Cap at 99% — 100% only after the server confirms the finalize step.
    const frac = totalBytes > 0 ? Math.min(uploadedBytes / totalBytes, 0.99) : 0;
    setStatus(record.id, { progress: frac });
    onProgress?.(frac);
  };

  const sendChunk = async (index: number, blob: Blob): Promise<boolean> => {
    const ok = await uploadChunk(record.query, index, blob);
    if (!ok) return false;
    pending.delete(index);
    uploadedBytes += blob.size;
    report();
    try {
      await idbDelete(CHUNKS, chunkKey(record.id, index));
    } catch {}
    return true;
  };

  const addChunk = (blob: Blob): Promise<void> => {
    if (blob.size === 0) return Promise.resolve();
    const index = record.chunks.length;
    record.chunks.push({ index, size: blob.size });
    totalBytes += blob.size;
    pending.set(index, blob);
    queue = queue.then(async () => {
      try {
        await idbPut(CHUNKS, {
          id: chunkKey(record.id, index),
          uploadId: record.id,
          index,
          blob,
        } satisfies ChunkRecord);
        await idbPut(UPLOADS, record);
      } catch {}
      await sendChunk(index, blob);
    });
    return queue;
  };

  const finish: StreamingUpload["finish"] = async (finalQuery, progressCb) => {
    onProgress = progressCb;
    if (finalQuery) record.query = { ...record.query, ...finalQuery };
    record.closed = true;
    // Claim the upload for the whole finish: the background retry loop must
    // not start a second finalize for the same recording.
    active.add(record.id);
    try {
      await queue;
      try {
        await idbPut(UPLOADS, record);
      } catch {}
      if (record.chunks.length === 0) {
        await dropUpload(record.id);
        setStatus(record.id, null);
        return false;
      }
      for (const [index, blob] of [...pending].sort((a, b) => a[0] - b[0])) {
        await sendChunk(index, blob);
      }
      const ok =
        pending.size === 0 && (await finalizeRecording(record.query, record.chunks));
      if (ok) {
        await dropUpload(record.id);
        setStatus(record.id, { progress: 1 });
        setStatus(record.id, null);
        onProgress?.(1);
      } else {
        setStatus(record.id, { state: "failed" });
      }
      return ok;
    } finally {
      liveUploads.delete(record.id);
      active.delete(record.id);
    }
  };

  return { id: record.id, addChunk, finish };
}

async function dropUpload(uploadId: string): Promise<void> {
  try {
    for (const c of await chunksOf(uploadId)) await idbDelete(CHUNKS, c.id);
    await idbDelete(UPLOADS, uploadId);
  } catch {}
}

/**
 * Finish a streamed recording left behind by an earlier page load: upload the
 * chunks still in IndexedDB, then finalize against the stored manifest.
 */
async function resumeUpload(record: UploadRecord): Promise<boolean> {
  if (active.has(record.id)) return false;
  active.add(record.id);
  setStatus(record.id, { state: "uploading", progress: 0, label: record.label });
  try {
    if (!record.closed) {
      // The recorder died with the tab; the chunks it managed to emit are all
      // we will ever get, so treat the manifest as complete.
      record.closed = true;
      await idbPut(UPLOADS, record);
    }
    if (record.chunks.length === 0) {
      await dropUpload(record.id);
      setStatus(record.id, null);
      return false;
    }
    const stored = (await chunksOf(record.id)).sort((a, b) => a.index - b.index);
    const total = record.chunks.reduce((n, c) => n + c.size, 0);
    let uploaded = total - stored.reduce((n, c) => n + c.blob.size, 0);
    setStatus(record.id, { progress: Math.min(uploaded / total, 0.99) });
    for (const c of stored) {
      if (!(await uploadChunk(record.query, c.index, c.blob))) {
        setStatus(record.id, { state: "failed" });
        return false;
      }
      uploaded += c.blob.size;
      setStatus(record.id, { progress: Math.min(uploaded / total, 0.99) });
      await idbDelete(CHUNKS, c.id);
    }
    const ok = await finalizeRecording(record.query, record.chunks);
    if (ok) {
      await dropUpload(record.id);
      setStatus(record.id, null);
    } else {
      setStatus(record.id, { state: "failed" });
    }
    return ok;
  } catch {
    setStatus(record.id, { state: "failed" });
    return false;
  } finally {
    active.delete(record.id);
  }
}

// ── Single-blob uploads (fallback + legacy queue) ───────────────────────────

async function uploadEntry(
  entry: PendingRecording,
  onProgress?: (frac: number) => void
): Promise<boolean> {
  if (active.has(entry.id)) return false;
  active.add(entry.id);
  setStatus(entry.id, { state: "uploading", progress: 0, label: entry.label });
  const ok = await uploadRecording(entry.blob, entry.query, (frac) => {
    setStatus(entry.id, { progress: frac });
    onProgress?.(frac);
  });
  active.delete(entry.id);
  if (ok) {
    setStatus(entry.id, null);
    try {
      await idbDelete(STORE, entry.id);
    } catch {}
  } else {
    setStatus(entry.id, { state: "failed" });
  }
  return ok;
}

/**
 * Persist a finished recording to IndexedDB, then upload it. Returns whether
 * the upload succeeded now; if not, the entry stays pending and the background
 * manager retries it later (including after a page reload).
 */
export async function enqueueRecording(
  blob: Blob,
  query: RecordingQuery,
  onProgress?: (frac: number) => void,
  label?: string
): Promise<boolean> {
  const entry: PendingRecording = {
    id: newId(),
    blob,
    query,
    label,
    createdAt: Date.now(),
  };
  try {
    await idbPut(STORE, entry);
  } catch {
    // IndexedDB unavailable — fall back to a plain one-shot upload.
  }
  return uploadEntry(entry, onProgress);
}

/** Retry every persisted recording that isn't already uploading. */
export async function retryPendingRecordings(): Promise<void> {
  try {
    for (const entry of (await idbAll<PendingRecording>(STORE)) ?? []) {
      if (!active.has(entry.id)) void uploadEntry(entry);
    }
    for (const record of (await idbAll<UploadRecord>(UPLOADS)) ?? []) {
      if (liveUploads.has(record.id) || active.has(record.id)) continue;
      void resumeUpload(record);
    }
  } catch {}
}
