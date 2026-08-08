import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { authUser } from "@/lib/supabase/server";
import { COUNTDOWN_MS, pickDuelProblem } from "@/lib/duel";

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

  await db()
    .from("duel_room_players")
    .update({ ready_at: ready ? new Date().toISOString() : null })
    .eq("room_id", roomId)
    .eq("user_id", user.id);

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

  const [userA, userB] = all.map((p) => p.user_id);
  const problemId = await pickDuelProblem(userA, userB);
  if (!problemId) {
    await db().from("duel_rooms").update({ status: "lobby" }).eq("id", roomId);
    await db()
      .from("duel_room_players")
      .update({ ready_at: null })
      .eq("room_id", roomId);
    return NextResponse.json(
      { error: "no eligible problems left for this pair" },
      { status: 409 }
    );
  }

  const startAt = new Date(Date.now() + COUNTDOWN_MS).toISOString();
  const { data: match, error } = await db()
    .from("duel_matches")
    .insert({
      room_id: roomId,
      problem_id: problemId,
      started_at: startAt,
      total_time_sec: room.total_time_sec,
      grace_after_ac_sec: room.grace_after_ac_sec,
    })
    .select("id")
    .single();
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });

  for (const uid of [userA, userB]) {
    const { data: session } = await db()
      .from("sessions")
      .insert({
        kind: "duel",
        user_id: uid,
        problem_id: problemId,
        started_at: startAt,
        timer_sec: room.total_time_sec,
      })
      .select("id")
      .single();
    await db().from("duel_players").insert({
      match_id: match.id,
      user_id: uid,
      session_id: session!.id,
    });
  }

  return NextResponse.json({ ok: true, started: true });
}
