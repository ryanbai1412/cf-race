import { activeContestants } from "./contestants";
import { db, logDbError } from "./db";
import { eventTimerSec, gennaOnly } from "./event-settings";
import { notifyEvent } from "./notify";
import { pickPracticeProblem } from "./problem-bank";
import type { Contestant, StationRole } from "./types";

/** 5-4-3-2-1 plus a "GO!" beat; the race clock starts when the overlay clears. */
export const RACE_COUNTDOWN_MS = 6000;

/** Self-serve mode: un-ready window between both-ready and race start. */
export const SELF_SERVE_START_DELAY_MS = 5000;

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
    .select("id")
    .eq("id", problemId)
    .maybeSingle();
  if (!problem) return fail("unknown problem", 400);

  const { data: event } = await db()
    .from("events")
    .select("settings")
    .eq("id", eventId)
    .maybeSingle();
  if (gennaOnly(event?.settings)) {
    const { data: ref } = await db()
      .from("genna_problems")
      .select("problem_id")
      .eq("problem_id", problemId)
      .maybeSingle();
    if (!ref) {
      return fail("problem has no Genna reference session", 400);
    }
  }

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
      timer_sec: timerSec ?? eventTimerSec(event?.settings),
    })
    .select("*")
    .single();
  if (error) {
    // The partial unique index (one unfinished race per event) turns a lost
    // start race into a constraint violation.
    if (error.code === "23505") return fail("a race is already active", 409);
    return fail(error.message, 500);
  }

  // Session ids are minted here rather than read back from the insert: a
  // multi-row INSERT … RETURNING gives no ordering guarantee, so pairing
  // participants with returned rows positionally could hand a station the
  // other station's session (and with it its replay and recording).
  const sessionIds = participants.map(() => crypto.randomUUID());
  const { error: sErr } = await db()
    .from("sessions")
    .insert(
      participants.map((_c, i) => ({
        id: sessionIds[i],
        kind: "event",
        problem_id: problemId,
        started_at: startedAt,
        timer_sec: race.timer_sec,
      }))
    );
  if (sErr) {
    await db().from("races").delete().eq("id", race.id);
    return fail(sErr.message, 500);
  }

  const { error: pErr } = await db()
    .from("race_participants")
    .insert(
      participants.map((c, i) => ({
        race_id: race.id,
        contestant_id: c.id,
        station_role: c.station_role,
        session_id: sessionIds[i],
      }))
    );
  if (pErr) {
    // Don't leave an active race without participants — it would block
    // future starts and no station would ever join it.
    await db().from("races").delete().eq("id", race.id);
    await db().from("sessions").delete().in("id", sessionIds);
    return fail(pErr.message, 500);
  }

  const { error: readyErr } = await db()
    .from("contestants")
    .update({ ready_at: null })
    .eq("event_id", eventId)
    .not("ready_at", "is", null);
  logDbError(`startRace: clear ready ${eventId}`, readyErr);

  await notifyEvent(eventId, { type: "state_changed" });
  return { ok: true, race };
}

/**
 * Self-serve auto-start: while both stations are ready and no race is active,
 * the race starts SELF_SERVE_START_DELAY_MS after the last ready-up (players
 * can un-ready during that window). Returns the pending start moment, plus
 * the race if the deadline has passed and one was just started.
 */
export async function selfServeAutoStart(
  eventId: string,
  settings: unknown,
  contestants: Partial<Record<StationRole, Contestant>>
): Promise<{ autoStartAt: number | null; started: boolean }> {
  const s1 = contestants.station1;
  const s2 = contestants.station2;
  if (!s1?.ready_at || !s2?.ready_at) return { autoStartAt: null, started: false };
  const autoStartAt =
    Math.max(new Date(s1.ready_at).getTime(), new Date(s2.ready_at).getTime()) +
    SELF_SERVE_START_DELAY_MS;
  if (Date.now() < autoStartAt) return { autoStartAt, started: false };
  let problemId: string | null = null;
  if (gennaOnly(settings)) {
    const [{ data: refs }, { data: played }] = await Promise.all([
      db().from("genna_problems").select("problem_id"),
      db().from("races").select("problem_id").eq("event_id", eventId),
    ]);
    const all = (refs ?? []).map((r) => r.problem_id as string);
    const used = new Set((played ?? []).map((r) => r.problem_id as string));
    // Prefer problems this event hasn't raced yet; cycle when exhausted.
    const pool = all.filter((id) => !used.has(id));
    const ids = pool.length > 0 ? pool : all;
    problemId = ids.length > 0 ? ids[Math.floor(Math.random() * ids.length)] : null;
  } else {
    problemId = await pickPracticeProblem(null);
  }
  if (!problemId) return { autoStartAt: null, started: false };
  // Concurrent polls may race here; the one-active-race unique index makes
  // the duplicate start a harmless 409.
  const result = await startRace({ eventId, problemId, timerSec: null });
  return { autoStartAt: null, started: result.ok };
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
    const { error: finishErr } = await db()
      .from("races")
      .update({ state: "finished" })
      .eq("id", race.id);
    logDbError(`finishRace: finish ${race.id}`, finishErr);
    const { error: dqErr } = await db()
      .from("race_participants")
      .update({ dq: true })
      .eq("race_id", race.id)
      .is("first_ac_at", null);
    logDbError(`finishRace: dq ${race.id}`, dqErr);
    const unsolved = (
      race.participants as { session_id: string | null; first_ac_at: string | null }[]
    )
      .filter((p) => p.session_id && !p.first_ac_at)
      .map((p) => p.session_id as string);
    if (unsolved.length > 0) {
      const { error: timeoutErr } = await db()
        .from("sessions")
        .update({ outcome: "timeout" })
        .in("id", unsolved)
        .is("outcome", null);
      logDbError(`finishRace: timeout sessions ${race.id}`, timeoutErr);
    }
  }
  const { error: retireErr } = await db()
    .from("contestants")
    .update({ retired_at: new Date().toISOString() })
    .eq("event_id", eventId)
    .is("retired_at", null);
  logDbError(`finishRace: retire contestants ${eventId}`, retireErr);
  await notifyEvent(eventId, { type: "state_changed" });
}

/**
 * The event's active race (with problem + participants), lazily transitioning
 * countdown → running once the start time has passed and running → finished
 * once every participant is done (AC) or the timer has expired. Contestants
 * are NOT retired on auto-finish — they go back to warm-up for the next race.
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
  if (!race) return null;
  const startMs = race.started_at ? new Date(race.started_at).getTime() : null;
  if (race.state === "countdown" && startMs !== null && startMs <= Date.now()) {
    race.state = "running";
    // Guarded on the state we read: two polls overlap here, and an
    // unconditional write could put a just-finished race back to running.
    await db()
      .from("races")
      .update({ state: "running" })
      .eq("id", race.id)
      .eq("state", "countdown");
  }
  if (race.state === "running" && startMs !== null) {
    const participants = race.participants as RaceParticipantRow[];
    const timeUp = Date.now() > startMs + race.timer_sec * 1000;
    const allDone =
      participants.length > 0 &&
      participants.every((p) => p.first_ac_at || p.dq);
    if (timeUp || allDone) {
      const closed = await autoFinishRace(race.id, participants);
      race.state = "finished";
      // Only the poll that actually closed the race announces it, so both
      // stations' polls don't each fan out a state change.
      if (closed) await notifyEvent(eventId, { type: "state_changed" });
      return null;
    }
  }
  return race;
}

/**
 * Close a race without retiring contestants (self-serve flow). Returns true
 * for the caller that actually closed it.
 */
async function autoFinishRace(
  raceId: string,
  participants: RaceParticipantRow[]
): Promise<boolean> {
  const { data: closed, error: finishErr } = await db()
    .from("races")
    .update({ state: "finished" })
    .eq("id", raceId)
    .neq("state", "finished")
    .select("id")
    .maybeSingle();
  logDbError(`autoFinishRace: finish ${raceId}`, finishErr);
  const unsolved = participants
    .filter((p) => p.session_id && !p.first_ac_at)
    .map((p) => p.session_id as string);
  if (unsolved.length > 0) {
    const { error: timeoutErr } = await db()
      .from("sessions")
      .update({ outcome: "timeout" })
      .in("id", unsolved)
      .is("outcome", null);
    logDbError(`autoFinishRace: timeout sessions ${raceId}`, timeoutErr);
  }
  return closed !== null;
}

/**
 * The event's most recent finished race (with problem + participants), for
 * the REVIEWING state on monitors and stations.
 */
export async function lastFinishedRace(eventId: string) {
  const { data: race } = await db()
    .from("races")
    .select("*, problem:problems(*), participants:race_participants(*)")
    .eq("event_id", eventId)
    .eq("state", "finished")
    .order("created_at", { ascending: false })
    .limit(1)
    .maybeSingle();
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
