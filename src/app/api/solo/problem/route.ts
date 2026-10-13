import { NextRequest, NextResponse } from "next/server";
import { getEffectiveUser } from "@/lib/impersonation";
import { pickPracticeProblem } from "@/lib/problem-bank";
import { DEFAULT_PROBLEM_RATING, isProblemRating } from "@/lib/problem-rating";
import { rateLimit } from "@/lib/rate-limit";

export const dynamic = "force-dynamic";

export async function POST(req: NextRequest) {
  const limited = rateLimit(req, { name: "practice-pick", limit: 60 });
  if (limited) return limited;
  const body = await req.json().catch(() => null);
  const rating = body?.rating === undefined ? DEFAULT_PROBLEM_RATING : body.rating;
  const exclude = body?.exclude ?? [];
  if (!isProblemRating(rating) || !Array.isArray(exclude) || exclude.length > 500 ||
    exclude.some((id) => typeof id !== "string" || id.length > 100)) {
    return NextResponse.json({ error: "Invalid rating or exclusions" }, { status: 400 });
  }
  const user = await getEffectiveUser();
  try {
    const problemId = await pickPracticeProblem(user?.id, new Set(exclude), rating);
    if (!problemId) return NextResponse.json({ error: `No eligible ${rating}-rated problems are available. Try another rating.` }, { status: 409 });
    return NextResponse.json({ problemId, rating });
  } catch {
    return NextResponse.json({ error: "Could not load the problem bank. Try again." }, { status: 503 });
  }
}
