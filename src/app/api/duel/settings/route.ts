import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { getEffectiveUser } from "@/lib/impersonation";

export const dynamic = "force-dynamic";

/** Update room timer settings from the lobby (either player, before ready-up). */
export async function POST(req: NextRequest) {
  const user = await getEffectiveUser();
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const body = await req.json().catch(() => null);
  const roomId = typeof body?.roomId === "string" ? body.roomId : "";
  if (!roomId) return NextResponse.json({ error: "bad request" }, { status: 400 });

  const norm = (v: unknown): number | null => {
    const n = Number(v);
    if (!Number.isFinite(n) || n <= 0) return null;
    return Math.min(Math.round(n), 24 * 3600);
  };
  const totalTimeSec = "totalTimeSec" in (body ?? {}) ? norm(body.totalTimeSec) : undefined;
  const graceSec = "graceAfterAcSec" in (body ?? {}) ? norm(body.graceAfterAcSec) : undefined;

  const [{ data: member }, { data: room }] = await Promise.all([
    db()
      .from("duel_room_players")
      .select("user_id")
      .eq("room_id", roomId)
      .eq("user_id", user.id)
      .maybeSingle(),
    db().from("duel_rooms").select("status").eq("id", roomId).maybeSingle(),
  ]);
  if (!member) return NextResponse.json({ error: "not in room" }, { status: 403 });

  if (!room || room.status !== "lobby") {
    return NextResponse.json({ error: "room is not in the lobby" }, { status: 400 });
  }

  const update: Record<string, number | null> = {};
  if (totalTimeSec !== undefined) update.total_time_sec = totalTimeSec;
  if (graceSec !== undefined) update.grace_after_ac_sec = graceSec;
  if (Object.keys(update).length === 0) return NextResponse.json({ ok: true });

  const { error } = await db().from("duel_rooms").update(update).eq("id", roomId);
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ ok: true });
}
