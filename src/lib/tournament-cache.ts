import { db, logDbError } from "./db";
import type { Problem } from "./types";
import {
  loadSnapshotByCode,
  tick,
  tickDue,
  type TournamentMemberRow,
  type TournamentSnapshot,
} from "./tournament";

/**
 * Per-instance caches for the tournament state poll. Every open tournament
 * page polls every few seconds; without these each poll costs several
 * PostgREST calls, and a few dozen viewers queued up enough of them to take
 * the REST layer down. With them, an instance costs about one snapshot read
 * per tournament per second however many viewers it serves.
 */

const SNAPSHOT_TTL_MS = 1000;
const PROBLEM_TTL_MS = 60_000;
const LAST_SEEN_WRITE_MS = 15_000;
const LAST_SEEN_FLUSH_MS = 5000;
const MAX_ENTRIES = 500;
const IN_FLIGHT_MAX_MS = 15_000;

type Entry<T> = { value: Promise<T>; startedAt: number; settledAt: number | null; settled?: T };

/** TTL cache that also coalesces concurrent loads of the same key. */
function memo<T>(
  cache: Map<string, Entry<T>>,
  key: string,
  ttlMs: number,
  load: () => Promise<T>,
  keep: (value: T) => boolean = () => true
): Promise<T> {
  const now = Date.now();
  const hit = cache.get(key);
  if (hit && (hit.settledAt === null ? now - hit.startedAt < IN_FLIGHT_MAX_MS : now - hit.settledAt < ttlMs)) {
    return hit.value;
  }
  if (cache.size >= MAX_ENTRIES) {
    cache.forEach((e, k) => {
      if (e.settledAt !== null && now - e.settledAt >= ttlMs) cache.delete(k);
    });
  }
  const entry: Entry<T> = { value: load(), startedAt: now, settledAt: null };
  cache.set(key, entry);
  const drop = () => {
    if (cache.get(key) === entry) cache.delete(key);
  };
  entry.value.then((v) => {
    if (!keep(v)) return drop();
    entry.settled = v;
    entry.settledAt = Date.now();
  }, drop);
  return entry.value;
}

const snapshots = new Map<string, Entry<TournamentSnapshot | null>>();

/** The viewer-independent snapshot, at most ~1s stale. Never caches misses or errors. */
export function cachedSnapshotByCode(code: string): Promise<TournamentSnapshot | null> {
  return memo(snapshots, code, SNAPSHOT_TTL_MS, () => loadSnapshotByCode(code), Boolean);
}

/**
 * Drop this instance's cached snapshot after a mutation, so the caller's
 * next poll sees it. Loads still in flight may predate the mutation, so
 * they go too.
 */
export function invalidateTournament(tournamentId: string): void {
  snapshots.forEach((entry, code) => {
    if (entry.settledAt === null || entry.settled?.tournament.id === tournamentId) {
      snapshots.delete(code);
    }
  });
}

type TickRun = { run: Promise<boolean>; startedAt: number };
const ticks = new Map<string, TickRun>();

/**
 * Run the lazy engine only when the snapshot says a transition is due, and
 * at most once at a time per tournament on this instance. Resolves true
 * when the tournament changed (the cache is already invalidated).
 */
export function tickIfDue(snap: TournamentSnapshot): Promise<boolean> {
  const id = snap.tournament.id;
  const running = ticks.get(id);
  if (running && Date.now() - running.startedAt < IN_FLIGHT_MAX_MS) return running.run;
  if (!tickDue(snap)) return Promise.resolve(false);
  const entry: TickRun = {
    startedAt: Date.now(),
    run: tick(id)
      .then((changed) => {
        if (changed) invalidateTournament(id);
        return changed;
      })
      .finally(() => {
        if (ticks.get(id) === entry) ticks.delete(id);
      }),
  };
  ticks.set(id, entry);
  return entry.run;
}

const unseen = new Map<string, Set<string>>();
const lastFlush = new Map<string, number>();

/**
 * Keep `last_seen_at` fresh enough for the online dot (45s window) with one
 * batched write per tournament every few seconds instead of one per member.
 */
export async function noteSeen(member: TournamentMemberRow): Promise<void> {
  const now = Date.now();
  if (now - Date.parse(member.last_seen_at) <= LAST_SEEN_WRITE_MS) return;
  const tid = member.tournament_id;
  const pending = unseen.get(tid) ?? new Set<string>();
  pending.add(member.id);
  unseen.set(tid, pending);
  if (now - (lastFlush.get(tid) ?? 0) < LAST_SEEN_FLUSH_MS) return;
  lastFlush.set(tid, now);
  unseen.delete(tid);
  const { error } = await db()
    .from("tournament_members")
    .update({ last_seen_at: new Date(now).toISOString() })
    .in("id", Array.from(pending));
  logDbError(`tournament: last_seen ${tid}`, error);
}

const problems = new Map<string, Entry<Problem | null>>();

export function cachedProblem(id: string): Promise<Problem | null> {
  return memo(
    problems,
    id,
    PROBLEM_TTL_MS,
    async () => {
      const { data, error } = await db()
        .from("problems")
        .select("*")
        .eq("id", id)
        .maybeSingle<Problem>();
      if (error) throw new Error(`cachedProblem: ${error.message}`);
      return data ?? null;
    },
    Boolean
  );
}
