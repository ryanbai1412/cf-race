import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/event-auth";
import { raceParticipantByStation } from "@/lib/races";
import { requireSessionAccess } from "@/lib/session-auth";

/**
 * Webcam recordings live in the private `recordings` bucket. The webm itself
 * is uploaded straight from the browser via a signed upload URL (serverless
 * request-body limits are far too small for video), in two steps:
 *
 *   POST /api/recordings?step=sign&…     → { path, token }
 *   POST /api/recordings?step=confirm&…  → records path/offset in the DB
 *
 * Solo/duel runs identify themselves with ?sessionId=…, event races with
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

  // Both flows end up writing to the participant's universal session; the
  // event-race branch just resolves the session through the race + station.
  let targetSessionId: string;
  let path: string;
  if (sessionId) {
    const access = await requireSessionAccess(sessionId);
    if (!access.ok) return access.response;
    targetSessionId = access.session.id;
    path = `${access.session.kind}/${sessionId}.webm`;
  } else if (raceId && (station === "station1" || station === "station2")) {
    const event = await requireEvent(eventId);
    if (!event) return NextResponse.json({ error: "unauthorized" }, { status: 401 });
    const found = await raceParticipantByStation(eventId, raceId, station);
    if (!found?.participant.session_id) {
      return NextResponse.json({ error: "unknown race" }, { status: 400 });
    }
    targetSessionId = found.participant.session_id;
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

  const { error } = await db()
    .from("sessions")
    .update({ recording_path: path, recording_offset_ms: offsetMs })
    .eq("id", targetSessionId);
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ ok: true, path });
}
