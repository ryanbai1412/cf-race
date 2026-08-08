import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/event-auth";
import {
  sanitizeEditorEvents,
  type IncomingEditorEvent,
} from "@/lib/editor-events";
import { raceParticipantByStation } from "@/lib/races";
import { buildSessionLog } from "@/lib/session-log";
import type { StationRole } from "@/lib/types";

export const dynamic = "force-dynamic";

/** Persist a batch of editor events recorded during a race. */
export async function POST(req: NextRequest) {
  const body = (await req.json().catch(() => null)) as {
    eventId?: string;
    raceId?: string;
    station?: string;
    events?: IncomingEditorEvent[];
  } | null;
  const event = await requireEvent(body?.eventId ?? "");
  if (!event) return NextResponse.json({ error: "unauthorized" }, { status: 401 });
  if (
    !body ||
    !body.raceId ||
    (body.station !== "station1" && body.station !== "station2") ||
    !Array.isArray(body.events) ||
    body.events.length === 0
  ) {
    return NextResponse.json({ error: "bad request" }, { status: 400 });
  }

  const found = await raceParticipantByStation(
    body.eventId ?? "",
    body.raceId,
    body.station as StationRole
  );
  if (!found?.participant.session_id) {
    return NextResponse.json({ error: "not found" }, { status: 404 });
  }

  const rows = sanitizeEditorEvents(body.events).map((row) => ({
    ...row,
    session_id: found.participant.session_id,
  }));
  const { error } = await db().from("session_events").insert(rows);
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ ok: true });
}

/**
 * Assemble a replay log (same shape as a tourist log) for one station of a
 * race, from the participant's universal session.
 */
export async function GET(req: NextRequest) {
  const eventId = req.nextUrl.searchParams.get("eventId") ?? "";
  const raceId = req.nextUrl.searchParams.get("raceId") ?? "";
  const station = req.nextUrl.searchParams.get("station") ?? "";
  const event = await requireEvent(eventId);
  if (!event) return NextResponse.json({ error: "unauthorized" }, { status: 401 });
  if (!raceId || (station !== "station1" && station !== "station2")) {
    return NextResponse.json({ error: "bad request" }, { status: 400 });
  }

  const found = await raceParticipantByStation(eventId, raceId, station);
  if (!found?.participant.session_id || !found.race.started_at) {
    return NextResponse.json({ error: "not found" }, { status: 404 });
  }
  const built = await buildSessionLog(found.participant.session_id);
  if (!built) return NextResponse.json({ error: "not found" }, { status: 404 });
  const { session, log } = built;

  const { data: contestant } = await db()
    .from("contestants")
    .select("name, country")
    .eq("id", found.participant.contestant_id)
    .maybeSingle();

  // Full problem row so the replay can render the statement pane.
  const { data: problemRow } = await db()
    .from("problems")
    .select("*")
    .eq("id", session.problem_id)
    .maybeSingle();

  let recordingUrl: string | null = null;
  if (session.recording_path) {
    const { data: signed } = await db()
      .storage.from("recordings")
      .createSignedUrl(session.recording_path, 3600);
    recordingUrl = signed?.signedUrl ?? null;
  }

  return NextResponse.json({
    problemId: session.problem_id,
    lang: log.lang,
    solveMs: session.solve_ms,
    events: log.events,
    contestant: contestant
      ? { name: contestant.name, country: contestant.country }
      : null,
    timerSec: session.timer_sec ?? found.race.timer_sec,
    problem: problemRow ?? null,
    recordingUrl,
    recordingOffsetMs: session.recording_offset_ms ?? 0,
  });
}
