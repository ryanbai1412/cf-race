import { NextRequest, NextResponse } from "next/server";
import { activeContestants } from "@/lib/contestants";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/event-auth";
import { gennaReference } from "@/lib/genna";
import { requireWebcam, selfServe } from "@/lib/event-settings";
import { activeRace, lastFinishedRace, selfServeAutoStart } from "@/lib/races";
import type { ClientState, RaceParticipantState } from "@/lib/types";

export const dynamic = "force-dynamic";

export async function GET(req: NextRequest) {
  const eventId = req.nextUrl.searchParams.get("eventId") ?? "";
  const event = await requireEvent(eventId);
  if (!event) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  // eslint-disable-next-line prefer-const
  let [race, active] = await Promise.all([
    activeRace(eventId),
    activeContestants(eventId, { excludeRetired: true }),
  ]);

  let autoStartAt: number | null = null;
  if (!race && selfServe(event.settings)) {
    const auto = await selfServeAutoStart(eventId, event.settings, active);
    autoStartAt = auto.autoStartAt;
    if (auto.started) race = await activeRace(eventId);
  }

  const [lastRace, gennaRef] = await Promise.all([
    race ? Promise.resolve(null) : lastFinishedRace(eventId),
    race ? gennaReference(race.problem_id) : Promise.resolve(null),
  ]);

  let lastRaceState: ClientState["lastRace"] = null;
  if (lastRace) {
    const participants = lastRace.participants as RaceParticipantState[];
    const ids = participants.map((p) => p.contestant_id);
    const [{ data: rows }, lastRef] = await Promise.all([
      ids.length > 0
        ? db().from("contestants").select("id, name, country").in("id", ids)
        : Promise.resolve({ data: [] }),
      gennaReference(lastRace.problem_id),
    ]);
    lastRaceState = {
      ...lastRace,
      contestants: Object.fromEntries(
        (rows ?? []).map((c) => [c.id, { name: c.name, country: c.country }])
      ),
      gennaSolveMs: lastRef?.solve_ms ?? null,
    };
  }

  const state: ClientState = {
    serverNow: Date.now(),
    event: {
      id: event.id,
      name: event.name,
      requireWebcam: requireWebcam(event.settings),
      selfServe: selfServe(event.settings),
    },
    contestants: active,
    autoStartAt,
    race: race ?? null,
    lastRace: lastRaceState,
    gennaSolveMs: gennaRef?.solve_ms ?? null,
  };
  return NextResponse.json(state);
}
