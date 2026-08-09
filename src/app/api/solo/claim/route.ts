import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { getEffectiveUser } from "@/lib/impersonation";

export const dynamic = "force-dynamic";

/**
 * Merge anonymous (localStorage) solo runs into the signed-in account:
 * claims ownership of sessions that don't belong to anyone yet.
 */
export async function POST(req: NextRequest) {
  const user = await getEffectiveUser();
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const body = await req.json().catch(() => null);
  const ids: string[] = Array.isArray(body?.sessionIds)
    ? body.sessionIds.filter((s: unknown) => typeof s === "string").slice(0, 500)
    : [];
  if (ids.length === 0) return NextResponse.json({ claimed: 0 });

  const { data, error } = await db()
    .from("sessions")
    .update({ user_id: user.id })
    .in("id", ids)
    .is("user_id", null)
    .select("id");
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ claimed: (data ?? []).length });
}
