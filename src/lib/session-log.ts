import { db } from "./db";
import { fetchEditorEventRows } from "./editor-events";
import type { Lang, Problem } from "./types";
import type { EditorDeltaChange, RunSummary, TouristEvent } from "./tourist";

export type SessionKind = "solo" | "duel" | "event";

/** Shape of GET /api/solo/replay responses (client + server share this). */
export type SessionReplayResponse = {
  problemId: string;
  lang: Lang;
  solveMs: number | null;
  events: TouristEvent[];
  outcome: "solved" | "timeout" | "abandoned" | null;
  timerSec: number;
  startedAt: string;
  problemName: string;
  touristTimeMs: number | null;
  problem: Problem | null;
  recordingUrl: string | null;
  recordingOffsetMs: number;
};

export type SessionRow = {
  id: string;
  kind: SessionKind;
  user_id: string | null;
  problem_id: string;
  lang: Lang | null;
  started_at: string;
  timer_sec: number | null;
  solve_ms: number | null;
  outcome: "solved" | "timeout" | "abandoned" | null;
  recording_path: string | null;
  recording_offset_ms: number | null;
};

/**
 * Build the tourist-format event log for a session (any kind) from the
 * single session_events playback stream (editor snapshots/deltas, runs,
 * tabs, scroll, submit + verdict moments).
 */
export async function buildSessionLog(sessionId: string): Promise<{
  session: SessionRow;
  log: {
    problemId: string;
    lang: Lang;
    solveMs: number | null;
    events: TouristEvent[];
  };
} | null> {
  const { data: session } = await db()
    .from("sessions")
    .select("*")
    .eq("id", sessionId)
    .maybeSingle<SessionRow>();
  if (!session) return null;

  const snaps = await fetchEditorEventRows("session_events", {
    session_id: sessionId,
  });

  const events: TouristEvent[] = [];
  for (const s of snaps) {
    if (s.kind === "run") events.push({ t: s.t_ms, type: "run" });
    else if (s.kind === "submit") events.push({ t: s.t_ms, type: "submit" });
    else if (s.kind === "verdict" && s.payload)
      events.push({
        t: s.t_ms,
        type: "verdict",
        verdict: (s.payload as { verdict: string }).verdict,
      });
    else if (s.kind === "run_result" && s.payload)
      events.push({ t: s.t_ms, type: "run_result", result: s.payload as RunSummary });
    else if (s.kind === "tab" && s.payload)
      events.push({ t: s.t_ms, type: "tab", tab: (s.payload as { tab: string }).tab });
    else if (s.kind === "scroll" && s.payload)
      events.push({
        t: s.t_ms,
        type: "scroll",
        frac: (s.payload as { frac: number }).frac,
      });
    else if (s.kind === "delta" && s.payload)
      events.push({
        t: s.t_ms,
        type: "delta",
        lang: s.lang === "py" ? "py" : "cpp",
        changes: (s.payload as { changes: EditorDeltaChange[] }).changes,
      });
    else if (
      s.kind === "run_result" ||
      s.kind === "tab" ||
      s.kind === "scroll" ||
      s.kind === "delta" ||
      s.kind === "verdict"
    )
      continue;
    else
      events.push({
        t: s.t_ms,
        type: "snapshot",
        code: s.code,
        lang: s.lang === "py" ? "py" : "cpp",
      });
  }
  events.sort((a, b) => a.t - b.t);
  let lang: Lang = session.lang ?? "cpp";
  const codeSnaps = snaps.filter(
    (s) => s.kind === "snapshot" || s.kind === "delta"
  );
  if (codeSnaps.length > 0) {
    lang = codeSnaps[codeSnaps.length - 1].lang as Lang;
  }

  return {
    session,
    log: {
      problemId: session.problem_id,
      lang,
      solveMs: session.solve_ms,
      events,
    },
  };
}

/** A session's replay payload with a signed webcam URL, shared by surfaces. */
export async function buildSessionReplay(
  sessionId: string
): Promise<SessionReplayResponse | null> {
  const built = await buildSessionLog(sessionId);
  if (!built) return null;
  const { session, log } = built;

  let recordingUrl: string | null = null;
  if (session.recording_path) {
    const { data } = await db()
      .storage.from("recordings")
      .createSignedUrl(session.recording_path, 3600);
    recordingUrl = data?.signedUrl ?? null;
  }

  const { data: problem } = await db()
    .from("problems")
    .select("*")
    .eq("id", session.problem_id)
    .maybeSingle();

  return {
    ...log,
    outcome: session.outcome,
    timerSec: session.timer_sec ?? 0,
    startedAt: session.started_at,
    problemName: problem?.name ?? session.problem_id,
    touristTimeMs: problem?.tourist_time_ms ?? null,
    problem: problem ?? null,
    recordingUrl,
    recordingOffsetMs: session.recording_offset_ms ?? 0,
  };
}
