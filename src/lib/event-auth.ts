import { cookies } from "next/headers";
import { db } from "./db";

export type EventRow = {
  id: string;
  name: string;
  secret: string;
  settings: Record<string, unknown>;
  created_at: string;
};

export function eventCookieName(eventId: string): string {
  return `cfr_${eventId.replace(/-/g, "")}`;
}

/**
 * Validates access to an event from either the ?k= query param or the
 * event cookie. Returns the event row when authorized, null otherwise.
 */
export async function authorizeEvent(
  eventId: string,
  keyParam: string | undefined
): Promise<EventRow | null> {
  const { data: event } = await db()
    .from("events")
    .select("*")
    .eq("id", eventId)
    .maybeSingle();
  if (!event) return null;

  const cookieKey = cookies().get(eventCookieName(eventId))?.value;
  const provided = keyParam ?? cookieKey;
  if (!provided || provided !== event.secret) return null;
  return event as EventRow;
}
