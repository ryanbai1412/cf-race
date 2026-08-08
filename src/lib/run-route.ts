import { NextResponse } from "next/server";
import { randomUUID } from "crypto";
import { db } from "./db";
import { judgeConfigured, judgeRun, samplesToTests } from "./judge";
import { requireSessionAccess } from "./session-auth";
import { MAX_CUSTOM_INPUT_LEN, MAX_SOURCE_LEN } from "./limits";
import type { Lang, Problem } from "./types";

export type RunRequestBody = {
  lang: Lang;
  source: string;
  problemId: string;
  customInput: string | null;
  sessionId: string | null;
};

/** Parse the shared fields of a run request (race + solo). */
export function parseRunBody(body: unknown): RunRequestBody | null {
  const b = body as Record<string, unknown> | null;
  const lang = b?.lang === "cpp" || b?.lang === "py" ? (b.lang as Lang) : null;
  const source = typeof b?.source === "string" ? b.source : "";
  const problemId = typeof b?.problemId === "string" ? b.problemId : "";
  const customInput = typeof b?.customInput === "string" ? b.customInput : null;
  const sessionId = typeof b?.sessionId === "string" ? b.sessionId : null;
  if (!lang || !source || source.length > MAX_SOURCE_LEN) return null;
  return { lang, source, problemId, customInput, sessionId };
}

/**
 * Run a source against a problem's samples (or custom input) on the judge.
 * Shared by /api/judge/run and /api/solo/run.
 */
export async function runOnJudge(run: RunRequestBody): Promise<NextResponse> {
  if (!judgeConfigured()) {
    return NextResponse.json(
      { error: "Judge service is not configured yet" },
      { status: 503 }
    );
  }

  // Runs attributed to a session require access to that session.
  if (run.sessionId) {
    const access = await requireSessionAccess(run.sessionId);
    if (!access.ok) return access.response;
  }

  const { data: problem } = await db()
    .from("problems")
    .select("*")
    .eq("id", run.problemId)
    .maybeSingle<Problem>();
  if (!problem) return NextResponse.json({ error: "unknown problem" }, { status: 400 });

  const tests =
    run.customInput !== null
      ? [
          {
            name: "custom",
            input: run.customInput.slice(0, MAX_CUSTOM_INPUT_LEN),
            expected: null,
          },
        ]
      : samplesToTests(problem.samples);

  try {
    const result = await judgeRun({
      runId: randomUUID(),
      lang: run.lang,
      source: run.source,
      tests,
      timeLimitMs: problem.time_limit_ms,
      memoryLimitMb: problem.memory_limit_mb,
    });
    if (problem.special_judge) result.checkerUnreliable = true;
    if (run.sessionId) {
      const verdict = !result.compile.ok
        ? "CE"
        : result.results.every((r) => r.verdict === "AC")
          ? "AC"
          : (result.results.find((r) => r.verdict !== "AC")?.verdict ?? null);
      await db().from("session_submissions").insert({
        session_id: run.sessionId,
        kind: "run",
        lang: run.lang,
        source: run.source,
        verdict,
        details: { custom: run.customInput !== null },
        judged_at: new Date().toISOString(),
      });
    }
    return NextResponse.json(result);
  } catch (e) {
    return NextResponse.json(
      { error: e instanceof Error ? e.message : "judge error" },
      { status: 502 }
    );
  }
}
