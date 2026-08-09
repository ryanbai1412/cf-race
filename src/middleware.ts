import { NextResponse, type NextRequest } from "next/server";
import { createServerClient } from "@supabase/ssr";
import type { JWK } from "@supabase/supabase-js";

const JWKS_TTL_MS = 10 * 60 * 1000;
type Jwks = { keys: JWK[] };
let jwks: Jwks | null = null;
let jwksFetchedAt = 0;

/**
 * The project's JWT signing keys, cached at module scope so verification in
 * getClaims() stays local across invocations (a fresh client per request
 * would otherwise refetch them every time).
 */
async function signingKeys(): Promise<Jwks | undefined> {
  if (jwks && Date.now() - jwksFetchedAt < JWKS_TTL_MS) return jwks;
  try {
    const res = await fetch(
      `${process.env.NEXT_PUBLIC_SUPABASE_URL}/auth/v1/.well-known/jwks.json`
    );
    if (!res.ok) return jwks ?? undefined;
    jwks = (await res.json()) as Jwks;
    jwksFetchedAt = Date.now();
    return jwks;
  } catch {
    return jwks ?? undefined;
  }
}

/** Refresh Supabase auth sessions on solo/duel/auth routes (@supabase/ssr). */
export async function middleware(request: NextRequest) {
  let response = NextResponse.next({ request });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll: () => request.cookies.getAll(),
        setAll: (cookiesToSet) => {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value)
          );
          response = NextResponse.next({ request });
          cookiesToSet.forEach(({ name, value, options }) =>
            response.cookies.set(name, value, options)
          );
        },
      },
    }
  );

  // Verifies the JWT locally (JWKS) and refreshes expired sessions; avoids
  // a per-request round-trip to the auth server that getUser() would make.
  await supabase.auth.getClaims(undefined, { jwks: await signingKeys() });
  return response;
}

export const config = {
  matcher: [
    "/",
    "/problems/:path*",
    "/problems",
    "/sessions",
    "/replay/:path*",
    "/duels",
    "/events",
    "/solo/:path*",
    "/solo",
    "/duel/:path*",
    "/duel",
    "/auth/:path*",
    "/api/solo/:path*",
    "/api/duel/:path*",
    "/api/shares",
    "/api/events",
  ],
};
