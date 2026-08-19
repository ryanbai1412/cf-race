import Link from "next/link";
import { getEffectiveUser } from "@/lib/impersonation";
import { db } from "@/lib/db";
import { sweepStaleSessions } from "@/lib/session-lifecycle";
import { pickPracticeProblem } from "@/lib/problem-bank";
import { Landing } from "@/components/shell/landing";
import { LegacyClaim } from "@/components/shell/legacy-claim";
import { QuickActions } from "@/components/shell/quick-actions";
import { OutcomeBadge } from "@/components/shell/outcome-badge";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { EmptyState, PageHeader, SectionTitle } from "@/components/shell/page";
import { formatMsPrecise } from "@/lib/templates";
import { safeRedirectPath } from "@/lib/safe-redirect";
import { Video } from "lucide-react";

export const dynamic = "force-dynamic";

type RecentSession = {
  id: string;
  kind: string;
  problem_id: string;
  started_at: string;
  outcome: "solved" | "timeout" | "abandoned" | null;
  solve_ms: number | null;
};

export default async function HomePage({
  searchParams,
}: {
  searchParams: { next?: string };
}) {
  const user = await getEffectiveUser();

  if (!user) {
    const practiceProblemId = await pickPracticeProblem(null);
    const next = safeRedirectPath(searchParams.next);
    return <Landing next={next} practiceProblemId={practiceProblemId} />;
  }

  const [
    practiceProblemId,
    { data: recent },
    { data: solvedRows },
    { data: myMatches },
    { data: shares },
  ] = await Promise.all([
    pickPracticeProblem(user.id),
    db()
      .from("sessions")
      .select("id, kind, problem_id, started_at, outcome, solve_ms")
      .eq("user_id", user.id)
      .order("started_at", { ascending: false })
      .limit(10),
    db()
      .from("sessions")
      .select("problem_id, kind, started_at")
      .eq("user_id", user.id)
      .eq("outcome", "solved"),
    db()
      .from("duel_players")
      .select("match_id, duel_matches!inner(winner_user_id, finished_at)")
      .eq("user_id", user.id)
      .not("duel_matches.finished_at", "is", null),
    db()
      .from("session_shares")
      .select("session_id, sessions!inner(user_id)")
      .eq("sessions.user_id", user.id)
      .is("revoked_at", null),
    sweepStaleSessions({ userId: user.id }),
  ]);

  const sessions = (recent ?? []) as RecentSession[];
  const shareBySession = new Map<string, boolean>();
  for (const s of shares ?? []) shareBySession.set(s.session_id, true);

  const solvedProblems = new Set((solvedRows ?? []).map((s) => s.problem_id));
  const weekAgo = Date.now() - 7 * 24 * 3600 * 1000;
  const soloSolvesThisWeek = (solvedRows ?? []).filter(
    (s) => s.kind === "solo" && new Date(s.started_at).getTime() > weekAgo
  ).length;

  let wins = 0;
  let losses = 0;
  for (const p of myMatches ?? []) {
    const m = p.duel_matches as unknown as {
      winner_user_id: string | null;
      finished_at: string | null;
    };
    if (m.winner_user_id === user.id) wins += 1;
    else if (m.winner_user_id !== null) losses += 1;
  }

  return (
    <main className="relative min-h-[calc(100vh-3.5rem)] overflow-hidden px-6 py-10">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(99,102,241,0.12),transparent_60%)]" />
      <LegacyClaim userId={user.id} />
      <div className="relative mx-auto w-full max-w-5xl space-y-8">
        <div className="space-y-4">
          <PageHeader
            eyebrow="Home"
            title="Ready to race?"
            description="Practice solo, duel a friend, or run a booth event."
          />
          <QuickActions practiceProblemId={practiceProblemId} />
        </div>

        <div className="grid grid-cols-3 gap-3">
          {[
            { label: "Problems solved", value: solvedProblems.size },
            { label: "Duel record", value: `${wins}–${losses}` },
            { label: "Solo solves this week", value: soloSolvesThisWeek },
          ].map((s) => (
            <Card key={s.label} className="border-border/60 bg-card/60">
              <CardContent className="p-4">
                <p className="font-mono text-2xl font-bold tabular-nums">
                  {s.value}
                </p>
                <p className="text-xs text-muted-foreground">{s.label}</p>
              </CardContent>
            </Card>
          ))}
        </div>

        <section className="space-y-3">
          <SectionTitle>Recent activity</SectionTitle>
          {sessions.length === 0 ? (
            <div className="flex flex-col items-center gap-3 rounded-lg border border-border/60 bg-card/60 py-8">
              <EmptyState className="p-0">
                No runs yet — solve your first problem to start your history.
              </EmptyState>
              {practiceProblemId && (
                <Button asChild size="sm">
                  <Link href={`/problems/${practiceProblemId}/solve`}>
                    Solve your first problem
                  </Link>
                </Button>
              )}
            </div>
          ) : (
            <div className="divide-y divide-border/60 rounded-lg border border-border/60 bg-card/60">
              {sessions.map((s) => (
                <div key={s.id} className="flex items-center gap-3 px-4 py-3">
                  <Link
                    href={`/problems/${s.problem_id}`}
                    className="font-mono text-sm text-primary hover:underline"
                  >
                    {s.problem_id}
                  </Link>
                  <Badge variant="outline" className="font-mono text-xs">
                    {s.kind}
                  </Badge>
                  <OutcomeBadge outcome={s.outcome} />
                  {s.outcome === "solved" && s.solve_ms !== null && (
                    <span className="font-mono text-xs text-green-400 tabular-nums">
                      {formatMsPrecise(s.solve_ms)}
                    </span>
                  )}
                  {shareBySession.get(s.id) && (
                    <Badge variant="outline" className="font-mono text-xs">
                      shared
                    </Badge>
                  )}
                  <span className="ml-auto font-mono text-xs text-muted-foreground">
                    {new Date(s.started_at).toLocaleDateString()}
                  </span>
                  <Button asChild size="sm" variant="ghost">
                    <Link href={`/replay/${s.id}`}>
                      <Video className="mr-1.5 h-3.5 w-3.5" />
                      Replay
                    </Link>
                  </Button>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
