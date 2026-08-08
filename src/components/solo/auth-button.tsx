"use client";

import { useEffect, useMemo, useState } from "react";
import type { User } from "@supabase/supabase-js";
import { supabaseBrowser } from "@/lib/supabase/client";
import { Button } from "@/components/ui/button";
import { LogIn, LogOut } from "lucide-react";
import { toast } from "sonner";

export function useSoloAuth() {
  const supabase = useMemo(() => supabaseBrowser(), []);
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    void supabase.auth.getUser().then(({ data }) => {
      setUser(data.user ?? null);
      setLoading(false);
    });
    const { data: sub } = supabase.auth.onAuthStateChange((_e, session) => {
      setUser(session?.user ?? null);
    });
    return () => sub.subscription.unsubscribe();
  }, [supabase]);

  return { supabase, user, loading };
}

/** Google sign-in / sign-out (Supabase Auth), shared by solo and duel. */
export function SoloAuthButton({
  user,
  supabase,
  next = "/solo",
}: ReturnType<typeof useSoloAuth> & { next?: string }) {
  if (user) {
    return (
      <div className="flex items-center gap-2">
        <span className="font-mono text-xs text-muted-foreground">
          {user.email ?? "signed in"}
        </span>
        <Button
          size="sm"
          variant="ghost"
          onClick={() => void supabase.auth.signOut()}
        >
          <LogOut className="mr-1.5 h-3.5 w-3.5" />
          Sign out
        </Button>
      </div>
    );
  }
  return (
    <Button
      size="sm"
      variant="secondary"
      onClick={async () => {
        const { error } = await supabase.auth.signInWithOAuth({
          provider: "google",
          options: {
            redirectTo: `${window.location.origin}/auth/callback?next=${encodeURIComponent(next)}`,
          },
        });
        if (error) toast.error(`Google sign-in unavailable: ${error.message}`);
      }}
    >
      <LogIn className="mr-1.5 h-3.5 w-3.5" />
      Log in with Google
    </Button>
  );
}
