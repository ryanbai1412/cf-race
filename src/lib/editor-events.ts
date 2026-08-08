import { db } from "./db";
import type { Lang } from "./types";
import type { EditorDeltaChange, RunSummary, TouristEvent } from "./tourist";

export type EditorEventRow = {
  t_ms: number;
  code: string;
  lang: string;
  kind: string | null;
  payload: unknown;
};

export type IncomingEditorEvent = {
  t: number;
  code: string;
  lang: Lang;
  kind?: string;
  payload?: unknown;
};

const EVENT_KINDS = new Set([
  "snapshot",
  "delta",
  "run",
  "run_result",
  "tab",
  "scroll",
]);

/**
 * Normalize a client-supplied editor-event batch into rows ready for insert
 * (caller merges in its own foreign-key columns). Caps batch size, code
 * length, and payload size.
 */
export function sanitizeEditorEvents(
  events: IncomingEditorEvent[]
): EditorEventRow[] {
  return events.slice(0, 1000).map((e) => ({
    t_ms: Math.max(0, Math.round(e.t)),
    code: String(e.code).slice(0, 100_000),
    lang: e.lang === "py" ? "py" : "cpp",
    kind: e.kind && EVENT_KINDS.has(e.kind) ? e.kind : "snapshot",
    payload:
      e.payload && JSON.stringify(e.payload).length <= 20_000 ? e.payload : null,
  }));
}

/**
 * Convert persisted event rows into a sorted tourist-format event log.
 * Returns the log and the language of the final code state.
 */
export function buildReplayEvents(
  rows: EditorEventRow[],
  fallbackLang: Lang = "cpp"
): { events: TouristEvent[]; lang: Lang } {
  const events: TouristEvent[] = [];
  for (const s of rows) {
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
  let lang: Lang = fallbackLang;
  const codeSnaps = rows.filter(
    (s) => s.kind === "snapshot" || s.kind === "delta"
  );
  if (codeSnaps.length > 0) lang = codeSnaps[codeSnaps.length - 1].lang as Lang;
  return { events, lang };
}

const PAGE = 1000;
const MAX_ROWS = 50_000;

/**
 * Fetch all editor-event rows for one recording, paging past PostgREST's
 * per-request row cap (delta logs are per-keystroke, so runs can easily
 * exceed 1000 rows). Ordered by t_ms then id so same-millisecond events
 * replay in insertion order.
 */
export async function fetchEditorEventRows(
  table: "session_events",
  filter: Record<string, string>
): Promise<EditorEventRow[]> {
  const rows: EditorEventRow[] = [];
  for (let from = 0; from < MAX_ROWS; from += PAGE) {
    let q = db()
      .from(table)
      .select("t_ms, code, lang, kind, payload")
      .order("t_ms", { ascending: true })
      .order("id", { ascending: true })
      .range(from, from + PAGE - 1);
    for (const [k, v] of Object.entries(filter)) q = q.eq(k, v);
    const { data, error } = await q;
    if (error || !data || data.length === 0) break;
    rows.push(...(data as EditorEventRow[]));
    if (data.length < PAGE) break;
  }
  return rows;
}
