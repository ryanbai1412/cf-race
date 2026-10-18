import { describe, expect, it, vi } from "vitest";
import { tick } from "../tournament";

const mocks = vi.hoisted(() => ({
  snapshot: null as unknown,
  claimed: new Set<string>(),
  problemReads: 0,
  inFlight: 0,
  maxInFlight: 0,
  gamesInserted: 0,
}));

vi.mock("../tournament-broadcast", () => ({ publishTournamentState: vi.fn() }));
vi.mock("../db", () => ({
  logDbError: vi.fn(),
  db: () => ({
    rpc: async () => ({ data: mocks.snapshot, error: null }),
    from(table: string) {
      const ops: string[] = [];
      const eqs: unknown[] = [];
      const resolve = async () => {
        mocks.inFlight++;
        mocks.maxInFlight = Math.max(mocks.maxInFlight, mocks.inFlight);
        await new Promise((r) => setTimeout(r, 5));
        mocks.inFlight--;
        if (table === "tournaments") return { data: [{ id: "t1" }], error: null };
        if (table === "problems") {
          mocks.problemReads++;
          return { data: [{ id: "p1", tags: [] }, { id: "p2", tags: [] }], error: null };
        }
        if (table === "tournament_matches" && ops.includes("select")) {
          const id = eqs[0] as string;
          if (mocks.claimed.has(id)) return { data: [], error: null };
          mocks.claimed.add(id);
          return { data: [{ id }], error: null };
        }
        if (table === "sessions") return { data: { id: `s${Math.random()}` }, error: null };
        if (table === "tournament_games") mocks.gamesInserted++;
        return { data: null, error: null };
      };
      const q: Record<string, unknown> = {
        then: (ok: (v: unknown) => unknown, err: (e: unknown) => unknown) => resolve().then(ok, err),
      };
      for (const op of ["select", "update", "insert", "or", "is", "in", "neq", "single", "order"]) {
        q[op] = () => (ops.push(op), q);
      }
      q.eq = (_col: string, v: unknown) => (eqs.push(v), q);
      return q;
    },
  }),
}));

const readyMatch = (slot: number) => ({
  id: `m${slot}`,
  tournament_id: "t1",
  bracket: "main",
  round: 1,
  slot,
  format: "bo1",
  game_sec: 180,
  member_a: `a${slot}`,
  member_b: `b${slot}`,
  a_wins: 0,
  b_wins: 0,
  status: "ready",
  ready_deadline: "2020-01-01T00:00:00Z",
  a_ready_at: null,
  b_ready_at: null,
  winner_member_id: null,
  loser_member_id: null,
  decided_by: null,
  coin: null,
  finished_at: null,
});

describe("tick over a whole round", () => {
  it("starts every due match concurrently and reads the problem pool once", async () => {
    const matches = [0, 1, 2, 3].map(readyMatch);
    mocks.snapshot = { id: "t1", status: "running", members: [], matches, games: [] };
    expect(await tick("t1")).toBe(true);
    expect(mocks.gamesInserted).toBe(4);
    expect(mocks.problemReads).toBe(1);
    expect(mocks.maxInFlight).toBeGreaterThanOrEqual(4);
  });
});
