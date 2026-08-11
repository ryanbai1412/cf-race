import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/event-auth";
import { notifyEvent } from "@/lib/notify";

/** Retire a single contestant (their station returns to check-in). */
export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  const eventId = typeof body?.eventId === "string" ? body.eventId : "";
  const contestantId =
    typeof body?.contestantId === "string" ? body.contestantId : "";

  const event = await requireEvent(eventId);
  if (!event || !contestantId) {
    return NextResponse.json({ error: "invalid request" }, { status: 400 });
  }

  const { error } = await db()
    .from("contestants")
    .update({ retired_at: new Date().toISOString() })
    .eq("event_id", eventId)
    .eq("id", contestantId)
    .is("retired_at", null);
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });

  await notifyEvent(eventId, { type: "state_changed" });
  return NextResponse.json({ ok: true });
}
