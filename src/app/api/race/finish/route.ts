import { NextRequest, NextResponse } from "next/server";
import { requireEvent } from "@/lib/event-auth";
import { finishRace } from "@/lib/races";

/** Finish/reset the active race (admin action, also called on auto-reset). */
export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  const eventId = typeof body?.eventId === "string" ? body.eventId : "";
  const event = await requireEvent(eventId);
  if (!event) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  await finishRace(eventId);
  return NextResponse.json({ ok: true });
}
