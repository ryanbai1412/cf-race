import { db } from "./db";

export type EditorEventRow = {
  t_ms: number;
  code: string;
  lang: string;
  kind: string | null;
  payload: unknown;
};

const PAGE = 1000;
const MAX_ROWS = 50_000;

/**
 * Fetch all editor-event rows for one recording, paging past PostgREST's
 * per-request row cap (delta logs are per-keystroke, so runs can easily
 * exceed 1000 rows). Ordered by t_ms then id so same-millisecond events
 * replay in insertion order.
 */
export async function fetchEditorEventRows(
  table: "race_editor_events" | "solo_editor_events",
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
