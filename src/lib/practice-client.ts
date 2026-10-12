import type { ProblemRating } from "./problem-rating";

export async function requestPracticeProblem(rating: ProblemRating, exclude: string[] = []): Promise<string> {
  const res = await fetch("/api/solo/problem", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ rating, exclude }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error ?? "Could not pick a problem. Try again.");
  return data.problemId;
}
