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

const inflight = new Map<string, Promise<Compiled>>();

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
        argv: ["/usr/bin/g++", ...CPP_FLAGS[mode], "-o", "prog", "main.cpp"],
        files: { "main.cpp": source },
        timeLimitMs: 20000,
        wallTimeMs: 30000,
        memoryLimitMb: 2048,
        procs: 16,
        fsizeKb: 262144,
        env: { TMPDIR: "/tmp" },
      },
      { collect: ["prog"] }
    );
    await fs.promises.mkdir(dir, { recursive: true });
    const stderr = res.stderr.toString("utf8");
    if (res.status === "OK" && res.exitCode === 0 && res.outFiles?.["prog"]) {
      if (stderr) await fs.promises.writeFile(path.join(dir, "compile.warnings"), stderr);
      await fs.promises.writeFile(binPath, res.outFiles["prog"], { mode: 0o755 });
      return { ok: true, stderr, binPath };
    }
    const msg =
      stderr ||
      (res.status === "TLE" ? "compiler time limit exceeded" : "compilation failed");
    await fs.promises.writeFile(errPath, msg);
    return { ok: false, stderr: msg };
  })().finally(() => inflight.delete(key));
  inflight.set(key, p);
  return p;
}
