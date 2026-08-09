import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { config } from "./config.js";
import { sandboxRun } from "./sandbox.js";
import { Lang } from "./types.js";

export type CompileMode = "debug" | "submit";

export const CPP_FLAGS: Record<CompileMode, string[]> = {
  debug: ["-O1", "-g", "-fsanitize=address,undefined", "-std=c++20"],
  submit: ["-O2", "-std=c++20"],
};

export interface Compiled {
  ok: boolean;
  stderr: string;
  /** For cpp: absolute path to the cached binary. For py: undefined. */
  binPath?: string;
}

export function cacheKey(lang: Lang, mode: CompileMode, source: string): string {
  const flags = lang === "cpp" ? CPP_FLAGS[mode].join(" ") : "";
  return crypto
    .createHash("sha256")
    .update(`${lang}\0${flags}\0`)
    .update(source)
    .digest("hex");
}

// Precompiled bits/stdc++.h per flag set (built in the Docker image); cuts
// cold compiles from seconds to a few hundred ms.
const PCH_ROOT = process.env.PCH_ROOT ?? "/opt/pch";
function pchArgs(mode: CompileMode): string[] {
  const dir = path.join(PCH_ROOT, mode);
  return fs.existsSync(path.join(dir, "bits", "stdc++.h.gch"))
    ? ["-I", dir, "-Winvalid-pch"]
    : [];
}

const inflight = new Map<string, Promise<Compiled>>();

// LRU eviction for the compile cache, keyed on binary mtime (touched on every
// cache hit). Serialized so concurrent compiles trigger at most one pass.
let evictChain: Promise<void> = Promise.resolve();
function scheduleEviction(): void {
  evictChain = evictChain
    .then(evictOnce)
    .catch((e) => console.error("cache eviction failed:", e));
}

async function evictOnce(): Promise<void> {
  let names: string[];
  try {
    names = await fs.promises.readdir(config.cacheDir);
  } catch {
    return;
  }
  const entries: { name: string; dir: string; size: number; mtimeMs: number }[] = [];
  let total = 0;
  for (const name of names) {
    const dir = path.join(config.cacheDir, name);
    let size = 0;
    let mtimeMs = 0;
    let files: string[];
    try {
      files = await fs.promises.readdir(dir);
    } catch {
      continue;
    }
    for (const f of files) {
      try {
        const st = await fs.promises.stat(path.join(dir, f));
        size += st.size;
        mtimeMs = Math.max(mtimeMs, st.mtimeMs);
      } catch {
        /* entry may be evicted/written concurrently */
      }
    }
    entries.push({ name, dir, size, mtimeMs });
    total += size;
  }
  if (total <= config.cacheMaxBytes) return;
  entries.sort((a, b) => a.mtimeMs - b.mtimeMs);
  // Evict below the cap with headroom so each overflow doesn't re-trigger.
  const target = config.cacheMaxBytes * 0.8;
  for (const e of entries) {
    if (total <= target) break;
    if (inflight.has(e.name)) continue;
    await fs.promises.rm(e.dir, { recursive: true, force: true });
    total -= e.size;
  }
}

export async function compile(
  lang: Lang,
  mode: CompileMode,
  source: string
): Promise<Compiled> {
  if (lang === "py") return { ok: true, stderr: "" };

  const key = cacheKey(lang, mode, source);
  const dir = path.join(config.cacheDir, key);
  const binPath = path.join(dir, "prog");
  const errPath = path.join(dir, "compile.stderr");
  if (fs.existsSync(binPath)) {
    const now = new Date();
    fs.promises.utimes(binPath, now, now).catch(() => {});
    const warnPath = path.join(dir, "compile.warnings");
    const stderr = fs.existsSync(warnPath) ? fs.readFileSync(warnPath, "utf8") : "";
    return { ok: true, stderr, binPath };
  }
  if (fs.existsSync(errPath)) {
    return { ok: false, stderr: fs.readFileSync(errPath, "utf8") };
  }

  const existing = inflight.get(key);
  if (existing) return existing;

  const p = (async (): Promise<Compiled> => {
    const res = await sandboxRun(
      {
        argv: ["/usr/bin/g++", ...CPP_FLAGS[mode], ...pchArgs(mode), "-o", "prog", "main.cpp"],
        files: { "main.cpp": source },
        dirs: fs.existsSync(PCH_ROOT) ? [PCH_ROOT] : undefined,
        timeLimitMs: 20000,
        wallTimeMs: 30000,
        memoryLimitMb: 2048,
        procs: 16,
        fsizeKb: 262144,
        env: { TMPDIR: "/tmp" },
      },
      { collect: ["prog"] }
    );
    const stderr = res.stderr.toString("utf8");
    if (res.status === "OK" && res.exitCode === 0 && res.outFiles?.["prog"]) {
      try {
        await fs.promises.mkdir(dir, { recursive: true });
        if (stderr)
          await fs.promises.writeFile(path.join(dir, "compile.warnings"), stderr);
        await fs.promises.writeFile(binPath, res.outFiles["prog"], { mode: 0o755 });
      } catch (e) {
        // Cache write failure (e.g. ENOSPC) is a judge problem, not a CE;
        // surface it as a transient error and never persist it.
        await fs.promises.rm(dir, { recursive: true, force: true }).catch(() => {});
        scheduleEviction();
        throw new Error(`compile cache write failed: ${String(e)}`);
      }
      scheduleEviction();
      return { ok: true, stderr, binPath };
    }
    if (res.exitCode === 0 && res.status === "OK") {
      // Compiler claims success but produced no binary: infrastructure
      // failure (sandbox/collect), so don't cache it as a CE.
      throw new Error("compile produced no binary");
    }
    const msg =
      stderr ||
      (res.status === "TLE" ? "compiler time limit exceeded" : "compilation failed");
    await fs.promises.mkdir(dir, { recursive: true });
    await fs.promises.writeFile(errPath, msg);
    return { ok: false, stderr: msg };
  })().finally(() => inflight.delete(key));
  inflight.set(key, p);
  return p;
}
