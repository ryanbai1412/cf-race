import { NextRequest, NextResponse } from "next/server";
import { buildSessionReplay } from "@/lib/session-log";
import { canViewSession, loadSessionForReplay } from "@/lib/replay-access";

export const dynamic = "force-dynamic";

/**
 * Assemble the replay log for a session — the exact TouristLog shape plus
 * outcome metadata and a signed URL for the webcam video (if recorded).
 * Access follows §5.3 of the unified-app PRD; denials are 404s so session
 * existence is never leaked.
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

  const replay = await buildSessionReplay(sessionId);
  if (!replay) return NextResponse.json({ error: "not found" }, { status: 404 });
  return NextResponse.json(replay);
}
