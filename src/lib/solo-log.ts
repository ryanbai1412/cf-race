import { db } from "./db";
import type { Lang } from "./types";
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
  const [{ data: snaps }, { data: subs }] = await Promise.all([
    db()
      .from("solo_editor_events")
      .select("t_ms, code, lang, kind")
      .eq("session_id", sessionId)
      .order("t_ms", { ascending: true })
      .limit(5000),
    db()
      .from("solo_submissions")
      .select("submitted_at, judged_at, verdict, lang")
      .eq("session_id", sessionId)
      .order("submitted_at", { ascending: true }),
  ]);

  const events: TouristEvent[] = [];
  for (const s of snaps ?? []) {
    if (s.kind === "run") events.push({ t: s.t_ms, type: "run" });
    else events.push({ t: s.t_ms, type: "snapshot", code: s.code });
  }
  let lang: Lang = session.lang ?? "cpp";
  for (const s of subs ?? []) {
    events.push({ t: new Date(s.submitted_at).getTime() - startMs, type: "submit" });
    if (s.verdict && s.verdict !== "PENDING") {
      events.push({
        t: new Date(s.judged_at ?? s.submitted_at).getTime() - startMs,
        type: "verdict",
        verdict: s.verdict,
      });
    }
    lang = s.lang === "py" ? "py" : "cpp";
  }
  events.sort((a, b) => a.t - b.t);
  if ((snaps ?? []).length > 0) {
    lang = (snaps ?? [])[snaps!.length - 1].lang as Lang;
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
