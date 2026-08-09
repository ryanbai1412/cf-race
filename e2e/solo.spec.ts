import { expect, test } from "@playwright/test";
import { applyDeltaChanges, type TouristEvent } from "../src/lib/tourist";
import {
  WA_SOLUTION,
  api,
  refSolution,
  rest,
  setMonaco,
} from "./helpers";

/** Final code for one language, replayed from snapshots + deltas. */
function reconstructCode(events: TouristEvent[], lang: "cpp" | "py"): string {
  let code = "";
  for (const e of events) {
    if (e.type === "snapshot" && e.lang === lang) code = e.code;
    else if (e.type === "delta" && e.lang === lang)
      code = applyDeltaChanges(code, e.changes);
  }
  return code;
}

/**
 * Solo golden path against the real judge: the invariants under test are
 * server behaviors an attacker/regression could break — verdicts come from
 * full hidden tests, WA never stamps a solve, AC stamps solve_ms exactly
 * once, replay reconstructs what was actually typed, and the submission cap
 * holds even for direct API callers.
 */
const PROBLEM = "2024A";

type SessionRow = {
  id: string;
  outcome: string | null;
  solve_ms: number | null;
  lang: string | null;
};

test.describe("solo run", () => {
  test("UI run: type in Monaco, submit WA then AC, replay reconstructs code", async ({
    page,
    request,
  }) => {
    await page.goto(`/solo/${PROBLEM}`);
    await page.getByRole("button", { name: /start/i }).click();

    // Countdown is 4s; the editor is usable at GO.
    await page.waitForURL(`**/solo/${PROBLEM}`);
    await page.getByText(/GO!|\d+:\d+/).first().waitFor();

    // Switch to Python and put a distinctive program in the editor.
    await page.getByRole("button", { name: /python/i }).click();
    const typed = "# e2e marker\n" + refSolution(PROBLEM);
    await setMonaco(page, typed, "py");

    // The recorder flushes every 5s — wait for events to land server-side.
    const sessionId = await page.evaluate(() => {
      const raw = sessionStorage.getItem("cfr-solo-active");
      return raw ? (JSON.parse(raw) as { sessionId: string }).sessionId : null;
    });
    expect(sessionId).toBeTruthy();
    await expect
      .poll(
        async () => {
          const rows = await rest<{ kind: string }[]>(
            `session_events?session_id=eq.${sessionId}&select=kind`
          );
          return rows.length;
        },
        { timeout: 20_000 }
      )
      .toBeGreaterThan(0);

    // WA first: verdict must be WA and the session must NOT be solved.
    const wa = await api<{ verdict: string }>(request, "/api/solo/submit", {
      sessionId,
      lang: "py",
      source: WA_SOLUTION,
    });
    expect(wa.status).toBe(200);
    expect(wa.json.verdict).toBe("WA");
    let [session] = await rest<SessionRow[]>(
      `sessions?id=eq.${sessionId}&select=id,outcome,solve_ms,lang`
    );
    expect(session.outcome).toBeNull();
    expect(session.solve_ms).toBeNull();

    // AC: solved is stamped with a positive solve_ms and the submit lang.
    const ac = await api<{ verdict: string; solveMs: number }>(
      request,
      "/api/solo/submit",
      { sessionId, lang: "py", source: refSolution(PROBLEM) }
    );
    expect(ac.status).toBe(200);
    expect(ac.json.verdict).toBe("AC");
    [session] = await rest<SessionRow[]>(
      `sessions?id=eq.${sessionId}&select=id,outcome,solve_ms,lang`
    );
    expect(session.outcome).toBe("solved");
    expect(session.solve_ms).toBeGreaterThan(0);
    expect(session.lang).toBe("py");

    // Replay: the event stream must reconstruct the exact typed code and
    // carry the submit/verdict markers for both submissions.
    const replayRes = await request.get(
      `http://localhost:3100/api/solo/replay?sessionId=${sessionId}`
    );
    expect(replayRes.status()).toBe(200);
    const replay = (await replayRes.json()) as {
      lang: string;
      events: TouristEvent[];
    };
    expect(replay.lang).toBe("py");
    const verdicts = replay.events
      .filter((e): e is { type: "verdict"; verdict: string } => e.type === "verdict")
      .map((e) => e.verdict);
    expect(verdicts).toEqual(["WA", "AC"]);
    // Reconstruct the Python buffer exactly the way the replay player does
    // (snapshots + deltas) — it must equal what was actually typed.
    const finalCode = reconstructCode(replay.events, "py");
    expect(finalCode).toBe(typed);
  });

  test("AC solve_ms is stamped once: a second AC cannot overwrite it", async ({
    request,
  }) => {
    const started = await api<{ sessionId: string }>(request, "/api/solo/session", {
      problemId: PROBLEM,
    });
    const sessionId = started.json.sessionId;

    const first = await api<{ verdict: string }>(request, "/api/solo/submit", {
      sessionId,
      lang: "py",
      source: refSolution(PROBLEM),
    });
    expect(first.json.verdict).toBe("AC");
    const [{ solve_ms: stamped }] = await rest<SessionRow[]>(
      `sessions?id=eq.${sessionId}&select=id,outcome,solve_ms,lang`
    );

    // The route rejects re-submitting a solved session outright.
    const second = await api<{ error: string }>(request, "/api/solo/submit", {
      sessionId,
      lang: "py",
      source: refSolution(PROBLEM),
    });
    expect(second.status).toBe(400);
    const [after] = await rest<SessionRow[]>(
      `sessions?id=eq.${sessionId}&select=id,outcome,solve_ms,lang`
    );
    expect(after.solve_ms).toBe(stamped);
  });

  test("submission cap holds for direct API callers (DB trigger)", async ({
    request,
  }) => {
    const started = await api<{ sessionId: string }>(request, "/api/solo/session", {
      problemId: PROBLEM,
    });
    const sessionId = started.json.sessionId;

    // Fill the 50-submission cap with dummy judged rows (service role, so
    // this bypasses the route's advisory count — the trigger must hold).
    const dummies = Array.from({ length: 50 }, () => ({
      session_id: sessionId,
      kind: "submit",
      lang: "py",
      source: "pass",
      verdict: "WA",
    }));
    await rest("session_submissions", { method: "POST", body: dummies });

    try {
      const over = await api<{ error: string }>(request, "/api/solo/submit", {
        sessionId,
        lang: "py",
        source: WA_SOLUTION,
      });
      expect(over.status).toBe(400);
      expect(over.json.error).toMatch(/submission limit/i);
    } finally {
      await rest(`session_submissions?session_id=eq.${sessionId}`, {
        method: "DELETE",
      });
      await rest(`session_events?session_id=eq.${sessionId}`, { method: "DELETE" });
      await rest(`sessions?id=eq.${sessionId}`, { method: "DELETE" });
    }
  });
});
