import { unstable_cache } from "next/cache";
import { db } from "./db";
import { invalidatedProblemIds } from "./duel";
import { DEFAULT_PROBLEM_RATING, type ProblemRating } from "./problem-rating";

export type BankProblem = {
  id: string;
  name: string;
  rating: number | null;
  tags: string[];
  tourist_time_ms: number | null;
};

/**
 * Problems shown in the bank: hidden-tagged and the warmup are excluded.
 * Cached across requests (the bank is global, not user-scoped) — changes
 * from `pnpm seed` show up within a minute.
 */
export const visibleProblems = unstable_cache(
  async (): Promise<BankProblem[]> => {
    const { data, error } = await db()
      .from("problems")
      .select("id, name, rating, tags, tourist_time_ms")
      .neq("id", "warmup-sum")
      .order("id", { ascending: true });
    if (error) throw new Error("Could not load the problem bank");
    return ((data ?? []) as BankProblem[]).filter(
      (p) => !(p.tags ?? []).includes("hidden")
    );
  },
  ["visible-problems"],
  { revalidate: 60, tags: ["problems"] }
);

/**
 * Random practice pick: a non-hidden problem the user hasn't solved or
 * invalidated yet (falls back to any eligible problem).
 */
export async function pickPracticeProblem(
  userId?: string | null,
  exclude?: ReadonlySet<string>,
  rating: ProblemRating = DEFAULT_PROBLEM_RATING
): Promise<string | null> {
  const [problems, invalidated] = await Promise.all([
    visibleProblems(),
    invalidatedProblemIds([userId]),
  ]);
  let eligible = problems.filter(
    (p) => p.rating === rating && !invalidated.has(p.id) && !exclude?.has(p.id)
  );

  if (userId) {
    const { data: solved, error } = await db()
      .from("sessions")
      .select("problem_id")
      .eq("user_id", userId)
      .eq("outcome", "solved");
    if (error) throw new Error("Could not load solved problems");
    const solvedIds = new Set((solved ?? []).map((s) => s.problem_id));
    const unsolved = eligible.filter((p) => !solvedIds.has(p.id));
    if (unsolved.length > 0) eligible = unsolved;
  }

  if (eligible.length === 0) return null;
  return eligible[Math.floor(Math.random() * eligible.length)].id;
}
