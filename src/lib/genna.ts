import { db } from "./db";

export type GennaReference = {
  problem_id: string;
  session_id: string;
  solve_ms: number | null;
};

/** All Genna reference sessions, keyed by problem id. */
export async function gennaReferences(): Promise<Map<string, GennaReference>> {
  const { data } = await db()
    .from("genna_problems")
    .select("problem_id, session_id, session:sessions(solve_ms)");
  const map = new Map<string, GennaReference>();
  for (const row of data ?? []) {
    const session = row.session as unknown as { solve_ms: number | null } | null;
    map.set(row.problem_id, {
      problem_id: row.problem_id,
      session_id: row.session_id,
      solve_ms: session?.solve_ms ?? null,
    });
  }
  return map;
}

/** The Genna reference for one problem, or null. */
export async function gennaReference(
  problemId: string
): Promise<GennaReference | null> {
  const { data } = await db()
    .from("genna_problems")
    .select("problem_id, session_id, session:sessions(solve_ms)")
    .eq("problem_id", problemId)
    .maybeSingle();
  if (!data) return null;
  const session = data.session as unknown as { solve_ms: number | null } | null;
  return {
    problem_id: data.problem_id,
    session_id: data.session_id,
    solve_ms: session?.solve_ms ?? null,
  };
}
