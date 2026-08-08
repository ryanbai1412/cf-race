import { NextRequest, NextResponse } from "next/server";
import { activeContestants } from "@/lib/contestants";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/event-auth";
import type { ClientState } from "@/lib/types";

export const dynamic = "force-dynamic";

export async function GET(req: NextRequest) {
  const eventId = req.nextUrl.searchParams.get("eventId") ?? "";
  const event = await requireEvent(eventId);
  if (!event) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const [{ data: race }, active] = await Promise.all([
    db()
      .from("races")
      .select("*, problem:problems(*), participants:race_participants(*)")
      .eq("event_id", eventId)
      .neq("state", "finished")
      .order("created_at", { ascending: false })
      .limit(1)
      .maybeSingle(),
    activeContestants(eventId, { excludeRetired: true }),
  ]);

  // Lazily transition countdown → running once the start time has passed.
  if (
    race &&
    race.state === "countdown" &&
    race.started_at &&
    new Date(race.started_at).getTime() <= Date.now()
  ) {
    race.state = "running";
    await db().from("races").update({ state: "running" }).eq("id", race.id);
  }

  const state: ClientState = {
    serverNow: Date.now(),
    event: { id: event.id, name: event.name },
    contestants: active,
    race: race ?? null,
  };
  return NextResponse.json(state);
}
