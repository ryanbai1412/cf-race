import { NextRequest, NextResponse } from "next/server";
import { AccessToken } from "livekit-server-sdk";
import { requireEvent } from "@/lib/api-auth";

export const dynamic = "force-dynamic";

/**
 * Mint a LiveKit token for an event room.
 * Stations publish their webcam; monitors subscribe only.
 */
export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  const eventId = typeof body?.eventId === "string" ? body.eventId : "";
  const identity = typeof body?.identity === "string" ? body.identity.slice(0, 64) : "";
  const publish = body?.publish === true;

  const event = await requireEvent(eventId);
  if (!event || !identity) {
    return NextResponse.json({ error: "invalid request" }, { status: 400 });
  }
  const apiKey = process.env.LIVEKIT_API_KEY;
  const apiSecret = process.env.LIVEKIT_API_SECRET;
  if (!apiKey || !apiSecret) {
    return NextResponse.json({ error: "LiveKit not configured" }, { status: 503 });
  }

  const at = new AccessToken(apiKey, apiSecret, { identity, ttl: "12h" });
  at.addGrant({
    room: `event-${eventId}`,
    roomJoin: true,
    canPublish: publish,
    canSubscribe: true,
  });
  return NextResponse.json({ token: await at.toJwt() });
}
