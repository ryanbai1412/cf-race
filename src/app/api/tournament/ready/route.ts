import { NextRequest, NextResponse } from "next/server";
import { currentMatchFor, setReady, tickAndPublish } from "@/lib/tournament";
import { invalidateTournament } from "@/lib/tournament-cache";
import { bad, readJson, tournamentFromCode } from "@/lib/tournament-route";

export const dynamic = "force-dynamic";

/** Ready up for my next game; the game starts once both players are ready. */
export async function POST(req: NextRequest) {
  const body = await readJson(req);
  const found = await tournamentFromCode(body.code);
  if (!found.ok) return found.response;
  const { t, me, snap } = found;
  if (!me) return bad("Join the tournament first", 403);
  const match = currentMatchFor(snap, me.id);
  if (!match || match.status !== "ready") return bad("Your match isn't waiting on you");
  await setReady(match, me.id);
  await tickAndPublish(t.id);
  invalidateTournament(t.id);
  return NextResponse.json({ ok: true });
}
