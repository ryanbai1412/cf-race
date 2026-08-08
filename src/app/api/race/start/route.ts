import { NextRequest, NextResponse } from "next/server";
import { activeContestants } from "@/lib/contestants";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/event-auth";
import { notifyEvent } from "@/lib/notify";

// 5-4-3-2-1 plus a "GO!" beat; the race clock starts when the overlay clears.
const COUNTDOWN_MS = 6000;

export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  const eventId = typeof body?.eventId === "string" ? body.eventId : "";
  const problemId = typeof body?.problemId === "string" ? body.problemId : "";
  const rawTimerSec = body?.timerSec;
  if (
    rawTimerSec !== undefined &&
    rawTimerSec !== null &&
    !(Number.isInteger(rawTimerSec) && rawTimerSec >= 30 && rawTimerSec <= 3600)
  ) {
    return NextResponse.json(
      { error: "timer must be an integer between 30 and 3600 seconds" },
      { status: 400 }
    );
  }
  const timerSec = typeof rawTimerSec === "number" ? rawTimerSec : null;

  const event = await requireEvent(eventId);
  if (!event || !problemId) {
    return NextResponse.json({ error: "invalid request" }, { status: 400 });
  }

  const { data: problem } = await db()
    .from("problems")
    .select("id, race_timer_sec")
    .eq("id", problemId)
    .maybeSingle();
  if (!problem) return NextResponse.json({ error: "unknown problem" }, { status: 400 });

  // Refuse if a race is already active.
  const { data: existing } = await db()
    .from("races")
    .select("id")
    .eq("event_id", eventId)
    .neq("state", "finished")
    .limit(1);
  if (existing && existing.length > 0) {
    return NextResponse.json({ error: "a race is already active" }, { status: 409 });
  }

  // Active contestants become participants.
  const active = await activeContestants(eventId);
  const participants = Object.values(active);
  if (participants.length === 0) {
    return NextResponse.json({ error: "no contestants checked in" }, { status: 400 });
  }

  const startedAt = new Date(Date.now() + COUNTDOWN_MS).toISOString();
  const { data: race, error } = await db()
    .from("races")
    .insert({
      event_id: eventId,
      problem_id: problemId,
      state: "countdown",
      started_at: startedAt,
      timer_sec: timerSec ?? problem.race_timer_sec,
    })
    .select("*")
    .single();
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });

  const { error: pErr } = await db()
    .from("race_participants")
    .insert(
      participants.map((c) => ({
        race_id: race.id,
        contestant_id: c.id,
        station_role: c.station_role,
      }))
    );
  if (pErr) {
    // Don't leave an active race without participants — it would block
    // future starts and no station would ever join it.
    await db().from("races").delete().eq("id", race.id);
    return NextResponse.json({ error: pErr.message }, { status: 500 });
  }

  await notifyEvent(eventId, { type: "state_changed" });
  return NextResponse.json({ race });
}
