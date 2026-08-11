import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/event-auth";

export const dynamic = "force-dynamic";

/** Update event settings (admin console, event-cookie authorized). */
export async function POST(req: NextRequest) {
  const body = (await req.json().catch(() => null)) as {
    eventId?: string;
    requireWebcam?: boolean;
    selfServe?: boolean;
    gennaOnly?: boolean;
  } | null;
  const eventId = body?.eventId ?? "";
  const event = await requireEvent(eventId);
  if (!event)
    return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const settings = {
    ...(event.settings ?? {}),
    ...(typeof body?.requireWebcam === "boolean"
      ? { requireWebcam: body.requireWebcam }
      : {}),
    ...(typeof body?.gennaOnly === "boolean"
      ? { gennaOnly: body.gennaOnly }
      : {}),
  };
  const { error } = await db()
    .from("events")
    .update({ settings })
    .eq("id", eventId);
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ ok: true, settings });
}
