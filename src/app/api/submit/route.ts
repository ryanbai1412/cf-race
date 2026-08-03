import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/api-auth";
import { judgeConfigured, judgeSubmit } from "@/lib/judge";
import { notifyEvent } from "@/lib/notify";

export const maxDuration = 120;
const MAX_SUBMISSIONS = 10;

export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  const eventId = typeof body?.eventId === "string" ? body.eventId : "";
  const raceId = typeof body?.raceId === "string" ? body.raceId : "";
  const contestantId = typeof body?.contestantId === "string" ? body.contestantId : "";
  const lang = body?.lang === "cpp" || body?.lang === "py" ? body.lang : null;
  const source = typeof body?.source === "string" ? body.source : "";

  const event = await requireEvent(eventId);
  if (!event || !raceId || !contestantId || !lang || !source || source.length > 200_000) {
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

  const { count } = await db()
    .from("submissions")
    .select("id", { count: "exact", head: true })
    .eq("race_id", raceId)
    .eq("contestant_id", contestantId);
  if ((count ?? 0) >= MAX_SUBMISSIONS) {
    return NextResponse.json({ error: "submission limit reached" }, { status: 400 });
  }

  const submittedAt = new Date().toISOString();
  const { data: sub, error } = await db()
    .from("submissions")
    .insert({
      race_id: raceId,
      contestant_id: contestantId,
      lang,
      source,
      verdict: "PENDING",
      submitted_at: submittedAt,
    })
    .select("id")
    .single();
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });

  await notifyEvent(eventId, { type: "state_changed" });

  try {
    const result = await judgeSubmit({
      submissionId: sub.id,
      lang,
      source,
      problemId: race.problem_id,
    });
    await db()
      .from("submissions")
      .update({
        verdict: result.verdict,
        judged_at: new Date().toISOString(),
        details: {
          failedTest: result.failedTest,
          passedCount: result.passedCount,
          totalCount: result.totalCount,
          timeMsMax: result.timeMsMax,
          compileError: result.compileError,
        },
      })
      .eq("id", sub.id);

    if (result.verdict === "AC" && !participant.first_ac_at) {
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
    return NextResponse.json({ ...result, submissionId: sub.id });
  } catch (e) {
    // The attempt never got a verdict, so drop it instead of leaving a
    // permanently PENDING row that also eats one of the 10 submissions.
    await db().from("submissions").delete().eq("id", sub.id);
    await notifyEvent(eventId, { type: "state_changed" });
    return NextResponse.json(
      {
        error: `Judge unavailable, submission not counted (${
          e instanceof Error ? e.message : "judge error"
        })`,
      },
      { status: 502 }
    );
  }
}
