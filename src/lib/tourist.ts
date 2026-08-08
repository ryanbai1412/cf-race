import type { Lang, RunResult } from "./types";

/** Compact summary of a run-samples / custom-input run, stored in event logs. */
export type RunSummary = {
  target: "samples" | "custom";
  compiled: boolean;
  verdict: string; // overall: AC when all sample tests pass, else worst verdict
  passed: number;
  total: number;
  compileStderr?: string;
  tests?: { name: string; verdict: string; timeMs: number }[];
};

export function summarizeRun(
  result: RunResult,
  target: "samples" | "custom"
): RunSummary {
  const order = ["AC", "SKIP", "WA", "RE", "TLE", "ML"];
  let worst = "AC";
  let passed = 0;
  for (const r of result.results) {
    if (r.verdict === "AC") passed++;
    if (order.indexOf(r.verdict) > order.indexOf(worst)) worst = r.verdict;
  }
  return {
    target,
    compiled: result.compile.ok,
    verdict: result.compile.ok ? worst : "CE",
    passed,
    total: result.results.length,
    compileStderr: result.compile.ok
      ? undefined
      : result.compile.stderr.slice(0, 4000),
    tests: result.results.map((r) => ({
      name: r.name,
      verdict: r.verdict,
      timeMs: r.timeMs,
    })),
  };
}

/**
 * One text mutation from Monaco's onDidChangeModelContent: replace `l`
 * characters at offset `o` with `text`. All changes within a single delta
 * event are relative to the document state before that event.
 */
export type EditorDeltaChange = { o: number; l: number; text: string };

export type TouristEvent =
  | { t: number; type: "snapshot"; code: string; lang?: Lang }
  | { t: number; type: "delta"; lang?: Lang; changes: EditorDeltaChange[] }
  | { t: number; type: "run" }
  | { t: number; type: "run_result"; result: RunSummary }
  | { t: number; type: "tab"; tab: string }
  | { t: number; type: "scroll"; frac: number }
  | { t: number; type: "submit" }
  | { t: number; type: "verdict"; verdict: string };

export type TouristLog = {
  problemId: string;
  lang: Lang;
  solveMs: number;
  events: TouristEvent[];
};

/**
 * Apply one delta event's changes to a document. Changes are applied in
 * descending-offset order so earlier edits don't shift later offsets.
 * Throws if any change is out of bounds (caller falls back to a keyframe).
 */
export function applyDeltaChanges(
  code: string,
  changes: EditorDeltaChange[]
): string {
  const sorted = [...changes].sort((a, b) => b.o - a.o);
  let next = code;
  for (const c of sorted) {
    if (c.o < 0 || c.l < 0 || c.o + c.l > next.length) {
      throw new Error("delta out of bounds");
    }
    next = next.slice(0, c.o) + c.text + next.slice(c.o + c.l);
  }
  return next;
}

/** Editor state reconstructed from an event-log prefix. */
export type ReplayState = {
  /** One buffer per language tab. */
  buffers: Record<Lang, string>;
  activeLang: Lang | null;
  solved: boolean;
  submitted: boolean;
};

function initialReplayState(): ReplayState {
  return {
    buffers: { cpp: "", py: "" },
    activeLang: null,
    solved: false,
    submitted: false,
  };
}

/**
 * Pure fold step: `state` after one more event. Snapshot events are keyframes
 * that overwrite a buffer; delta events splice into it. A delta that doesn't
 * apply cleanly is skipped — the next keyframe (≤10s away) self-heals.
 */
function foldEvent(state: ReplayState, ev: TouristEvent): ReplayState {
  if (ev.type === "snapshot") {
    const lang = ev.lang ?? state.activeLang ?? "cpp";
    return {
      ...state,
      buffers: { ...state.buffers, [lang]: ev.code },
      activeLang: lang,
    };
  }
  if (ev.type === "delta") {
    const lang = ev.lang ?? state.activeLang ?? "cpp";
    let code = state.buffers[lang];
    try {
      code = applyDeltaChanges(code, ev.changes);
    } catch {
      return { ...state, activeLang: lang };
    }
    return {
      ...state,
      buffers: { ...state.buffers, [lang]: code },
      activeLang: lang,
    };
  }
  if (ev.type === "submit") return { ...state, submitted: true };
  if (ev.type === "verdict" && ev.verdict === "AC")
    return { ...state, solved: true };
  return state;
}

/** What a player consumer needs each frame. */
export type ReplayFrame = {
  code: string;
  lang: Lang | null;
  solved: boolean;
  submitted: boolean;
  /**
   * True when the visible document can't be patched incrementally (first
   * frame, backward seek, keyframe, or language switch) and must be replaced
   * wholesale; otherwise `deltas` holds the change batches (one per delta
   * event, each batch relative to the document before it) applied since the
   * previous frame.
   */
  reset: boolean;
  deltas: EditorDeltaChange[][];
};

const CHECKPOINT_EVERY = 200;

/**
 * Incremental cursor over a replay event log. Forward playback applies only
 * the events since the previous frame (cheap, per-keystroke smooth); backward
 * seeks restore the nearest earlier full-state checkpoint and replay forward.
 * Works identically for old snapshot-only logs and new delta logs.
 */
export class TouristPlayer {
  private events: TouristEvent[];
  private idx = 0;
  private state: ReplayState = initialReplayState();
  private checkpoints: { idx: number; state: ReplayState }[] = [];

  constructor(events: TouristEvent[]) {
    this.events = events;
  }

  /** Advance (or seek) to `clockMs` and describe how to update the view. */
  advance(clockMs: number): ReplayFrame {
    let reset = this.idx === 0;
    const deltas: EditorDeltaChange[][] = [];
    const prevLang = this.state.activeLang;

    // Backward seek: restore the nearest checkpoint at or before the target.
    if (this.idx > 0 && this.events[this.idx - 1].t > clockMs) {
      let cp: { idx: number; state: ReplayState } = {
        idx: 0,
        state: initialReplayState(),
      };
      for (let i = this.checkpoints.length - 1; i >= 0; i--) {
        const c = this.checkpoints[i];
        if (c.idx === 0 || this.events[c.idx - 1].t <= clockMs) {
          cp = c;
          break;
        }
      }
      this.idx = cp.idx;
      this.state = cp.state;
      reset = true;
    }

    while (this.idx < this.events.length && this.events[this.idx].t <= clockMs) {
      const ev = this.events[this.idx];
      if (ev.type === "snapshot") reset = true;
      else if (ev.type === "delta" && !reset) deltas.push(ev.changes);
      this.state = foldEvent(this.state, ev);
      this.idx++;
      if (this.idx % CHECKPOINT_EVERY === 0) {
        const last = this.checkpoints[this.checkpoints.length - 1];
        if (!last || last.idx < this.idx) {
          this.checkpoints.push({ idx: this.idx, state: this.state });
        }
      }
    }

    const lang = this.state.activeLang;
    if (lang !== prevLang) reset = true;
    return {
      code: lang ? this.state.buffers[lang] : "",
      lang,
      solved: this.state.solved,
      submitted: this.state.submitted,
      reset,
      deltas: reset ? [] : deltas,
    };
  }
}

/** State of the tourist ghost at a given race-clock time (one-shot fold). */
export function touristStateAt(
  log: Pick<TouristLog, "events">,
  clockMs: number
): { code: string; lang: Lang | null; solved: boolean; submitted: boolean } {
  let state = initialReplayState();
  for (const ev of log.events) {
    if (ev.t > clockMs) break;
    state = foldEvent(state, ev);
  }
  return {
    code: state.activeLang ? state.buffers[state.activeLang] : "",
    lang: state.activeLang,
    solved: state.solved,
    submitted: state.submitted,
  };
}
