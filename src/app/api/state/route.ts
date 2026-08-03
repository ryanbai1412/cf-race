import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/api-auth";
import type { ClientState, Contestant, StationRole } from "@/lib/types";

export const dynamic = "force-dynamic";

export async function GET(req: NextRequest) {
  const eventId = req.nextUrl.searchParams.get("eventId") ?? "";
  const event = await requireEvent(eventId);
  if (!event) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const [{ data: race }, { data: contestants }] = await Promise.all([
    db()
      .from("races")
      .select("*, problem:problems(*), participants:race_participants(*)")
      .eq("event_id", eventId)
      .neq("state", "finished")
      .order("created_at", { ascending: false })
      .limit(1)
      .maybeSingle(),
    db()
      .from("contestants")
      .select("*")
      .eq("event_id", eventId)
      .is("retired_at", null)
      .order("created_at", { ascending: false }),
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

  // Active contestant per station = most recent non-retired one.
  const active: Partial<Record<StationRole, Contestant>> = {};
  for (const c of (contestants ?? []) as Contestant[]) {
    if (!active[c.station_role]) active[c.station_role] = c;
  }

  const state: ClientState = {
    serverNow: Date.now(),
    event: { id: event.id, name: event.name },
    contestants: active,
    race: race ?? null,
  };
  return NextResponse.json(state);
}
