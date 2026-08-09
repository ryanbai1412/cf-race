import { db } from "./db";
import { invalidatedProblemIds } from "./duel";

export type BankProblem = {
  id: string;
  name: string;
  rating: number | null;
  tags: string[];
  tourist_time_ms: number | null;
};

/** Problems shown in the bank: hidden-tagged and the warmup are excluded. */
export async function visibleProblems(): Promise<BankProblem[]> {
  const { data } = await db()
    .from("problems")
    .select("id, name, rating, tags, tourist_time_ms")
    .neq("id", "warmup-sum")
    .order("id", { ascending: true });
  return ((data ?? []) as BankProblem[]).filter(
    (p) => !(p.tags ?? []).includes("hidden")
  );
}

/**
 * Random practice pick: a non-hidden, non-invalidated problem the user
 * hasn't solved yet (falls back to any eligible problem).
 */
export async function pickPracticeProblem(
  userId?: string | null
): Promise<string | null> {
  const [problems, invalidated] = await Promise.all([
    visibleProblems(),
    invalidatedProblemIds(),
  ]);
  let eligible = problems.filter((p) => !invalidated.has(p.id));

  if (userId) {
    const { data: solved } = await db()
      .from("sessions")
      .select("problem_id")
      .eq("user_id", userId)
      .eq("outcome", "solved");
    const solvedIds = new Set((solved ?? []).map((s) => s.problem_id));
    const unsolved = eligible.filter((p) => !solvedIds.has(p.id));
    if (unsolved.length > 0) eligible = unsolved;
  }

  if (eligible.length === 0) return null;
  return eligible[Math.floor(Math.random() * eligible.length)].id;
}
