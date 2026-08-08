import { NextResponse } from "next/server";
import { db } from "./db";
import { judgeSubmit, type SubmitResult } from "./judge";
import { MAX_SUBMISSIONS } from "./limits";
import type { Lang } from "./types";

/** True when the caller already used all of its official submissions. */
export async function submissionLimitReached(
  table: "submissions" | "session_submissions",
  filter: Record<string, string>
): Promise<boolean> {
  let q = db().from(table).select("id", { count: "exact", head: true });
  for (const [k, v] of Object.entries(filter)) q = q.eq(k, v);
  const { count } = await q;
  return (count ?? 0) >= MAX_SUBMISSIONS;
}

/**
 * The shared official-submission lifecycle: insert a PENDING row, judge the
 * source on full tests, then record the verdict. On judge failure the pending
 * row is deleted so it neither sticks around forever nor eats a submission.
 */
export async function judgeOfficialSubmission(opts: {
  table: "submissions" | "solo_submissions";
  insertRow: Record<string, unknown>;
  lang: Lang;
  source: string;
  problemId: string;
}): Promise<
  | { ok: true; submissionId: string; result: SubmitResult }
  | { ok: false; response: NextResponse }
> {
  const { data: sub, error } = await db()
    .from(opts.table)
    .insert({
      ...opts.insertRow,
      lang: opts.lang,
      source: opts.source,
      verdict: "PENDING",
    })
    .select("id")
    .single();
  if (error) {
    return {
      ok: false,
      response: NextResponse.json({ error: error.message }, { status: 500 }),
    };
  }

  try {
    const result = await judgeSubmit({
      submissionId: sub.id,
      lang: opts.lang,
      source: opts.source,
      problemId: opts.problemId,
    });
    await db()
      .from(opts.table)
      .update({
        verdict: result.verdict,
        judged_at: new Date().toISOString(),
        details: {
          failedTest: result.failedTest,
          passedCount: result.passedCount,
          totalCount: result.totalCount,
          timeMsMax: result.timeMsMax,
          compileError: result.compileError,
        },
      })
      .eq("id", sub.id);
    return { ok: true, submissionId: sub.id, result };
  } catch (e) {
    // The attempt never got a verdict, so drop it instead of leaving a
    // permanently PENDING row that also eats one of the submissions.
    await db().from(opts.table).delete().eq("id", sub.id);
    return {
      ok: false,
      response: NextResponse.json(
        {
          error: `Judge unavailable, submission not counted (${
            e instanceof Error ? e.message : "judge error"
          })`,
        },
        { status: 502 }
      ),
    };
  }
}
