import { loadSnapshot } from "./tournament";
import { tournamentTopic } from "./tournament-format";
import { buildPublicState } from "./tournament-view";

const PUBLISH_TIMEOUT_MS = 3000;
// Stays under the project's 256 KB Realtime payload cap; bigger states go out as a bare version nudge.
const MAX_STATE_BYTES = 200_000;

export type TournamentPush = { v: number; state?: Awaited<ReturnType<typeof buildPublicState>> };

const pending = new Map<string, { again: boolean; done: Promise<void> }>();

/**
 * Push the shared public state to every open tab of a tournament. Concurrent
 * calls for one tournament collapse into one follow-up publish, so the last
 * push always reflects the latest writes. Never throws.
 */
export function publishTournamentState(tournamentId: string): Promise<void> {
  const cur = pending.get(tournamentId);
  if (cur) {
    cur.again = true;
    return cur.done;
  }
  const entry = { again: false, done: Promise.resolve() };
  pending.set(tournamentId, entry);
  entry.done = (async () => {
    try {
      do {
        entry.again = false;
        try {
          await publishOnce(tournamentId);
        } catch (e) {
          console.error(`[tournament] publish ${tournamentId}:`, e);
        }
      } while (entry.again);
    } finally {
      pending.delete(tournamentId);
    }
  })();
  return entry.done;
}

async function publishOnce(tournamentId: string): Promise<void> {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) return;
  // Taken before the read so a later push never carries older data.
  const v = Date.now();
  const snap = await loadSnapshot(tournamentId);
  if (!snap) return;
  let push: TournamentPush = { v, state: await buildPublicState(snap) };
  if (JSON.stringify(push).length > MAX_STATE_BYTES) push = { v };
  const res = await fetch(`${url}/realtime/v1/api/broadcast`, {
    method: "POST",
    headers: { apikey: key, authorization: `Bearer ${key}`, "content-type": "application/json" },
    body: JSON.stringify({
      messages: [{ topic: tournamentTopic(tournamentId), event: "state", payload: push, private: true }],
    }),
    cache: "no-store",
    signal: AbortSignal.timeout(PUBLISH_TIMEOUT_MS),
  });
  if (!res.ok) throw new Error(`broadcast ${res.status}: ${(await res.text()).slice(0, 200)}`);
}
