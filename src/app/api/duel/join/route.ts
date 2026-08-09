import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { getEffectiveUser } from "@/lib/impersonation";

export const dynamic = "force-dynamic";

/** Join a duel room (max 2 players; rejoining is a no-op). */
export async function POST(req: NextRequest) {
  const user = await getEffectiveUser();
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const body = await req.json().catch(() => null);
  const roomId = typeof body?.roomId === "string" ? body.roomId : "";
  if (!roomId) return NextResponse.json({ error: "bad request" }, { status: 400 });

  const [{ data: room }, { data: players }] = await Promise.all([
    db().from("duel_rooms").select("id").eq("id", roomId).maybeSingle(),
    db().from("duel_room_players").select("user_id").eq("room_id", roomId),
  ]);
  if (!room) return NextResponse.json({ error: "unknown room" }, { status: 404 });

  const existing = players ?? [];
  if (existing.some((p) => p.user_id === user.id)) {
    return NextResponse.json({ ok: true, joined: true });
  }
  if (existing.length >= 2) {
    return NextResponse.json({ error: "room full" }, { status: 409 });
  }

  const meta = user.user_metadata as Record<string, unknown>;
  const { error } = await db().from("duel_room_players").insert({
    room_id: roomId,
    user_id: user.id,
    name:
      (typeof meta.full_name === "string" && meta.full_name) ||
      (typeof meta.name === "string" && meta.name) ||
      user.email ||
      "Player",
    avatar_url: typeof meta.avatar_url === "string" ? meta.avatar_url : null,
  });
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ ok: true, joined: true });
}
