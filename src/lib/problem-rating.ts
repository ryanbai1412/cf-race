export const PROBLEM_RATINGS = [800, 1000, 1200, 1400, 1600] as const;
export type ProblemRating = (typeof PROBLEM_RATINGS)[number];
export const DEFAULT_PROBLEM_RATING: ProblemRating = 800;
export const SOLO_TIMERS = [180, 300, 600, 900, 1800] as const;
export const DEFAULT_SOLO_TIMER = 180;

export function isProblemRating(value: unknown): value is ProblemRating {
  return typeof value === "number" && (PROBLEM_RATINGS as readonly number[]).includes(value);
}

export function isSoloTimer(value: unknown): value is (typeof SOLO_TIMERS)[number] {
  return typeof value === "number" && (SOLO_TIMERS as readonly number[]).includes(value);
}

export function ratingCounts(problems: { rating: number | null }[]): Record<ProblemRating, number> {
  const counts: Record<ProblemRating, number> = { 800: 0, 1000: 0, 1200: 0, 1400: 0, 1600: 0 };
  for (const p of problems) if (isProblemRating(p.rating)) counts[p.rating]++;
  return counts;
}
