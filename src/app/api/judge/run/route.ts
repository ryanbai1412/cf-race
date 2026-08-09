import { NextRequest, NextResponse } from "next/server";
import { requireEvent } from "@/lib/event-auth";
import { parseRunBody, runOnJudge } from "@/lib/run-route";
import { rateLimit } from "@/lib/rate-limit";

export const maxDuration = 60;

/** Run samples / custom input for a race station (event-authorized). */
export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  const eventId =
    typeof (body as { eventId?: unknown } | null)?.eventId === "string"
      ? (body as { eventId: string }).eventId
      : "";
  const run = parseRunBody(body);

  const event = await requireEvent(eventId);
  if (!event || !run) {
    return NextResponse.json({ error: "invalid request" }, { status: 400 });
  }
  const limited = rateLimit(req, { name: "judge-run", limit: 240 });
  if (limited) return limited;
  return runOnJudge(run);
}
