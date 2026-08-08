"use client";

import { uploadRecording } from "./webcam-recorder";

/**
 * Resilient webcam-recording uploads. Finished recordings are persisted to
 * IndexedDB before the upload starts, so a closed tab or lost connection
 * doesn't lose the video: the layout-mounted manager retries pending uploads
 * on every page load and periodically after that, deleting each entry only
 * once the /api/recordings confirm step succeeds.
 */

const DB_NAME = "cfr-recordings";
const STORE = "pending";

type PendingRecording = {
  id: string;
  blob: Blob;
  /** Query params for /api/recordings (identifies the solo session or race). */
  query: Record<string, string>;
  createdAt: number;
};

export type UploadStatus = {
  id: string;
  progress: number;
  state: "uploading" | "failed";
};

function openDb(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    if (typeof indexedDB === "undefined") {
      reject(new Error("indexedDB unavailable"));
      return;
    }
    const req = indexedDB.open(DB_NAME, 1);
    req.onupgradeneeded = () => {
      if (!req.result.objectStoreNames.contains(STORE)) {
        req.result.createObjectStore(STORE, { keyPath: "id" });
      }
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function idbPut(entry: PendingRecording): Promise<void> {
  const db = await openDb();
  try {
    await new Promise<void>((resolve, reject) => {
      const tx = db.transaction(STORE, "readwrite");
      tx.objectStore(STORE).put(entry);
      tx.oncomplete = () => resolve();
      tx.onerror = () => reject(tx.error);
    });
  } finally {
    db.close();
  }
}

async function idbDelete(id: string): Promise<void> {
  const db = await openDb();
  try {
    await new Promise<void>((resolve, reject) => {
      const tx = db.transaction(STORE, "readwrite");
      tx.objectStore(STORE).delete(id);
      tx.oncomplete = () => resolve();
      tx.onerror = () => reject(tx.error);
    });
  } finally {
    db.close();
  }
}

async function idbAll(): Promise<PendingRecording[]> {
  const db = await openDb();
  try {
    return await new Promise((resolve, reject) => {
      const req = db.transaction(STORE, "readonly").objectStore(STORE).getAll();
      req.onsuccess = () => resolve(req.result as PendingRecording[]);
      req.onerror = () => reject(req.error);
    });
  } finally {
    db.close();
  }
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

async function uploadEntry(
  entry: PendingRecording,
  onProgress?: (frac: number) => void
): Promise<boolean> {
  if (active.has(entry.id)) return false;
  active.add(entry.id);
  setStatus(entry.id, { state: "uploading", progress: 0 });
  const ok = await uploadRecording(entry.blob, entry.query, (frac) => {
    setStatus(entry.id, { progress: frac });
    onProgress?.(frac);
  });
  active.delete(entry.id);
  if (ok) {
    setStatus(entry.id, null);
    try {
      await idbDelete(entry.id);
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
  query: Record<string, string>,
  onProgress?: (frac: number) => void
): Promise<boolean> {
  const id =
    typeof crypto !== "undefined" && "randomUUID" in crypto
      ? crypto.randomUUID()
      : `${Date.now()}-${Math.random().toString(36).slice(2)}`;
  const entry: PendingRecording = { id, blob, query, createdAt: Date.now() };
  try {
    await idbPut(entry);
  } catch {
    // IndexedDB unavailable — fall back to a plain one-shot upload.
  }
  return uploadEntry(entry, onProgress);
}

/** Retry every persisted recording that isn't already uploading. */
export async function retryPendingRecordings(): Promise<void> {
  let entries: PendingRecording[];
  try {
    entries = await idbAll();
  } catch {
    return;
  }
  for (const entry of entries) {
    if (!active.has(entry.id)) void uploadEntry(entry);
  }
}
