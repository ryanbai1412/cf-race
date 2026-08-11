import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/event-auth";

export const dynamic = "force-dynamic";

export async function GET(req: NextRequest) {
  const eventId = req.nextUrl.searchParams.get("eventId") ?? "";
  const event = await requireEvent(eventId);
  if (!event) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const [{ data, error }, { data: refs }] = await Promise.all([
    db()
      .from("problems")
      .select("id, name, rating, race_timer_sec, tourist_time_ms, special_judge")
      .order("id"),
    db().from("genna_problems").select("problem_id, session:sessions(solve_ms)"),
  ]);
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });

  const genna = new Map(
    (refs ?? []).map((r) => [
      r.problem_id,
      (r.session as unknown as { solve_ms: number | null } | null)?.solve_ms ??
        null,
    ])
  );
  const problems = (data ?? []).map((p) => ({
    ...p,
    genna_ref: genna.has(p.id),
    genna_solve_ms: genna.get(p.id) ?? null,
  }));
  return NextResponse.json({ problems });
}
