import { db } from "./db";
import type { Contestant, StationRole } from "./types";

/**
 * The active contestant per station: the most recently checked-in,
 * non-retired one (pass `retiredOnly: false` to include retired rows,
 * matching race-start semantics).
 */
export async function activeContestants(
  eventId: string,
  opts: { excludeRetired?: boolean } = {}
): Promise<Partial<Record<StationRole, Contestant>>> {
  let q = db()
    .from("contestants")
    .select("*")
    .eq("event_id", eventId)
    .order("created_at", { ascending: false });
  if (opts.excludeRetired) q = q.is("retired_at", null);
  const { data } = await q;
  const active: Partial<Record<StationRole, Contestant>> = {};
  for (const c of (data ?? []) as Contestant[]) {
    if (!active[c.station_role]) active[c.station_role] = c;
  }
  return active;
}
