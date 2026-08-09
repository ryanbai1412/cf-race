import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { getEffectiveUser } from "@/lib/impersonation";
import { rateLimit } from "@/lib/rate-limit";

export const dynamic = "force-dynamic";

/**
 * Invalidate a problem for the caller ("don't give me this one again") or
 * revoke that invalidation. Invalidations are per-user: they exclude the
 * problem from the caller's practice/duel picks and from any duel they take
 * part in, never from anyone else's. Body: { problemId, reason? } or
 * { problemId, revoke: true }.
 */
export async function POST(req: NextRequest) {
  const user = await getEffectiveUser();
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const limited = rateLimit(req, {
    name: "invalidate",
    limit: 120,
    subject: user.id,
  });
  if (limited) return limited;

  const body = await req.json().catch(() => null);
  const problemId = typeof body?.problemId === "string" ? body.problemId : "";
  const revoke = body?.revoke === true;
  const reason =
    typeof body?.reason === "string" ? body.reason.slice(0, 500) : null;
  if (!problemId) return NextResponse.json({ error: "bad request" }, { status: 400 });

  const { data: problem } = await db()
    .from("problems")
    .select("id")
    .eq("id", problemId)
    .maybeSingle();
  if (!problem) return NextResponse.json({ error: "unknown problem" }, { status: 404 });

  if (revoke) {
    const { error } = await db()
      .from("problem_invalidations")
      .update({ revoked_at: new Date().toISOString() })
      .eq("problem_id", problemId)
      .eq("by_user", user.id)
      .is("revoked_at", null);
    if (error) return NextResponse.json({ error: error.message }, { status: 500 });
    return NextResponse.json({ ok: true, invalidated: false });
  }

  const { error } = await db().from("problem_invalidations").insert({
    problem_id: problemId,
    by_user: user.id,
    reason,
  });
  // 23505 = the one-active-per-(problem,user) index: already invalidated.
  if (error && error.code !== "23505") {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
  return NextResponse.json({ ok: true, invalidated: true });
}
