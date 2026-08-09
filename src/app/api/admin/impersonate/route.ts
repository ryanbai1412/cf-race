import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireAdmin } from "@/lib/admin-api";
import {
  IMPERSONATION_COOKIE,
  IMPERSONATION_TTL_MS,
  signImpersonation,
} from "@/lib/impersonation";

/** Start impersonating a user (admin only). */
export async function POST(req: NextRequest) {
  const gate = await requireAdmin();
  if (!gate.ok) return gate.response;

  const { userId } = (await req.json().catch(() => ({}))) as {
    userId?: string;
  };
  if (!userId) {
    return NextResponse.json({ error: "userId required" }, { status: 400 });
  }
  const { data, error } = await db().auth.admin.getUserById(userId);
  if (error || !data.user) {
    return NextResponse.json({ error: "unknown user" }, { status: 404 });
  }

  const res = NextResponse.json({ ok: true, email: data.user.email ?? null });
  res.cookies.set(
    IMPERSONATION_COOKIE,
    signImpersonation(userId, process.env.SUPABASE_SERVICE_ROLE_KEY!),
    {
      httpOnly: true,
      sameSite: "lax",
      secure: process.env.NODE_ENV === "production",
      path: "/",
      maxAge: IMPERSONATION_TTL_MS / 1000,
    }
  );
  return res;
}

/** Stop impersonating (clears the cookie). */
export async function DELETE() {
  const gate = await requireAdmin();
  if (!gate.ok) return gate.response;
  const res = NextResponse.json({ ok: true });
  res.cookies.set(IMPERSONATION_COOKIE, "", { path: "/", maxAge: 0 });
  return res;
}
