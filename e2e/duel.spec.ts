import { expect, test } from "@playwright/test";
import {
  WA_SOLUTION,
  api,
  judgeHasProblem,
  problemsWithRef,
  refSolution,
  rest,
  signInTestUser,
} from "./helpers";

/**
 * Duel invariants: the problem stays hidden until GO, the first AC wins
 * (atomic winner stamp — a later AC can't steal it), a grace-window AC still
 * counts as solved, and the duel-specific 10-submission cap holds.
 */
const USER_A = "duel-tester-a@example.com";
const USER_B = "duel-tester-b@example.com";

test("duel: ready-up, hidden problem, first AC wins, grace AC counts", async ({
  browser,
}) => {
  test.setTimeout(300_000);

  const ctxA = await browser.newContext();
  const ctxB = await browser.newContext();
  const { userId: idA } = await signInTestUser(ctxA, USER_A);
  const { userId: idB } = await signInTestUser(ctxB, USER_B);
  const pageA = await ctxA.newPage();
  const pageB = await ctxB.newPage();

  // Force a deterministic problem pick: temporarily invalidate every problem
  // except one target with a local ref solution the pair hasn't played.
  const all = await rest<{ id: string }[]>("problems?select=id");
  const playedA = await rest<{ match_id: string }[]>(
    `duel_players?user_id=eq.${idA}&select=match_id`
  );
  const playedMatches = playedA.map((p) => p.match_id);
  const playedProblems = new Set<string>(
    playedMatches.length
      ? (
          await rest<{ problem_id: string }[]>(
            `duel_matches?id=in.(${playedMatches.join(",")})&select=problem_id`
          )
        ).map((m) => m.problem_id)
      : []
  );
  const solved = await rest<{ problem_id: string }[]>(
    `sessions?user_id=in.(${idA},${idB})&outcome=eq.solved&select=problem_id`
  );
  const solvedSet = new Set(solved.map((s) => s.problem_id));
  let target: string | undefined;
  for (const id of problemsWithRef()) {
    if (playedProblems.has(id) || solvedSet.has(id) || id === "warmup-sum") continue;
    if (await judgeHasProblem(id)) {
      target = id;
      break;
    }
  }
  expect(target).toBeTruthy();
  const others = all
    .map((p) => p.id)
    .filter((id) => id !== target);
  await rest("problem_invalidations", {
    method: "POST",
    body: others.map((problem_id) => ({
      problem_id,
      reason: "e2e-fixture",
    })),
  });

  let roomId = "";
  let matchId = "";
  try {
    // Create + join the room.
    const created = await api<{ roomId: string }>(pageA.request, "/api/duel/create", {});
    expect(created.status).toBe(200);
    roomId = created.json.roomId;
    const joined = await api(pageB.request, "/api/duel/join", { roomId });
    expect(joined.status).toBe(200);

    // Both ready → the match starts server-side.
    const readyA = await api(pageA.request, "/api/duel/ready", { roomId, ready: true });
    expect(readyA.status).toBe(200);
    const readyB = await api<{ started: boolean }>(pageB.request, "/api/duel/ready", {
      roomId,
      ready: true,
    });
    expect(readyB.status).toBe(200);
    expect(readyB.json.started).toBe(true);

    // Before GO the problem must be hidden from /state.
    const early = await pageA.request.get(
      `http://localhost:3100/api/duel/state?roomId=${roomId}`
    );
    const earlyState = (await early.json()) as {
      match: { id: string; startAtMs: number; problem: unknown; yourSessionId: string };
    };
    matchId = earlyState.match.id;
    if (Date.now() < earlyState.match.startAtMs) {
      expect(earlyState.match.problem).toBeNull();
    }

    // Fixture rows served their purpose once the problem is stamped.
    await rest(`problem_invalidations?reason=eq.e2e-fixture`, { method: "DELETE" });
    const [match] = await rest<{ problem_id: string }[]>(
      `duel_matches?id=eq.${matchId}&select=problem_id`
    );
    expect(match.problem_id).toBe(target);

    // Wait for GO, get both session ids.
    await pageA.waitForTimeout(3500);
    const stateA = (await (
      await pageA.request.get(`http://localhost:3100/api/duel/state?roomId=${roomId}`)
    ).json()) as { match: { yourSessionId: string } };
    const stateB = (await (
      await pageB.request.get(`http://localhost:3100/api/duel/state?roomId=${roomId}`)
    ).json()) as { match: { yourSessionId: string } };
    const sessionA = stateA.match.yourSessionId;
    const sessionB = stateB.match.yourSessionId;
    expect(sessionA).toBeTruthy();
    expect(sessionB).toBeTruthy();
    expect(sessionA).not.toBe(sessionB);

    // A cannot submit through B's session (ownership).
    const stolen = await api<{ error: string }>(pageA.request, "/api/duel/submit", {
      sessionId: sessionB,
      lang: "py",
      source: WA_SOLUTION,
    });
    expect(stolen.status).toBe(403);

    // A ACs first → winner. B ACs in the grace window → solved, NOT winner.
    const acA = await api<{ verdict: string }>(pageA.request, "/api/duel/submit", {
      sessionId: sessionA,
      lang: "py",
      source: refSolution(target!),
    });
    expect(acA.json.verdict, JSON.stringify(acA.json)).toBe("AC");
    const acB = await api<{ verdict: string }>(pageB.request, "/api/duel/submit", {
      sessionId: sessionB,
      lang: "py",
      source: refSolution(target!),
    });
    expect(acB.json.verdict, JSON.stringify(acB.json)).toBe("AC");

    const [finalMatch] = await rest<
      { winner_user_id: string; first_ac_at: string }[]
    >(`duel_matches?id=eq.${matchId}&select=winner_user_id,first_ac_at`);
    expect(finalMatch.first_ac_at).not.toBeNull();
    expect(finalMatch.winner_user_id).toBe(idA);
    const sessions = await rest<{ id: string; outcome: string }[]>(
      `sessions?id=in.(${sessionA},${sessionB})&select=id,outcome`
    );
    expect(sessions.every((s) => s.outcome === "solved")).toBe(true);

    // Duel cap is 10 (not solo's 50): fill and prove the trigger holds.
    const capSession = sessionB;
    await rest(`session_submissions?session_id=eq.${capSession}`, {
      method: "DELETE",
    });
    await rest("session_submissions", {
      method: "POST",
      body: Array.from({ length: 10 }, () => ({
        session_id: capSession,
        kind: "submit",
        lang: "py",
        source: "pass",
        verdict: "WA",
      })),
    });
    const overRes = await fetch(
      `${process.env.NEXT_PUBLIC_SUPABASE_URL}/rest/v1/session_submissions`,
      {
        method: "POST",
        headers: {
          apikey: process.env.SUPABASE_SERVICE_ROLE_KEY!,
          authorization: `Bearer ${process.env.SUPABASE_SERVICE_ROLE_KEY}`,
          "content-type": "application/json",
        },
        body: JSON.stringify({
          session_id: capSession,
          kind: "submit",
          lang: "py",
          source: "pass",
          verdict: "WA",
        }),
      }
    );
    expect(overRes.status).toBe(400);
    expect(await overRes.text()).toContain("submission limit");
  } finally {
    await rest(`problem_invalidations?reason=eq.e2e-fixture`, { method: "DELETE" });
    if (matchId) {
      const players = await rest<{ session_id: string }[]>(
        `duel_players?match_id=eq.${matchId}&select=session_id`
      );
      await rest(`duel_players?match_id=eq.${matchId}`, { method: "DELETE" });
      for (const p of players) {
        await rest(`session_submissions?session_id=eq.${p.session_id}`, {
          method: "DELETE",
        });
        await rest(`session_events?session_id=eq.${p.session_id}`, {
          method: "DELETE",
        });
        await rest(`sessions?id=eq.${p.session_id}`, { method: "DELETE" });
      }
      await rest(`duel_matches?id=eq.${matchId}`, { method: "DELETE" });
    }
    if (roomId) {
      await rest(`duel_room_players?room_id=eq.${roomId}`, { method: "DELETE" });
      await rest(`duel_rooms?id=eq.${roomId}`, { method: "DELETE" });
    }
    await ctxA.close();
    await ctxB.close();
  }
});
