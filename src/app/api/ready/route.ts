import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/event-auth";
import { notifyEvent } from "@/lib/notify";
import { rateLimit } from "@/lib/rate-limit";

/** Toggle a contestant's warm-up readiness (event-cookie authorized). */
export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  const eventId = typeof body?.eventId === "string" ? body.eventId : "";
  const contestantId =
    typeof body?.contestantId === "string" ? body.contestantId : "";
  const ready = typeof body?.ready === "boolean" ? body.ready : null;

  const event = await requireEvent(eventId);
  if (!event || !contestantId || ready === null) {
    return NextResponse.json({ error: "invalid request" }, { status: 400 });
  }
  const limited = rateLimit(req, { name: "ready", limit: 120 });
  if (limited) return limited;

  const { data, error } = await db()
    .from("contestants")
    .update({ ready_at: ready ? new Date().toISOString() : null })
    .eq("id", contestantId)
    .eq("event_id", eventId)
    .is("retired_at", null)
    .select("id")
    .maybeSingle();
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  if (!data) return NextResponse.json({ error: "unknown contestant" }, { status: 404 });

  await notifyEvent(eventId, { type: "state_changed" });
  return NextResponse.json({ ok: true });
}
