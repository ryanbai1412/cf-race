import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/event-auth";
import { notifyEvent } from "@/lib/notify";

/**
 * Finish/reset the active race (admin action, also called on auto-reset).
 * Marks the race finished and DQs participants without an AC if the timer ran out.
 */
export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  const eventId = typeof body?.eventId === "string" ? body.eventId : "";
  const event = await requireEvent(eventId);
  if (!event) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const { data: race } = await db()
    .from("races")
    .select("id")
    .eq("event_id", eventId)
    .neq("state", "finished")
    .order("created_at", { ascending: false })
    .limit(1)
    .maybeSingle();
  if (race) {
    await db().from("races").update({ state: "finished" }).eq("id", race.id);
    await db()
      .from("race_participants")
      .update({ dq: true })
      .eq("race_id", race.id)
      .is("first_ac_at", null);
  }
  await db()
    .from("contestants")
    .update({ retired_at: new Date().toISOString() })
    .eq("event_id", eventId)
    .is("retired_at", null);
  await notifyEvent(eventId, { type: "state_changed" });
  return NextResponse.json({ ok: true });
}
