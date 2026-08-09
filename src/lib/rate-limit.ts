import { NextResponse, type NextRequest } from "next/server";

/**
 * Deliberately generous fixed-window rate limiting, kept in the instance's
 * memory. Serverless instances are per-region and recycled, so this is a
 * blunt abuse ceiling (a single client cannot hammer one instance), not a
 * precise quota — the point is that no public route is unbounded.
 */

type Window = { count: number; resetAt: number };

const windows = new Map<string, Window>();
const MAX_KEYS = 20_000;

/** Client identity for limiting: the proxy-provided IP, else a shared bucket. */
function clientKey(req: NextRequest): string {
  const forwarded = req.headers.get("x-forwarded-for");
  const ip =
    forwarded?.split(",")[0]?.trim() || req.headers.get("x-real-ip") || "unknown";
  return ip;
}

function hit(key: string, limit: number, windowMs: number): number | null {
  const now = Date.now();
  const existing = windows.get(key);
  if (!existing || existing.resetAt <= now) {
    // Bounded map: drop the whole generation rather than tracking an LRU.
    if (windows.size >= MAX_KEYS) windows.clear();
    windows.set(key, { count: 1, resetAt: now + windowMs });
    return null;
  }
  existing.count += 1;
  if (existing.count > limit) return Math.ceil((existing.resetAt - now) / 1000);
  return null;
}

export type RateLimitOptions = {
  /** Bucket name, so different routes don't share a counter. */
  name: string;
  /** Requests allowed per window. */
  limit: number;
  /** Window length in ms (default 1 minute). */
  windowMs?: number;
  /** Extra identity beyond the client IP (e.g. a session or user id). */
  subject?: string | null;
};

/**
 * A 429 response when this caller is over the limit, or null to proceed.
 *
 *     const limited = rateLimit(req, { name: "solo-run", limit: 120 });
 *     if (limited) return limited;
 */
export function rateLimit(
  req: NextRequest,
  opts: RateLimitOptions
): NextResponse | null {
  const windowMs = opts.windowMs ?? 60_000;
  const key = `${opts.name}:${opts.subject ?? clientKey(req)}`;
  const retryAfter = hit(key, opts.limit, windowMs);
  if (retryAfter === null) return null;
  return NextResponse.json(
    { error: "Too many requests — slow down and try again." },
    { status: 429, headers: { "Retry-After": String(Math.max(1, retryAfter)) } }
  );
}
