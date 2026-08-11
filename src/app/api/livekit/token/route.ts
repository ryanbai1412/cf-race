import { NextRequest, NextResponse } from "next/server";
import { AccessToken } from "livekit-server-sdk";
import { requireEvent } from "@/lib/event-auth";
import { rateLimit } from "@/lib/rate-limit";

export const dynamic = "force-dynamic";

/** Only the fixed set of event devices can appear in a room. */
const STATION_IDENTITY = /^station[12]$/;
const MONITOR_IDENTITY = /^monitor-[a-z0-9-]{1,40}$/;

/**
 * Mint a LiveKit token for an event room. Stations publish their webcam;
 * monitors subscribe only — the publish grant follows the identity rather
 * than the request, so a monitor device cannot ask for one.
 */
export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  const eventId = typeof body?.eventId === "string" ? body.eventId : "";
  const identity = typeof body?.identity === "string" ? body.identity : "";

  const event = await requireEvent(eventId);
  const isStation = STATION_IDENTITY.test(identity);
  if (!event || !(isStation || MONITOR_IDENTITY.test(identity))) {
    return NextResponse.json({ error: "invalid request" }, { status: 400 });
  }
  const limited = rateLimit(req, { name: "livekit-token", limit: 120 });
  if (limited) return limited;

  const apiKey = process.env.LIVEKIT_API_KEY;
  const apiSecret = process.env.LIVEKIT_API_SECRET;
  if (!apiKey || !apiSecret) {
    return NextResponse.json({ error: "LiveKit not configured" }, { status: 503 });
  }

  const at = new AccessToken(apiKey, apiSecret, { identity, ttl: "4h" });
  at.addGrant({
    room: `event-${eventId}`,
    roomJoin: true,
    canPublish: isStation,
    canSubscribe: true,
  });
  return NextResponse.json({ token: await at.toJwt() });
}
