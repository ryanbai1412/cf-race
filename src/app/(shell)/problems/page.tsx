import { redirect } from "next/navigation";
import { getEffectiveUser } from "@/lib/impersonation";
import { db } from "@/lib/db";
import { invalidatedProblemIds } from "@/lib/duel";
import { visibleProblems } from "@/lib/problem-bank";
import { sweepStaleSessions } from "@/lib/session-lifecycle";
import {
  ProblemsTable,
  type ProblemBankRow,
  type ProblemStatus,
} from "@/components/problems/problems-table";
import { PageHeader, PageShell } from "@/components/shell/page";

export const dynamic = "force-dynamic";

export default async function ProblemsPage() {
  const user = await getEffectiveUser();
  if (!user) redirect("/?next=/problems");

  const [problems, invalidated, { data: sessions }, { data: myRatings }] =
    await Promise.all([
      visibleProblems(),
      invalidatedProblemIds(),
      sweepStaleSessions({ userId: user.id }).then(() =>
        db()
          .from("sessions")
          .select("problem_id, outcome, solve_ms")
          .eq("user_id", user.id)
      ),
      db()
        .from("problem_ratings")
        .select("problem_id, stars")
        .eq("user_id", user.id),
    ]);
  const starsByProblem = new Map(
    (myRatings ?? []).map((r) => [r.problem_id as string, r.stars as number])
  );

  const byProblem = new Map<
    string,
    { best: number | null; attempted: boolean; count: number }
  >();
  for (const s of sessions ?? []) {
    const cur = byProblem.get(s.problem_id) ?? {
      best: null,
      attempted: false,
      count: 0,
    };
    cur.count += 1;
    if (s.outcome === "solved") {
      cur.best =
        cur.best === null
          ? s.solve_ms
          : Math.min(cur.best, s.solve_ms ?? Infinity);
    } else {
      cur.attempted = true;
    }
    byProblem.set(s.problem_id, cur);
  }

  const rows: ProblemBankRow[] = problems.map((p) => {
    const mine = byProblem.get(p.id);
    const status: ProblemStatus = invalidated.has(p.id)
      ? "invalidated"
      : mine?.best != null
        ? "solved"
        : mine?.attempted
          ? "attempted"
          : "unsolved";
    return {
      id: p.id,
      name: p.name,
      rating: p.rating,
      tags: p.tags ?? [],
      touristTimeMs: p.tourist_time_ms,
      status,
      bestSolveMs: mine?.best ?? null,
      sessionCount: mine?.count ?? 0,
      myStars: starsByProblem.get(p.id) ?? null,
    };
  });

  return (
    <PageShell>
      <PageHeader
        eyebrow="Problem bank"
        title="Problems"
        description="The bank — every run is timed and recorded."
      />
      <ProblemsTable problems={rows} />
    </PageShell>
  );
}
