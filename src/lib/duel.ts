import { db } from "./db";
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
    .select("*")
    .eq("room_id", roomId)
    .order("created_at", { ascending: false })
    .limit(1)
    .maybeSingle<DuelMatchRow>();
  if (!match) return null;
  const { data: players } = await db()
    .from("duel_players")
    .select("*")
    .eq("match_id", match.id);
  const sessionIds = (players ?? []).map((p) => p.session_id);
  const { data: sessions } = await db()
    .from("sessions")
    .select("id, user_id, problem_id, lang, started_at, outcome, solve_ms, recording_path")
    .in("id", sessionIds);
  return {
    match,
    players: (players ?? []) as DuelPlayerRow[],
    sessions: (sessions ?? []) as DuelSessionRow[],
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
      await db()
        .from("sessions")
        .update({ outcome: "timeout" })
        .eq("id", s.id)
        .is("outcome", null);
    }
  }
  const { data: updated } = await db()
    .from("duel_matches")
    .update({
      finished_at: new Date().toISOString(),
      winner_user_id: winner,
    })
    .eq("id", match.id)
    .is("finished_at", null)
    .select("*")
    .maybeSingle<DuelMatchRow>();
  await db()
    .from("duel_rooms")
    .update({ status: "lobby" })
    .eq("id", roomId)
    .eq("status", "racing");
  await db()
    .from("duel_room_players")
    .update({ ready_at: null })
    .eq("room_id", roomId);
  return updated ?? { ...match, finished_at: new Date().toISOString(), winner_user_id: winner };
}

/** Problem ids currently invalidated (active, non-revoked invalidations). */
export async function invalidatedProblemIds(): Promise<Set<string>> {
  const { data } = await db()
    .from("problem_invalidations")
    .select("problem_id")
    .is("revoked_at", null);
  return new Set((data ?? []).map((r) => r.problem_id as string));
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
      db().from("problems").select("id").neq("id", "warmup-sum"),
      invalidatedProblemIds(),
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
    .map((p) => p.id as string)
    .filter(
      (id) => !solvedIds.has(id) && !invalidated.has(id) && !usedByPair.has(id)
    );
  if (pool.length === 0) return null;
  return pool[Math.floor(Math.random() * pool.length)];
}
