import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/event-auth";
import { judgeConfigured } from "@/lib/judge";
import { MAX_SOURCE_LEN } from "@/lib/limits";
import { notifyEvent } from "@/lib/notify";
import {
  judgeOfficialSubmission,
  submissionLimitReached,
} from "@/lib/submission-route";

export const maxDuration = 120;

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

  const { data: race } = await db()
    .from("races")
    .select("*, participants:race_participants(*)")
    .eq("id", raceId)
    .eq("event_id", eventId)
    .maybeSingle();
  if (!race || race.state === "finished") {
    return NextResponse.json({ error: "race is not active" }, { status: 400 });
  }
  const participant = race.participants.find(
    (p: { contestant_id: string }) => p.contestant_id === contestantId
  );
  if (!participant) {
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

  if (
    await submissionLimitReached("submissions", {
      race_id: raceId,
      contestant_id: contestantId,
    })
  ) {
    return NextResponse.json({ error: "submission limit reached" }, { status: 400 });
  }

  const submittedAt = new Date().toISOString();
  await notifyEvent(eventId, { type: "state_changed" });
  const judged = await judgeOfficialSubmission({
    table: "submissions",
    insertRow: {
      race_id: raceId,
      contestant_id: contestantId,
      submitted_at: submittedAt,
    },
    lang,
    source,
    problemId: race.problem_id,
  });
  if (!judged.ok) {
    await notifyEvent(eventId, { type: "state_changed" });
    return judged.response;
  }

  if (judged.result.verdict === "AC" && !participant.first_ac_at) {
    await db()
      .from("race_participants")
      .update({ first_ac_at: submittedAt })
      .eq("race_id", raceId)
      .eq("contestant_id", contestantId)
      .is("first_ac_at", null);
    await notifyEvent(eventId, {
      type: "confetti",
      station: participant.station_role,
    });
  }
  await notifyEvent(eventId, { type: "state_changed" });
  return NextResponse.json({ ...judged.result, submissionId: judged.submissionId });
}
