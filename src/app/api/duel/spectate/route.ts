import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { getEffectiveUser } from "@/lib/impersonation";
import { latestMatch, resolveMatch } from "@/lib/duel";
import { buildDuelReview } from "@/lib/duel-review";

export const dynamic = "force-dynamic";

/**
 * Live review payload for whoever holds a room link but isn't racing in it.
 * Same shape as /api/duel/review plus the server clock, so the client can run
 * the shared replay clock against wall time. Nothing is returned before GO:
 * the problem must not leak to spectators before the players see it.
 */
export async function GET(req: NextRequest) {
  const user = await getEffectiveUser();
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const roomId = req.nextUrl.searchParams.get("roomId") ?? "";
  if (!roomId) return NextResponse.json({ error: "bad request" }, { status: 400 });

  const { data: room } = await db()
    .from("duel_rooms")
    .select("id, status")
    .eq("id", roomId)
    .maybeSingle<{ id: string; status: string }>();
  if (!room) return NextResponse.json({ error: "not found" }, { status: 404 });

  if (room.status === "racing") await resolveMatch(roomId);
  const cur = await latestMatch(roomId);
  if (!cur || Date.now() < new Date(cur.match.started_at).getTime()) {
    return NextResponse.json({ error: "not started" }, { status: 404 });
  }

  const review = await buildDuelReview(cur.match.id);
  if (!review) return NextResponse.json({ error: "not found" }, { status: 404 });
  return NextResponse.json({ ...review, serverNow: Date.now() });
}
