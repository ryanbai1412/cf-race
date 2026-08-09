import { expect, test } from "@playwright/test";
import { api, refSolution, rest } from "./helpers";

/**
 * Event race invariants: booth cookie auth gates the APIs, only one race can
 * be active per event (DB-enforced), first AC stamps the participant +
 * session atomically, and finishing DQs the unsolved.
 */
const PROBLEM = "2024A";

type ParticipantRow = {
  station_role: string;
  first_ac_at: string | null;
  dq: boolean;
  session_id: string;
};

test("event race: join, race, one-active invariant, first AC, finish", async ({
  browser,
}) => {
  // Create the event and join two stations + admin through the secret link.
  const context = await browser.newContext();
  const page = await context.newPage();
  const created = await api<{ id: string; secret: string }>(
    page.request,
    "/api/events",
    { name: `e2e ${Date.now()}` }
  );
  expect(created.status).toBe(200);
  const { id: eventId, secret } = created.json;

  try {
    await page.goto(`/e/${eventId}/join?k=${secret}&to=/admin`);
    await page.waitForURL(`**/e/${eventId}/admin`);

    // Unauthorized access must be rejected: no cookie, no state.
    const bare = await browser.newContext();
    const noAuth = await bare.request.get(
      `http://localhost:3100/api/state?eventId=${eventId}`
    );
    expect(noAuth.status()).toBe(401);
    await bare.close();

    // Check in both stations (API — the cookie from join covers the event).
    const contestantByStation: Record<string, string> = {};
    for (const station of ["station1", "station2"] as const) {
      const res = await api<{ contestant: { id: string } }>(
        page.request,
        "/api/checkin",
        { eventId, station, name: `E2E ${station}`, country: "NL" }
      );
      expect(res.status).toBe(200);
      contestantByStation[station] = res.json.contestant.id;
    }

    // Start a race and prove the one-active-race invariant (409 on repeat).
    const start = await api<{ race: { id: string } }>(page.request, "/api/race/start", {
      eventId,
      problemId: PROBLEM,
      timerSec: 600,
    });
    expect(start.status).toBe(200);
    const raceId = start.json.race.id;
    const dupe = await api<{ error: string }>(page.request, "/api/race/start", {
      eventId,
      problemId: PROBLEM,
      timerSec: 600,
    });
    expect(dupe.status).toBe(409);

    // Both stations got universal sessions.
    const participants = await rest<ParticipantRow[]>(
      `race_participants?race_id=eq.${raceId}&select=station_role,first_ac_at,dq,session_id`
    );
    expect(participants).toHaveLength(2);
    expect(participants.every((p) => p.session_id)).toBe(true);

    // Wait out the 6s countdown, then station1 submits the reference AC.
    await page.waitForTimeout(6500);
    const submit = await api<{ verdict: string }>(page.request, "/api/submit", {
      eventId,
      raceId,
      contestantId: contestantByStation.station1,
      lang: "py",
      source: refSolution(PROBLEM),
    });
    expect(submit.status).toBe(200);
    expect(submit.json.verdict).toBe("AC");

    // First AC stamped on the participant AND its session, atomically.
    const after = await rest<ParticipantRow[]>(
      `race_participants?race_id=eq.${raceId}&select=station_role,first_ac_at,dq,session_id`
    );
    const winner = after.find((p) => p.station_role === "station1")!;
    const loser = after.find((p) => p.station_role === "station2")!;
    expect(winner.first_ac_at).not.toBeNull();
    expect(loser.first_ac_at).toBeNull();
    const [winnerSession] = await rest<{ outcome: string; solve_ms: number }[]>(
      `sessions?id=eq.${winner.session_id}&select=outcome,solve_ms`
    );
    expect(winnerSession.outcome).toBe("solved");
    expect(winnerSession.solve_ms).toBeGreaterThan(0);

    // The leaderboard surfaces the solve for this event.
    const lb = await page.request.get(
      `http://localhost:3100/api/leaderboard?eventId=${eventId}`
    );
    const rows = ((await lb.json()) as { rows: { race_id: string }[] }).rows;
    expect(rows.some((r) => r.race_id === raceId)).toBe(true);

    // Finish: the unsolved station is DQ'd and its session timed out.
    const finish = await api(page.request, "/api/race/finish", { eventId });
    expect(finish.status).toBe(200);
    const final = await rest<ParticipantRow[]>(
      `race_participants?race_id=eq.${raceId}&select=station_role,first_ac_at,dq,session_id`
    );
    expect(final.find((p) => p.station_role === "station2")!.dq).toBe(true);
    const [loserSession] = await rest<{ outcome: string }[]>(
      `sessions?id=eq.${loser.session_id}&select=outcome`
    );
    expect(loserSession.outcome).toBe("timeout");
  } finally {
    // Fixture cleanup: remove everything this test created.
    const races = await rest<{ id: string }[]>(
      `races?event_id=eq.${eventId}&select=id`
    );
    for (const r of races) {
      const ps = await rest<{ session_id: string }[]>(
        `race_participants?race_id=eq.${r.id}&select=session_id`
      );
      await rest(`race_participants?race_id=eq.${r.id}`, { method: "DELETE" });
      for (const p of ps) {
        await rest(`session_submissions?session_id=eq.${p.session_id}`, {
          method: "DELETE",
        });
        await rest(`session_events?session_id=eq.${p.session_id}`, {
          method: "DELETE",
        });
        await rest(`sessions?id=eq.${p.session_id}`, { method: "DELETE" });
      }
    }
    await rest(`races?event_id=eq.${eventId}`, { method: "DELETE" });
    await rest(`contestants?event_id=eq.${eventId}`, { method: "DELETE" });
    await rest(`events?id=eq.${eventId}`, { method: "DELETE" });
    await context.close();
  }
});
