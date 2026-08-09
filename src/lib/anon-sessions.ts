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

/**
 * Stable per-browser id stamped onto anonymous sessions (sessions.browser_id)
 * so sign-in can claim them even if the session-list cookie is lost. Minting
 * writes a cookie, so only call from route handlers / server actions.
 */
const BID_COOKIE = "cfr_bid";

export function browserId(): string | null {
  const raw = cookies().get(BID_COOKIE)?.value;
  return raw && /^[0-9a-f-]{36}$/.test(raw) ? raw : null;
}

export function ensureBrowserId(): string {
  const existing = browserId();
  if (existing) return existing;
  const id = crypto.randomUUID();
  cookies().set(BID_COOKIE, id, {
    httpOnly: true,
    sameSite: "lax",
    secure: process.env.NODE_ENV === "production",
    path: "/",
    maxAge: MAX_AGE_SEC,
  });
  return id;
}
