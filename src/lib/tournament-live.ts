import type { MatchView, PublicTournamentState, TournamentStateView } from "./tournament-view";

/** Client mirror of currentMatchFor: the member's seat that isn't done yet. */
export function currentMatchId(matches: MatchView[], memberId: string): string | null {
  const seated = (m: MatchView) => m.a === memberId || m.b === memberId;
  return (
    matches.find((m) => m.status !== "done" && m.status !== "pending" && seated(m))?.id ??
    matches.find((m) => m.status === "pending" && seated(m))?.id ??
    null
  );
}

const openGame = (m: MatchView | undefined) =>
  m?.games.filter((g) => !g.finishedAtMs).sort((x, y) => y.gameNo - x.gameNo)[0];

/** Overlay a pushed public state on this viewer's state, keeping the per-viewer fields. */
export function applyPush(prev: TournamentStateView, pub: PublicTournamentState, now: number): TournamentStateView {
  const me = prev.me ? pub.members.find((m) => m.id === prev.me!.id) ?? prev.me : null;
  const myMatchId =
    me?.role === "participant" && pub.tournament.status !== "lobby" ? currentMatchId(pub.matches, me.id) : null;
  return {
    ...prev,
    serverNow: now,
    tournament: pub.tournament,
    members: pub.members,
    rounds: pub.rounds,
    matches: pub.matches,
    me,
    myMatchId,
  };
}

function viewerKey(s: TournamentStateView): string {
  if (!s.me || s.me.role !== "participant") return s.tournament.status;
  const mid = currentMatchId(s.matches, s.me.id);
  const m = s.matches.find((x) => x.id === mid);
  return [s.tournament.status, mid, m?.status, openGame(m)?.id].join("|");
}

/** Whether a push changed something only /state can tell this viewer (their game, their seat). */
export function needsViewerRefresh(prev: TournamentStateView, next: TournamentStateView): boolean {
  if (prev.me && !next.members.some((m) => m.id === prev.me!.id)) return true;
  return viewerKey(prev) !== viewerKey(next);
}

/** Comparable public content, ignoring fields that drift with time (online, GO reveals). */
export function publicSignature(s: Pick<TournamentStateView, "tournament" | "rounds" | "matches" | "members">): string {
  return JSON.stringify([
    s.tournament,
    s.rounds,
    s.members.map((m) => ({ ...m, online: null })),
    s.matches.map((m) => ({ ...m, games: m.games.map((g) => ({ ...g, problemId: null, problemName: null })) })),
  ]);
}

/** The earliest timer-driven transition (ready window closing or game clock running out). */
export function nextDeadline(matches: MatchView[]): { at: number; match: MatchView } | null {
  let best: { at: number; match: MatchView } | null = null;
  for (const m of matches) {
    const at =
      m.status === "ready" ? m.readyDeadlineMs : m.status === "live" ? openGame(m)?.endsAtMs ?? null : null;
    if (at !== null && (!best || at < best.at)) best = { at, match: m };
  }
  return best;
}
