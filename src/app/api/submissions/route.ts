import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/event-auth";

export const dynamic = "force-dynamic";

export async function GET(req: NextRequest) {
  const eventId = req.nextUrl.searchParams.get("eventId") ?? "";
  const raceId = req.nextUrl.searchParams.get("raceId") ?? "";
  const contestantId = req.nextUrl.searchParams.get("contestantId") ?? "";
  const event = await requireEvent(eventId);
  if (!event || !raceId) {
    return NextResponse.json({ error: "unauthorized" }, { status: 401 });
  }
  let query = db()
    .from("submissions")
    .select("id, race_id, contestant_id, lang, verdict, details, submitted_at")
    .eq("race_id", raceId)
    .order("submitted_at", { ascending: false });
  if (contestantId) query = query.eq("contestant_id", contestantId);
  const { data, error } = await query;
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ submissions: data });
}
