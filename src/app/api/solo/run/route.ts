import { NextRequest, NextResponse } from "next/server";
import { parseRunBody, runOnJudge } from "@/lib/run-route";

export const maxDuration = 60;

/** Run samples / custom input for a solo run (same contract as /api/judge/run). */
export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  const run = parseRunBody(body);
  if (!run) {
    return NextResponse.json({ error: "invalid request" }, { status: 400 });
  }
  return runOnJudge(run);
}
