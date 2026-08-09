import type { User } from "@supabase/supabase-js";
import { db } from "./db";

/**
 * Built-in admins. EDIT THIS LIST to grant permanent admin access — one
 * lowercase email per line. These cannot be revoked from the /admin UI;
 * everyone else is granted/revoked through the `app_admins` table.
 */
export const ADMIN_EMAILS: readonly string[] = [
  "ryan@cognition.ai",
  "ryanbai1412@gmail.com",
];

/** Is this email a built-in (hard-coded, non-revocable) admin? */
export function isBuiltInAdminEmail(email: string | null | undefined): boolean {
  if (!email) return false;
  return ADMIN_EMAILS.includes(email.trim().toLowerCase());
}

/** Admin = built-in email allowlist OR a row in `app_admins`. */
export async function isAdmin(user: User | null): Promise<boolean> {
  if (!user) return false;
  if (isBuiltInAdminEmail(user.email)) return true;
  const { data } = await db()
    .from("app_admins")
    .select("user_id")
    .eq("user_id", user.id)
    .maybeSingle();
  return data !== null;
}

/** User ids with a granted (non-built-in) admin row. */
export async function grantedAdminIds(): Promise<Set<string>> {
  const { data } = await db().from("app_admins").select("user_id");
  return new Set((data ?? []).map((r) => r.user_id as string));
}
