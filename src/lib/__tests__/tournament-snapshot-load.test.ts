import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  rpc: vi.fn(),
  maybeSingle: vi.fn(),
  sql: null as null | ((...args: unknown[]) => unknown),
}));

vi.mock("@/lib/db", () => ({
  db: () => ({
    rpc: mocks.rpc,
    from: () => ({ select: () => ({ eq: () => ({ maybeSingle: mocks.maybeSingle }) }) }),
  }),
  logDbError: vi.fn(),
}));
vi.mock("@/lib/pg", () => ({ pg: () => mocks.sql }));

const row = {
  id: "t1",
  code: "ABC234",
  name: "T",
  created_by: null,
  status: "running",
  champion_member_id: null,
  created_at: "2026-10-18T20:00:00+00:00",
  started_at: null,
  finished_at: null,
  members: [
    { id: "m2", joined_at: "2026-10-18T20:00:02+00:00" },
    { id: "m1", joined_at: "2026-10-18T20:00:01+00:00" },
  ],
  matches: [],
  games: [
    {
      id: "g1",
      game_no: 1,
      problem_id: "p1",
      session_a: "s1",
      session_b: null,
      problem: { name: "Problem 1" },
      sa: { outcome: "solved", solve_ms: 1234 },
      sb: null,
    },
  ],
};

const missing = (code: string) => Object.assign(new Error("function missing"), { code });

function fakeSql(result: () => Promise<unknown>) {
  return vi.fn(() => Object.assign(result(), { cancel: vi.fn() }));
}

async function load() {
  return import("../tournament");
}

beforeEach(() => {
  vi.resetModules();
  mocks.rpc.mockReset();
  mocks.maybeSingle.mockReset();
  mocks.sql = null;
  vi.spyOn(console, "warn").mockImplementation(() => {});
});

afterEach(() => {
  vi.useRealTimers();
  vi.restoreAllMocks();
});

describe("loadSnapshotByCode", () => {
  it("uses one GET RPC without DATABASE_URL and splits out the embedded metadata", async () => {
    mocks.rpc.mockResolvedValue({ data: row, error: null });
    const snap = await (await load()).loadSnapshotByCode("ABC234");
    expect(mocks.rpc).toHaveBeenCalledWith("tournament_snapshot", { p_code: "ABC234" }, { get: true });
    expect(mocks.maybeSingle).not.toHaveBeenCalled();
    expect(snap?.tournament).not.toHaveProperty("members");
    expect(snap?.members.map((m) => m.id)).toEqual(["m1", "m2"]);
    expect(snap?.games[0]).not.toHaveProperty("problem");
    expect(snap?.problemNames.get("p1")).toBe("Problem 1");
    expect(snap?.sessions.get("s1")).toEqual({ outcome: "solved", solve_ms: 1234 });
  });

  it("returns null for an unknown code", async () => {
    mocks.rpc.mockResolvedValue({ data: null, error: null });
    expect(await (await load()).loadSnapshotByCode("NOPE22")).toBeNull();
  });

  it("falls back to the embedded select while the function is missing, re-checking after 60s", async () => {
    vi.useFakeTimers();
    mocks.rpc.mockResolvedValue({ data: null, error: missing("PGRST202") });
    mocks.maybeSingle.mockResolvedValue({ data: row, error: null });
    const { loadSnapshotByCode } = await load();

    expect((await loadSnapshotByCode("ABC234"))?.tournament.id).toBe("t1");
    await loadSnapshotByCode("ABC234");
    expect(mocks.rpc).toHaveBeenCalledTimes(1);
    expect(mocks.maybeSingle).toHaveBeenCalledTimes(2);

    vi.advanceTimersByTime(60_000);
    mocks.rpc.mockResolvedValue({ data: row, error: null });
    await loadSnapshotByCode("ABC234");
    await loadSnapshotByCode("ABC234");
    expect(mocks.rpc).toHaveBeenCalledTimes(3);
    expect(mocks.maybeSingle).toHaveBeenCalledTimes(2);
  });

  it("surfaces other RPC errors instead of falling back", async () => {
    mocks.rpc.mockResolvedValue({ data: null, error: { code: "57014", message: "canceling statement" } });
    await expect((await load()).loadSnapshotByCode("ABC234")).rejects.toThrow("canceling statement");
    expect(mocks.maybeSingle).not.toHaveBeenCalled();
  });

  it("reads over the direct connection when DATABASE_URL is set", async () => {
    const sql = fakeSql(() => Promise.resolve([{ snap: row }]));
    mocks.sql = sql;
    const { loadSnapshot } = await load();
    expect((await loadSnapshot("t1"))?.tournament.code).toBe("ABC234");
    expect(sql).toHaveBeenCalledTimes(1);
    expect(sql.mock.calls[0]).toContain("t1");
    expect(mocks.rpc).not.toHaveBeenCalled();
  });

  it("falls back from the direct connection to the embedded select when the function is missing", async () => {
    mocks.sql = fakeSql(() => Promise.reject(missing("42883")));
    mocks.maybeSingle.mockResolvedValue({ data: row, error: null });
    expect((await (await load()).loadSnapshotByCode("ABC234"))?.tournament.id).toBe("t1");
    expect(mocks.rpc).not.toHaveBeenCalled();
  });

  it("fails a hung direct read after 10s and cancels it", async () => {
    vi.useFakeTimers();
    const pending = Object.assign(new Promise(() => {}), { cancel: vi.fn() });
    mocks.sql = vi.fn(() => pending);
    const result = (await load()).loadSnapshotByCode("ABC234");
    const assertion = expect(result).rejects.toThrow(/^loadSnapshot: tournament_snapshot timed out$/);
    await vi.advanceTimersByTimeAsync(10_000);
    await assertion;
    expect(pending.cancel).toHaveBeenCalled();
  });
});
