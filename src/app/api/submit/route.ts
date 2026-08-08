import { NextRequest, NextResponse } from "next/server";
import { db, logDbError } from "@/lib/db";
import { requireEvent } from "@/lib/event-auth";
import { judgeConfigured } from "@/lib/judge";
import { MAX_SOURCE_LEN } from "@/lib/limits";
import { notifyEvent } from "@/lib/notify";
import { raceWithParticipants } from "@/lib/races";
import {
  judgeOfficialSubmission,
  submissionLimitReached,
} from "@/lib/submission-route";

export const maxDuration = 120;

/** Official submission during an event race: full-test judging, first AC wins. */
export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  const eventId = typeof body?.eventId === "string" ? body.eventId : "";
  const raceId = typeof body?.raceId === "string" ? body.raceId : "";
  const contestantId = typeof body?.contestantId === "string" ? body.contestantId : "";
  const lang = body?.lang === "cpp" || body?.lang === "py" ? body.lang : null;
  const source = typeof body?.source === "string" ? body.source : "";

  const event = await requireEvent(eventId);
  if (!event || !raceId || !contestantId || !lang || !source || source.length > MAX_SOURCE_LEN) {
    return NextResponse.json({ error: "invalid request" }, { status: 400 });
  }
  if (!judgeConfigured()) {
    return NextResponse.json(
      { error: "Judge service is not configured yet" },
      { status: 503 }
    );
  }

  const found = await raceWithParticipants(eventId, raceId);
  if (!found || found.race.state === "finished") {
    return NextResponse.json({ error: "race is not active" }, { status: 400 });
  }
  const { race, participants } = found;
  const participant = participants.find((p) => p.contestant_id === contestantId);
  if (!participant || !participant.session_id) {
    return NextResponse.json({ error: "not a participant" }, { status: 403 });
  }
  if (participant.first_ac_at) {
    return NextResponse.json({ error: "already solved" }, { status: 400 });
  }

  // Enforce race timer server-side (small grace for latency).
  if (race.started_at) {
    const endMs = new Date(race.started_at).getTime() + race.timer_sec * 1000 + 3000;
    if (Date.now() > endMs) {
      return NextResponse.json({ error: "time is up" }, { status: 400 });
    }
  }

  const sessionId = participant.session_id;
  if (
    await submissionLimitReached("session_submissions", {
      session_id: sessionId,
      kind: "submit",
    })
  ) {
    return NextResponse.json({ error: "submission limit reached" }, { status: 400 });
  }

  const submittedAt = new Date().toISOString();
  await notifyEvent(eventId, { type: "state_changed" });
  const judged = await judgeOfficialSubmission({
    table: "session_submissions",
    insertRow: { session_id: sessionId, kind: "submit", submitted_at: submittedAt },
    lang,
    source,
    problemId: race.problem_id,
  });
  if (!judged.ok) {
    await notifyEvent(eventId, { type: "state_changed" });
    return judged.response;
  }

  // Submit + verdict moments become part of the single playback stream.
  const startMs = race.started_at ? new Date(race.started_at).getTime() : Date.now();
  const { error: markerErr } = await db().from("session_events").insert([
    {
      session_id: sessionId,
      t_ms: Math.max(0, new Date(submittedAt).getTime() - startMs),
      lang,
      kind: "submit",
      payload: { submissionId: judged.submissionId },
    },
    {
      session_id: sessionId,
      t_ms: Math.max(0, Date.now() - startMs),
      lang,
      kind: "verdict",
      payload: { submissionId: judged.submissionId, verdict: judged.result.verdict },
    },
  ]);
  logDbError(`event submit: replay markers ${sessionId}`, markerErr);

  if (judged.result.verdict === "AC" && !participant.first_ac_at) {
    const solveMs = Math.max(0, new Date(submittedAt).getTime() - startMs);
    // Single transaction: participant first-AC + session solved stamp.
    const { data: stamped, error: acErr } = await db().rpc("record_event_ac", {
      p_session_id: sessionId,
      p_race_id: raceId,
      p_contestant_id: contestantId,
      p_submitted_at: submittedAt,
      p_solve_ms: solveMs,
      p_lang: lang,
    });
    logDbError(`event submit: record_event_ac ${raceId}/${contestantId}`, acErr);
    if (stamped === true) {
      await notifyEvent(eventId, {
        type: "confetti",
        station: participant.station_role,
      });
    }
  }
  await notifyEvent(eventId, { type: "state_changed" });
  return NextResponse.json({ ...judged.result, submissionId: judged.submissionId });
}
