import type { BroadcastMsg } from "./types";

/** Broadcast a message to an event channel from the server (HTTP, no WS). */
export async function notifyEvent(
  eventId: string,
  msg: BroadcastMsg
): Promise<void> {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) return;
  try {
    await fetch(`${url}/realtime/v1/api/broadcast`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        apikey: key,
        Authorization: `Bearer ${key}`,
      },
      body: JSON.stringify({
        messages: [
          { topic: `event:${eventId}`, event: "msg", payload: msg, private: false },
        ],
      }),
    });
  } catch {
    // Broadcast is best-effort; clients also poll /api/state.
  }
}
