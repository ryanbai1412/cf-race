import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { canViewSession, loadSessionForReplay } from "@/lib/access";

export const dynamic = "force-dynamic";

/**
 * A session's official submissions. Access matches the replay: a duel
 * opponent must not be able to watch the other player's verdicts land while
 * the match is still running. Denials are 404s so ids are never probed.
 */
export async function GET(req: NextRequest) {
  const sessionId = req.nextUrl.searchParams.get("sessionId") ?? "";
  if (!sessionId) {
    return NextResponse.json({ error: "bad request" }, { status: 400 });
  }
  const session = await loadSessionForReplay(sessionId);
  if (!session || !(await canViewSession(session))) {
    return NextResponse.json({ error: "not found" }, { status: 404 });
  }
  const { data, error } = await db()
    .from("session_submissions")
    .select("id, session_id, lang, verdict, details, submitted_at")
    .eq("session_id", sessionId)
    .eq("kind", "submit")
    .order("submitted_at", { ascending: false });
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ submissions: data });
}
