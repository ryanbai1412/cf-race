import fs from "node:fs";
import path from "node:path";
import { config } from "./config.js";
import { clearProblemCache } from "./problems.js";

/**
 * Incremental problem-package sync from Supabase Storage. A state file next
 * to the packages records each object's version (etag/updated_at); only
 * new or changed objects are downloaded, so this is cheap enough to run on
 * a timer — new problems become gradable without a judge restart.
 */

const BUCKET = process.env.PROBLEMS_BUCKET ?? "problems";
const STATE_FILE = ".sync-state.json";
const LIST_TIMEOUT_MS = 30_000;
const DOWNLOAD_TIMEOUT_MS = 180_000;

type RemoteObject = { path: string; version: string; size: number | null };
type SyncState = Record<string, string>;

function creds(): { url: string; key: string } | null {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  return url && key ? { url, key } : null;
}

async function list(
  url: string,
  key: string,
  prefix: string
): Promise<
  {
    name: string;
    id: string | null;
    updated_at?: string;
    metadata?: { eTag?: string; size?: number };
  }[]
> {
  type Entry = {
    name: string;
    id: string | null;
    updated_at?: string;
    metadata?: { eTag?: string; size?: number };
  };
  // Paged: a silently truncated listing would leave test files undownloaded,
  // and a submission judged against a partial test set can pass wrongly.
  const all: Entry[] = [];
  const pageSize = 1000;
  for (let offset = 0; ; offset += pageSize) {
    const res = await fetch(`${url}/storage/v1/object/list/${BUCKET}`, {
      method: "POST",
      headers: {
        apikey: key,
        authorization: `Bearer ${key}`,
        "content-type": "application/json",
      },
      body: JSON.stringify({ prefix, limit: pageSize, offset }),
      signal: AbortSignal.timeout(LIST_TIMEOUT_MS),
    });
    if (!res.ok) {
      throw new Error(`list ${prefix} failed: ${res.status} ${await res.text()}`);
    }
    const page = (await res.json()) as Entry[];
    all.push(...page);
    if (page.length < pageSize) return all;
  }
}

async function walk(
  url: string,
  key: string,
  prefix: string,
  out: RemoteObject[]
): Promise<void> {
  const entries = await list(url, key, prefix);
  for (const e of entries) {
    const full = prefix ? `${prefix}/${e.name}` : e.name;
    // Folders come back with id === null in Supabase Storage listings.
    if (e.id === null) await walk(url, key, full, out);
    else
      out.push({
        path: full,
        version: e.metadata?.eTag ?? e.updated_at ?? "",
        size: e.metadata?.size ?? null,
      });
  }
}

/** Object names come from the bucket; never let them escape problemsDir. */
function safeObjectPath(p: string): boolean {
  return (
    !path.isAbsolute(p) &&
    p.split("/").every((seg) => seg.length > 0 && seg !== "." && seg !== "..")
  );
}

async function download(url: string, key: string, objectPath: string): Promise<void> {
  const dest = path.join(config.problemsDir, objectPath);
  await fs.promises.mkdir(path.dirname(dest), { recursive: true });
  const res = await fetch(`${url}/storage/v1/object/${BUCKET}/${objectPath}`, {
    headers: { apikey: key, authorization: `Bearer ${key}` },
    signal: AbortSignal.timeout(DOWNLOAD_TIMEOUT_MS),
  });
  if (!res.ok) throw new Error(`download ${objectPath} failed: ${res.status}`);
  // Write to a temp file and rename so a concurrent judge run never sees a
  // partially written test file.
  const tmp = `${dest}.partial-${process.pid}`;
  await fs.promises.writeFile(tmp, Buffer.from(await res.arrayBuffer()));
  await fs.promises.rename(tmp, dest);
}

function statePath(): string {
  return path.join(config.problemsDir, STATE_FILE);
}

function loadState(): SyncState {
  try {
    return JSON.parse(fs.readFileSync(statePath(), "utf8")) as SyncState;
  } catch {
    return {};
  }
}

/** Sync changed/new packages; returns the number of files downloaded. */
export async function syncProblems(): Promise<number> {
  const c = creds();
  if (!c) return 0;

  const remote: RemoteObject[] = [];
  await walk(c.url, c.key, "", remote);
  for (const o of remote) {
    if (!safeObjectPath(o.path)) throw new Error(`unsafe object path: ${o.path}`);
  }
  const state = loadState();
  let seeded = false;
  const changed = remote.filter((o) => {
    const dest = path.join(config.problemsDir, o.path);
    if (state[o.path] === o.version && fs.existsSync(dest)) return false;
    if (state[o.path] === undefined) {
      // No state yet (first run on a pre-populated volume): trust files whose
      // size matches the bucket instead of re-downloading everything.
      const stat = fs.statSync(dest, { throwIfNoEntry: false });
      if (stat && o.size !== null && stat.size === o.size) {
        state[o.path] = o.version;
        seeded = true;
        return false;
      }
    }
    return true;
  });
  if (changed.length === 0) {
    if (seeded) await saveState(state);
    return 0;
  }

  console.log(`sync: downloading ${changed.length}/${remote.length} objects`);
  const CONC = 16;
  let i = 0;
  let downloaded = 0;
  try {
    await Promise.all(
      Array.from({ length: CONC }, async () => {
        while (i < changed.length) {
          const o = changed[i++];
          await download(c.url, c.key, o.path);
          state[o.path] = o.version;
          downloaded++;
        }
      })
    );
  } finally {
    // A failed tick still recorded whatever landed, so the next one resumes
    // instead of starting over; the cache must forget lists read before them.
    await saveState(state);
    if (downloaded > 0) clearProblemCache();
  }
  return changed.length;
}

/** Persist the sync state atomically: a torn state file resets the sync. */
async function saveState(state: SyncState): Promise<void> {
  await fs.promises.mkdir(config.problemsDir, { recursive: true });
  const tmp = `${statePath()}.tmp-${process.pid}`;
  await fs.promises.writeFile(tmp, JSON.stringify(state));
  await fs.promises.rename(tmp, statePath());
}

/**
 * Run syncProblems immediately (in the background) and then on an interval,
 * logging failures without crashing.
 */
export function scheduleProblemSync(intervalSec: number): void {
  if (!creds() || intervalSec <= 0) return;
  let running = false;
  const tick = async () => {
    if (running) return;
    running = true;
    try {
      const n = await syncProblems();
      if (n > 0) console.log(`sync: ${n} objects updated`);
    } catch (e) {
      console.error("sync: failed", e);
    } finally {
      running = false;
    }
  };
  void tick();
  setInterval(tick, intervalSec * 1000).unref();
}
