import { db } from "./db";
import { buildReplayEvents, fetchEditorEventRows } from "./editor-events";
import type { Lang, Problem } from "./types";
import type { TouristEvent } from "./tourist";

/** Shape of GET /api/solo/replay responses (client + server share this). */
export type SoloReplayResponse = {
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

export type SoloSessionRow = {
  id: string;
  problem_id: string;
  lang: Lang | null;
  started_at: string;
  timer_sec: number;
  solve_ms: number | null;
  outcome: "solved" | "timeout" | "abandoned" | null;
  recording_path: string | null;
  recording_offset_ms: number | null;
};

/**
 * Build the tourist-format event log for a solo session: editor snapshots from
 * solo_editor_events, submit/verdict moments from solo_submissions.
 */
export async function buildSoloLog(sessionId: string): Promise<{
  session: SoloSessionRow;
  log: {
    problemId: string;
    lang: Lang;
    solveMs: number | null;
    events: TouristEvent[];
  };
} | null> {
  const { data: session } = await db()
    .from("solo_sessions")
    .select("*")
    .eq("id", sessionId)
    .maybeSingle<SoloSessionRow>();
  if (!session) return null;

  const startMs = new Date(session.started_at).getTime();
  const [snaps, { data: subs }] = await Promise.all([
    fetchEditorEventRows("solo_editor_events", { session_id: sessionId }),
    db()
      .from("solo_submissions")
      .select("submitted_at, judged_at, verdict, lang")
      .eq("session_id", sessionId)
      .order("submitted_at", { ascending: true }),
  ]);

  const { events, lang } = buildReplayEvents(
    snaps,
    subs ?? [],
    startMs,
    session.lang ?? "cpp"
  );

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
