import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { authUser } from "@/lib/supabase/server";

export const dynamic = "force-dynamic";

const COUNTDOWN_MS = 3000;
const TIMER_SEC = 180;

/** Start a solo practice run: creates a sessions row (kind solo) with GO at now+3s. */
export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  const problemId = typeof body?.problemId === "string" ? body.problemId : "";
  if (!problemId) {
    return NextResponse.json({ error: "invalid request" }, { status: 400 });
  }

  const { data: problem } = await db()
    .from("problems")
    .select("id")
    .eq("id", problemId)
    .maybeSingle();
  if (!problem) return NextResponse.json({ error: "unknown problem" }, { status: 400 });

  const user = await authUser();
  const startAtMs = Date.now() + COUNTDOWN_MS;
  const { data: session, error } = await db()
    .from("sessions")
    .insert({
      kind: "solo",
      problem_id: problemId,
      started_at: new Date(startAtMs).toISOString(),
      timer_sec: TIMER_SEC,
      user_id: user?.id ?? null,
    })
    .select("id")
    .single();
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });

  return NextResponse.json({
    sessionId: session.id,
    startAtMs,
    timerSec: TIMER_SEC,
    serverNow: Date.now(),
  });
}
