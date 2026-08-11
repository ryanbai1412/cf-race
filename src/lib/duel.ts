import { db, logDbError } from "./db";
import type { Lang } from "./types";

/** Latency grace (ms) added to server-side time-window checks. */
export const SUBMIT_GRACE_MS = 3000;
export const COUNTDOWN_MS = 3000;
export const DEFAULT_GRACE_AFTER_AC_SEC = 60;

export type DuelRoomRow = {
  id: string;
  created_by: string;
  status: "lobby" | "racing" | "done";
  total_time_sec: number | null;
  grace_after_ac_sec: number | null;
  created_at: string;
};

export type DuelRoomPlayerRow = {
  room_id: string;
  user_id: string;
  name: string;
  avatar_url: string | null;
  joined_at: string;
  ready_at: string | null;
};

export type DuelMatchRow = {
  id: string;
  room_id: string;
  problem_id: string;
  started_at: string;
  total_time_sec: number | null;
  grace_after_ac_sec: number | null;
  first_ac_at: string | null;
  winner_user_id: string | null;
  finished_at: string | null;
};

export type DuelPlayerRow = {
  match_id: string;
  user_id: string;
  session_id: string;
};

export type DuelSessionRow = {
  id: string;
  user_id: string | null;
  problem_id: string;
  lang: Lang | null;
  started_at: string;
  outcome: "solved" | "timeout" | "abandoned" | null;
  solve_ms: number | null;
  recording_path: string | null;
};

/** The latest match in a room, with its players and sessions. */
export async function latestMatch(roomId: string): Promise<{
  match: DuelMatchRow;
  players: DuelPlayerRow[];
  sessions: DuelSessionRow[];
} | null> {
  const { data: match } = await db()
    .from("duel_matches")
    .select(
      "*, duel_players(match_id, user_id, session_id, sessions(id, user_id, problem_id, lang, started_at, outcome, solve_ms, recording_path))"
    )
    .eq("room_id", roomId)
    .order("created_at", { ascending: false })
    .limit(1)
    .maybeSingle<
      DuelMatchRow & {
        duel_players: (DuelPlayerRow & { sessions: DuelSessionRow | null })[];
      }
    >();
  if (!match) return null;
  const { duel_players: rows, ...matchRow } = match;
  return {
    match: matchRow as DuelMatchRow,
    players: rows.map(({ match_id, user_id, session_id }) => ({
      match_id,
      user_id,
      session_id,
    })),
    sessions: rows.flatMap((r) => (r.sessions ? [r.sessions] : [])),
  };
}

/** When the match hard-ends, in epoch ms (Infinity when open-ended). */
export function matchEndMs(match: DuelMatchRow): number {
  const startMs = new Date(match.started_at).getTime();
  let end = Infinity;
  if (match.total_time_sec) end = startMs + match.total_time_sec * 1000;
  if (match.first_ac_at && match.grace_after_ac_sec != null) {
    end = Math.min(
      end,
      new Date(match.first_ac_at).getTime() + match.grace_after_ac_sec * 1000
    );
  }
  return end;
}

/**
 * Lazily finish a match when its end conditions are met: all sessions have an
 * outcome, or the time window (total cutoff / grace after first AC) expired.
 * Marks non-AC sessions timeout, stamps winner + finished_at, and returns the
 * room to the lobby for a rematch.
 */
export async function resolveMatch(roomId: string): Promise<DuelMatchRow | null> {
  const cur = await latestMatch(roomId);
  if (!cur) return null;
  const { match, sessions } = cur;
  if (match.finished_at) return match;

  const now = Date.now();
  const allDecided =
    sessions.length > 0 && sessions.every((s) => s.outcome !== null);
  const timeExpired = now > matchEndMs(match) + SUBMIT_GRACE_MS;
  if (!allDecided && !timeExpired) return match;

  const acs = sessions
    .filter((s) => s.outcome === "solved" && s.solve_ms !== null)
    .sort((a, b) => (a.solve_ms ?? 0) - (b.solve_ms ?? 0));
  const winner = acs[0]?.user_id ?? null;

  for (const s of sessions) {
    if (s.outcome === null) {
      const { error } = await db()
        .from("sessions")
        .update({ outcome: "timeout" })
        .eq("id", s.id)
        .is("outcome", null);
      logDbError(`resolveMatch: timeout session ${s.id}`, error);
    }
  }
  const { data: updated, error: finishErr } = await db()
    .from("duel_matches")
    .update({
      finished_at: new Date().toISOString(),
      winner_user_id: winner,
    })
    .eq("id", match.id)
    .is("finished_at", null)
    .select("*")
    .maybeSingle<DuelMatchRow>();
  logDbError(`resolveMatch: finish match ${match.id}`, finishErr);
  // Both players poll this concurrently, so only the caller that actually
  // stamped finished_at returns the room to the lobby: a late loser must not
  // wipe ready flags the players have already set for the rematch.
  if (updated) {
    const { error: roomErr } = await db()
      .from("duel_rooms")
      .update({ status: "lobby" })
      .eq("id", roomId)
      .eq("status", "racing");
    logDbError(`resolveMatch: reset room ${roomId}`, roomErr);
    const { error: readyErr } = await db()
      .from("duel_room_players")
      .update({ ready_at: null })
      .eq("room_id", roomId);
    logDbError(`resolveMatch: clear ready ${roomId}`, readyErr);
  }
  return updated ?? { ...match, finished_at: new Date().toISOString(), winner_user_id: winner };
}

/**
 * Start a match for a room whose start was already claimed (status flipped
 * lobby → racing): pick the problem, create the match and one session per
 * player with a server-stamped start (now + countdown).
 */
export async function startDuelMatch(
  room: DuelRoomRow,
  playerIds: [string, string]
): Promise<{ ok: true } | { ok: false; error: string; status: number }> {
  const [userA, userB] = playerIds;
  const problemId = await pickDuelProblem(userA, userB);
  if (!problemId) {
    await releaseRoom(room.id);
    return { ok: false, error: "no eligible problems left for this pair", status: 409 };
  }

  const startAt = new Date(Date.now() + COUNTDOWN_MS).toISOString();
  const { data: match, error } = await db()
    .from("duel_matches")
    .insert({
      room_id: room.id,
      problem_id: problemId,
      started_at: startAt,
      total_time_sec: room.total_time_sec,
      grace_after_ac_sec: room.grace_after_ac_sec,
    })
    .select("id")
    .single();
  if (error) {
    await releaseRoom(room.id);
    return { ok: false, error: error.message, status: 500 };
  }

  // Session ids are minted here so a failure halfway through can be undone
  // precisely, and so no player is left in a racing room without a session.
  const sessionIds: string[] = [];
  for (const uid of playerIds) {
    const sessionId = crypto.randomUUID();
    const { error: sErr } = await db().from("sessions").insert({
      id: sessionId,
      kind: "duel",
      user_id: uid,
      problem_id: problemId,
      started_at: startAt,
      timer_sec: room.total_time_sec,
    });
    if (sErr) {
      await abandonPartialMatch(room.id, match.id, sessionIds);
      return { ok: false, error: sErr.message, status: 500 };
    }
    sessionIds.push(sessionId);
    const { error: pErr } = await db().from("duel_players").insert({
      match_id: match.id,
      user_id: uid,
      session_id: sessionId,
    });
    if (pErr) {
      await abandonPartialMatch(room.id, match.id, sessionIds);
      return { ok: false, error: pErr.message, status: 500 };
    }
  }
  return { ok: true };
}

/** Undo a start claim: back to the lobby with everyone un-readied. */
async function releaseRoom(roomId: string): Promise<void> {
  const { error: roomErr } = await db()
    .from("duel_rooms")
    .update({ status: "lobby" })
    .eq("id", roomId);
  logDbError(`releaseRoom: reset room ${roomId}`, roomErr);
  const { error: readyErr } = await db()
    .from("duel_room_players")
    .update({ ready_at: null })
    .eq("room_id", roomId);
  logDbError(`releaseRoom: clear ready ${roomId}`, readyErr);
}

/**
 * A match that failed to get a session for every player can never be raced or
 * resolved, and would strand the room in `racing` — drop it and reopen the
 * lobby so the players can ready up again.
 */
async function abandonPartialMatch(
  roomId: string,
  matchId: string,
  sessionIds: string[]
): Promise<void> {
  const { error: playersErr } = await db()
    .from("duel_players")
    .delete()
    .eq("match_id", matchId);
  logDbError(`abandonPartialMatch: players ${matchId}`, playersErr);
  const { error: matchErr } = await db()
    .from("duel_matches")
    .delete()
    .eq("id", matchId);
  logDbError(`abandonPartialMatch: match ${matchId}`, matchErr);
  if (sessionIds.length > 0) {
    const { error: sessionsErr } = await db()
      .from("sessions")
      .delete()
      .in("id", sessionIds);
    logDbError(`abandonPartialMatch: sessions ${matchId}`, sessionsErr);
  }
  await releaseRoom(roomId);
}

/**
 * Problem ids these users have invalidated ("don't give me this one again").
 * Invalidations are per-user, so a pick for two players excludes the union of
 * both players' choices.
 */
export async function invalidatedProblemIds(
  userIds: (string | null | undefined)[]
): Promise<Set<string>> {
  const ids = userIds.filter((id): id is string => Boolean(id));
  if (ids.length === 0) return new Set();
  const { data } = await db()
    .from("problem_invalidations")
    .select("problem_id")
    .in("by_user", ids)
    .is("revoked_at", null);
  return new Set((data ?? []).map((r) => r.problem_id as string));
}

/** The reason this user invalidated a problem, or null when they haven't. */
export async function invalidationFor(
  problemId: string,
  userId: string
): Promise<{ reason: string | null; created_at: string } | null> {
  const { data } = await db()
    .from("problem_invalidations")
    .select("reason, created_at")
    .eq("problem_id", problemId)
    .eq("by_user", userId)
    .is("revoked_at", null)
    .maybeSingle<{ reason: string | null; created_at: string }>();
  return data ?? null;
}

/**
 * Server-side random pick: a uniformly random problem that (a) neither player
 * has solved, (b) is not invalidated, (c) was not used in a previous match
 * between this pair.
 */
export async function pickDuelProblem(
  userA: string,
  userB: string
): Promise<string | null> {
  const [{ data: problems }, invalidated, { data: solved }, { data: aMatches }] =
    await Promise.all([
      db()
        .from("problems")
        .select("id, tags")
        .neq("id", "warmup-sum"),
      invalidatedProblemIds([userA, userB]),
      db()
        .from("sessions")
        .select("problem_id, user_id")
        .in("user_id", [userA, userB])
        .eq("outcome", "solved"),
      db().from("duel_players").select("match_id").eq("user_id", userA),
    ]);

  // Matches involving both players (any room).
  const aMatchIds = (aMatches ?? []).map((m) => m.match_id);
  let usedByPair = new Set<string>();
  if (aMatchIds.length > 0) {
    const { data: shared } = await db()
      .from("duel_players")
      .select("match_id")
      .eq("user_id", userB)
      .in("match_id", aMatchIds);
    const sharedIds = (shared ?? []).map((m) => m.match_id);
    if (sharedIds.length > 0) {
      const { data: used } = await db()
        .from("duel_matches")
        .select("problem_id")
        .in("id", sharedIds);
      usedByPair = new Set((used ?? []).map((m) => m.problem_id as string));
    }
  }

  const solvedIds = new Set((solved ?? []).map((s) => s.problem_id as string));
  const pool = (problems ?? [])
    .filter((p) => !((p.tags as string[] | null) ?? []).includes("hidden"))
    .map((p) => p.id as string)
    .filter(
      (id) => !solvedIds.has(id) && !invalidated.has(id) && !usedByPair.has(id)
    );
  if (pool.length === 0) return null;
  return pool[Math.floor(Math.random() * pool.length)];
}
