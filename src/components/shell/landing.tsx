"use client";

import Link from "next/link";
import { supabaseBrowser } from "@/lib/supabase/client";
import { BuiltByDevin } from "@/components/shell/built-by-devin";
import { Button } from "@/components/ui/button";
import { Eyebrow } from "@/components/shell/page";
import { LogIn, Play } from "lucide-react";
import { toast } from "sonner";

/** Logged-out landing: product pitch, Google sign-in, anonymous practice. */
export function Landing({
  next,
  practiceProblemId,
}: {
  next: string;
  practiceProblemId: string | null;
}) {
  const signIn = async () => {
    const supabase = supabaseBrowser();
    const { error } = await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: `${window.location.origin}/auth/callback?next=${encodeURIComponent(next)}`,
      },
    });
    if (error) toast.error(`Google sign-in unavailable: ${error.message}`);
  };

  return (
    <main className="relative flex min-h-[calc(100vh-3.5rem)] flex-col items-center justify-center overflow-hidden px-6">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(99,102,241,0.15),transparent_60%)]" />
      <div className="z-10 flex flex-col items-center gap-8 text-center">
        <div className="space-y-3">
          <Eyebrow>Code vs Racing</Eyebrow>
          <h1 className="max-w-2xl text-5xl font-extrabold tracking-tight sm:text-6xl">
            Race the fastest coders alive.
          </h1>
          <p className="mx-auto max-w-xl text-lg text-muted-foreground">
            Timed competitive programming sprints — solve Codeforces problems
            against the clock, duel a friend, and replay every run keystroke by
            keystroke.
          </p>
        </div>
        <div className="flex flex-wrap items-center justify-center gap-3">
          <Button size="lg" onClick={signIn}>
            <LogIn className="mr-2 h-4 w-4" />
            Sign in with Google
          </Button>
          {practiceProblemId && (
            <Button asChild size="lg" variant="secondary">
              <Link href={`/problems/${practiceProblemId}/solve`}>
                <Play className="mr-2 h-4 w-4" />
                Just practice
              </Link>
            </Button>
          )}
        </div>
        <p className="max-w-md font-mono text-xs text-muted-foreground">
          Practice works without an account — sign in to keep your history and
          share replays.
        </p>
        <BuiltByDevin />
      </div>
    </main>
  );
}
