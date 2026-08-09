import { cookies } from "next/headers";
import { createServerClient } from "@supabase/ssr";
import { createClient, type SupabaseClient, type User } from "@supabase/supabase-js";

/** Server Supabase client bound to the request's auth cookies (anon key). */
export function supabaseServer() {
  const store = cookies();
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      global: {
        // Opt out of Next.js's fetch data cache: PostgREST reads are GETs,
        // which route handlers would otherwise cache indefinitely.
        fetch: (input: RequestInfo | URL, init?: RequestInit) =>
          fetch(input, { ...init, cache: "no-store" }),
      },
      cookies: {
        getAll: () => store.getAll(),
        setAll: (cookiesToSet) => {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              store.set(name, value, options)
            );
          } catch {
            // Called from a Server Component — middleware refreshes sessions.
          }
        },
      },
    }
  );
}

// Module-level client reused across requests so the auth JWKS cache survives
// between invocations (getClaims verifies asymmetric JWTs locally against it).
let verifier: SupabaseClient | null = null;
function jwtVerifier(): SupabaseClient {
  if (!verifier) {
    verifier = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
      { auth: { persistSession: false, autoRefreshToken: false } }
    );
  }
  return verifier;
}

/**
 * The signed-in user for this request, or null.
 *
 * Verifies the access token's signature locally (JWKS, ES256) instead of a
 * per-request network call to the auth server; middleware still refreshes
 * expired sessions. Falls back to auth.getUser() when local verification
 * isn't possible (e.g. symmetric-key projects).
 */
export async function authUser(): Promise<User | null> {
  const supabase = supabaseServer();
  const { data } = await supabase.auth.getSession();
  const session = data.session;
  if (!session) return null;
  const { data: claims, error } = await jwtVerifier().auth.getClaims(
    session.access_token
  );
  if (claims && !error) {
    // Build the user from the verified claims (session.user comes from the
    // cookie unverified, and reading it logs a per-request warning).
    const c = claims.claims;
    return {
      id: c.sub,
      aud: typeof c.aud === "string" ? c.aud : "authenticated",
      email: c.email,
      phone: c.phone,
      role: c.role,
      is_anonymous: c.is_anonymous,
      app_metadata: c.app_metadata ?? {},
      user_metadata: c.user_metadata ?? {},
      created_at: "",
    };
  }
  // Local verification failed — fall back to the network check rather than
  // trusting unverified cookie contents.
  const { data: verified } = await supabase.auth.getUser();
  return verified.user ?? null;
}
