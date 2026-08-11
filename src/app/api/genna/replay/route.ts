import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/event-auth";
import { gennaReference } from "@/lib/genna";
import { buildSessionLog } from "@/lib/session-log";

export const dynamic = "force-dynamic";

/**
 * The Genna reference session's replay log for one problem, event-gated,
 * for the monitor ghost column: editor events, submission moments, solve
 * time, and the webcam recording (signed URL).
 */
export async function GET(req: NextRequest) {
  const eventId = req.nextUrl.searchParams.get("eventId") ?? "";
  const problemId = req.nextUrl.searchParams.get("problemId") ?? "";
  const event = await requireEvent(eventId);
  if (!event) return NextResponse.json({ error: "unauthorized" }, { status: 401 });
  if (!problemId) {
    return NextResponse.json({ error: "bad request" }, { status: 400 });
  }

  const ref = await gennaReference(problemId);
  if (!ref) return NextResponse.json({ error: "not found" }, { status: 404 });

  const built = await buildSessionLog(ref.session_id);
  if (!built) return NextResponse.json({ error: "not found" }, { status: 404 });
  const { session, log } = built;

  let recordingUrl: string | null = null;
  if (session.recording_path) {
    const { data: signed } = await db()
      .storage.from("recordings")
      .createSignedUrl(session.recording_path, 3600);
    recordingUrl = signed?.signedUrl ?? null;
  }

  return NextResponse.json({
    problemId,
    lang: log.lang,
    solveMs: session.solve_ms,
    events: log.events,
    recordingUrl,
    recordingOffsetMs: session.recording_offset_ms ?? 0,
  });
}
