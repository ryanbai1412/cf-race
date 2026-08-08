import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
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

  const { data: session } = await db()
    .from("solo_sessions")
    .select("*")
    .eq("id", sessionId)
    .maybeSingle();
  if (!session) {
    return NextResponse.json({ error: "unknown session" }, { status: 400 });
  }
  if (session.outcome === "solved") {
    return NextResponse.json({ error: "already solved" }, { status: 400 });
  }

  // Enforce the solo timer server-side (small grace for latency).
  const startMs = new Date(session.started_at).getTime();
  if (Date.now() > startMs + session.timer_sec * 1000 + 3000) {
    return NextResponse.json({ error: "time is up" }, { status: 400 });
  }

  if (await submissionLimitReached("solo_submissions", { session_id: sessionId })) {
    return NextResponse.json({ error: "submission limit reached" }, { status: 400 });
  }

  const submittedAt = new Date().toISOString();
  const judged = await judgeOfficialSubmission({
    table: "solo_submissions",
    insertRow: { session_id: sessionId, submitted_at: submittedAt },
    lang,
    source,
    problemId: session.problem_id,
  });
  if (!judged.ok) return judged.response;

  let solveMs: number | null = null;
  if (judged.result.verdict === "AC") {
    solveMs = Math.max(0, new Date(submittedAt).getTime() - startMs);
    await db()
      .from("solo_sessions")
      .update({ outcome: "solved", solve_ms: solveMs, lang })
      .eq("id", sessionId)
      .is("solve_ms", null);
  }
  return NextResponse.json({ ...judged.result, submissionId: judged.submissionId, solveMs });
}
