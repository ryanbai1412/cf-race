import { describe, expect, it } from "vitest";
import { applyPush, needsViewerRefresh, nextDeadline, publicSignature } from "../tournament-live";
import type { GameView, MatchView, MemberView, PublicTournamentState, TournamentStateView } from "../tournament-view";

const member = (id: string, extra: Partial<MemberView> = {}): MemberView => ({
  id, name: id, role: "participant", isAdmin: false, isOwner: false, seed: null, online: true, signedIn: false, ...extra,
});
const game = (id: string, extra: Partial<GameView> = {}): GameView => ({
  id, gameNo: 1, problemId: null, problemName: null, startAtMs: 0, endsAtMs: 1000, suddenDeath: false,
  winner: null, decidedBy: null, coin: null, finishedAtMs: null, firstAcAtMs: null, ...extra,
});
const match = (id: string, extra: Partial<MatchView> = {}): MatchView => ({
  id, bracket: "main", round: 1, slot: 0, format: "single", gameSec: 300, a: "p1", b: "p2", aWins: 0, bWins: 0,
  status: "pending", readyDeadlineMs: null, aReady: false, bReady: false, winner: null, loser: null,
  decidedBy: null, coin: null, finishedAtMs: null, games: [], ...extra,
});
const pub = (matches: MatchView[], members = [member("p1"), member("p2")]): PublicTournamentState => ({
  serverNow: 1,
  tournament: { id: "t", code: "ABC", name: "T", status: "running", startedAtMs: 0, finishedAtMs: null, champion: null },
  members,
  rounds: 1,
  matches,
});
const viewer = (p: PublicTournamentState, meId: string | null): TournamentStateView => ({
  ...p,
  me: meId ? p.members.find((m) => m.id === meId) ?? null : null,
  kicked: false,
  signedIn: true,
  myMatchId: meId ? p.matches[0]?.id ?? null : null,
  myGame: null,
});

describe("applyPush", () => {
  it("keeps per-viewer fields and refreshes me from the member list", () => {
    const prev = viewer(pub([match("m", { status: "ready" })]), "p1");
    const secret = { ...prev, myGame: { gameId: "g" } as TournamentStateView["myGame"] };
    const next = applyPush(secret, pub([match("m", { status: "ready" })], [member("p1", { isAdmin: true }), member("p2")]), 42);
    expect(next.myGame).toBe(secret.myGame);
    expect(next.signedIn).toBe(true);
    expect(next.me?.isAdmin).toBe(true);
    expect(next.serverNow).toBe(42);
    expect(next.myMatchId).toBe("m");
  });
});

describe("needsViewerRefresh", () => {
  it("fires for the players when their game starts, not for spectators", () => {
    const before = pub([match("m", { status: "ready" })]);
    const after = pub([match("m", { status: "live", games: [game("g")] })]);
    const p1 = viewer(before, "p1");
    expect(needsViewerRefresh(p1, applyPush(p1, after, 0))).toBe(true);
    const spectator = viewer(pub(before.matches, [...before.members, member("s", { role: "spectator" })]), "s");
    expect(needsViewerRefresh(spectator, applyPush(spectator, { ...after, members: spectator.members }, 0))).toBe(false);
  });

  it("fires when I disappear from the member list", () => {
    const p1 = viewer(pub([match("m")]), "p1");
    expect(needsViewerRefresh(p1, applyPush(p1, pub([match("m")], [member("p2")]), 0))).toBe(true);
  });
});

describe("publicSignature", () => {
  it("ignores online flags and GO reveals", () => {
    const a = pub([match("m", { status: "live", games: [game("g")] })]);
    const b = pub([match("m", { status: "live", games: [game("g", { problemId: "x", problemName: "X" })] })], [member("p1", { online: false }), member("p2")]);
    expect(publicSignature(a)).toBe(publicSignature(b));
    expect(publicSignature(a)).not.toBe(publicSignature(pub([match("m", { status: "done" })])));
  });
});

describe("nextDeadline", () => {
  it("picks the earliest ready window or game clock", () => {
    const d = nextDeadline([
      match("r", { status: "ready", readyDeadlineMs: 5000 }),
      match("l", { status: "live", games: [game("g1", { finishedAtMs: 1, endsAtMs: 100 }), game("g2", { gameNo: 2, endsAtMs: 3000 })] }),
      match("p"),
    ]);
    expect(d).toMatchObject({ at: 3000, match: { id: "l" } });
    expect(nextDeadline([match("d", { status: "done" })])).toBeNull();
  });
});
