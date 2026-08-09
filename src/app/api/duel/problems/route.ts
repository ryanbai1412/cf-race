import { NextResponse } from "next/server";
import { db } from "@/lib/db";
import { getEffectiveUser } from "@/lib/impersonation";

export const dynamic = "force-dynamic";

/**
 * Problem bank data for /duel/problems: every problem with solved-by-you /
 * solved-by-anyone flags and the active invalidation (if any).
 */
export async function GET() {
  const user = await getEffectiveUser();
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const [{ data: problems }, { data: solved }, { data: invalidations }] =
    await Promise.all([
      db()
        .from("problems")
        .select("id, name, rating, tourist_time_ms")
        .neq("id", "warmup-sum")
        .order("id", { ascending: true }),
      db()
        .from("sessions")
        .select("problem_id, user_id, solve_ms")
        .eq("outcome", "solved"),
      db()
        .from("problem_invalidations")
        .select("problem_id, reason, created_at")
        .is("revoked_at", null),
    ]);

  const solvedByYou = new Map<string, number | null>();
  const solvedByAnyone = new Set<string>();
  for (const s of solved ?? []) {
    solvedByAnyone.add(s.problem_id);
    if (s.user_id === user.id) {
      const prev = solvedByYou.get(s.problem_id);
      if (prev === undefined || (s.solve_ms ?? Infinity) < (prev ?? Infinity)) {
        solvedByYou.set(s.problem_id, s.solve_ms);
      }
    }
  }
  const invalidatedBy = new Map(
    (invalidations ?? []).map((i) => [i.problem_id, i.reason as string | null])
  );

  return NextResponse.json({
    problems: (problems ?? []).map((p) => ({
      id: p.id,
      name: p.name,
      rating: p.rating,
      touristTimeMs: p.tourist_time_ms,
      solvedByYouMs: solvedByYou.has(p.id) ? (solvedByYou.get(p.id) ?? null) : undefined,
      solvedByAnyone: solvedByAnyone.has(p.id),
      invalidated: invalidatedBy.has(p.id),
      invalidReason: invalidatedBy.get(p.id) ?? null,
    })),
  });
}
