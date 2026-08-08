import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/event-auth";
import { raceWithParticipants } from "@/lib/races";

export const dynamic = "force-dynamic";

/** Official submissions for a race, read from session_submissions. */
export async function GET(req: NextRequest) {
  const eventId = req.nextUrl.searchParams.get("eventId") ?? "";
  const raceId = req.nextUrl.searchParams.get("raceId") ?? "";
  const contestantId = req.nextUrl.searchParams.get("contestantId") ?? "";
  const event = await requireEvent(eventId);
  if (!event || !raceId) {
    return NextResponse.json({ error: "unauthorized" }, { status: 401 });
  }

  const found = await raceWithParticipants(eventId, raceId);
  if (!found) return NextResponse.json({ error: "not found" }, { status: 404 });
  const participants = contestantId
    ? found.participants.filter((p) => p.contestant_id === contestantId)
    : found.participants;
  const bySession = new Map(
    participants
      .filter((p) => p.session_id)
      .map((p) => [p.session_id as string, p.contestant_id])
  );
  if (bySession.size === 0) return NextResponse.json({ submissions: [] });

  const { data, error } = await db()
    .from("session_submissions")
    .select("id, session_id, lang, verdict, details, submitted_at")
    .in("session_id", [...bySession.keys()])
    .eq("kind", "submit")
    .order("submitted_at", { ascending: false });
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({
    submissions: (data ?? []).map((s) => ({
      id: s.id,
      race_id: raceId,
      contestant_id: bySession.get(s.session_id),
      lang: s.lang,
      verdict: s.verdict,
      details: s.details,
      submitted_at: s.submitted_at,
    })),
  });
}
