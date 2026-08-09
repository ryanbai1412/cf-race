import { NextRequest, NextResponse } from "next/server";
import { activeContestants } from "@/lib/contestants";
import { requireEvent } from "@/lib/event-auth";
import { requireWebcam } from "@/lib/event-settings";
import { activeRace } from "@/lib/races";
import type { ClientState } from "@/lib/types";

export const dynamic = "force-dynamic";

export async function GET(req: NextRequest) {
  const eventId = req.nextUrl.searchParams.get("eventId") ?? "";
  const event = await requireEvent(eventId);
  if (!event) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const [race, active] = await Promise.all([
    activeRace(eventId),
    activeContestants(eventId, { excludeRetired: true }),
  ]);

  const state: ClientState = {
    serverNow: Date.now(),
    event: {
      id: event.id,
      name: event.name,
      requireWebcam: requireWebcam(event.settings),
    },
    contestants: active,
    race: race ?? null,
  };
  return NextResponse.json(state);
}
