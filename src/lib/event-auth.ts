import crypto from "node:crypto";
import { cookies } from "next/headers";
import { db } from "./db";
import { isEventAdmin } from "./event-admins";
import { getEffectiveUser } from "./impersonation";

export type EventRow = {
  id: string;
  name: string;
  secret: string;
  settings: Record<string, unknown>;
  created_at: string;
  created_by: string | null;
};

export function eventCookieName(eventId: string): string {
  return `cfr_${eventId.replace(/-/g, "")}`;
}

/** Constant-time comparison of an event secret against a provided key. */
export function secretMatches(secret: string, provided: string): boolean {
  const a = Buffer.from(secret);
  const b = Buffer.from(provided);
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}

/**
 * Validates access to an event from the event cookie, or — for logged-in users
 * — from event admin membership (creator or `event_admins`). The secret is
 * never accepted from the URL here: `/e/[eventId]/join?k=` trades it for the
 * cookie in a redirect exactly once, so it never lands in a rendered page's
 * address bar, history entry or Referer header.
 */
export async function authorizeEvent(eventId: string): Promise<EventRow | null> {
  if (!eventId) return null;
  const { data: event } = await db()
    .from("events")
    .select("*")
    .eq("id", eventId)
    .maybeSingle();
  if (!event) return null;

  const cookieKey = cookies().get(eventCookieName(eventId))?.value;
  if (cookieKey && secretMatches(event.secret, cookieKey)) {
    return event as EventRow;
  }

  const user = await getEffectiveUser();
  if (user && (await isEventAdmin(event as EventRow, user.id))) {
    return event as EventRow;
  }
  return null;
}

/** Authorize an API request for an event (event cookie or event admin). */
export function requireEvent(eventId: string): Promise<EventRow | null> {
  return authorizeEvent(eventId);
}
