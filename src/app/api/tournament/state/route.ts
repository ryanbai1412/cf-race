import { NextRequest, NextResponse } from "next/server";
import { getEffectiveUser } from "@/lib/impersonation";
import { memberFromList } from "@/lib/tournament-auth";
import { cachedSnapshotByCode, noteSeen, tickIfDue } from "@/lib/tournament-cache";
import { bad, codeParam, noSuchTournament, unavailable } from "@/lib/tournament-route";
import { buildStateView } from "@/lib/tournament-view";

export const dynamic = "force-dynamic";

/** Polled by every open tournament page; also drives the lazy engine. */
export async function GET(req: NextRequest) {
  const code = codeParam(req.nextUrl.searchParams.get("code"));
  if (!code) return bad("missing code");
  try {
    const [first, user] = await Promise.all([cachedSnapshotByCode(code), getEffectiveUser()]);
    if (!first) return noSuchTournament();
    const snap = (await tickIfDue(first)) ? (await cachedSnapshotByCode(code)) ?? first : first;
    const { me, kicked } = await memberFromList(snap.tournament.id, snap.members, async () =>
      user ? user.id : null
    );
    if (me) await noteSeen(me);
    return NextResponse.json(await buildStateView(snap, me, { kicked, signedIn: user !== null }));
  } catch (e) {
    console.error(e);
    return unavailable();
  }
}
