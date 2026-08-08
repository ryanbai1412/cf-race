import { cookies } from "next/headers";

/**
 * Anonymous solo sessions are remembered in an httpOnly cookie so this
 * browser can replay them and so sign-in can claim them
 * (docs/flows/11-unified-app-detailed.md §1.2, §5.3).
 */
const COOKIE = "cfr_anon_sessions";
const MAX_IDS = 50;
const MAX_AGE_SEC = 60 * 60 * 24 * 365;

export function anonSessionIds(): string[] {
  const raw = cookies().get(COOKIE)?.value;
  if (!raw) return [];
  return raw.split(",").filter((id) => /^[0-9a-f-]{36}$/.test(id));
}

export function rememberAnonSession(sessionId: string): void {
  const ids = anonSessionIds().filter((id) => id !== sessionId);
  ids.push(sessionId);
  cookies().set(COOKIE, ids.slice(-MAX_IDS).join(","), {
    httpOnly: true,
    sameSite: "lax",
    secure: process.env.NODE_ENV === "production",
    path: "/",
    maxAge: MAX_AGE_SEC,
  });
}

export function clearAnonSessions(): void {
  cookies().set(COOKIE, "", { path: "/", maxAge: 0 });
}
