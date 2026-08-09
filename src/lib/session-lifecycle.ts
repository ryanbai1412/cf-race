import { db, logDbError } from "./db";

/** Inactivity window after which an active session is considered abandoned. */
export const SESSION_IDLE_MS = 15 * 60 * 1000;

type SweepFilter = {
  userId?: string;
  sessionIds?: string[];
  problemId?: string;
};

/**
 * Lazily abandon active sessions that have been idle for 15+ minutes
 * (docs/flows/11-unified-app-detailed.md §5.1). Called from server reads so
 * stale runs never show as active; abandoned sessions keep their events and
 * recording but never count as solves.
 */
export async function sweepStaleSessions(filter?: SweepFilter): Promise<void> {
  const cutoff = new Date(Date.now() - SESSION_IDLE_MS).toISOString();
  let q = db()
    .from("sessions")
    .update({ outcome: "abandoned" })
    .is("outcome", null)
    .lt("last_event_at", cutoff);
  if (filter?.userId) q = q.eq("user_id", filter.userId);
  if (filter?.sessionIds) q = q.in("id", filter.sessionIds);
  if (filter?.problemId) q = q.eq("problem_id", filter.problemId);
  const { error } = await q;
  logDbError("sweepStaleSessions", error);
}

/**
 * Abandon a user's still-active solo runs on a problem — called when they
 * start a new run of the same problem (the new run supersedes the old one).
 * Only solo sessions: duel/event sessions on the same problem are owned by
 * their match/race lifecycle and must not be forfeited by a practice run.
 */
export async function abandonActiveSessions(args: {
  problemId: string;
  userId?: string | null;
  sessionIds?: string[];
}): Promise<void> {
  const { problemId, userId, sessionIds } = args;
  if (!userId && (!sessionIds || sessionIds.length === 0)) return;
  let q = db()
    .from("sessions")
    .update({ outcome: "abandoned" })
    .is("outcome", null)
    .eq("kind", "solo")
    .eq("problem_id", problemId);
  q = userId ? q.eq("user_id", userId) : q.in("id", sessionIds ?? []);
  const { error } = await q;
  logDbError("abandonActiveSessions", error);
}
