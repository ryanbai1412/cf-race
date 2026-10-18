import { createHash, randomBytes } from "node:crypto";
import { cookies } from "next/headers";
import { db } from "./db";
import { getEffectiveUser } from "./impersonation";
import type { TournamentMemberRow } from "./tournament";

/**
 * Tournament members are capability-authorized: joining mints a random
 * token, the raw value lives in an httpOnly cookie scoped to the tournament
 * and only its hash is stored. Signed-in members are also recognized by
 * user id, so an admin can pick their seat back up from another browser.
 */
const COOKIE_PREFIX = "cfr_tm_";
const COOKIE_MAX_AGE = 60 * 60 * 24 * 30;

export function hashToken(token: string): string {
  return createHash("sha256").update(token).digest("hex");
}

export function mintToken(): { token: string; hash: string } {
  const token = randomBytes(24).toString("base64url");
  return { token, hash: hashToken(token) };
}

export function setMemberCookie(tournamentId: string, token: string): void {
  cookies().set(COOKIE_PREFIX + tournamentId, token, {
    httpOnly: true,
    sameSite: "lax",
    secure: process.env.NODE_ENV === "production",
    path: "/",
    maxAge: COOKIE_MAX_AGE,
  });
}

/** The caller's (non-kicked) membership in a tournament, if any. */
export async function currentMember(
  tournamentId: string
): Promise<TournamentMemberRow | null> {
  const token = cookies().get(COOKIE_PREFIX + tournamentId)?.value;
  if (token) {
    const { data } = await db()
      .from("tournament_members")
      .select("*")
      .eq("tournament_id", tournamentId)
      .eq("token_hash", hashToken(token))
      .maybeSingle<TournamentMemberRow>();
    if (data) return data.kicked_at ? null : data;
  }
  const user = await getEffectiveUser();
  if (!user) return null;
  const { data } = await db()
    .from("tournament_members")
    .select("*")
    .eq("tournament_id", tournamentId)
    .eq("user_id", user.id)
    .is("kicked_at", null)
    .order("joined_at", { ascending: true })
    .limit(1)
    .maybeSingle<TournamentMemberRow>();
  return data ?? null;
}

/**
 * The caller's membership resolved from an already-loaded member list, with
 * the same precedence as currentMember: a matching token cookie wins (and a
 * kicked token yields `kicked` with no user-id fallback), else the earliest
 * live seat held by the signed-in user.
 */
export async function memberFromList(
  tournamentId: string,
  members: TournamentMemberRow[],
  userId: () => Promise<string | null>
): Promise<{ me: TournamentMemberRow | null; kicked: boolean }> {
  const token = cookies().get(COOKIE_PREFIX + tournamentId)?.value;
  if (token) {
    const hash = hashToken(token);
    const seat = members.find((m) => m.token_hash === hash);
    if (seat) return seat.kicked_at ? { me: null, kicked: true } : { me: seat, kicked: false };
  }
  const uid = await userId();
  const mine = uid
    ? members
        .filter((m) => m.user_id === uid && !m.kicked_at)
        .sort((x, y) => Date.parse(x.joined_at) - Date.parse(y.joined_at))[0]
    : undefined;
  return { me: mine ?? null, kicked: false };
}

/**
 * The member a tournament game session belongs to, when the caller holds
 * that member's seat. Used by the shared session routes (events, finish).
 */
export async function tournamentSessionSeat(
  sessionId: string
): Promise<{ member: TournamentMemberRow; gameId: string } | null> {
  const { data: game } = await db()
    .from("tournament_games")
    .select("id, tournament_id, session_a, session_b, tournament_matches(member_a, member_b)")
    .or(`session_a.eq.${sessionId},session_b.eq.${sessionId}`)
    .maybeSingle<{
      id: string;
      tournament_id: string;
      session_a: string | null;
      session_b: string | null;
      tournament_matches: { member_a: string | null; member_b: string | null } | null;
    }>();
  if (!game?.tournament_matches) return null;
  const memberId =
    game.session_a === sessionId
      ? game.tournament_matches.member_a
      : game.tournament_matches.member_b;
  const me = await currentMember(game.tournament_id);
  if (!me || me.id !== memberId) return null;
  return { member: me, gameId: game.id };
}
