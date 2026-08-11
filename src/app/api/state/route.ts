import { NextRequest, NextResponse } from "next/server";
import { activeContestants } from "@/lib/contestants";
import { requireEvent } from "@/lib/event-auth";
import { requireWebcam, selfServe } from "@/lib/event-settings";
import { activeRace, selfServeAutoStart } from "@/lib/races";
import type { ClientState } from "@/lib/types";

export const dynamic = "force-dynamic";

export async function GET(req: NextRequest) {
  const eventId = req.nextUrl.searchParams.get("eventId") ?? "";
  const event = await requireEvent(eventId);
  if (!event) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  // eslint-disable-next-line prefer-const
  let [race, active] = await Promise.all([
    activeRace(eventId),
    activeContestants(eventId, { excludeRetired: true }),
  ]);

  let autoStartAt: number | null = null;
  if (!race && selfServe(event.settings)) {
    const auto = await selfServeAutoStart(eventId, active);
    autoStartAt = auto.autoStartAt;
    if (auto.started) race = await activeRace(eventId);
  }

  const state: ClientState = {
    serverNow: Date.now(),
    event: {
      id: event.id,
      name: event.name,
      requireWebcam: requireWebcam(event.settings),
      selfServe: selfServe(event.settings),
    },
    contestants: active,
    autoStartAt,
    race: race ?? null,
  };
  return NextResponse.json(state);
}
