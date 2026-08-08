import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/event-auth";
import {
  buildReplayEvents,
  fetchEditorEventRows,
  sanitizeEditorEvents,
  type IncomingEditorEvent,
} from "@/lib/editor-events";

export const dynamic = "force-dynamic";

/** Persist a batch of editor snapshots recorded during a race. */
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

  const rows = sanitizeEditorEvents(body.events).map((row) => ({
    ...row,
    race_id: body.raceId,
    station_role: body.station,
  }));
  const { error } = await db().from("race_editor_events").insert(rows);
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ ok: true });
}

/**
 * Assemble a replay log (same shape as a tourist log) for one station of a
 * race: editor snapshots from race_editor_events, submit/verdict moments from
 * the submissions table.
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

  const { data: race } = await db()
    .from("races")
    .select("*, participants:race_participants(*, contestant:contestants(*))")
    .eq("id", raceId)
    .eq("event_id", eventId)
    .maybeSingle();
  if (!race || !race.started_at) {
    return NextResponse.json({ error: "not found" }, { status: 404 });
  }
  const startMs = new Date(race.started_at).getTime();
  const participant = (
    race.participants as {
      contestant_id: string;
      station_role: string;
      first_ac_at: string | null;
      contestant: { name: string; country: string | null } | null;
    }[]
  ).find((p) => p.station_role === station);
  if (!participant) {
    return NextResponse.json({ error: "not found" }, { status: 404 });
  }

  const [snaps, { data: subs }] = await Promise.all([
    fetchEditorEventRows("race_editor_events", {
      race_id: raceId,
      station_role: station,
    }),
    db()
      .from("submissions")
      .select("submitted_at, judged_at, verdict, lang")
      .eq("race_id", raceId)
      .eq("contestant_id", participant.contestant_id)
      .order("submitted_at", { ascending: true }),
  ]);

  const { events, lang } = buildReplayEvents(snaps, subs ?? [], startMs);

  const solveMs = participant.first_ac_at
    ? new Date(participant.first_ac_at).getTime() - startMs
    : null;

  // Full problem row so the replay can render the statement pane.
  const { data: problemRow } = await db()
    .from("problems")
    .select("*")
    .eq("id", race.problem_id)
    .maybeSingle();

  // Webcam recording for this station, if one was uploaded.
  const { data: rec } = await db()
    .from("race_recordings")
    .select("path, offset_ms")
    .eq("race_id", raceId)
    .eq("station_role", station)
    .maybeSingle();
  let recordingUrl: string | null = null;
  if (rec?.path) {
    const { data: signed } = await db()
      .storage.from("recordings")
      .createSignedUrl(rec.path, 3600);
    recordingUrl = signed?.signedUrl ?? null;
  }

  return NextResponse.json({
    problemId: race.problem_id,
    lang,
    solveMs,
    events,
    contestant: participant.contestant
      ? { name: participant.contestant.name, country: participant.contestant.country }
      : null,
    timerSec: race.timer_sec,
    problem: problemRow ?? null,
    recordingUrl,
    recordingOffsetMs: rec?.offset_ms ?? 0,
  });
}
