import { afterEach, describe, expect, it, vi } from "vitest";

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
  vi.resetModules();
});

async function capacity() {
  vi.stubEnv("JUDGE_TOKEN", "test");
  vi.stubEnv("JUDGE_WORKERS", "2");
  vi.stubEnv("CACHE_MAX_BYTES", "536870912");
  const { config } = await import("../src/config.js");
  const { pool } = await import("../src/judge.js");
  return { config, pool };
}

describe("8 GB capacity settings", () => {
  it("applies the worker and compile-cache overrides", async () => {
    const { config } = await capacity();
    expect(config.workers).toBe(2);
    expect(config.cacheMaxBytes).toBe(512 * 1024 * 1024);
  });

  it("queues sandbox work above two workers and drains in order", async () => {
    const { pool } = await capacity();
    const gates = Array.from({ length: 4 }, deferred);
    const started: number[] = [];
    const jobs = gates.map((gate, i) =>
      pool.run(async () => {
        started.push(i);
        await gate.promise;
      })
    );

    expect(started).toEqual([0, 1]);
    expect(pool.pending).toBe(2);
    gates[0].resolve();
    await jobs[0];
    expect(started).toEqual([0, 1, 2]);
    expect(pool.pending).toBe(1);
    gates[1].resolve();
    await jobs[1];
    expect(started).toEqual([0, 1, 2, 3]);
    gates[2].resolve();
    gates[3].resolve();
    await Promise.all(jobs);
    expect(pool.pending).toBe(0);
  });

  it("releases a worker after a sandbox failure", async () => {
    const { pool } = await capacity();
    const gate = deferred();
    const first = pool.run(() => gate.promise).catch((error) => error);
    const secondGate = deferred();
    const second = pool.run(() => secondGate.promise);
    const next = vi.fn(async () => {});
    const third = pool.run(next);
    expect(next).not.toHaveBeenCalled();

    gate.reject(new Error("sandbox failed"));
    expect(await first).toEqual(new Error("sandbox failed"));
    await third;
    expect(next).toHaveBeenCalledOnce();
    secondGate.resolve();
    await second;
    expect(pool.pending).toBe(0);
  });
});
