import { NextRequest, NextResponse } from "next/server";
import { buildDuelReview } from "@/lib/duel-review";

export const dynamic = "force-dynamic";

/**
 * Everything /duel/review/[matchId] needs: both players' replay logs (editor
 * events + submissions in TouristLog shape) with signed webcam URLs, driven
 * by one shared clock on the client.
 */
export async function GET(req: NextRequest) {
  const matchId = req.nextUrl.searchParams.get("matchId") ?? "";
  if (!matchId) return NextResponse.json({ error: "bad request" }, { status: 400 });

  const review = await buildDuelReview(matchId);
  if (!review) return NextResponse.json({ error: "not found" }, { status: 404 });
  return NextResponse.json(review);
}
