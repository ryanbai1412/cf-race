import { NextRequest, NextResponse } from "next/server";
import { parseRunBody, runOnJudge } from "@/lib/run-route";
import { rateLimit } from "@/lib/rate-limit";

export const maxDuration = 60;

/**
 * Run samples / custom input for a solo or duel run (same contract as
 * /api/judge/run). A session is required: runs are always attributed to one,
 * which is also what authorizes the compute.
 */
export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  const run = parseRunBody(body);
  if (!run || !run.sessionId) {
    return NextResponse.json({ error: "invalid request" }, { status: 400 });
  }
  const limited = rateLimit(req, {
    name: "solo-run",
    limit: 120,
    subject: run.sessionId,
  });
  if (limited) return limited;
  return runOnJudge(run);
}
