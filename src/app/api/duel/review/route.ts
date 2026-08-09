import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { authUser } from "@/lib/supabase/server";
import { buildDuelReview } from "@/lib/duel-review";

export const dynamic = "force-dynamic";

/**
 * Everything /duel/review/[matchId] needs: both players' replay logs (editor
 * events + submissions in TouristLog shape) with signed webcam URLs, driven
 * by one shared clock on the client. Match participants only (PRD 11 §5.3);
 * everyone else goes through a share token (/api/shared/review). Denials are
 * 404s so match existence is never leaked.
 */
export async function GET(req: NextRequest) {
  const matchId = req.nextUrl.searchParams.get("matchId") ?? "";
  if (!matchId) return NextResponse.json({ error: "bad request" }, { status: 400 });

  const user = await authUser();
  if (!user) return NextResponse.json({ error: "not found" }, { status: 404 });
  const { data: me } = await db()
    .from("duel_players")
    .select("match_id")
    .eq("match_id", matchId)
    .eq("user_id", user.id)
    .maybeSingle();
  if (!me) return NextResponse.json({ error: "not found" }, { status: 404 });

  const review = await buildDuelReview(matchId);
  if (!review) return NextResponse.json({ error: "not found" }, { status: 404 });
  return NextResponse.json(review);
}
