import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import { getEffectiveUser } from "@/lib/impersonation";
import { db } from "@/lib/db";
import { sweepStaleSessions } from "@/lib/session-lifecycle";
import { StatementPane } from "@/components/race/statement-pane";
import { InvalidateToggle } from "@/components/problems/invalidate-toggle";
import { StarRating } from "@/components/problems/star-rating";
import { OutcomeBadge } from "@/components/shell/outcome-badge";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { formatMsPrecise } from "@/lib/templates";
import type { Problem } from "@/lib/types";
import {
  EmptyState,
  PageHeader,
  PageShell,
  SectionTitle,
} from "@/components/shell/page";
import { ArrowLeft, Play, Video } from "lucide-react";

export const dynamic = "force-dynamic";

type SessionHistoryRow = {
  id: string;
  kind: string;
  started_at: string;
  outcome: "solved" | "timeout" | "abandoned" | null;
  solve_ms: number | null;
};

export default async function ProblemDetailPage({
  params,
}: {
  params: { id: string };
}) {
  const user = await getEffectiveUser();
  if (!user) redirect(`/?next=/problems/${params.id}`);

  const { data: problem } = await db()
    .from("problems")
    .select("*")
    .eq("id", params.id)
    .maybeSingle<Problem & { tags: string[] | null }>();
  if (!problem || (problem.tags ?? []).includes("hidden")) notFound();

  const [{ data: sessions }, { data: invalidation }, { data: myRating }, { data: allRatings }] = await Promise.all([
    db()
      .from("sessions")
      .select("id, kind, started_at, outcome, solve_ms")
      .eq("user_id", user.id)
      .eq("problem_id", problem.id)
      .order("started_at", { ascending: false })
      .limit(100),
    db()
      .from("problem_invalidations")
      .select("reason, by_user, created_at")
      .eq("problem_id", problem.id)
      .is("revoked_at", null)
      .maybeSingle(),
    db()
      .from("problem_ratings")
      .select("stars")
      .eq("user_id", user.id)
      .eq("problem_id", problem.id)
      .maybeSingle(),
    db()
      .from("problem_ratings")
      .select("stars")
      .eq("problem_id", problem.id),
    sweepStaleSessions({ userId: user.id, problemId: problem.id }),
  ]);

  const ratings = (allRatings ?? []) as { stars: number }[];
  const avgStars =
    ratings.length > 0
      ? ratings.reduce((a, r) => a + r.stars, 0) / ratings.length
      : null;

  const history = (sessions ?? []) as SessionHistoryRow[];

  return (
    <PageShell className="space-y-6">
      <Button asChild size="sm" variant="ghost" className="-ml-3">
        <Link href="/problems">
          <ArrowLeft className="mr-1.5 h-3.5 w-3.5" />
          Problems
        </Link>
      </Button>

      <PageHeader
        eyebrow={problem.id}
        title={
          <span className="flex flex-wrap items-center gap-3">
            {problem.name}
            {problem.rating !== null && (
              <Badge variant="outline" className="font-mono text-xs">
                {problem.rating}
              </Badge>
            )}
          </span>
        }
        description={
          <span className="flex items-center gap-2">
            {history.some((s) => s.outcome === "solved") && (
              <StarRating
                problemId={problem.id}
                initial={myRating?.stars ?? null}
              />
            )}
            {avgStars !== null && (
              <span className="font-mono text-xs text-muted-foreground">
                avg {avgStars.toFixed(1)} ({ratings.length})
              </span>
            )}
          </span>
        }
        actions={
          <>
            <InvalidateToggle
              problemId={problem.id}
              invalidated={invalidation !== null}
            />
            <Button asChild size="sm">
              <Link href={`/problems/${problem.id}/solve`}>
                <Play className="mr-1.5 h-3.5 w-3.5" />
                Solve
              </Link>
            </Button>
          </>
        }
      />

      {invalidation && (
        <div className="rounded-md border border-amber-500/50 bg-amber-500/10 px-4 py-3 text-sm text-amber-400">
          Invalidated {new Date(invalidation.created_at).toLocaleDateString()} —
          excluded from duel and practice picks.
          {invalidation.reason && <> Reason: {invalidation.reason}</>}
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-[1fr_320px]">
        <div className="h-[60vh] overflow-hidden rounded-lg border border-border/60 bg-card/40">
          <StatementPane problem={problem} />
        </div>

        <section className="space-y-3">
          <SectionTitle>Your sessions</SectionTitle>
          {history.length === 0 ? (
            <div className="rounded-lg border border-border/60 bg-card/60">
              <EmptyState>No runs yet.</EmptyState>
            </div>
          ) : (
            <div className="divide-y divide-border/60 rounded-lg border border-border/60 bg-card/60">
              {history.map((s) => (
                <div
                  key={s.id}
                  className="flex min-w-0 flex-wrap items-center gap-2 px-3 py-2.5"
                >
                  <Badge variant="muted" className="font-mono text-xs">
                    {s.kind}
                  </Badge>
                  <OutcomeBadge outcome={s.outcome} />
                  {s.outcome === "solved" && s.solve_ms !== null && (
                    <span className="font-mono text-xs text-green-400 tabular-nums">
                      {formatMsPrecise(s.solve_ms)}
                    </span>
                  )}
                  <span className="ml-auto font-mono text-xs text-muted-foreground">
                    {new Date(s.started_at).toLocaleString([], {
                      dateStyle: "short",
                      timeStyle: "short",
                    })}
                  </span>
                  <Button asChild size="sm" variant="ghost">
                    <Link href={`/replay/${s.id}`} aria-label="Watch replay">
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
    </PageShell>
  );
}
