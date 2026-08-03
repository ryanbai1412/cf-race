import { NextRequest, NextResponse } from "next/server";
import { supabaseServer } from "@/lib/supabase/server";

/** OAuth code exchange for Supabase Auth (Google login). */
export async function GET(req: NextRequest) {
  const code = req.nextUrl.searchParams.get("code");
  const next = req.nextUrl.searchParams.get("next") ?? "/solo";
  const safeNext = next.startsWith("/") ? next : "/solo";

  if (code) {
    const { error } = await supabaseServer().auth.exchangeCodeForSession(code);
    if (!error) {
      return NextResponse.redirect(new URL(safeNext, req.nextUrl.origin));
    }
  }
  return NextResponse.redirect(
    new URL(`${safeNext}?auth_error=1`, req.nextUrl.origin)
  );
}
