import fs from "node:fs";
import path from "node:path";
import { ProblemMeta } from "./types.js";

/** The requested problem package does not exist on disk. */
export class ProblemNotFoundError extends Error {}

/**
 * A test stored on disk. Only paths are held in memory; inputs are streamed
 * into the sandbox and expected outputs are read per-test at check time.
 */
export interface DiskTest {
  name: string;
  inputPath: string;
  expectedPath: string | null;
}

const metaCache = new Map<string, ProblemMeta>();
const testListCache = new Map<string, DiskTest[]>();

/** Drop cached metadata after a problem sync so updates are picked up. */
export function clearProblemCache(): void {
  metaCache.clear();
  testListCache.clear();
}

function problemDir(id: string): string {
  if (!/^[A-Za-z0-9_.-]+(\/[A-Za-z0-9_.-]+)?$/.test(id))
    throw new Error(`invalid problem id: ${id}`);
  return path.join(process.env.PROBLEMS_DIR ?? "/data/problems", id);
}

export async function loadMeta(id: string): Promise<ProblemMeta> {
  const cached = metaCache.get(id);
  if (cached) return cached;
  const p = path.join(problemDir(id), "meta.json");
  let raw: string;
  try {
    raw = await fs.promises.readFile(p, "utf8");
  } catch (e) {
    if ((e as NodeJS.ErrnoException).code === "ENOENT")
      throw new ProblemNotFoundError(`unknown problem: ${id}`);
    throw e;
  }
  let meta: ProblemMeta;
  try {
    meta = JSON.parse(raw) as ProblemMeta;
  } catch {
    throw new Error(`corrupt meta.json for problem ${id}`);
  }
  metaCache.set(id, meta);
  return meta;
}

async function listPairs(
  dir: string,
  inExt: string,
  outExt: string
): Promise<DiskTest[]> {
  let names: string[];
  try {
    names = await fs.promises.readdir(dir);
  } catch (e) {
    if ((e as NodeJS.ErrnoException).code === "ENOENT") return [];
    throw e;
  }
  const outs = new Set(names.filter((f) => f.endsWith(outExt)));
  return names
    .filter((f) => f.endsWith(inExt))
    .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }))
    .map((f) => {
      const base = f.slice(0, -inExt.length);
      return {
        name: base,
        inputPath: path.join(dir, f),
        expectedPath: outs.has(base + outExt) ? path.join(dir, base + outExt) : null,
      };
    });
}

async function cachedPairs(cacheKey: string, dir: string): Promise<DiskTest[]> {
  const cached = testListCache.get(cacheKey);
  if (cached) return cached;
  const tests = await listPairs(dir, ".in", ".out");
  testListCache.set(cacheKey, tests);
  return tests;
}

export async function loadSamples(id: string): Promise<DiskTest[]> {
  const tests = await cachedPairs(`samples:${id}`, path.join(problemDir(id), "samples"));
  return tests.map((t) => ({ ...t, name: `sample${t.name}` }));
}

export async function loadFullTests(id: string): Promise<DiskTest[]> {
  return cachedPairs(`tests:${id}`, path.join(problemDir(id), "tests"));
}
