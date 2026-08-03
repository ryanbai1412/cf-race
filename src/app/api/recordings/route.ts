import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/api-auth";

export const maxDuration = 60;
const MAX_BYTES = 100 * 1024 * 1024;

/**
 * Upload a webcam webm to the private `recordings` bucket.
 * Solo runs:   POST /api/recordings?sessionId=…&offsetMs=…
 * Event races: POST /api/recordings?eventId=…&raceId=…&station=…&offsetMs=…
 * offsetMs = recorder start − race/run start (video time = clock − offset).
 */
export async function POST(req: NextRequest) {
  const q = req.nextUrl.searchParams;
  const sessionId = q.get("sessionId") ?? "";
  const eventId = q.get("eventId") ?? "";
  const raceId = q.get("raceId") ?? "";
  const station = q.get("station") ?? "";
  const offsetRaw = Number(q.get("offsetMs") ?? "0");
  const offsetMs = Number.isFinite(offsetRaw) ? Math.round(offsetRaw) : 0;

  let path: string;
  if (sessionId) {
    const { data: session } = await db()
      .from("solo_sessions")
      .select("id")
      .eq("id", sessionId)
      .maybeSingle();
    if (!session) {
      return NextResponse.json({ error: "unknown session" }, { status: 400 });
    }
    path = `solo/${sessionId}.webm`;
  } else if (raceId && (station === "station1" || station === "station2")) {
    const event = await requireEvent(eventId);
    if (!event) return NextResponse.json({ error: "unauthorized" }, { status: 401 });
    const { data: race } = await db()
      .from("races")
      .select("id")
      .eq("id", raceId)
      .eq("event_id", eventId)
      .maybeSingle();
    if (!race) return NextResponse.json({ error: "unknown race" }, { status: 400 });
    path = `race/${raceId}-${station}.webm`;
  } else {
    return NextResponse.json({ error: "bad request" }, { status: 400 });
  }

  const buf = await req.arrayBuffer();
  if (buf.byteLength === 0 || buf.byteLength > MAX_BYTES) {
    return NextResponse.json({ error: "bad recording size" }, { status: 400 });
  }

  const { error: upErr } = await db()
    .storage.from("recordings")
    .upload(path, buf, { contentType: "video/webm", upsert: true });
  if (upErr) return NextResponse.json({ error: upErr.message }, { status: 500 });

  if (sessionId) {
    const { error } = await db()
      .from("solo_sessions")
      .update({ recording_path: path, recording_offset_ms: offsetMs })
      .eq("id", sessionId);
    if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  } else {
    const { error } = await db()
      .from("race_recordings")
      .upsert({
        race_id: raceId,
        station_role: station,
        path,
        offset_ms: offsetMs,
      });
    if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  }
  return NextResponse.json({ ok: true, path });
}
