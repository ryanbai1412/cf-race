import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { judgeConfigured, judgeSubmit } from "@/lib/judge";

export const maxDuration = 120;
const MAX_SUBMISSIONS = 10;

/** Official submission during a solo run: full-test judging, AC ends the run. */
export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  const sessionId = typeof body?.sessionId === "string" ? body.sessionId : "";
  const lang = body?.lang === "cpp" || body?.lang === "py" ? body.lang : null;
  const source = typeof body?.source === "string" ? body.source : "";

  if (!sessionId || !lang || !source || source.length > 200_000) {
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

  const { count } = await db()
    .from("solo_submissions")
    .select("id", { count: "exact", head: true })
    .eq("session_id", sessionId);
  if ((count ?? 0) >= MAX_SUBMISSIONS) {
    return NextResponse.json({ error: "submission limit reached" }, { status: 400 });
  }

  const submittedAt = new Date().toISOString();
  const { data: sub, error } = await db()
    .from("solo_submissions")
    .insert({
      session_id: sessionId,
      lang,
      source,
      verdict: "PENDING",
      submitted_at: submittedAt,
    })
    .select("id")
    .single();
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });

  try {
    const result = await judgeSubmit({
      submissionId: sub.id,
      lang,
      source,
      problemId: session.problem_id,
    });
    await db()
      .from("solo_submissions")
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

    let solveMs: number | null = null;
    if (result.verdict === "AC") {
      solveMs = new Date(submittedAt).getTime() - startMs;
      await db()
        .from("solo_sessions")
        .update({ outcome: "solved", solve_ms: solveMs, lang })
        .eq("id", sessionId)
        .is("solve_ms", null);
    }
    return NextResponse.json({ ...result, submissionId: sub.id, solveMs });
  } catch (e) {
    await db()
      .from("solo_submissions")
      .update({ verdict: null, details: { error: "judge failed" } })
      .eq("id", sub.id);
    return NextResponse.json(
      { error: e instanceof Error ? e.message : "judge error" },
      { status: 502 }
    );
  }
}
