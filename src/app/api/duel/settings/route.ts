import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { getEffectiveUser } from "@/lib/impersonation";
import { isProblemRating } from "@/lib/problem-rating";

export const dynamic = "force-dynamic";

export async function POST(req: NextRequest) {
  const user = await getEffectiveUser();
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });
  const body = await req.json().catch(() => null);
  const roomId = typeof body?.roomId === "string" ? body.roomId : "";
  if (!roomId) return NextResponse.json({ error: "bad request" }, { status: 400 });
  const patch: Record<string, number | null> = {};
  if ("rating" in body) {
    if (!isProblemRating(body.rating)) return NextResponse.json({ error: "Invalid rating" }, { status: 400 });
    patch.rating = body.rating;
  }
  for (const key of ["totalTimeSec", "graceAfterAcSec"] as const) {
    if (!(key in body)) continue;
    const value = body[key];
    if (value !== null && (typeof value !== "number" || !Number.isInteger(value) || value < 1 || value > 86400)) {
      return NextResponse.json({ error: "Invalid timer" }, { status: 400 });
    }
    patch[key] = value;
  }
  const { data, error } = await db().rpc("duel_lobby_action", {
    p_room_id: roomId, p_user_id: user.id, p_action: "settings", p_patch: patch,
  });
  if (error || !data) return NextResponse.json({ error: "Could not save room settings" }, { status: 500 });
  const result = data as { ok: boolean; error?: string; status?: number };
  if (!result.ok) return NextResponse.json({ error: result.error }, { status: result.status ?? 500 });
  return NextResponse.json({ ok: true });
}
