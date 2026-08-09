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

type RemoteObject = { path: string; version: string };
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
    metadata?: { eTag?: string };
  }[]
> {
  const res = await fetch(`${url}/storage/v1/object/list/${BUCKET}`, {
    method: "POST",
    headers: {
      apikey: key,
      authorization: `Bearer ${key}`,
      "content-type": "application/json",
    },
    body: JSON.stringify({ prefix, limit: 10000, offset: 0 }),
  });
  if (!res.ok) {
    throw new Error(`list ${prefix} failed: ${res.status} ${await res.text()}`);
  }
  return (await res.json()) as {
    name: string;
    id: string | null;
    updated_at?: string;
    metadata?: { eTag?: string };
  }[];
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
    else out.push({ path: full, version: e.metadata?.eTag ?? e.updated_at ?? "" });
  }
}

async function download(url: string, key: string, objectPath: string): Promise<void> {
  const dest = path.join(config.problemsDir, objectPath);
  await fs.promises.mkdir(path.dirname(dest), { recursive: true });
  const res = await fetch(`${url}/storage/v1/object/${BUCKET}/${objectPath}`, {
    headers: { apikey: key, authorization: `Bearer ${key}` },
  });
  if (!res.ok) throw new Error(`download ${objectPath} failed: ${res.status}`);
  await fs.promises.writeFile(dest, Buffer.from(await res.arrayBuffer()));
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
  const state = loadState();
  const changed = remote.filter(
    (o) =>
      state[o.path] !== o.version ||
      !fs.existsSync(path.join(config.problemsDir, o.path))
  );
  if (changed.length === 0) return 0;

  console.log(`sync: downloading ${changed.length}/${remote.length} objects`);
  const CONC = 16;
  let i = 0;
  await Promise.all(
    Array.from({ length: CONC }, async () => {
      while (i < changed.length) {
        const o = changed[i++];
        await download(c.url, c.key, o.path);
        state[o.path] = o.version;
      }
    })
  );

  await fs.promises.mkdir(config.problemsDir, { recursive: true });
  await fs.promises.writeFile(statePath(), JSON.stringify(state));
  clearProblemCache();
  return changed.length;
}

/** Run syncProblems on an interval, logging failures without crashing. */
export function scheduleProblemSync(intervalSec: number): void {
  if (!creds() || intervalSec <= 0) return;
  const tick = async () => {
    try {
      const n = await syncProblems();
      if (n > 0) console.log(`sync: ${n} objects updated`);
    } catch (e) {
      console.error("sync: failed", e);
    }
  };
  setInterval(tick, intervalSec * 1000).unref();
}
