import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/event-auth";
import { gennaReferences } from "@/lib/genna";

export const dynamic = "force-dynamic";

export type GennaLeaderboardRow = {
  contestant_id: string;
  name: string;
  country: string | null;
  problem_id: string;
  solve_ms: number;
  genna_ms: number;
  delta_ms: number;
};

/**
 * Best solve-time deltas vs the Genna reference times: one row per
 * contestant+problem, sorted by delta ascending (negative = beat him).
 */
export async function GET(req: NextRequest) {
  const eventId = req.nextUrl.searchParams.get("eventId") ?? "";
  const event = await requireEvent(eventId);
  if (!event) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const { data: races, error: racesError } = await db()
    .from("races")
    .select("id")
    .eq("event_id", eventId);
  if (racesError) {
    return NextResponse.json({ error: racesError.message }, { status: 500 });
  }
  const raceIds = (races ?? []).map((r) => r.id);
  if (raceIds.length === 0) return NextResponse.json({ rows: [] });

  const [{ data: solves, error }, refs] = await Promise.all([
    db()
      .from("leaderboard")
      .select("*")
      .in("race_id", raceIds)
      .order("solve_ms", { ascending: true })
      .limit(500),
    gennaReferences(),
  ]);
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });

  const best = new Map<string, GennaLeaderboardRow>();
  for (const s of solves ?? []) {
    const ref = refs.get(s.problem_id);
    if (!ref || ref.solve_ms === null) continue;
    const key = `${s.contestant_id}:${s.problem_id}`;
    const delta = s.solve_ms - ref.solve_ms;
    const cur = best.get(key);
    if (!cur || delta < cur.delta_ms) {
      best.set(key, {
        contestant_id: s.contestant_id,
        name: s.name,
        country: s.country,
        problem_id: s.problem_id,
        solve_ms: s.solve_ms,
        genna_ms: ref.solve_ms,
        delta_ms: delta,
      });
    }
  }
  const rows = [...best.values()].sort((a, b) => a.delta_ms - b.delta_ms).slice(0, 50);
  return NextResponse.json({ rows });
}
