import { beforeEach, describe, expect, it, vi } from "vitest";
import { DEFAULT_PROBLEM_RATING, DEFAULT_SOLO_TIMER, isProblemRating, isSoloTimer, PROBLEM_RATINGS, ratingCounts } from "../problem-rating";

const store = vi.hoisted(() => ({
  rows: {} as Record<string, Record<string, unknown>[]>,
  errors: new Set<string>(),
  rpc: vi.fn(),
}));
vi.mock("next/cache", () => ({ unstable_cache: (fn: unknown) => fn }));
vi.mock("../db", () => ({
  db: () => ({
    rpc: store.rpc,
    from: (table: string) => {
      let rows = [...(store.rows[table] ?? [])];
      const builder = {
        select: () => builder,
        order: () => builder,
        eq: (key: string, value: unknown) => { rows = rows.filter((r) => r[key] === value); return builder; },
        neq: (key: string, value: unknown) => { rows = rows.filter((r) => r[key] !== value); return builder; },
        in: (key: string, values: unknown[]) => { rows = rows.filter((r) => values.includes(r[key])); return builder; },
        is: (key: string, value: unknown) => { rows = rows.filter((r) => r[key] === value); return builder; },
        then: (resolve: (r: unknown) => unknown) => resolve({ data: rows, error: store.errors.has(table) ? new Error("offline") : null }),
      };
      return builder;
    },
  }),
  logDbError: vi.fn(),
}));
import { pickPracticeProblem } from "../problem-bank";
import { pickDuelProblem, startDuelMatch, type DuelRoomRow } from "../duel";

beforeEach(() => {
  store.rows = {
    problems: [
      { id: "easy", name: "Easy", rating: 800, tags: [] },
      { id: "hard", name: "Hard", rating: 1600, tags: [] },
      { id: "hidden", name: "Hidden", rating: 1600, tags: ["hidden"] },
      { id: "warmup-sum", rating: 800, tags: [] },
    ],
    sessions: [], problem_invalidations: [],
  };
  store.errors.clear();
  store.rpc.mockReset();
});

const claimedRoom: DuelRoomRow = {
  id: "room", created_by: "a", created_at: "2026-01-01T00:00:00Z",
  status: "racing", total_time_sec: 180, grace_after_ac_sec: null,
  problem_rating: 800, settings_version: 0,
  start_claimed_at: "2026-01-01T00:00:00.123456Z",
};

describe("lost duel start responses", () => {
  it("binds an empty-pool reset to the original claim", async () => {
    store.rows.problems = [];
    store.rpc.mockResolvedValueOnce({ data: { ok: true }, error: null });
    expect(await startDuelMatch(claimedRoom, ["a", "b"])).toMatchObject({ ok: false, status: 409 });
    expect(store.rpc.mock.calls[0][0]).toBe("duel_lobby_action");
    expect(store.rpc.mock.calls[0][1].p_patch.startClaimedAt).toBe(claimedRoom.start_claimed_at);
  });

  it("does not reset a newer claim after the database rejects a stale start", async () => {
    store.rpc.mockResolvedValueOnce({ data: { ok: false, error: "Race attempt changed", status: 409 }, error: null });
    expect(await startDuelMatch(claimedRoom, ["a", "b"])).toMatchObject({ ok: false, status: 409 });
    expect(store.rpc).toHaveBeenCalledTimes(1);
    expect(store.rpc.mock.calls[0][1].p_claim_time).toBe(claimedRoom.start_claimed_at);
  });

  it("preserves a committed match when its RPC response is lost", async () => {
    store.rpc.mockRejectedValueOnce(new Error("lost response"));
    store.rpc.mockResolvedValueOnce({ data: { ok: true, activeMatch: true }, error: null });
    expect(await startDuelMatch(claimedRoom, ["a", "b"])).toEqual({ ok: true });
    expect(store.rpc.mock.calls.map((call) => call[0])).toEqual(["duel_start_match", "duel_lobby_action"]);
    expect(store.rpc.mock.calls[1][1].p_action).toBe("reset");
    expect(store.rpc.mock.calls[0][1].p_claim_time).toBe(claimedRoom.start_claimed_at);
    expect(store.rpc.mock.calls[1][1].p_patch.startClaimedAt).toBe(claimedRoom.start_claimed_at);
  });

  it("resets an uncommitted claim after a failed RPC", async () => {
    store.rpc.mockResolvedValueOnce({ data: null, error: new Error("timeout") });
    store.rpc.mockResolvedValueOnce({ data: { ok: true, activeMatch: false }, error: null });
    expect(await startDuelMatch(claimedRoom, ["a", "b"])).toMatchObject({ ok: false, status: 503 });
    expect(store.rpc.mock.calls.map((call) => call[0])).toEqual(["duel_start_match", "duel_lobby_action"]);
  });

  it("returns a retry error when recovery is also unavailable", async () => {
    store.rpc.mockRejectedValueOnce(new Error("network unavailable"));
    store.rpc.mockRejectedValueOnce(new Error("network unavailable"));
    expect(await startDuelMatch(claimedRoom, ["a", "b"])).toMatchObject({ ok: false, status: 503 });
  });
});

describe("rating and timer choices", () => {
  it("defaults to800 and three minutes", () => {
    expect(DEFAULT_PROBLEM_RATING).toBe(800);
    expect(DEFAULT_SOLO_TIMER).toBe(180);
    expect(PROBLEM_RATINGS).toEqual([800, 1000, 1200, 1400, 1600]);
  });
  it.each([null, undefined, "800", 0, 900, 1800, 800.5, NaN])("rejects unsupported rating %s", (r) => expect(isProblemRating(r)).toBe(false));
  it.each(PROBLEM_RATINGS)("supports exact rating %s", (r) => expect(isProblemRating(r)).toBe(true));
  it("accepts only supported solo timers", () => {
    for (const t of [180, 300, 600, 900, 1800]) expect(isSoloTimer(t)).toBe(true);
    for (const t of [0, -1, 181, null, "180", Infinity]) expect(isSoloTimer(t)).toBe(false);
  });
  it("counts exact pools and excludes unrated/unsupported metadata", () => {
    expect(ratingCounts([{ rating: 800 }, { rating: 1600 }, { rating: null }, { rating: 900 }]))
      .toEqual({ 800: 1, 1000: 0, 1200: 0, 1400: 0, 1600: 1 });
  });
});

describe("practice picker", () => {
  it("defaults to800, excluding warmup", async () => expect(await pickPracticeProblem()).toBe("easy"));
  it("selects only the requested exact rating, excluding hidden", async () => expect(await pickPracticeProblem(null, undefined, 1600)).toBe("hard"));
  it("never falls back to another rating", async () => expect(await pickPracticeProblem(null, undefined, 1200)).toBeNull());
  it("honors explicit exclusions", async () => expect(await pickPracticeProblem(null, new Set(["hard"]), 1600)).toBeNull());
  it("honors per-user invalidations", async () => {
    store.rows.problem_invalidations = [{ problem_id: "hard", by_user: "u", revoked_at: null }];
    expect(await pickPracticeProblem("u", undefined, 1600)).toBeNull();
    expect(await pickPracticeProblem("other", undefined, 1600)).toBe("hard");
  });
  it("prefers unsolved but permits repeats only in the same pool", async () => {
    store.rows.problems.push({ id: "other", rating: 1600, tags: [] });
    store.rows.sessions = [{ problem_id: "hard", user_id: "u", outcome: "solved" }];
    expect(await pickPracticeProblem("u", undefined, 1600)).toBe("other");
    expect(await pickPracticeProblem("u", new Set(["other"]), 1600)).toBe("hard");
  });
  it("does not interpret database failures as an empty/eligible pool", async () => {
    store.errors.add("problem_invalidations");
    await expect(pickPracticeProblem("u", undefined, 1600)).rejects.toThrow();
  });
});

describe("duel picker", () => {
  it("defaults to800", async () => expect(await pickDuelProblem("a", "b")).toBe("easy"));
  it("uses the requested pool", async () => expect(await pickDuelProblem("a", "b", 1600)).toBe("hard"));
  it("never falls back when a requested pool is empty", async () => expect(await pickDuelProblem("a", "b", 1000)).toBeNull());
  it.each(["a", "b"])("excludes problems seen by %s, regardless of outcome", async (user_id) => {
    store.rows.sessions = [{ user_id, problem_id: "hard", outcome: "timeout" }];
    expect(await pickDuelProblem("a", "b", 1600)).toBeNull();
  });
  it("excludes either player's invalidations", async () => {
    store.rows.problem_invalidations = [{ problem_id: "hard", by_user: "b", revoked_at: null }];
    expect(await pickDuelProblem("a", "b", 1600)).toBeNull();
  });
  it("fails closed when the seen-problem query fails", async () => {
    store.errors.add("sessions");
    await expect(pickDuelProblem("a", "b", 1600)).rejects.toThrow();
  });
});
