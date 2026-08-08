import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/event-auth";

export const dynamic = "force-dynamic";

/** Recent races for an event (for the admin replay list). */
export async function GET(req: NextRequest) {
  const eventId = req.nextUrl.searchParams.get("eventId") ?? "";
  const event = await requireEvent(eventId);
  if (!event) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const { data, error } = await db()
    .from("races")
    .select(
      "id, problem_id, state, started_at, timer_sec, problem:problems(name), participants:race_participants(station_role, first_ac_at, dq, contestant:contestants(name, country))"
    )
    .eq("event_id", eventId)
    .not("started_at", "is", null)
    .order("started_at", { ascending: false })
    .limit(30);
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ races: data });
}
