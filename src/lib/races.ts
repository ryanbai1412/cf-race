import { activeContestants } from "./contestants";
import { db } from "./db";
import { notifyEvent } from "./notify";
import type { StationRole } from "./types";

/** 5-4-3-2-1 plus a "GO!" beat; the race clock starts when the overlay clears. */
export const RACE_COUNTDOWN_MS = 6000;

export type ServiceError = { ok: false; error: string; status: number };
const fail = (error: string, status: number): ServiceError => ({
  ok: false,
  error,
  status,
});

export type RaceParticipantRow = {
  race_id: string;
  contestant_id: string;
  station_role: StationRole;
  first_ac_at: string | null;
  dq: boolean;
  session_id: string | null;
};

/**
 * Start a race for an event: active contestants become participants and each
 * participant gets a `sessions` row (kind='event') that carries its replay
 * stream, submissions, and webcam recording.
 */
export async function startRace(args: {
  eventId: string;
  problemId: string;
  timerSec: number | null;
}): Promise<{ ok: true; race: Record<string, unknown> } | ServiceError> {
  const { eventId, problemId, timerSec } = args;

  const { data: problem } = await db()
    .from("problems")
    .select("id, race_timer_sec")
    .eq("id", problemId)
    .maybeSingle();
  if (!problem) return fail("unknown problem", 400);

  const { data: existing } = await db()
    .from("races")
    .select("id")
    .eq("event_id", eventId)
    .neq("state", "finished")
    .limit(1);
  if (existing && existing.length > 0) {
    return fail("a race is already active", 409);
  }

  const active = await activeContestants(eventId);
  const participants = Object.values(active);
  if (participants.length === 0) {
    return fail("no contestants checked in", 400);
  }

  const startedAt = new Date(Date.now() + RACE_COUNTDOWN_MS).toISOString();
  const { data: race, error } = await db()
    .from("races")
    .insert({
      event_id: eventId,
      problem_id: problemId,
      state: "countdown",
      started_at: startedAt,
      timer_sec: timerSec ?? problem.race_timer_sec,
    })
    .select("*")
    .single();
  if (error) {
    // The partial unique index (one unfinished race per event) turns a lost
    // start race into a constraint violation.
    if (error.code === "23505") return fail("a race is already active", 409);
    return fail(error.message, 500);
  }

  const { data: sessions, error: sErr } = await db()
    .from("sessions")
    .insert(
      participants.map(() => ({
        kind: "event",
        problem_id: problemId,
        started_at: startedAt,
        timer_sec: race.timer_sec,
      }))
    )
    .select("id");
  if (sErr || !sessions || sessions.length !== participants.length) {
    await db().from("races").delete().eq("id", race.id);
    return fail(sErr?.message ?? "failed to create sessions", 500);
  }

  const { error: pErr } = await db()
    .from("race_participants")
    .insert(
      participants.map((c, i) => ({
        race_id: race.id,
        contestant_id: c.id,
        station_role: c.station_role,
        session_id: sessions[i].id,
      }))
    );
  if (pErr) {
    // Don't leave an active race without participants — it would block
    // future starts and no station would ever join it.
    await db().from("races").delete().eq("id", race.id);
    return fail(pErr.message, 500);
  }

  await notifyEvent(eventId, { type: "state_changed" });
  return { ok: true, race };
}

/**
 * Finish/reset the active race: mark it finished, DQ participants without an
 * AC, time out their sessions, and retire all contestants.
 */
export async function finishRace(eventId: string): Promise<void> {
  const { data: race } = await db()
    .from("races")
    .select("id, participants:race_participants(session_id, first_ac_at)")
    .eq("event_id", eventId)
    .neq("state", "finished")
    .order("created_at", { ascending: false })
    .limit(1)
    .maybeSingle();
  if (race) {
    await db().from("races").update({ state: "finished" }).eq("id", race.id);
    await db()
      .from("race_participants")
      .update({ dq: true })
      .eq("race_id", race.id)
      .is("first_ac_at", null);
    const unsolved = (
      race.participants as { session_id: string | null; first_ac_at: string | null }[]
    )
      .filter((p) => p.session_id && !p.first_ac_at)
      .map((p) => p.session_id as string);
    if (unsolved.length > 0) {
      await db()
        .from("sessions")
        .update({ outcome: "timeout" })
        .in("id", unsolved)
        .is("outcome", null);
    }
  }
  await db()
    .from("contestants")
    .update({ retired_at: new Date().toISOString() })
    .eq("event_id", eventId)
    .is("retired_at", null);
  await notifyEvent(eventId, { type: "state_changed" });
}

/**
 * The event's active race (with problem + participants), lazily transitioning
 * countdown → running once the start time has passed.
 */
export async function activeRace(eventId: string) {
  const { data: race } = await db()
    .from("races")
    .select("*, problem:problems(*), participants:race_participants(*)")
    .eq("event_id", eventId)
    .neq("state", "finished")
    .order("created_at", { ascending: false })
    .limit(1)
    .maybeSingle();
  if (
    race &&
    race.state === "countdown" &&
    race.started_at &&
    new Date(race.started_at).getTime() <= Date.now()
  ) {
    race.state = "running";
    await db().from("races").update({ state: "running" }).eq("id", race.id);
  }
  return race ?? null;
}

/** A race participant (with its session id) looked up by station role. */
export async function raceParticipantByStation(
  eventId: string,
  raceId: string,
  station: StationRole
): Promise<{ race: Record<string, unknown>; participant: RaceParticipantRow } | null> {
  const found = await raceWithParticipants(eventId, raceId);
  if (!found) return null;
  const participant = found.participants.find((p) => p.station_role === station);
  if (!participant) return null;
  return { race: found.race, participant };
}

/** A race (scoped to its event) with typed participants. */
export async function raceWithParticipants(
  eventId: string,
  raceId: string
): Promise<{
  race: Record<string, unknown> & {
    problem_id: string;
    state: string;
    started_at: string | null;
    timer_sec: number;
  };
  participants: RaceParticipantRow[];
} | null> {
  const { data: race } = await db()
    .from("races")
    .select("*, participants:race_participants(*)")
    .eq("id", raceId)
    .eq("event_id", eventId)
    .maybeSingle();
  if (!race) return null;
  const { participants, ...rest } = race;
  return { race: rest, participants: participants as RaceParticipantRow[] };
}
