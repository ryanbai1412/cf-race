import { NextRequest, NextResponse } from "next/server";
import { requireEvent } from "@/lib/event-auth";
import { startRace } from "@/lib/races";

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

  const started = await startRace({ eventId, problemId, timerSec });
  if (!started.ok) {
    return NextResponse.json({ error: started.error }, { status: started.status });
  }
  return NextResponse.json({ race: started.race });
}
