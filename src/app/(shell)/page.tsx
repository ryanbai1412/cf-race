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
import { formatMsPrecise } from "@/lib/templates";
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
  const practiceProblemId = await pickPracticeProblem(user?.id);

  if (!user) {
    const next =
      typeof searchParams.next === "string" && searchParams.next.startsWith("/")
        ? searchParams.next
        : "/";
    return <Landing next={next} practiceProblemId={practiceProblemId} />;
  }

  await sweepStaleSessions({ userId: user.id });
  const [{ data: recent }, { data: solvedRows }, { data: myPlayers }] =
    await Promise.all([
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
      db().from("duel_players").select("match_id").eq("user_id", user.id),
    ]);

  const sessions = (recent ?? []) as RecentSession[];
  const shareBySession = new Map<string, boolean>();
  if (sessions.length > 0) {
    const { data: shares } = await db()
      .from("session_shares")
      .select("session_id")
      .in(
        "session_id",
        sessions.map((s) => s.id)
      )
      .is("revoked_at", null);
    for (const s of shares ?? []) shareBySession.set(s.session_id, true);
  }

  const solvedProblems = new Set((solvedRows ?? []).map((s) => s.problem_id));
  const weekAgo = Date.now() - 7 * 24 * 3600 * 1000;
  const soloSolvesThisWeek = (solvedRows ?? []).filter(
    (s) => s.kind === "solo" && new Date(s.started_at).getTime() > weekAgo
  ).length;

  const matchIds = (myPlayers ?? []).map((p) => p.match_id);
  let wins = 0;
  let losses = 0;
  if (matchIds.length > 0) {
    const { data: matches } = await db()
      .from("duel_matches")
      .select("id, winner_user_id, finished_at")
      .in("id", matchIds)
      .not("finished_at", "is", null);
    for (const m of matches ?? []) {
      if (m.winner_user_id === user.id) wins += 1;
      else if (m.winner_user_id !== null) losses += 1;
    }
  }

  return (
    <main className="relative min-h-[calc(100vh-3.5rem)] overflow-hidden px-6 py-10">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(99,102,241,0.12),transparent_60%)]" />
      <LegacyClaim userId={user.id} />
      <div className="relative mx-auto max-w-4xl space-y-8">
        <div className="space-y-4">
          <h1 className="text-3xl font-bold tracking-tight">Ready to race?</h1>
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
          <h2 className="text-lg font-semibold">Recent activity</h2>
          {sessions.length === 0 ? (
            <Card className="border-border/60 bg-card/60">
              <CardContent className="flex flex-col items-start gap-3 p-6">
                <p className="text-muted-foreground">
                  No runs yet — solve your first problem to start your history.
                </p>
                {practiceProblemId && (
                  <Button asChild>
                    <Link href={`/problems/${practiceProblemId}/solve`}>
                      Solve your first problem
                    </Link>
                  </Button>
                )}
              </CardContent>
            </Card>
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
