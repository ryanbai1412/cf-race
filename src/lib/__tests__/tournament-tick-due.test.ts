import { describe, expect, it } from "vitest";
import {
  tickDue,
  type TournamentGameRow,
  type TournamentMatchRow,
  type TournamentMemberRow,
  type TournamentSnapshot,
} from "../tournament";

const NOW = Date.parse("2026-10-18T20:00:00Z");
const iso = (offsetMs: number) => new Date(NOW + offsetMs).toISOString();

function member(id: string, kicked = false): TournamentMemberRow {
  return {
    id,
    tournament_id: "t",
    token_hash: `h-${id}`,
    user_id: null,
    name: id,
    role: "participant",
    is_admin: false,
    is_owner: false,
    seed: null,
    kicked_at: kicked ? iso(-1000) : null,
    joined_at: iso(-60_000),
    last_seen_at: iso(-1000),
  };
}

function match(over: Partial<TournamentMatchRow>): TournamentMatchRow {
  return {
    id: "m",
    tournament_id: "t",
    bracket: "main",
    round: 1,
    slot: 0,
    format: "single",
    game_sec: 300,
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
    ...over,
  };
}

function game(over: Partial<TournamentGameRow>): TournamentGameRow {
  return {
    id: "g",
    match_id: "m",
    tournament_id: "t",
    game_no: 1,
    problem_id: "p",
    started_at: iso(-60_000),
    ends_at: iso(60_000),
    sudden_death: false,
    session_a: "sa",
    session_b: "sb",
    first_ac_at: null,
    winner_member_id: null,
    decided_by: null,
    coin: null,
    finished_at: null,
    ...over,
  };
}

function snap(
  matches: TournamentMatchRow[],
  games: TournamentGameRow[] = [],
  members = [member("a"), member("b"), member("c"), member("d")],
  status: TournamentSnapshot["tournament"]["status"] = "running"
): TournamentSnapshot {
  return {
    tournament: {
      id: "t",
      code: "ABCDEF",
      name: "T",
      created_by: null,
      status,
      champion_member_id: null,
      created_at: iso(-120_000),
      started_at: iso(-90_000),
      finished_at: null,
    },
    members,
    matches,
    games,
    problemNames: new Map(),
    sessions: new Map(),
  };
}

const r1 = (slot: number, over: Partial<TournamentMatchRow> = {}) =>
  match({ id: `r1-${slot}`, slot, member_a: `a${slot}`, member_b: `b${slot}`, ...over });

describe("tickDue", () => {
  it("is false outside running", () => {
    expect(tickDue(snap([match({})], [], undefined, "lobby"), NOW)).toBe(false);
    expect(tickDue(snap([match({})], [], undefined, "finished"), NOW)).toBe(false);
  });

  it("opens a round-1 pending match", () => {
    expect(tickDue(snap([match({ status: "pending" })]), NOW)).toBe(true);
  });

  it("waits on a later-round match until the previous round is done", () => {
    const final = match({ id: "f", round: 2, slot: 0, member_a: null, member_b: null });
    const live = r1(0, { status: "live" });
    const done = r1(1, { status: "done", winner_member_id: "a1" });
    expect(tickDue(snap([live, done, final], [game({ match_id: live.id })]), NOW)).toBe(false);
  });

  it("is due when a ready window lapses or both players are ready", () => {
    const waiting = match({ status: "ready", ready_deadline: iso(10_000) });
    expect(tickDue(snap([waiting]), NOW)).toBe(false);
    expect(tickDue(snap([{ ...waiting, ready_deadline: iso(-1) }]), NOW)).toBe(true);
    expect(tickDue(snap([{ ...waiting, a_ready_at: iso(-1), b_ready_at: iso(-1) }]), NOW)).toBe(true);
    expect(tickDue(snap([{ ...waiting, a_ready_at: iso(-1) }]), NOW)).toBe(false);
  });

  it("is due when the live game is solved or out of time", () => {
    const live = match({ status: "live" });
    expect(tickDue(snap([live], [game({})]), NOW)).toBe(false);
    expect(tickDue(snap([live], [game({ first_ac_at: iso(-1) })]), NOW)).toBe(true);
    expect(tickDue(snap([live], [game({ ends_at: iso(-1) })]), NOW)).toBe(true);
    expect(tickDue(snap([live], [game({ ends_at: iso(-1), finished_at: iso(-1) })]), NOW)).toBe(false);
  });

  it("is due when a seated player was kicked", () => {
    const live = match({ status: "live" });
    const members = [member("a", true), member("b")];
    expect(tickDue(snap([live], [game({})], members), NOW)).toBe(true);
  });

  it("is due once every match is done so the tournament can finish", () => {
    const final = match({ status: "done", winner_member_id: "a" });
    expect(tickDue(snap([final]), NOW)).toBe(true);
  });
});
