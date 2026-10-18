import { loadSnapshot, loadTournamentByCode, tick, type TournamentRow, type TournamentSnapshot } from "./tournament";

/**
 * Per-instance read cache for the state poll. Every open tournament tab polls,
 * so concurrent viewers share one DB read per tournament per TTL; a pending
 * load is shared rather than duplicated.
 */
export const STATE_CACHE_TTL_MS = 1000;
const MAX_ENTRIES = 500;
const TICK_EVERY_MS = 1000;

type Entry<T> = { resolvedAt: number | null; value: Promise<T> };

function memo<T>(map: Map<string, Entry<T>>, key: string, fresh: boolean, load: () => Promise<T>): Promise<T> {
  const hit = map.get(key);
  if (hit && (hit.resolvedAt === null || (!fresh && Date.now() - hit.resolvedAt < STATE_CACHE_TTL_MS))) {
    return hit.value;
  }
  if (map.size > MAX_ENTRIES) map.clear();
  const entry: Entry<T> = { resolvedAt: null, value: load() };
  map.set(key, entry);
  entry.value.then(
    () => {
      entry.resolvedAt = Date.now();
    },
    () => {
      if (map.get(key) === entry) map.delete(key);
    }
  );
  return entry.value;
}

const byCode = new Map<string, Entry<TournamentRow | null>>();
const snapshots = new Map<string, Entry<TournamentSnapshot | null>>();
const lastTick = new Map<string, number>();

export function cachedTournamentByCode(code: string, fresh: boolean) {
  return memo(byCode, code, fresh, () => loadTournamentByCode(code));
}

export function cachedSnapshot(tournamentId: string, fresh: boolean) {
  return memo(snapshots, tournamentId, fresh, () => loadSnapshot(tournamentId));
}

export async function throttledTick(tournamentId: string, fresh: boolean): Promise<void> {
  const now = Date.now();
  if (!fresh && now - (lastTick.get(tournamentId) ?? 0) < TICK_EVERY_MS) return;
  if (lastTick.size > MAX_ENTRIES) lastTick.clear();
  lastTick.set(tournamentId, now);
  await tick(tournamentId);
}
