import fs from "node:fs";
import path from "node:path";
import { ProblemMeta, TestCase } from "./types.js";

const metaCache = new Map<string, ProblemMeta>();

/** Drop cached metadata after a problem sync so updates are picked up. */
export function clearProblemCache(): void {
  metaCache.clear();
}

function problemDir(id: string): string {
  if (!/^[A-Za-z0-9_.-]+(\/[A-Za-z0-9_.-]+)?$/.test(id))
    throw new Error(`invalid problem id: ${id}`);
  return path.join(process.env.PROBLEMS_DIR ?? "/data/problems", id);
}

export function loadMeta(id: string): ProblemMeta {
  const cached = metaCache.get(id);
  if (cached) return cached;
  const p = path.join(problemDir(id), "meta.json");
  const meta = JSON.parse(fs.readFileSync(p, "utf8")) as ProblemMeta;
  metaCache.set(id, meta);
  return meta;
}

function loadPairs(dir: string, inExt: string, outExt: string): TestCase[] {
  if (!fs.existsSync(dir)) return [];
  const ins = fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(inExt))
    .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
  const tests: TestCase[] = [];
  for (const f of ins) {
    const base = f.slice(0, -inExt.length);
    const outPath = path.join(dir, base + outExt);
    tests.push({
      name: base,
      input: fs.readFileSync(path.join(dir, f), "utf8"),
      expected: fs.existsSync(outPath) ? fs.readFileSync(outPath, "utf8") : null,
    });
  }
  return tests;
}

export function loadSamples(id: string): TestCase[] {
  return loadPairs(path.join(problemDir(id), "samples"), ".in", ".out").map(
    (t) => ({ ...t, name: `sample${t.name}` })
  );
}

export function loadFullTests(id: string): TestCase[] {
  return loadPairs(path.join(problemDir(id), "tests"), ".in", ".out");
}
