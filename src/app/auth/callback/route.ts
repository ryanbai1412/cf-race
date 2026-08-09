import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { supabaseServer } from "@/lib/supabase/server";
import { anonSessionIds, clearAnonSessions } from "@/lib/anon-sessions";

/** OAuth code exchange for Supabase Auth (Google login). */
export async function GET(req: NextRequest) {
  const code = req.nextUrl.searchParams.get("code");
  const next = req.nextUrl.searchParams.get("next") ?? "/";
  const safeNext = next.startsWith("/") ? next : "/";

  if (code) {
    const { data, error } = await supabaseServer().auth.exchangeCodeForSession(code);
    if (!error) {
      // Claim this browser's anonymous runs for the account (PRD 11 §1.2).
      const anonIds = anonSessionIds();
      if (data.user && anonIds.length > 0) {
        await db()
          .from("sessions")
          .update({ user_id: data.user.id })
          .in("id", anonIds)
          .is("user_id", null);
        clearAnonSessions();
      }
      return NextResponse.redirect(new URL(safeNext, req.nextUrl.origin));
    }
  }
  return NextResponse.redirect(
    new URL(`${safeNext}?auth_error=1`, req.nextUrl.origin)
  );
}
