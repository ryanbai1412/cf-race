import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireAdmin } from "@/lib/admin-api";

/** Set, replace, or remove a problem's Genna reference session. */
export async function POST(req: NextRequest) {
  const gate = await requireAdmin();
  if (!gate.ok) return gate.response;

  const body = (await req.json().catch(() => ({}))) as {
    problemId?: string;
    sessionId?: string;
    remove?: boolean;
  };
  const problemId = typeof body.problemId === "string" ? body.problemId : "";
  if (!problemId) {
    return NextResponse.json({ error: "problemId required" }, { status: 400 });
  }

  if (body.remove) {
    const { error } = await db()
      .from("genna_problems")
      .delete()
      .eq("problem_id", problemId);
    if (error) return NextResponse.json({ error: error.message }, { status: 500 });
    return NextResponse.json({ ok: true });
  }

  const sessionId = typeof body.sessionId === "string" ? body.sessionId : "";
  if (!sessionId) {
    return NextResponse.json({ error: "sessionId required" }, { status: 400 });
  }

  const { data: session } = await db()
    .from("sessions")
    .select("id, problem_id, outcome, solve_ms")
    .eq("id", sessionId)
    .maybeSingle();
  if (!session || session.problem_id !== problemId) {
    return NextResponse.json({ error: "session/problem mismatch" }, { status: 400 });
  }
  if (session.outcome !== "solved" || session.solve_ms === null) {
    return NextResponse.json({ error: "session is not a solve" }, { status: 400 });
  }
  const { count } = await db()
    .from("session_events")
    .select("id", { count: "exact", head: true })
    .eq("session_id", sessionId);
  if (!count) {
    return NextResponse.json({ error: "session has no replay events" }, { status: 400 });
  }

  const { error } = await db()
    .from("genna_problems")
    .upsert({ problem_id: problemId, session_id: sessionId });
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ ok: true });
}
