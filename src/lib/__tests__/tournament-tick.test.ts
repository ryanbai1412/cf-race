import { beforeEach, describe, expect, it, vi } from "vitest";
import { tick, tickAndPublish } from "../tournament";

const mocks = vi.hoisted(() => ({
  publish: vi.fn(async () => {}),
  lease: true,
  readyOpened: 0,
  snapshot: null as unknown,
}));

vi.mock("../tournament-broadcast", () => ({ publishTournamentState: mocks.publish }));
vi.mock("../db", () => ({
  logDbError: vi.fn(),
  db: () => ({
    from(table: string) {
      const ops: string[] = [];
      const resolve = () => {
        if (ops.includes("maybeSingle")) return { data: mocks.snapshot, error: null };
        if (table === "tournaments" && ops.includes("select") && ops.includes("update")) {
          return { data: mocks.lease ? [{ id: "t1" }] : [], error: null };
        }
        if (table === "tournament_matches" && ops.includes("update")) {
          return { data: mocks.readyOpened++ === 0 ? [{ id: "m1" }] : [], error: null };
        }
        return { data: null, error: null };
      };
      const q: Record<string, unknown> = {
        then: (ok: (v: unknown) => unknown, err: (e: unknown) => unknown) =>
          Promise.resolve(resolve()).then(ok, err),
      };
      for (const op of ["select", "update", "insert", "eq", "or", "is", "in", "order"]) {
        q[op] = () => (ops.push(op), q);
      }
      q.maybeSingle = () => (ops.push("maybeSingle"), q);
      return q;
    },
  }),
}));

const match = {
  id: "m1",
  tournament_id: "t1",
  bracket: "main",
  round: 1,
  slot: 0,
  format: "bo1",
  game_sec: 180,
  member_a: "a",
  member_b: "b",
  a_wins: 0,
  b_wins: 0,
  status: "pending",
  ready_deadline: null,
  a_ready_at: null,
  b_ready_at: null,
  winner_member_id: null,
  loser_member_id: null,
  decided_by: null,
  coin: null,
  finished_at: null,
};
const member = (id: string) => ({ id, joined_at: "2026-01-01T00:00:00Z", kicked_at: null });

describe("tick publishing", () => {
  beforeEach(() => {
    mocks.publish.mockClear();
    mocks.lease = true;
    mocks.readyOpened = 0;
    mocks.snapshot = {
      id: "t1",
      status: "running",
      members: [member("a"), member("b")],
      matches: [match],
      games: [],
    };
  });

  it("publishes once when a pass changes state", async () => {
    expect(await tick("t1")).toBe(true);
    expect(mocks.publish).toHaveBeenCalledTimes(1);
  });

  it("does not publish when nothing changed", async () => {
    mocks.readyOpened = 1;
    expect(await tick("t1")).toBe(false);
    expect(mocks.publish).not.toHaveBeenCalled();
  });

  it("tickAndPublish publishes even when the tick is a no-op or leased elsewhere", async () => {
    mocks.lease = false;
    await tickAndPublish("t1");
    expect(mocks.publish).toHaveBeenCalledTimes(1);
  });
});
