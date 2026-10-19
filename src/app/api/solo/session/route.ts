import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { getEffectiveUser } from "@/lib/impersonation";
import {
  anonSessionIds,
  ensureBrowserId,
  rememberAnonSession,
} from "@/lib/anon-sessions";
import { abandonActiveSessions } from "@/lib/session-lifecycle";
import { rateLimit } from "@/lib/rate-limit";
import { DEFAULT_SOLO_TIMER, isSoloTimer } from "@/lib/problem-rating";
import { invalidatedProblemIds } from "@/lib/duel";

export const dynamic = "force-dynamic";

// 3-2-1 plus a "GO!" beat; the race clock starts when the overlay clears.
const COUNTDOWN_MS = 4000;

/** Start a solo practice run: creates a sessions row (kind solo) with GO after the countdown. */
export async function POST(req: NextRequest) {
  const limited = rateLimit(req, { name: "solo-session", limit: 60 });
  if (limited) return limited;

  const body = await req.json().catch(() => null);
  const problemId = typeof body?.problemId === "string" ? body.problemId : "";
  const timerSec = body?.timerSec === undefined ? DEFAULT_SOLO_TIMER : body.timerSec;
  if (!problemId || !isSoloTimer(timerSec)) {
    return NextResponse.json({ error: "invalid request" }, { status: 400 });
  }

  const { data: problem } = await db()
    .from("problems")
    .select("id, tags")
    .eq("id", problemId)
    .maybeSingle();
  if (!problem || (problem.tags ?? []).includes("hidden")) return NextResponse.json({ error: "unknown problem" }, { status: 400 });

  const user = await getEffectiveUser();
  if ((await invalidatedProblemIds([user?.id])).has(problemId)) {
    return NextResponse.json({ error: "This problem is invalidated. Choose another." }, { status: 409 });
  }
  // A new run of the same problem supersedes any still-active one.
  await abandonActiveSessions({
    problemId,
    userId: user?.id ?? null,
    sessionIds: user ? undefined : anonSessionIds(),
  });
  const startAtMs = Date.now() + COUNTDOWN_MS;
  const { data: session, error } = await db()
    .from("sessions")
    .insert({
      kind: "solo",
      problem_id: problemId,
      started_at: new Date(startAtMs).toISOString(),
      timer_sec: timerSec,
      user_id: user?.id ?? null,
      browser_id: user ? null : ensureBrowserId(),
    })
    .select("id")
    .single();
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });

  if (!user) rememberAnonSession(session.id);

  return NextResponse.json({
    sessionId: session.id,
    startAtMs,
    timerSec,
    serverNow: Date.now(),
  });
}
