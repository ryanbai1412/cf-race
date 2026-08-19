import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { supabaseServer } from "@/lib/supabase/server";
import {
  anonSessionIds,
  browserId,
  clearAnonSessions,
} from "@/lib/anon-sessions";
import { safeRedirectPath } from "@/lib/safe-redirect";

/** OAuth code exchange for Supabase Auth (Google login). */
export async function GET(req: NextRequest) {
  const code = req.nextUrl.searchParams.get("code");
  const next = req.nextUrl.searchParams.get("next") ?? "/";
  const safeNext = safeRedirectPath(next);

  if (code) {
    const { data, error } = await supabaseServer().auth.exchangeCodeForSession(code);
    if (!error) {
      // Claim this browser's anonymous runs for the account (PRD 11 §1.2):
      // by browser_id (server-side record) and by the session-list cookie
      // (covers sessions created before browser_id existed).
      if (data.user) {
        const bid = browserId();
        if (bid) {
          await db()
            .from("sessions")
            .update({ user_id: data.user.id })
            .eq("browser_id", bid)
            .is("user_id", null);
        }
        const anonIds = anonSessionIds();
        if (anonIds.length > 0) {
          await db()
            .from("sessions")
            .update({ user_id: data.user.id })
            .in("id", anonIds)
            .is("user_id", null);
          clearAnonSessions();
        }
      }
      return NextResponse.redirect(new URL(safeNext, req.nextUrl.origin));
    }
  }
  return NextResponse.redirect(
    new URL(`${safeNext}?auth_error=1`, req.nextUrl.origin)
  );
}
