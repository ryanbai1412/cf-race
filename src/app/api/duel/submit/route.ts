import { NextRequest, NextResponse } from "next/server";
import { db, logDbError } from "@/lib/db";
import { authUser } from "@/lib/supabase/server";
import { judgeConfigured } from "@/lib/judge";
import { DUEL_MAX_SUBMISSIONS, MAX_SOURCE_LEN } from "@/lib/limits";
import {
  judgeOfficialSubmission,
  submissionLimitReached,
} from "@/lib/submission-route";
import {
  SUBMIT_GRACE_MS,
  matchEndMs,
  resolveMatch,
  type DuelMatchRow,
} from "@/lib/duel";

export const maxDuration = 120;

/**
 * Official submission during a duel: full-test judging. Time windows (total
 * cutoff + grace after first AC), the submission cap, and match state are
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

  if (
    await submissionLimitReached(
      "session_submissions",
      { session_id: sessionId, kind: "submit" },
      DUEL_MAX_SUBMISSIONS
    )
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
  logDbError(`duel submit: replay markers ${sessionId}`, markerErr);

  let solveMs: number | null = null;
  if (judged.result.verdict === "AC") {
    solveMs = Math.max(0, new Date(submittedAt).getTime() - startMs);
    const { error: solvedErr } = await db()
      .from("sessions")
      .update({ outcome: "solved", solve_ms: solveMs, lang })
      .eq("id", sessionId)
      .is("solve_ms", null);
    logDbError(`duel submit: solved stamp ${sessionId}`, solvedErr);
    // First AC wins: stamp the winner + start the grace window once.
    const { error: acErr } = await db()
      .from("duel_matches")
      .update({
        first_ac_at: submittedAt,
        winner_user_id: user.id,
      })
      .eq("id", match.id)
      .is("first_ac_at", null);
    logDbError(`duel submit: first AC ${match.id}`, acErr);
    await resolveMatch(match.room_id);
  }
  return NextResponse.json({
    ...judged.result,
    submissionId: judged.submissionId,
    solveMs,
  });
}
