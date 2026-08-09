import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { buildDuelReview } from "@/lib/duel-review";

export const dynamic = "force-dynamic";

/** Public duel-review payload for an unrevoked match share token (PRD 11 §5.4). */
export async function GET(req: NextRequest) {
  const token = req.nextUrl.searchParams.get("token") ?? "";
  if (!token) return NextResponse.json({ error: "bad request" }, { status: 400 });

  const { data: share } = await db()
    .from("match_shares")
    .select("match_id")
    .eq("token", token)
    .is("revoked_at", null)
    .maybeSingle();
  if (!share) return NextResponse.json({ error: "not found" }, { status: 404 });

  const review = await buildDuelReview(share.match_id);
  if (!review) return NextResponse.json({ error: "not found" }, { status: 404 });
  return NextResponse.json(review);
}
