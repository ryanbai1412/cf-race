import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/api-auth";
import { notifyEvent } from "@/lib/notify";

export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  const eventId = typeof body?.eventId === "string" ? body.eventId : "";
  const station = body?.station === "station1" || body?.station === "station2" ? body.station : null;
  const name = typeof body?.name === "string" ? body.name.trim().slice(0, 40) : "";
  const country = typeof body?.country === "string" ? body.country.slice(0, 2).toUpperCase() : null;

  const event = await requireEvent(eventId);
  if (!event || !station || !name) {
    return NextResponse.json({ error: "invalid request" }, { status: 400 });
  }

  const { data, error } = await db()
    .from("contestants")
    .insert({ event_id: eventId, station_role: station, name, country })
    .select("*")
    .single();
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });

  await notifyEvent(eventId, { type: "state_changed" });
  return NextResponse.json({ contestant: data });
}
