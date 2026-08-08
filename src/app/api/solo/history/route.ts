import { NextResponse } from "next/server";
import { db } from "@/lib/db";
import { authUser } from "@/lib/supabase/server";
import type { SoloHistoryEntry, SoloOutcome } from "@/lib/solo";

export const dynamic = "force-dynamic";

/** The signed-in user's solo run history (account-backed replay list). */
export async function GET() {
  const user = await authUser();
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const { data, error } = await db()
    .from("sessions")
    .select("id, problem_id, started_at, outcome, solve_ms")
    .eq("kind", "solo")
    .eq("user_id", user.id)
    .order("started_at", { ascending: false })
    .limit(500);
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });

  const entries: SoloHistoryEntry[] = (data ?? []).map((s) => ({
    sessionId: s.id,
    problemId: s.problem_id,
    startedAt: new Date(s.started_at).getTime(),
    outcome: (s.outcome ?? "pending") as SoloOutcome,
    solveMs: s.solve_ms,
  }));
  return NextResponse.json({ entries });
}
