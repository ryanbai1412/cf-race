import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { buildSessionReplay } from "@/lib/session-log";

export const dynamic = "force-dynamic";

/** Public replay payload for an unrevoked session share token (PRD 11 §5.4). */
export async function GET(req: NextRequest) {
  const token = req.nextUrl.searchParams.get("token") ?? "";
  if (!token) return NextResponse.json({ error: "bad request" }, { status: 400 });

  const { data: share } = await db()
    .from("session_shares")
    .select("session_id")
    .eq("token", token)
    .is("revoked_at", null)
    .maybeSingle();
  if (!share) return NextResponse.json({ error: "not found" }, { status: 404 });

  const replay = await buildSessionReplay(share.session_id);
  if (!replay) return NextResponse.json({ error: "not found" }, { status: 404 });
  return NextResponse.json(replay);
}
