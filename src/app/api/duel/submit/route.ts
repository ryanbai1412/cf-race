import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { authUser } from "@/lib/supabase/server";
import { judgeConfigured, judgeSubmit } from "@/lib/judge";
import {
  MAX_SUBMISSIONS,
  SUBMIT_GRACE_MS,
  matchEndMs,
  resolveMatch,
  type DuelMatchRow,
} from "@/lib/duel";

export const maxDuration = 120;

/**
 * Official submission during a duel: full-test judging. Time windows (total
 * cutoff + grace after first AC), the 10-submission cap, and match state are
 * all enforced server-side. First AC stamps the match winner; a grace-window
 * AC still counts as solved for the other player.
 */
export async function POST(req: NextRequest) {
  const user = await authUser();
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

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
    .from("sessions")
    .select("*")
    .eq("id", sessionId)
    .eq("kind", "duel")
    .maybeSingle();
  if (!session) {
    return NextResponse.json({ error: "unknown session" }, { status: 400 });
  }
  if (session.user_id !== user.id) {
    return NextResponse.json({ error: "not your session" }, { status: 403 });
  }
  if (session.outcome === "solved") {
    return NextResponse.json({ error: "already solved" }, { status: 400 });
  }

  const { data: player } = await db()
    .from("duel_players")
    .select("match_id")
    .eq("session_id", sessionId)
    .maybeSingle();
  if (!player) {
    return NextResponse.json({ error: "no match for session" }, { status: 400 });
  }
  const { data: match } = await db()
    .from("duel_matches")
    .select("*")
    .eq("id", player.match_id)
    .maybeSingle<DuelMatchRow>();
  if (!match) return NextResponse.json({ error: "unknown match" }, { status: 400 });

  const now = Date.now();
  const startMs = new Date(match.started_at).getTime();
  if (match.finished_at || now > matchEndMs(match) + SUBMIT_GRACE_MS) {
    return NextResponse.json({ error: "match is over" }, { status: 400 });
  }
  if (now < startMs) {
    return NextResponse.json({ error: "match has not started" }, { status: 400 });
  }

  const { count } = await db()
    .from("session_submissions")
    .select("id", { count: "exact", head: true })
    .eq("session_id", sessionId)
    .eq("kind", "submit");
  if ((count ?? 0) >= MAX_SUBMISSIONS) {
    return NextResponse.json({ error: "submission limit reached" }, { status: 400 });
  }

  const submittedAt = new Date().toISOString();
  const { data: sub, error } = await db()
    .from("session_submissions")
    .insert({
      session_id: sessionId,
      kind: "submit",
      lang,
      source,
      verdict: "PENDING",
      submitted_at: submittedAt,
    })
    .select("id")
    .single();
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });

  await db().from("session_events").insert({
    session_id: sessionId,
    t_ms: Math.max(0, new Date(submittedAt).getTime() - startMs),
    lang,
    kind: "submit",
    payload: { submissionId: sub.id },
  });

  try {
    const result = await judgeSubmit({
      submissionId: sub.id,
      lang,
      source,
      problemId: session.problem_id,
    });
    await db()
      .from("session_submissions")
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
    await db().from("session_events").insert({
      session_id: sessionId,
      t_ms: Math.max(0, Date.now() - startMs),
      lang,
      kind: "verdict",
      payload: { submissionId: sub.id, verdict: result.verdict },
    });

    let solveMs: number | null = null;
    if (result.verdict === "AC") {
      solveMs = Math.max(0, new Date(submittedAt).getTime() - startMs);
      await db()
        .from("sessions")
        .update({ outcome: "solved", solve_ms: solveMs, lang })
        .eq("id", sessionId)
        .is("solve_ms", null);
      // First AC wins: stamp the winner + start the grace window once.
      await db()
        .from("duel_matches")
        .update({
          first_ac_at: submittedAt,
          winner_user_id: user.id,
        })
        .eq("id", match.id)
        .is("first_ac_at", null);
      await resolveMatch(match.room_id);
    }
    return NextResponse.json({ ...result, submissionId: sub.id, solveMs });
  } catch (e) {
    // The attempt never got a verdict, so drop it instead of leaving a
    // permanently PENDING row that also eats one of the 10 submissions.
    await db().from("session_submissions").delete().eq("id", sub.id);
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
