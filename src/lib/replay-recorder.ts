import { applyDeltaChanges, type EditorDeltaChange, type RunSummary } from "./tourist";
import type { Lang } from "./types";

/** Buffered editor event, matching the /api/replay and /api/solo/events wire rows. */
export type RecordedEditorEvent = {
  t: number;
  code: string;
  lang: Lang;
  kind?: "delta" | "run" | "run_result" | "tab" | "scroll";
  payload?:
    | { changes: EditorDeltaChange[] }
    | RunSummary
    | { tab: string }
    | { frac: number };
};

/** Keyframe cadence: at least one full snapshot per this many ms of editing. */
const KEYFRAME_INTERVAL_MS = 10_000;
/** Changes bigger than this (serialized) are stored as a keyframe instead. */
const MAX_DELTA_BYTES = 8_000;

/**
 * Per-keystroke editor recorder shared by the solo and station clients.
 * Records delta events with periodic snapshot keyframes; a shadow copy of the
 * document verifies every delta (prefix + delta must equal the editor's actual
 * text) and falls back to a keyframe on any mismatch.
 */
export function createEditorRecorder(opts: {
  /** Current recording clock in ms, or null when not recording. */
  now: () => number | null;
  push: (ev: RecordedEditorEvent) => void;
}) {
  let shadow: { code: string; lang: Lang } | null = null;
  let lastKeyframeT = -Infinity;

  const keyframe = (t: number, code: string, lang: Lang) => {
    opts.push({ t, code, lang });
    shadow = { code, lang };
    lastKeyframeT = t;
  };

  /** Full-code keyframe: mount, language switch, template reset. */
  const snapshot = (code: string, lang: Lang) => {
    const t = opts.now();
    if (t === null) return;
    keyframe(t, code, lang);
  };

  /** One Monaco content change; `code` is the editor's text after it. */
  const delta = (changes: EditorDeltaChange[], code: string, lang: Lang) => {
    const t = opts.now();
    if (t === null) return;
    let expected: string | null = null;
    if (shadow && shadow.lang === lang) {
      try {
        expected = applyDeltaChanges(shadow.code, changes);
      } catch {
        expected = null;
      }
    }
    if (
      expected !== code ||
      t - lastKeyframeT >= KEYFRAME_INTERVAL_MS ||
      JSON.stringify(changes).length > MAX_DELTA_BYTES
    ) {
      keyframe(t, code, lang);
      return;
    }
    opts.push({ t, code: "", lang, kind: "delta", payload: { changes } });
    shadow = { code, lang };
  };

  return { snapshot, delta };
}
