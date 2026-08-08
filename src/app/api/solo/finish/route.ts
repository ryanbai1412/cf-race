import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireSessionAccess } from "@/lib/session-auth";

export const dynamic = "force-dynamic";

/** Mark a non-AC end of a solo run (timeout, or abandoned via sendBeacon). */
export async function POST(req: NextRequest) {
  // sendBeacon posts as text/plain, so parse the body manually.
  let body: { sessionId?: unknown; outcome?: unknown } | null = null;
  try {
    body = JSON.parse(await req.text());
  } catch {
    body = null;
  }
  const sessionId = typeof body?.sessionId === "string" ? body.sessionId : "";
  const outcome = body?.outcome === "timeout" || body?.outcome === "abandoned"
    ? body.outcome
    : null;
  if (!sessionId || !outcome) {
    return NextResponse.json({ error: "bad request" }, { status: 400 });
  }
  const access = await requireSessionAccess(sessionId);
  if (!access.ok) return access.response;
  const { error } = await db()
    .from("sessions")
    .update({ outcome })
    .eq("id", sessionId)
    .is("outcome", null);
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ ok: true });
}
