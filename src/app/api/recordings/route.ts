import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/event-auth";

/**
 * Webcam recordings live in the private `recordings` bucket. The webm itself
 * is uploaded straight from the browser via a signed upload URL (serverless
 * request-body limits are far too small for video), in two steps:
 *
 *   POST /api/recordings?step=sign&…     → { path, token }
 *   POST /api/recordings?step=confirm&…  → records path/offset in the DB
 *
 * Solo runs identify themselves with ?sessionId=…, event races with
 * ?eventId=…&raceId=…&station=…. offsetMs = recorder start − race/run start
 * (video time = clock − offset).
 */
export async function POST(req: NextRequest) {
  const q = req.nextUrl.searchParams;
  const step = q.get("step") ?? "";
  const sessionId = q.get("sessionId") ?? "";
  const eventId = q.get("eventId") ?? "";
  const raceId = q.get("raceId") ?? "";
  const station = q.get("station") ?? "";
  const offsetRaw = Number(q.get("offsetMs") ?? "0");
  const offsetMs = Number.isFinite(offsetRaw) ? Math.round(offsetRaw) : 0;
  if (step !== "sign" && step !== "confirm") {
    return NextResponse.json({ error: "bad request" }, { status: 400 });
  }

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

  if (step === "sign") {
    const { data, error } = await db()
      .storage.from("recordings")
      .createSignedUploadUrl(path, { upsert: true });
    if (error || !data) {
      return NextResponse.json(
        { error: error?.message ?? "sign failed" },
        { status: 500 }
      );
    }
    return NextResponse.json({
      path: data.path,
      token: data.token,
      signedUrl: data.signedUrl,
    });
  }

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
