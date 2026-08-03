import { cookies } from "next/headers";
import { createServerClient } from "@supabase/ssr";
import type { User } from "@supabase/supabase-js";

/** Server Supabase client bound to the request's auth cookies (anon key). */
export function supabaseServer() {
  const store = cookies();
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
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

/** The signed-in user for this request, or null. */
export async function authUser(): Promise<User | null> {
  const { data } = await supabaseServer().auth.getUser();
  return data.user ?? null;
}
