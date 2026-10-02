import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { afterEach, beforeEach, expect, it, vi } from "vitest";
import type { ExecResult } from "../src/sandbox.js";

vi.mock("../src/sandbox.js", () => ({ sandboxRun: vi.fn() }));

let cacheDir: string;

beforeEach(async () => {
  cacheDir = await fs.promises.mkdtemp(path.join(os.tmpdir(), "compile-test-"));
  vi.stubEnv("JUDGE_TOKEN", "test");
  vi.stubEnv("CACHE_DIR", cacheDir);
  vi.stubEnv("CACHE_MAX_BYTES", "100");
  vi.stubEnv("COMPILE_MEMORY_MB", "1536");
});

afterEach(async () => {
  vi.restoreAllMocks();
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

function result(ok = true): ExecResult {
  return {
    status: "OK", exitCode: ok ? 0 : 1, timeMs: 1,
    stdout: Buffer.alloc(0), stderr: Buffer.from(ok ? "" : "e".repeat(60)),
    outFiles: ok ? { prog: Buffer.alloc(60) } : undefined,
  };
}

async function compiler(ok = true) {
  const { sandboxRun } = await import("../src/sandbox.js");
  vi.mocked(sandboxRun).mockResolvedValue(result(ok));
  const module = await import("../src/compile.js");
  return { ...module, sandboxRun };
}

async function cacheSize() {
  let bytes = 0;
  for (const name of await fs.promises.readdir(cacheDir)) {
    const dir = path.join(cacheDir, name);
    try {
      for (const file of await fs.promises.readdir(dir)) {
        bytes += (await fs.promises.stat(path.join(dir, file))).size;
      }
    } catch (e) {
      if ((e as NodeJS.ErrnoException).code !== "ENOENT") throw e;
    }
  }
  return bytes;
}

it("evicts compiler errors even when no compile succeeds", async () => {
  const { compile, sandboxRun } = await compiler(false);
  for (let i = 0; i < 8; i++) {
    expect(await compile("cpp", "submit", `invalid ${i}`)).toEqual({
      ok: false, stderr: "e".repeat(60),
    });
  }
  expect(sandboxRun).toHaveBeenCalledTimes(8);
  await vi.waitFor(async () => expect(await cacheSize()).toBeLessThanOrEqual(80));
});

it("counts compiler diagnostics together with cached binaries", async () => {
  const { compile, sandboxRun, cacheKey } = await compiler();
  const binary = await compile("cpp", "submit", "valid");
  await fs.promises.utimes(binary.binPath!, new Date(0), new Date(0));
  vi.mocked(sandboxRun).mockResolvedValue(result(false));
  await compile("cpp", "submit", "invalid");
  await vi.waitFor(() => expect(fs.existsSync(path.join(cacheDir, cacheKey("cpp", "submit", "valid")))).toBe(false));
  expect(await cacheSize()).toBe(60);
});

it("shares pins across cache hits and evicts only after every user releases", async () => {
  const { compile, withPinnedCompile, cacheKey } = await compiler();
  const started = deferred();
  const firstGate = deferred();
  const secondGate = deferred();
  const dir = path.join(cacheDir, cacheKey("cpp", "submit", "active"));
  const first = withPinnedCompile("cpp", "submit", "active", async () => {
    await compile("cpp", "submit", "active");
    started.resolve();
    await firstGate.promise;
  });
  await started.promise;
  const secondStarted = deferred();
  const second = withPinnedCompile("cpp", "submit", "active", async () => {
    await compile("cpp", "submit", "active");
    secondStarted.resolve();
    await secondGate.promise;
  });
  await secondStarted.promise;
  const churn = async (source: string) => {
    await compile("cpp", "submit", source);
    const otherDir = path.join(cacheDir, cacheKey("cpp", "submit", source));
    await vi.waitFor(() => expect(fs.existsSync(otherDir)).toBe(false));
    expect(fs.existsSync(path.join(dir, "prog"))).toBe(true);
  };
  await churn("churn 1");
  firstGate.resolve();
  await first;
  await churn("churn 2");
  secondGate.resolve();
  await second;
  await fs.promises.utimes(path.join(dir, "prog"), new Date(0), new Date(0));
  await compile("cpp", "submit", "churn 3");
  await vi.waitFor(() => expect(fs.existsSync(dir)).toBe(false));
});

it("releases pinned oversized entries when a request throws", async () => {
  vi.stubEnv("CACHE_MAX_BYTES", "10");
  const { compile, withPinnedCompile, cacheKey } = await compiler();
  const dir = path.join(cacheDir, cacheKey("cpp", "debug", "active"));
  await expect(withPinnedCompile("cpp", "debug", "active", async () => {
    await compile("cpp", "debug", "active");
    expect(fs.existsSync(path.join(dir, "prog"))).toBe(true);
    throw new Error("request failed");
  })).rejects.toThrow("request failed");
  await vi.waitFor(() => expect(fs.existsSync(dir)).toBe(false));
});

it("waits for an eviction already in progress before recompiling a pinned entry", async () => {
  const { compile, withPinnedCompile, cacheKey, sandboxRun } = await compiler();
  const dir = path.join(cacheDir, cacheKey("cpp", "submit", "old"));
  await fs.promises.mkdir(dir);
  await fs.promises.writeFile(path.join(dir, "prog"), Buffer.alloc(60));
  await fs.promises.utimes(path.join(dir, "prog"), new Date(0), new Date(0));
  const deleting = deferred();
  const gate = deferred();
  const rm = fs.promises.rm.bind(fs.promises);
  vi.spyOn(fs.promises, "rm").mockImplementation(async (target, options) => {
    if (target === dir) {
      deleting.resolve();
      await gate.promise;
    }
    return rm(target, options);
  });
  await compile("cpp", "submit", "overflow");
  await deleting.promise;
  let completed = false;
  const job = withPinnedCompile("cpp", "submit", "old", async () => {
    const compiled = await compile("cpp", "submit", "old");
    completed = true;
    expect(fs.existsSync(compiled.binPath!)).toBe(true);
  });
  expect(completed).toBe(false);
  expect(sandboxRun).toHaveBeenCalledOnce();
  gate.resolve();
  await job;
  expect(sandboxRun).toHaveBeenCalledTimes(2);
  await vi.waitFor(async () => expect(await cacheSize()).toBeLessThanOrEqual(80));
});

it("does not reuse a negative cache entry after the compiler memory limit changes", async () => {
  const { compile, sandboxRun } = await compiler(false);
  expect((await compile("cpp", "submit", "memory heavy")).ok).toBe(false);
  expect((await compile("cpp", "submit", "memory heavy")).ok).toBe(false);
  expect(sandboxRun).toHaveBeenCalledOnce();
  const { config } = await import("../src/config.js");
  config.compileMemoryMb = 2048;
  vi.mocked(sandboxRun).mockResolvedValue(result());
  expect((await compile("cpp", "submit", "memory heavy")).ok).toBe(true);
  expect(sandboxRun).toHaveBeenCalledTimes(2);
});

it("does not treat an unfinished binary write as a completed cache hit", async () => {
  const { compile, sandboxRun } = await compiler();
  const written = deferred();
  const gate = deferred();
  const write = fs.promises.writeFile.bind(fs.promises);
  vi.spyOn(fs.promises, "writeFile").mockImplementation(async (...args) => {
    await write(...args);
    if (String(args[0]).endsWith("/prog")) {
      written.resolve();
      await gate.promise;
    }
  });
  const first = compile("cpp", "submit", "same");
  await written.promise;
  let completed = false;
  const second = compile("cpp", "submit", "same").then((compiled) => {
    completed = true;
    return compiled;
  });
  await Promise.resolve();
  expect(completed).toBe(false);
  gate.resolve();
  const results = await Promise.all([first, second]);
  expect(results[0]).toEqual(results[1]);
  expect(sandboxRun).toHaveBeenCalledOnce();
});

it("cleans up failed diagnostic writes instead of persisting a partial CE", async () => {
  const { compile, sandboxRun } = await compiler(false);
  const write = vi.spyOn(fs.promises, "writeFile").mockRejectedValue(new Error("ENOSPC"));
  await expect(compile("cpp", "submit", "invalid")).rejects.toThrow("compile cache write failed");
  expect(await fs.promises.readdir(cacheDir)).toEqual([]);
  write.mockRestore();
  expect((await compile("cpp", "submit", "invalid")).ok).toBe(false);
  expect(sandboxRun).toHaveBeenCalledTimes(2);
});

it.each(["debug", "submit"] as const)(
  "enforces the configured compiler memory limit in %s mode",
  async (mode) => {
    vi.stubEnv("JUDGE_TOKEN", "test");
    vi.stubEnv("COMPILE_MEMORY_MB", "1536");
    const { sandboxRun } = await import("../src/sandbox.js");
    vi.mocked(sandboxRun).mockRejectedValue(new Error("stop before cache writes"));
    const { compile } = await import("../src/compile.js");

    await expect(compile("cpp", mode, "int main(){return 1536;}"))
      .rejects.toThrow("stop before cache writes");
    expect(sandboxRun).toHaveBeenCalledWith(
      expect.objectContaining({
        memoryLimitMb: 1536,
        timeLimitMs: 20000,
        wallTimeMs: 30000,
        procs: 16,
      }),
      { collect: ["prog"] }
    );
  }
);
