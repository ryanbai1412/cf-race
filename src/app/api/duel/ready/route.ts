import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { getEffectiveUser } from "@/lib/impersonation";
import { startDuelMatch, type DuelRoomRow } from "@/lib/duel";

export const dynamic = "force-dynamic";

export async function POST(req: NextRequest) {
  const user = await getEffectiveUser();
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });
  const body = await req.json().catch(() => null);
  const roomId = typeof body?.roomId === "string" ? body.roomId : "";
  const ready = body?.ready === true;
  if (!roomId || (ready && (!Number.isInteger(body?.settingsVersion) || body.settingsVersion < 0 || body.settingsVersion > 2147483647))) {
    return NextResponse.json({ error: "Invalid request. Refresh the lobby and try again." }, { status: 400 });
  }
  const { data, error } = await db().rpc("duel_lobby_action", {
    p_room_id: roomId, p_user_id: user.id, p_action: "ready",
    p_patch: { ready, settingsVersion: body?.settingsVersion },
  });
  if (error || !data) return NextResponse.json({ error: "Could not update readiness" }, { status: 500 });
  const result = data as { ok: boolean; error?: string; status?: number; claimed?: boolean; room: DuelRoomRow; playerIds: [string, string] };
  if (!result.ok) return NextResponse.json({ error: result.error }, { status: result.status ?? 500 });
  if (!result.claimed) return NextResponse.json({ ok: true, started: false });
  const started = await startDuelMatch(result.room, result.playerIds);
  if (!started.ok) return NextResponse.json({ error: started.error }, { status: started.status });
  return NextResponse.json({ ok: true, started: true });
}
