import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import {
  sanitizeEditorEvents,
  type IncomingEditorEvent,
} from "@/lib/editor-events";
import { requireSessionAccess } from "@/lib/session-auth";
import { rateLimit } from "@/lib/rate-limit";

export const dynamic = "force-dynamic";

/** Persist a batch of editor events recorded during a solo or duel run. */
export async function POST(req: NextRequest) {
  const body = (await req.json().catch(() => null)) as {
    sessionId?: string;
    events?: IncomingEditorEvent[];
  } | null;
  if (
    !body?.sessionId ||
    !Array.isArray(body.events) ||
    body.events.length === 0
  ) {
    return NextResponse.json({ error: "bad request" }, { status: 400 });
  }

  const access = await requireSessionAccess(body.sessionId);
  if (!access.ok) return access.response;

  // The client batches events every few seconds; 60/min leaves plenty of room.
  const limited = rateLimit(req, {
    name: "solo-events",
    limit: 60,
    subject: body.sessionId,
  });
  if (limited) return limited;

  const rows = sanitizeEditorEvents(body.events).map((row) => ({
    ...row,
    session_id: body.sessionId,
  }));
  const { error } = await db().from("session_events").insert(rows);
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ ok: true });
}
