import { redirect } from "next/navigation";
import { getEffectiveUser } from "@/lib/impersonation";
import { db } from "@/lib/db";
import { sweepStaleSessions } from "@/lib/session-lifecycle";
import {
  SessionsList,
  type SessionListRow,
} from "@/components/sessions/sessions-list";

export const dynamic = "force-dynamic";

export default async function SessionsPage() {
  const user = await getEffectiveUser();
  if (!user) redirect("/?next=/sessions");

  await sweepStaleSessions({ userId: user.id });
  const { data: sessions } = await db()
    .from("sessions")
    .select("id, kind, problem_id, started_at, outcome, solve_ms, timer_sec")
    .eq("user_id", user.id)
    .order("started_at", { ascending: false })
    .limit(500);

  const ids = (sessions ?? []).map((s) => s.id);
  const shared = new Set<string>();
  if (ids.length > 0) {
    const { data: shares } = await db()
      .from("session_shares")
      .select("session_id")
      .in("session_id", ids)
      .is("revoked_at", null);
    for (const s of shares ?? []) shared.add(s.session_id);
  }

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
    <main className="mx-auto max-w-4xl px-6 py-10">
      <div className="mb-6 space-y-1">
        <h1 className="text-3xl font-bold tracking-tight">Sessions</h1>
        <p className="text-sm text-muted-foreground">
          Every run you&apos;ve made — replay or share any of them.
        </p>
      </div>
      <SessionsList sessions={rows} />
    </main>
  );
}
