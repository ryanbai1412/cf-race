import { NextRequest, NextResponse } from "next/server";
import { revalidateTag } from "next/cache";
import { db } from "@/lib/db";
import { getEffectiveUser } from "@/lib/impersonation";

export const dynamic = "force-dynamic";

/**
 * Mark a problem invalid (excluded from picks + solved-tracking) or revoke
 * the active invalidation. Body: { problemId, reason? } or
 * { problemId, revoke: true }.
 */
export async function POST(req: NextRequest) {
  const user = await getEffectiveUser();
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

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
      .is("revoked_at", null);
    if (error) return NextResponse.json({ error: error.message }, { status: 500 });
    revalidateTag("problem-invalidations");
    return NextResponse.json({ ok: true, invalidated: false });
  }

  const { data: active } = await db()
    .from("problem_invalidations")
    .select("id")
    .eq("problem_id", problemId)
    .is("revoked_at", null)
    .maybeSingle();
  if (active) return NextResponse.json({ ok: true, invalidated: true });

  const { error } = await db().from("problem_invalidations").insert({
    problem_id: problemId,
    by_user: user.id,
    reason,
  });
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  revalidateTag("problem-invalidations");
  return NextResponse.json({ ok: true, invalidated: true });
}
