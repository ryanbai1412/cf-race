import { NextRequest, NextResponse } from "next/server";
import { randomUUID } from "crypto";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/api-auth";
import { judgeConfigured, judgeRun, samplesToTests } from "@/lib/judge";
import type { Problem } from "@/lib/types";

export const maxDuration = 60;

export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  const eventId = typeof body?.eventId === "string" ? body.eventId : "";
  const lang = body?.lang === "cpp" || body?.lang === "py" ? body.lang : null;
  const source = typeof body?.source === "string" ? body.source : "";
  const problemId = typeof body?.problemId === "string" ? body.problemId : "";
  const customInput = typeof body?.customInput === "string" ? body.customInput : null;

  const event = await requireEvent(eventId);
  if (!event || !lang || !source || source.length > 200_000) {
    return NextResponse.json({ error: "invalid request" }, { status: 400 });
  }
  if (!judgeConfigured()) {
    return NextResponse.json(
      { error: "Judge service is not configured yet" },
      { status: 503 }
    );
  }

  const { data: problem } = await db()
    .from("problems")
    .select("*")
    .eq("id", problemId)
    .maybeSingle<Problem>();
  if (!problem) return NextResponse.json({ error: "unknown problem" }, { status: 400 });

  const tests =
    customInput !== null
      ? [{ name: "custom", input: customInput.slice(0, 1_000_000), expected: null }]
      : samplesToTests(problem.samples);

  try {
    const result = await judgeRun({
      runId: randomUUID(),
      lang,
      source,
      tests,
      timeLimitMs: problem.time_limit_ms,
      memoryLimitMb: problem.memory_limit_mb,
    });
    if (problem.special_judge) result.checkerUnreliable = true;
    return NextResponse.json(result);
  } catch (e) {
    return NextResponse.json(
      { error: e instanceof Error ? e.message : "judge error" },
      { status: 502 }
    );
  }
}
