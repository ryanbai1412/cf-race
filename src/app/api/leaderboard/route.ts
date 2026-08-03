import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/api-auth";

export const dynamic = "force-dynamic";

export async function GET(req: NextRequest) {
  const eventId = req.nextUrl.searchParams.get("eventId") ?? "";
  const problemId = req.nextUrl.searchParams.get("problemId") ?? "";
  const event = await requireEvent(eventId);
  if (!event) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  // The leaderboard view has no event column; scope it to this event's races.
  const { data: races, error: racesError } = await db()
    .from("races")
    .select("id")
    .eq("event_id", eventId);
  if (racesError) {
    return NextResponse.json({ error: racesError.message }, { status: 500 });
  }
  const raceIds = (races ?? []).map((r) => r.id);
  if (raceIds.length === 0) return NextResponse.json({ rows: [] });

  let query = db()
    .from("leaderboard")
    .select("*")
    .in("race_id", raceIds)
    .order("solve_ms", { ascending: true })
    .limit(100);
  if (problemId) query = query.eq("problem_id", problemId);
  const { data, error } = await query;
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ rows: data });
}
