import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireAdmin } from "@/lib/admin-api";

type Pick = { problemId: string; sessionId: string; solveMs: number };

/**
 * Bulk-set a user's fastest solved session as the Genna reference for every
 * problem they've solved. `dryRun` returns the preview; `overwrite` replaces
 * existing references (otherwise only unreferenced problems are filled).
 */
export async function POST(req: NextRequest) {
  const gate = await requireAdmin();
  if (!gate.ok) return gate.response;

  const body = (await req.json().catch(() => ({}))) as {
    userId?: string;
    overwrite?: boolean;
    dryRun?: boolean;
  };
  const userId = typeof body.userId === "string" ? body.userId : "";
  if (!userId) {
    return NextResponse.json({ error: "userId required" }, { status: 400 });
  }

  const [{ data: sessions, error }, { data: refs }] = await Promise.all([
    db()
      .from("sessions")
      .select("id, problem_id, solve_ms, started_at")
      .eq("user_id", userId)
      .eq("outcome", "solved")
      .not("solve_ms", "is", null),
    db().from("genna_problems").select("problem_id, session_id"),
  ]);
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });

  const referenced = new Map((refs ?? []).map((r) => [r.problem_id, r.session_id]));

  // Fastest solve per problem; ties broken by latest started_at.
  const best = new Map<string, { id: string; solve_ms: number; started_at: string }>();
  for (const s of sessions ?? []) {
    const cur = best.get(s.problem_id);
    if (
      !cur ||
      s.solve_ms! < cur.solve_ms ||
      (s.solve_ms === cur.solve_ms && s.started_at > cur.started_at)
    ) {
      best.set(s.problem_id, {
        id: s.id,
        solve_ms: s.solve_ms!,
        started_at: s.started_at,
      });
    }
  }

  const picks: Pick[] = [];
  for (const [problemId, s] of best) {
    const existing = referenced.get(problemId);
    if (existing === s.id) continue; // already the reference
    if (existing && !body.overwrite) continue;
    picks.push({ problemId, sessionId: s.id, solveMs: s.solve_ms });
  }
  picks.sort((a, b) => a.problemId.localeCompare(b.problemId));

  if (body.dryRun) return NextResponse.json({ picks });

  if (picks.length > 0) {
    const { error: upsertError } = await db()
      .from("genna_problems")
      .upsert(
        picks.map((p) => ({ problem_id: p.problemId, session_id: p.sessionId }))
      );
    if (upsertError) {
      return NextResponse.json({ error: upsertError.message }, { status: 500 });
    }
  }
  return NextResponse.json({ applied: picks.length, picks });
}
