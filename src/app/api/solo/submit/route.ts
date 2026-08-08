import { NextRequest, NextResponse } from "next/server";
import { db, logDbError } from "@/lib/db";
import { requireSessionAccess } from "@/lib/session-auth";
import { judgeConfigured } from "@/lib/judge";
import { MAX_SOURCE_LEN } from "@/lib/limits";
import {
  judgeOfficialSubmission,
  submissionLimitReached,
} from "@/lib/submission-route";

export const maxDuration = 120;

/** Official submission during a solo run: full-test judging, AC ends the run. */
export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  const sessionId = typeof body?.sessionId === "string" ? body.sessionId : "";
  const lang = body?.lang === "cpp" || body?.lang === "py" ? body.lang : null;
  const source = typeof body?.source === "string" ? body.source : "";

  if (!sessionId || !lang || !source || source.length > MAX_SOURCE_LEN) {
    return NextResponse.json({ error: "invalid request" }, { status: 400 });
  }
  if (!judgeConfigured()) {
    return NextResponse.json(
      { error: "Judge service is not configured yet" },
      { status: 503 }
    );
  }

  const access = await requireSessionAccess(sessionId);
  if (!access.ok) return access.response;
  const session = access.session;
  if (session.kind !== "solo") {
    return NextResponse.json({ error: "unknown session" }, { status: 404 });
  }
  if (session.outcome === "solved") {
    return NextResponse.json({ error: "already solved" }, { status: 400 });
  }

  // Enforce the solo timer server-side (small grace for latency).
  const startMs = new Date(session.started_at).getTime();
  if (
    session.timer_sec !== null &&
    Date.now() > startMs + session.timer_sec * 1000 + 3000
  ) {
    return NextResponse.json({ error: "time is up" }, { status: 400 });
  }

  if (
    await submissionLimitReached("session_submissions", {
      session_id: sessionId,
      kind: "submit",
    })
  ) {
    return NextResponse.json({ error: "submission limit reached" }, { status: 400 });
  }

  const submittedAt = new Date().toISOString();
  const judged = await judgeOfficialSubmission({
    table: "session_submissions",
    insertRow: { session_id: sessionId, kind: "submit", submitted_at: submittedAt },
    lang,
    source,
    problemId: session.problem_id,
  });
  if (!judged.ok) return judged.response;

  // Submit + verdict moments become part of the single playback stream.
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
  logDbError(`solo submit: replay markers ${sessionId}`, markerErr);

  let solveMs: number | null = null;
  if (judged.result.verdict === "AC") {
    solveMs = Math.max(0, new Date(submittedAt).getTime() - startMs);
    const { error: solvedErr } = await db()
      .from("sessions")
      .update({ outcome: "solved", solve_ms: solveMs, lang })
      .eq("id", sessionId)
      .is("solve_ms", null);
    logDbError(`solo submit: solved stamp ${sessionId}`, solvedErr);
  }
  return NextResponse.json({ ...judged.result, submissionId: judged.submissionId, solveMs });
}
