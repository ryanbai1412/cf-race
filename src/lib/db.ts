import { createClient, SupabaseClient } from "@supabase/supabase-js";

let client: SupabaseClient | null = null;

// A hung PostgREST read would otherwise pin a coalesced in-flight load (and every poll waiting on it).
// Writes are left alone: aborting one can report a failure for a write that committed.
const REST_READ_TIMEOUT_MS = 10_000;

function restSignal(input: RequestInfo | URL, init?: RequestInit): AbortSignal | undefined {
  const url = typeof input === "string" ? input : input instanceof URL ? input.href : input.url;
  const own = init?.signal ?? undefined;
  const method = (init?.method ?? "GET").toUpperCase();
  if (!url.includes("/rest/v1/") || (method !== "GET" && method !== "HEAD")) return own;
  const timeout = AbortSignal.timeout(REST_READ_TIMEOUT_MS);
  return own ? AbortSignal.any([own, timeout]) : timeout;
}

export function db(): SupabaseClient {
  if (!client) {
    const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
    if (!url || !key) throw new Error("Supabase env vars missing");
    client = createClient(url, key, {
      auth: { persistSession: false },
      global: {
        // Opt out of Next.js's fetch data cache: PostgREST reads are GETs,
        // which route handlers would otherwise cache indefinitely.
        fetch: (input, init) => fetch(input, { ...init, cache: "no-store", signal: restSignal(input, init) }),
      },
    });
  }
  return client;
}

/**
 * Log a failed fire-and-forget write (shows up in server/Vercel logs).
 * Use for writes whose failure shouldn't fail the response but must not
 * disappear silently — replay markers, outcome stamps, lobby resets.
 */
export function logDbError(
  context: string,
  error: { message: string } | null
): void {
  if (error) console.error(`[db] ${context}: ${error.message}`);
}
