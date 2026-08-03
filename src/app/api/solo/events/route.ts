import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import type { Lang } from "@/lib/types";

export const dynamic = "force-dynamic";

/** Persist a batch of editor snapshots recorded during a solo run. */
export async function POST(req: NextRequest) {
  const body = (await req.json().catch(() => null)) as {
    sessionId?: string;
    events?: { t: number; code: string; lang: Lang; kind?: string }[];
  } | null;
  if (
    !body?.sessionId ||
    !Array.isArray(body.events) ||
    body.events.length === 0
  ) {
    return NextResponse.json({ error: "bad request" }, { status: 400 });
  }

  const rows = body.events.slice(0, 200).map((e) => ({
    session_id: body.sessionId,
    t_ms: Math.max(0, Math.round(e.t)),
    code: String(e.code).slice(0, 100_000),
    lang: e.lang === "py" ? "py" : "cpp",
    kind: e.kind === "run" ? "run" : "snapshot",
  }));
  const { error } = await db().from("solo_editor_events").insert(rows);
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ ok: true });
}
