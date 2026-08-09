import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { getEffectiveUser } from "@/lib/impersonation";
import { DEFAULT_GRACE_AFTER_AC_SEC } from "@/lib/duel";
import { rateLimit } from "@/lib/rate-limit";

export const dynamic = "force-dynamic";

/** Create a duel room; the creator joins it immediately. */
export async function POST(req: NextRequest) {
  const user = await getEffectiveUser();
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const limited = rateLimit(req, {
    name: "duel-create",
    limit: 60,
    subject: user.id,
  });
  if (limited) return limited;

  const { data: room, error } = await db()
    .from("duel_rooms")
    .insert({
      created_by: user.id,
      grace_after_ac_sec: DEFAULT_GRACE_AFTER_AC_SEC,
    })
    .select("id")
    .single();
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });

  const meta = user.user_metadata as Record<string, unknown>;
  const { error: joinErr } = await db().from("duel_room_players").insert({
    room_id: room.id,
    user_id: user.id,
    name:
      (typeof meta.full_name === "string" && meta.full_name) ||
      (typeof meta.name === "string" && meta.name) ||
      user.email ||
      "Player",
    avatar_url: typeof meta.avatar_url === "string" ? meta.avatar_url : null,
  });
  if (joinErr) {
    // Don't leave a hostless room behind — it could never start a duel.
    await db().from("duel_rooms").delete().eq("id", room.id);
    return NextResponse.json({ error: joinErr.message }, { status: 500 });
  }

  return NextResponse.json({ roomId: room.id });
}
