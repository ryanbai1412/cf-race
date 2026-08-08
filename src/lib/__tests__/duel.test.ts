import { describe, expect, it } from "vitest";
import { matchEndMs, SUBMIT_GRACE_MS, type DuelMatchRow } from "../duel";

const match = (partial: Partial<DuelMatchRow>): DuelMatchRow => ({
  id: "m1",
  room_id: "r1",
  problem_id: "p1",
  started_at: new Date(1_000_000).toISOString(),
  total_time_sec: null,
  grace_after_ac_sec: null,
  first_ac_at: null,
  winner_user_id: null,
  finished_at: null,
  ...partial,
});

describe("matchEndMs", () => {
  it("is open-ended without a cutoff or first AC", () => {
    expect(matchEndMs(match({}))).toBe(Infinity);
  });

  it("uses the total-time cutoff", () => {
    expect(matchEndMs(match({ total_time_sec: 600 }))).toBe(1_000_000 + 600_000);
  });

  it("shrinks to the grace window after the first AC", () => {
    const m = match({
      total_time_sec: 600,
      grace_after_ac_sec: 60,
      first_ac_at: new Date(1_000_000 + 120_000).toISOString(),
    });
    expect(matchEndMs(m)).toBe(1_000_000 + 120_000 + 60_000);
  });

  it("keeps the earlier of cutoff and grace end", () => {
    const m = match({
      total_time_sec: 120,
      grace_after_ac_sec: 300,
      first_ac_at: new Date(1_000_000 + 60_000).toISOString(),
    });
    expect(matchEndMs(m)).toBe(1_000_000 + 120_000);
  });

  it("ignores first AC when there is no grace setting", () => {
    const m = match({
      total_time_sec: 600,
      first_ac_at: new Date(1_000_000 + 60_000).toISOString(),
    });
    expect(matchEndMs(m)).toBe(1_000_000 + 600_000);
  });
});

describe("SUBMIT_GRACE_MS", () => {
  it("is a small latency allowance", () => {
    expect(SUBMIT_GRACE_MS).toBeGreaterThan(0);
    expect(SUBMIT_GRACE_MS).toBeLessThanOrEqual(5000);
  });
});
