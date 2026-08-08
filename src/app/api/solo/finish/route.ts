import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { authUser } from "@/lib/supabase/server";

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
  const { data: session } = await db()
    .from("sessions")
    .select("user_id")
    .eq("id", sessionId)
    .maybeSingle();
  if (!session) return NextResponse.json({ error: "not found" }, { status: 404 });
  // Owned sessions (duels, claimed solo runs) only accept their owner's beacon.
  if (session.user_id !== null) {
    const user = await authUser();
    if (user?.id !== session.user_id) {
      return NextResponse.json({ error: "not your session" }, { status: 403 });
    }
  }
  const { error } = await db()
    .from("sessions")
    .update({ outcome })
    .eq("id", sessionId)
    .is("outcome", null);
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ ok: true });
}
