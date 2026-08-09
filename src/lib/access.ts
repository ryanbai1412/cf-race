import { cookies } from "next/headers";
import { db } from "./db";
import { getEffectiveUser } from "./impersonation";
import { anonSessionIds } from "./anon-sessions";
import { eventCookieName, secretMatches } from "./event-auth";
import { sweepStaleSessions } from "./session-lifecycle";
import type { SessionRow } from "./session-log";

/**
 * All replay/review/share authorization in one place
 * (docs/flows/11-unified-app-detailed.md §5.3-§5.4). Routes call these and
 * translate a denial into a 404 so existence is never leaked.
 */

/**
 * Who may view a session replay: the owner, anyone in the browser that
 * created an anonymous session (cookie), either participant of a duel
 * session's match, or a holder of the event secret cookie for event
 * sessions.
 */
export async function canViewSession(session: SessionRow): Promise<boolean> {
  const user = await getEffectiveUser();
  if (session.user_id !== null && user?.id === session.user_id) return true;
  if (session.user_id === null && anonSessionIds().includes(session.id)) {
    return true;
  }

  if (session.kind === "duel" && user) {
    const { data: mine } = await db()
      .from("duel_players")
      .select("match_id")
      .eq("session_id", session.id)
      .maybeSingle();
    if (mine && (await canViewMatch(mine.match_id))) return true;
  }

  if (session.kind === "event") {
    const { data: participant } = await db()
      .from("race_participants")
      .select("race_id")
      .eq("session_id", session.id)
      .maybeSingle();
    if (participant) {
      const { data: race } = await db()
        .from("races")
        .select("event_id")
        .eq("id", participant.race_id)
        .maybeSingle();
      if (race) {
        const { data: event } = await db()
          .from("events")
          .select("secret")
          .eq("id", race.event_id)
          .maybeSingle();
        const key = cookies().get(eventCookieName(race.event_id))?.value;
        if (event && key && secretMatches(event.secret, key)) return true;
      }
    }
  }

  return false;
}

/** Who may view a duel match review: either participant. */
export async function canViewMatch(matchId: string): Promise<boolean> {
  const user = await getEffectiveUser();
  if (!user) return false;
  const { data: me } = await db()
    .from("duel_players")
    .select("match_id")
    .eq("match_id", matchId)
    .eq("user_id", user.id)
    .maybeSingle();
  return me !== null;
}

/** Who may mint/revoke a session share: the signed-in owner. */
export async function canShareSession(
  sessionId: string
): Promise<{ userId: string } | null> {
  const user = await getEffectiveUser();
  if (!user) return null;
  const { data: session } = await db()
    .from("sessions")
    .select("id, user_id")
    .eq("id", sessionId)
    .maybeSingle();
  if (!session || session.user_id !== user.id) return null;
  return { userId: user.id };
}

/** Who may mint/revoke a match share: either participant. */
export async function canShareMatch(
  matchId: string
): Promise<{ userId: string } | null> {
  const user = await getEffectiveUser();
  if (!user) return null;
  if (!(await canViewMatch(matchId))) return null;
  return { userId: user.id };
}

/** Load a session for replay, sweeping the idle timeout first. */
export async function loadSessionForReplay(
  sessionId: string
): Promise<SessionRow | null> {
  const { data } = await sweepStaleSessions({ sessionIds: [sessionId] }).then(
    () =>
      db().from("sessions").select("*").eq("id", sessionId).maybeSingle<SessionRow>()
  );
  return data;
}
