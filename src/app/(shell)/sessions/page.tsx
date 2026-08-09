import { redirect } from "next/navigation";
import { getEffectiveUser } from "@/lib/impersonation";
import { db } from "@/lib/db";
import { sweepStaleSessions } from "@/lib/session-lifecycle";
import {
  SessionsList,
  type SessionListRow,
} from "@/components/sessions/sessions-list";
import { PageHeader, PageShell } from "@/components/shell/page";

export const dynamic = "force-dynamic";

export default async function SessionsPage() {
  const user = await getEffectiveUser();
  if (!user) redirect("/?next=/sessions");

  const [{ data: sessions }, { data: shares }] = await Promise.all([
    db()
      .from("sessions")
      .select("id, kind, problem_id, started_at, outcome, solve_ms, timer_sec")
      .eq("user_id", user.id)
      .order("started_at", { ascending: false })
      .limit(500),
    db()
      .from("session_shares")
      .select("session_id, sessions!inner(user_id)")
      .eq("sessions.user_id", user.id)
      .is("revoked_at", null),
    sweepStaleSessions({ userId: user.id }),
  ]);

  const shared = new Set<string>((shares ?? []).map((s) => s.session_id));

  const rows: SessionListRow[] = (sessions ?? []).map((s) => ({
    id: s.id,
    kind: s.kind,
    problemId: s.problem_id,
    startedAt: s.started_at,
    outcome: s.outcome,
    solveMs: s.solve_ms,
    timerSec: s.timer_sec,
    shared: shared.has(s.id),
  }));

  return (
    <PageShell>
      <PageHeader
        eyebrow="History"
        title="Sessions"
        description={<>Every run you&apos;ve made — replay or share any of them.</>}
      />
      <SessionsList sessions={rows} />
    </PageShell>
  );
}
