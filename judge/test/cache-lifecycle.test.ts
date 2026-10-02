import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { afterEach, beforeEach, expect, it, vi } from "vitest";
import type { ExecResult } from "../src/sandbox.js";

vi.mock("../src/sandbox.js", () => ({ sandboxRun: vi.fn() }));
vi.mock("../src/problems.js", () => ({
  loadMeta: async () => ({ timeLimitMs: 1000, memoryLimitMb: 256 }),
  loadFullTests: async () => [0, 1, 2].map((i) => ({
    name: String(i), input: String(i), expected: "ok",
  })),
}));

let cacheDir: string;

beforeEach(async () => {
  cacheDir = await fs.promises.mkdtemp(path.join(os.tmpdir(), "cache-lifecycle-"));
  vi.stubEnv("JUDGE_TOKEN", "test");
  vi.stubEnv("CACHE_DIR", cacheDir);
  vi.stubEnv("CACHE_MAX_BYTES", "10");
  vi.stubEnv("JUDGE_WORKERS", "1");
});

afterEach(async () => {
  await fs.promises.rm(cacheDir, { recursive: true, force: true });
  vi.unstubAllEnvs();
  vi.resetAllMocks();
  vi.resetModules();
});

function deferred() {
  let resolve!: () => void;
  const promise = new Promise<void>((res) => { resolve = res; });
  return { promise, resolve };
}

function result(): ExecResult {
  return {
    status: "OK", exitCode: 0, timeMs: 1,
    stdout: Buffer.from("ok"), stderr: Buffer.alloc(0),
  };
}

it.each(["run", "submit"] as const)(
  "%s keeps its binary pinned until all queued tests finish after a sandbox error",
  async (kind) => {
    const { sandboxRun } = await import("../src/sandbox.js");
    const started = deferred();
    const gate = deferred();
    const seen: string[] = [];
    let binPath: string | undefined;
    vi.mocked(sandboxRun).mockImplementation(async (spec) => {
      if (spec.argv[0] === "/usr/bin/g++") {
        return { ...result(), outFiles: { prog: Buffer.alloc(60) } };
      }
      seen.push(spec.stdin!);
      const file = spec.files?.prog as { fromPath: string };
      binPath = file.fromPath;
      expect(fs.existsSync(binPath)).toBe(true);
      if (spec.stdin === "0") return { ...result(), internalError: "sandbox failed" };
      if (spec.stdin === "1") {
        started.resolve();
        await gate.promise;
      }
      expect(fs.existsSync(binPath)).toBe(true);
      return result();
    });
    const { handleRun, handleSubmit, pool } = await import("../src/judge.js");
    let settled = false;
    const request = kind === "run"
      ? handleRun({
          runId: "r", lang: "cpp", source: "active",
          tests: [0, 1, 2].map((i) => ({ name: String(i), input: String(i), expected: "ok" })),
        })
      : handleSubmit({ submissionId: "s", lang: "cpp", source: "active", problemId: "test" });
    const job = request.catch((error) => error).finally(() => { settled = true; });
    await started.promise;
    expect(pool.pending).toBe(1);
    expect(settled).toBe(false);
    expect(fs.existsSync(binPath!)).toBe(true);
    gate.resolve();
    expect(await job).toEqual(new Error("sandbox failed on 0: sandbox failed"));
    expect(seen).toEqual(["0", "1", "2"]);
    expect(pool.pending).toBe(0);
    await vi.waitFor(() => expect(fs.existsSync(binPath!)).toBe(false));
  }
);

it.each(["run", "submit"] as const)(
  "%s releases its binary if a progress callback throws",
  async (kind) => {
    const { sandboxRun } = await import("../src/sandbox.js");
    vi.mocked(sandboxRun).mockImplementation(async (spec) => spec.argv[0] === "/usr/bin/g++"
      ? { ...result(), outFiles: { prog: Buffer.alloc(60) } }
      : result());
    const { cacheKey } = await import("../src/compile.js");
    const { handleRun, handleSubmit } = await import("../src/judge.js");
    const update = () => { throw new Error("callback failed"); };
    const request = kind === "run"
      ? handleRun({ runId: "r", lang: "cpp", source: "active", tests: [] }, update)
      : handleSubmit({ submissionId: "s", lang: "cpp", source: "active", problemId: "test" }, update);
    await expect(request).rejects.toThrow("callback failed");
    const dir = path.join(cacheDir, cacheKey("cpp", kind === "run" ? "debug" : "submit", "active"));
    await vi.waitFor(() => expect(fs.existsSync(dir)).toBe(false));
  }
);
