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

export type TouristEvent =
  | { t: number; type: "snapshot"; code: string; lang?: Lang }
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

/** State of the tourist ghost at a given race-clock time. */
export function touristStateAt(
  log: Pick<TouristLog, "events">,
  clockMs: number
): { code: string; lang: Lang | null; solved: boolean; submitted: boolean } {
  let code = "";
  let lang: Lang | null = null;
  let solved = false;
  let submitted = false;
  for (const ev of log.events) {
    if (ev.t > clockMs) break;
    if (ev.type === "snapshot") {
      code = ev.code;
      if (ev.lang) lang = ev.lang;
    } else if (ev.type === "submit") submitted = true;
    else if (ev.type === "verdict" && ev.verdict === "AC") solved = true;
  }
  return { code, lang, solved, submitted };
}
