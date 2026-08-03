import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { buildSoloLog } from "@/lib/solo-log";

export const dynamic = "force-dynamic";

/**
 * Assemble the replay log for a solo run — the exact TouristLog shape plus
 * outcome metadata and a signed URL for the webcam video (if recorded).
 */
export async function GET(req: NextRequest) {
  const sessionId = req.nextUrl.searchParams.get("sessionId") ?? "";
  if (!sessionId) {
    return NextResponse.json({ error: "bad request" }, { status: 400 });
  }

  const built = await buildSoloLog(sessionId);
  if (!built) return NextResponse.json({ error: "not found" }, { status: 404 });
  const { session, log } = built;

  let recordingUrl: string | null = null;
  if (session.recording_path) {
    const { data } = await db()
      .storage.from("recordings")
      .createSignedUrl(session.recording_path, 3600);
    recordingUrl = data?.signedUrl ?? null;
  }

  const { data: problem } = await db()
    .from("problems")
    .select("name, rating, tourist_time_ms")
    .eq("id", session.problem_id)
    .maybeSingle();

  return NextResponse.json({
    ...log,
    outcome: session.outcome,
    timerSec: session.timer_sec,
    startedAt: session.started_at,
    problemName: problem?.name ?? session.problem_id,
    touristTimeMs: problem?.tourist_time_ms ?? null,
    recordingUrl,
    recordingOffsetMs: session.recording_offset_ms ?? 0,
  });
}
