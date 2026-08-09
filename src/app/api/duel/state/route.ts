import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { getEffectiveUser } from "@/lib/impersonation";
import {
  latestMatch,
  resolveMatch,
  type DuelRoomRow,
  type DuelRoomPlayerRow,
} from "@/lib/duel";
import type { Problem } from "@/lib/types";

export const dynamic = "force-dynamic";

/**
 * Full room state for the duel room page: room settings, players + ready
 * flags, and the current/last match. The problem is only included once the
 * server clock has reached the match start (revealed at GO).
 */
export async function GET(req: NextRequest) {
  const user = await getEffectiveUser();
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const roomId = req.nextUrl.searchParams.get("roomId") ?? "";
  if (!roomId) return NextResponse.json({ error: "bad request" }, { status: 400 });

  const [{ data: room }, { data: players }] = await Promise.all([
    db().from("duel_rooms").select("*").eq("id", roomId).maybeSingle<DuelRoomRow>(),
    db()
      .from("duel_room_players")
      .select("*")
      .eq("room_id", roomId)
      .order("joined_at", { ascending: true }),
  ]);
  if (!room) return NextResponse.json({ error: "unknown room" }, { status: 404 });

  // Lazily settle the current match (grace/cutoff expiry, both decided);
  // re-read the room only when the settle could have changed its status.
  let freshRoom: DuelRoomRow | null = null;
  if (room.status === "racing") {
    await resolveMatch(roomId);
    freshRoom = (
      await db().from("duel_rooms").select("*").eq("id", roomId).maybeSingle<DuelRoomRow>()
    ).data;
  }

  const cur = await latestMatch(roomId);

  let match: Record<string, unknown> | null = null;
  if (cur) {
    const startMs = new Date(cur.match.started_at).getTime();
    const revealed = Date.now() >= startMs;
    let problem: Problem | null = null;
    if (revealed) {
      const { data } = await db()
        .from("problems")
        .select("*")
        .eq("id", cur.match.problem_id)
        .maybeSingle<Problem>();
      problem = data ?? null;
    }
    const mine = cur.players.find((p) => p.user_id === user.id);
    match = {
      id: cur.match.id,
      startAtMs: startMs,
      totalTimeSec: cur.match.total_time_sec,
      graceAfterAcSec: cur.match.grace_after_ac_sec,
      firstAcAtMs: cur.match.first_ac_at
        ? new Date(cur.match.first_ac_at).getTime()
        : null,
      finishedAtMs: cur.match.finished_at
        ? new Date(cur.match.finished_at).getTime()
        : null,
      winnerUserId: cur.match.winner_user_id,
      yourSessionId: mine?.session_id ?? null,
      problem,
      players: cur.players.map((p) => {
        const s = cur.sessions.find((x) => x.id === p.session_id);
        return {
          userId: p.user_id,
          sessionId: p.session_id,
          outcome: s?.outcome ?? null,
          solveMs: s?.solve_ms ?? null,
        };
      }),
    };
  }

  return NextResponse.json({
    serverNow: Date.now(),
    userId: user.id,
    room: {
      id: room.id,
      status: (freshRoom ?? room).status,
      totalTimeSec: (freshRoom ?? room).total_time_sec,
      graceAfterAcSec: (freshRoom ?? room).grace_after_ac_sec,
      createdBy: room.created_by,
    },
    players: ((players ?? []) as DuelRoomPlayerRow[]).map((p) => ({
      userId: p.user_id,
      name: p.name,
      avatarUrl: p.avatar_url,
      ready: p.ready_at !== null,
    })),
    match,
  });
}
