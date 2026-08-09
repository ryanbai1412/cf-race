import { db } from "./db";
import { buildSessionReplay } from "./session-log";
import type { DuelMatchRow } from "./duel";

/**
 * Everything the duel review screen needs: both players' replay logs
 * (editor events + submissions in TouristLog shape) with signed webcam
 * URLs, driven by one shared clock on the client.
 */
export async function buildDuelReview(matchId: string) {
  const { data: match } = await db()
    .from("duel_matches")
    .select("*")
    .eq("id", matchId)
    .maybeSingle<DuelMatchRow>();
  if (!match) return null;

  const { data: players } = await db()
    .from("duel_players")
    .select("user_id, session_id")
    .eq("match_id", matchId);

  const userIds = (players ?? []).map((p) => p.user_id);
  const { data: names } = userIds.length
    ? await db()
        .from("duel_room_players")
        .select("user_id, name, avatar_url")
        .in("user_id", userIds)
    : { data: [] };
  const metaById = new Map((names ?? []).map((n) => [n.user_id, n]));

  const replays = await Promise.all(
    (players ?? []).map(async (p) => {
      const replay = await buildSessionReplay(p.session_id);
      const meta = metaById.get(p.user_id);
      return {
        userId: p.user_id,
        sessionId: p.session_id,
        name: meta?.name ?? "Player",
        avatarUrl: meta?.avatar_url ?? null,
        isWinner: match.winner_user_id === p.user_id,
        replay,
      };
    })
  );

  // Invalidations are per-user: the review shows one when either player has
  // invalidated the problem they duelled on.
  const { data: invalidation } = await db()
    .from("problem_invalidations")
    .select("reason, created_at")
    .eq("problem_id", match.problem_id)
    .in("by_user", userIds)
    .is("revoked_at", null)
    .limit(1)
    .maybeSingle();

  return {
    match: {
      id: match.id,
      roomId: match.room_id,
      problemId: match.problem_id,
      startedAt: match.started_at,
      finishedAt: match.finished_at,
      winnerUserId: match.winner_user_id,
      totalTimeSec: match.total_time_sec,
      graceAfterAcSec: match.grace_after_ac_sec,
    },
    invalidated: invalidation !== null,
    invalidReason: invalidation?.reason ?? null,
    players: replays,
  };
}
