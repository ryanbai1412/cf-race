import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/api-auth";
import { fetchEditorEventRows } from "@/lib/editor-events";
import type { Lang } from "@/lib/types";
import type { EditorDeltaChange, RunSummary, TouristEvent } from "@/lib/tourist";

export const dynamic = "force-dynamic";

/** Persist a batch of editor snapshots recorded during a race. */
export async function POST(req: NextRequest) {
  const body = (await req.json()) as {
    eventId?: string;
    raceId?: string;
    station?: string;
    events?: {
      t: number;
      code: string;
      lang: Lang;
      kind?: string;
      payload?: unknown;
    }[];
  };
  const event = await requireEvent(body.eventId ?? "");
  if (!event) return NextResponse.json({ error: "unauthorized" }, { status: 401 });
  if (
    !body.raceId ||
    (body.station !== "station1" && body.station !== "station2") ||
    !Array.isArray(body.events) ||
    body.events.length === 0
  ) {
    return NextResponse.json({ error: "bad request" }, { status: 400 });
  }

  const kinds = new Set(["snapshot", "delta", "run", "run_result", "tab", "scroll"]);
  const rows = body.events.slice(0, 1000).map((e) => ({
    race_id: body.raceId,
    station_role: body.station,
    t_ms: Math.max(0, Math.round(e.t)),
    code: String(e.code).slice(0, 100_000),
    lang: e.lang === "py" ? "py" : "cpp",
    kind: e.kind && kinds.has(e.kind) ? e.kind : "snapshot",
    payload:
      e.payload && JSON.stringify(e.payload).length <= 20_000 ? e.payload : null,
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

  const events: TouristEvent[] = [];
  for (const s of snaps) {
    if (s.kind === "run") events.push({ t: s.t_ms, type: "run" });
    else if (s.kind === "run_result" && s.payload)
      events.push({ t: s.t_ms, type: "run_result", result: s.payload as RunSummary });
    else if (s.kind === "tab" && s.payload)
      events.push({ t: s.t_ms, type: "tab", tab: (s.payload as { tab: string }).tab });
    else if (s.kind === "scroll" && s.payload)
      events.push({
        t: s.t_ms,
        type: "scroll",
        frac: (s.payload as { frac: number }).frac,
      });
    else if (s.kind === "delta" && s.payload)
      events.push({
        t: s.t_ms,
        type: "delta",
        lang: s.lang === "py" ? "py" : "cpp",
        changes: (s.payload as { changes: EditorDeltaChange[] }).changes,
      });
    else if (
      s.kind === "run_result" ||
      s.kind === "tab" ||
      s.kind === "scroll" ||
      s.kind === "delta"
    )
      continue;
    else
      events.push({
        t: s.t_ms,
        type: "snapshot",
        code: s.code,
        lang: s.lang === "py" ? "py" : "cpp",
      });
  }
  let lang: Lang = "cpp";
  for (const s of subs ?? []) {
    events.push({ t: new Date(s.submitted_at).getTime() - startMs, type: "submit" });
    if (s.verdict) {
      events.push({
        t: new Date(s.judged_at ?? s.submitted_at).getTime() - startMs,
        type: "verdict",
        verdict: s.verdict,
      });
    }
    lang = s.lang === "py" ? "py" : "cpp";
  }
  events.sort((a, b) => a.t - b.t);
  const codeSnaps = snaps.filter(
    (s) => s.kind === "snapshot" || s.kind === "delta"
  );
  if (codeSnaps.length > 0) lang = codeSnaps[codeSnaps.length - 1].lang as Lang;

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
