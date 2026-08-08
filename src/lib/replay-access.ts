import { cookies } from "next/headers";
import { db } from "./db";
import { authUser } from "./supabase/server";
import { anonSessionIds } from "./anon-sessions";
import { eventCookieName, secretMatches } from "./event-auth";
import { sweepStaleSessions } from "./session-lifecycle";
import type { SessionRow } from "./session-log";

/**
 * Replay access rules (docs/flows/11-unified-app-detailed.md §5.3):
 * the session owner, anyone in the browser that created an anonymous
 * session (cookie), either participant of a duel session's match, or a
 * holder of the event secret cookie for event sessions. Everything else
 * is a 404 — session existence is never leaked.
 */
export async function canViewSession(session: SessionRow): Promise<boolean> {
  const user = await authUser();
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
    if (mine) {
      const { data: me } = await db()
        .from("duel_players")
        .select("session_id")
        .eq("match_id", mine.match_id)
        .eq("user_id", user.id)
        .maybeSingle();
      if (me) return true;
    }
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

/** Load a session for replay, sweeping the idle timeout first. */
export async function loadSessionForReplay(
  sessionId: string
): Promise<SessionRow | null> {
  await sweepStaleSessions({ sessionIds: [sessionId] });
  const { data } = await db()
    .from("sessions")
    .select("*")
    .eq("id", sessionId)
    .maybeSingle<SessionRow>();
  return data;
}
