import { NextRequest, NextResponse } from "next/server";
import { requireEvent } from "@/lib/event-auth";
import { judgeConfigured, judgeSubmit } from "@/lib/judge";
import { MAX_SOURCE_LEN } from "@/lib/limits";
import { rateLimit } from "@/lib/rate-limit";
import { randomUUID } from "crypto";

export const maxDuration = 120;

/**
 * Practice submission during warm-up (event-authorized): full-test judging on
 * the judge, but nothing is persisted and no race state is touched.
 */
export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  const eventId = typeof body?.eventId === "string" ? body.eventId : "";
  const problemId = typeof body?.problemId === "string" ? body.problemId : "";
  const lang = body?.lang === "cpp" || body?.lang === "py" ? body.lang : null;
  const source = typeof body?.source === "string" ? body.source : "";

  const event = await requireEvent(eventId);
  if (!event || !problemId || !lang || !source || source.length > MAX_SOURCE_LEN) {
    return NextResponse.json({ error: "invalid request" }, { status: 400 });
  }
  if (!judgeConfigured()) {
    return NextResponse.json(
      { error: "Judge service is not configured yet" },
      { status: 503 }
    );
  }
  const limited = rateLimit(req, { name: "judge-submit", limit: 60 });
  if (limited) return limited;

  try {
    const result = await judgeSubmit({
      submissionId: randomUUID(),
      lang,
      source,
      problemId,
    });
    if (result.verdict === "IE") {
      throw new Error(result.compileError || "judge could not judge this attempt");
    }
    return NextResponse.json(result);
  } catch (e) {
    console.error("warm-up submit judge failure:", e);
    return NextResponse.json(
      { error: "Judge unavailable, try again" },
      { status: 502 }
    );
  }
}
