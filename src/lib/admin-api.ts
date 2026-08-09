import { NextResponse } from "next/server";
import type { User } from "@supabase/supabase-js";
import { isAdmin } from "./admin";
import { authUser } from "./supabase/server";

/**
 * Admin gate for /api/admin/* routes: re-verified on every call, always
 * against the REAL authed user (never the impersonated one). Denials are 404
 * so the admin surface's existence is never leaked.
 */
export async function requireAdmin(): Promise<
  { ok: true; user: User } | { ok: false; response: NextResponse }
> {
  const user = await authUser();
  if (!user || !(await isAdmin(user))) {
    return {
      ok: false,
      response: NextResponse.json({ error: "not found" }, { status: 404 }),
    };
  }
  return { ok: true, user };
}
