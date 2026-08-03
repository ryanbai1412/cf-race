import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { buildSoloLog } from "@/lib/solo-log";

export const dynamic = "force-dynamic";

/**
 * Promote a solo run to the tourist ghost: uploads its event log (already in
 * TouristLog format) to the `tourist` bucket as <problemId>.json, which the
 * monitors play back during live races.
 */
export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  const sessionId = typeof body?.sessionId === "string" ? body.sessionId : "";
  if (!sessionId) {
    return NextResponse.json({ error: "bad request" }, { status: 400 });
  }

  const built = await buildSoloLog(sessionId);
  if (!built) return NextResponse.json({ error: "not found" }, { status: 404 });
  const { session, log } = built;
  if (session.outcome !== "solved" || log.solveMs === null) {
    return NextResponse.json(
      { error: "only solved runs can become the tourist ghost" },
      { status: 400 }
    );
  }

  const path = `${session.problem_id}.json`;
  const { error: upErr } = await db()
    .storage.from("tourist")
    .upload(path, JSON.stringify(log), {
      contentType: "application/json",
      upsert: true,
    });
  if (upErr) return NextResponse.json({ error: upErr.message }, { status: 500 });

  await db()
    .from("problems")
    .update({ tourist_time_ms: log.solveMs })
    .eq("id", session.problem_id);

  return NextResponse.json({ ok: true, path });
}
