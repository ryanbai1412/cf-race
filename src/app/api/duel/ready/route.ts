import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { authUser } from "@/lib/supabase/server";
import { startDuelMatch } from "@/lib/duel";

export const dynamic = "force-dynamic";

/**
 * Async ready-up: toggles the caller's ready state. When both players are
 * ready, the server picks the problem, creates the match + two sessions with
 * a server-stamped start (now + 3s), and moves the room to `racing`. The
 * problem id is never returned here — it is revealed at GO via /state.
 */
export async function POST(req: NextRequest) {
  const user = await authUser();
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const body = await req.json().catch(() => null);
  const roomId = typeof body?.roomId === "string" ? body.roomId : "";
  const ready = body?.ready === true;
  if (!roomId) return NextResponse.json({ error: "bad request" }, { status: 400 });

  const { data: room } = await db()
    .from("duel_rooms")
    .select("*")
    .eq("id", roomId)
    .maybeSingle();
  if (!room) return NextResponse.json({ error: "unknown room" }, { status: 404 });
  if (room.status !== "lobby") {
    return NextResponse.json({ error: "room is not in the lobby" }, { status: 400 });
  }

  const { data: me } = await db()
    .from("duel_room_players")
    .select("user_id")
    .eq("room_id", roomId)
    .eq("user_id", user.id)
    .maybeSingle();
  if (!me) return NextResponse.json({ error: "not in room" }, { status: 403 });

  const { error: readyErr } = await db()
    .from("duel_room_players")
    .update({ ready_at: ready ? new Date().toISOString() : null })
    .eq("room_id", roomId)
    .eq("user_id", user.id);
  if (readyErr) {
    return NextResponse.json({ error: readyErr.message }, { status: 500 });
  }

  const { data: players } = await db()
    .from("duel_room_players")
    .select("user_id, ready_at")
    .eq("room_id", roomId);
  const all = players ?? [];
  const bothReady = all.length === 2 && all.every((p) => p.ready_at !== null);
  if (!bothReady) return NextResponse.json({ ok: true, started: false });

  // Both ready: claim the start by flipping the room to racing (exactly one
  // of the two concurrent ready calls wins this update).
  const { data: claimed } = await db()
    .from("duel_rooms")
    .update({ status: "racing" })
    .eq("id", roomId)
    .eq("status", "lobby")
    .select("id")
    .maybeSingle();
  if (!claimed) return NextResponse.json({ ok: true, started: true });

  const started = await startDuelMatch(room, [all[0].user_id, all[1].user_id]);
  if (!started.ok) {
    return NextResponse.json({ error: started.error }, { status: started.status });
  }
  return NextResponse.json({ ok: true, started: true });
}
