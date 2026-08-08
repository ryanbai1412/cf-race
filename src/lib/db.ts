import { createClient, SupabaseClient } from "@supabase/supabase-js";

let client: SupabaseClient | null = null;

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
        fetch: (input, init) => fetch(input, { ...init, cache: "no-store" }),
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
