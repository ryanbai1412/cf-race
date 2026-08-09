import { createHmac, timingSafeEqual } from "crypto";
import { cookies } from "next/headers";
import type { User } from "@supabase/supabase-js";
import { db } from "./db";
import { isAdmin } from "./admin";
import { authUser } from "./supabase/server";

/**
 * Admin impersonation (no real Supabase tokens are ever minted): a signed
 * httpOnly cookie `userId.issuedAtMs.signature`, HMAC'd with the service-role
 * key and only honoured when the REAL authed user is an admin.
 */

export const IMPERSONATION_COOKIE = "cfr_impersonate";
export const IMPERSONATION_TTL_MS = 60 * 60 * 1000;

function sign(payload: string, key: string): string {
  return createHmac("sha256", key).update(payload).digest("base64url");
}

/** Cookie value for impersonating `userId`, issued at `issuedAtMs`. */
export function signImpersonation(
  userId: string,
  key: string,
  issuedAtMs: number = Date.now()
): string {
  const payload = `${userId}.${issuedAtMs}`;
  return `${payload}.${sign(payload, key)}`;
}

/**
 * The impersonated user id if the cookie is well-formed, correctly signed and
 * younger than the 1-hour TTL; null otherwise.
 */
export function verifyImpersonation(
  value: string | undefined | null,
  key: string,
  nowMs: number = Date.now()
): string | null {
  if (!value) return null;
  const parts = value.split(".");
  if (parts.length !== 3) return null;
  const [userId, issuedAt, signature] = parts;
  if (!userId || !/^\d+$/.test(issuedAt)) return null;

  const expected = Buffer.from(sign(`${userId}.${issuedAt}`, key));
  const given = Buffer.from(signature);
  if (expected.length !== given.length || !timingSafeEqual(expected, given)) {
    return null;
  }

  const age = nowMs - Number(issuedAt);
  if (age < 0 || age > IMPERSONATION_TTL_MS) return null;
  return userId;
}

function signingKey(): string {
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!key) throw new Error("SUPABASE_SERVICE_ROLE_KEY missing");
  return key;
}

/** The impersonated user id from this request's cookie, or null. */
export function impersonatedUserIdFromCookie(): string | null {
  return verifyImpersonation(
    cookies().get(IMPERSONATION_COOKIE)?.value,
    signingKey()
  );
}

/**
 * The user that user-scoped reads/writes should act as: the impersonated user
 * when the REAL authed user is an admin with a valid cookie, else the real
 * user. Admin gating itself must always use `authUser()` instead.
 */
export async function getEffectiveUser(): Promise<User | null> {
  const real = await authUser();
  if (!real) return null;

  const targetId = impersonatedUserIdFromCookie();
  if (!targetId || targetId === real.id) return real;
  if (!(await isAdmin(real))) return real;

  const { data, error } = await db().auth.admin.getUserById(targetId);
  if (error || !data.user) return real;
  return data.user;
}

/**
 * Both identities for UI that must show impersonation state (banner, admin
 * page). `impersonating` is null when not impersonating.
 */
export async function getImpersonationState(): Promise<{
  real: User | null;
  effective: User | null;
  impersonating: User | null;
}> {
  const real = await authUser();
  const effective = await getEffectiveUser();
  const impersonating =
    real && effective && effective.id !== real.id ? effective : null;
  return { real, effective, impersonating };
}
