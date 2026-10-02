import { afterEach, describe, expect, it, vi } from "vitest";

vi.mock("../src/compile.js", () => ({
  compile: vi.fn(),
  withPinnedCompile: (_lang: unknown, _mode: unknown, _source: unknown, fn: () => Promise<unknown>) => fn(),
}));

function deferred() {
  let resolve!: () => void;
  let reject!: (error: Error) => void;
  const promise = new Promise<void>((res, rej) => {
    resolve = res;
    reject = rej;
  });
  return { promise, resolve, reject };
}

afterEach(() => {
  vi.unstubAllEnvs();
  vi.clearAllMocks();
  vi.resetModules();
});

async function capacity() {
  vi.stubEnv("JUDGE_TOKEN", "test");
  vi.stubEnv("JUDGE_WORKERS", "4");
  vi.stubEnv("COMPILE_MEMORY_MB", "1536");
  vi.stubEnv("CACHE_MAX_BYTES", "536870912");
  const { config } = await import("../src/config.js");
  const { pool, handleRun } = await import("../src/judge.js");
  return { config, pool, handleRun };
}

describe("8 GB capacity settings", () => {
  it("applies the worker and compile-cache overrides", async () => {
    const { config } = await capacity();
    expect(config.workers).toBe(4);
    expect(config.compileMemoryMb).toBe(1536);
    expect(config.cacheMaxBytes).toBe(512 * 1024 * 1024);
  });

  it("queues sandbox work above four workers and drains in order", async () => {
    const { pool } = await capacity();
    const gates = Array.from({ length: 6 }, deferred);
    const started: number[] = [];
    const jobs = gates.map((gate, i) =>
      pool.run(async () => {
        started.push(i);
        await gate.promise;
      })
    );

    expect(started).toEqual([0, 1, 2, 3]);
    expect(pool.pending).toBe(2);
    gates[0].resolve();
    await jobs[0];
    expect(started).toEqual([0, 1, 2, 3, 4]);
    expect(pool.pending).toBe(1);
    gates[1].resolve();
    await jobs[1];
    expect(started).toEqual([0, 1, 2, 3, 4, 5]);
    gates.slice(2).forEach((gate) => gate.resolve());
    await Promise.all(jobs);
    expect(pool.pending).toBe(0);
  });

  it("releases a worker after a sandbox failure", async () => {
    const { pool } = await capacity();
    const gate = deferred();
    const first = pool.run(() => gate.promise).catch((error) => error);
    const otherGates = Array.from({ length: 3 }, deferred);
    const others = otherGates.map((other) => pool.run(() => other.promise));
    const next = vi.fn(async () => {});
    const queued = pool.run(next);
    expect(next).not.toHaveBeenCalled();

    gate.reject(new Error("sandbox failed"));
    expect(await first).toEqual(new Error("sandbox failed"));
    await queued;
    expect(next).toHaveBeenCalledOnce();
    otherGates.forEach((other) => other.resolve());
    await Promise.all(others);
    expect(pool.pending).toBe(0);
  });

  it("allows four compiles and queues further requests", async () => {
    const { pool, handleRun } = await capacity();
    const { compile } = await import("../src/compile.js");
    const gates = Array.from({ length: 6 }, deferred);
    vi.mocked(compile).mockImplementation(async (_lang, _mode, source) => {
      await gates[Number(source)].promise;
      return { ok: false, stderr: "compile error" };
    });
    const jobs = gates.map((_, i) =>
      handleRun({ runId: `r${i}`, lang: "cpp", source: String(i), tests: [] })
    );
    await vi.waitFor(() => expect(compile).toHaveBeenCalledTimes(4));
    expect(pool.pending).toBe(2);
    gates[0].resolve();
    await jobs[0];
    await vi.waitFor(() => expect(compile).toHaveBeenCalledTimes(5));
    gates[1].resolve();
    await jobs[1];
    await vi.waitFor(() => expect(compile).toHaveBeenCalledTimes(6));
    gates.slice(2).forEach((gate) => gate.resolve());
    await Promise.all(jobs);
    expect(pool.pending).toBe(0);
  });
});
