import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { isBuiltInAdminEmail } from "@/lib/admin";
import { requireAdmin } from "@/lib/admin-api";

/** Grant or revoke DB-granted admin (built-in allowlist emails are fixed). */
export async function POST(req: NextRequest) {
  const gate = await requireAdmin();
  if (!gate.ok) return gate.response;

  const { userId, action } = (await req.json().catch(() => ({}))) as {
    userId?: string;
    action?: "grant" | "revoke";
  };
  if (!userId || (action !== "grant" && action !== "revoke")) {
    return NextResponse.json({ error: "bad request" }, { status: 400 });
  }

  const { data, error } = await db().auth.admin.getUserById(userId);
  if (error || !data.user) {
    return NextResponse.json({ error: "unknown user" }, { status: 404 });
  }
  if (isBuiltInAdminEmail(data.user.email)) {
    return NextResponse.json(
      { error: "built-in admin — edit src/lib/admin.ts" },
      { status: 400 }
    );
  }

  if (action === "grant") {
    const { error: upsertError } = await db()
      .from("app_admins")
      .upsert({ user_id: userId, granted_by: gate.user.id });
    if (upsertError) {
      return NextResponse.json({ error: upsertError.message }, { status: 500 });
    }
  } else {
    const { error: deleteError } = await db()
      .from("app_admins")
      .delete()
      .eq("user_id", userId);
    if (deleteError) {
      return NextResponse.json({ error: deleteError.message }, { status: 500 });
    }
  }
  return NextResponse.json({ ok: true });
}
