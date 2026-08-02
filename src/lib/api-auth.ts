import { cookies } from "next/headers";
import { db } from "./db";
import { eventCookieName, EventRow } from "./event-auth";

/** Authorize an API request for an event using the event cookie. */
export async function requireEvent(eventId: string): Promise<EventRow | null> {
  if (!eventId) return null;
  const key = cookies().get(eventCookieName(eventId))?.value;
  if (!key) return null;
  const { data: event } = await db()
    .from("events")
    .select("*")
    .eq("id", eventId)
    .maybeSingle();
  if (!event || event.secret !== key) return null;
  return event as EventRow;
}
