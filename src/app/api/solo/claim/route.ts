import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { browserId } from "@/lib/anon-sessions";
import { getEffectiveUser } from "@/lib/impersonation";

export const dynamic = "force-dynamic";

/**
 * Merge anonymous solo runs into the signed-in account: claims ownership of
 * unowned sessions by this browser's server-side browser_id, plus any
 * explicitly listed ids (sessions created before browser_id existed).
 */
export async function POST(req: NextRequest) {
  const user = await getEffectiveUser();
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const body = await req.json().catch(() => null);
  const ids: string[] = Array.isArray(body?.sessionIds)
    ? body.sessionIds.filter((s: unknown) => typeof s === "string").slice(0, 500)
    : [];

  let claimed = 0;
  const bid = browserId();
  if (bid) {
    const { data, error } = await db()
      .from("sessions")
      .update({ user_id: user.id })
      .eq("browser_id", bid)
      .is("user_id", null)
      .select("id");
    if (error) return NextResponse.json({ error: error.message }, { status: 500 });
    claimed += (data ?? []).length;
  }
  if (ids.length > 0) {
    const { data, error } = await db()
      .from("sessions")
      .update({ user_id: user.id })
      .in("id", ids)
      .is("user_id", null)
      .select("id");
    if (error) return NextResponse.json({ error: error.message }, { status: 500 });
    claimed += (data ?? []).length;
  }
  return NextResponse.json({ claimed });
}
