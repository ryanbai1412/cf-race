import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { getEffectiveUser } from "@/lib/impersonation";
import { loadSnapshot, tick } from "@/lib/tournament";
import { wasKicked } from "@/lib/tournament-auth";
import { tournamentFromCode, unavailable } from "@/lib/tournament-route";
import { buildStateView } from "@/lib/tournament-view";

export const dynamic = "force-dynamic";

const LAST_SEEN_WRITE_MS = 15_000;

/** Polled by every open tournament page; also drives the lazy engine. */
export async function GET(req: NextRequest) {
  const found = await tournamentFromCode(req.nextUrl.searchParams.get("code"));
  if (!found.ok) return found.response;
  const { t, me } = found;
  try {
    if (t.status === "running") await tick(t.id);
    if (me && Date.now() - Date.parse(me.last_seen_at) > LAST_SEEN_WRITE_MS) {
      await db()
        .from("tournament_members")
        .update({ last_seen_at: new Date().toISOString() })
        .eq("id", me.id);
    }
    const snap = await loadSnapshot(t.id);
    if (!snap) return NextResponse.json({ error: "not found" }, { status: 404 });
    const [kicked, user] = await Promise.all([
      me ? Promise.resolve(false) : wasKicked(t.id),
      getEffectiveUser(),
    ]);
    return NextResponse.json(await buildStateView(snap, me, { kicked, signedIn: user !== null }));
  } catch (e) {
    console.error(e);
    return unavailable();
  }
}
