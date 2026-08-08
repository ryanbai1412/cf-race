/**
 * Wire contract for the judge HTTP API (`POST /run`, `POST /submit`).
 *
 * Types only — this package has no runtime code, so consumers must use
 * `import type`. The judge implements these shapes in `judge/src`, the web
 * app consumes them in `src/lib/judge.ts`.
 */

export type Lang = "cpp" | "py";

/** Per-test verdicts. `SKIP` appears when an earlier test already failed. */
export type TestVerdict = "AC" | "WA" | "RE" | "TLE" | "ML" | "SKIP" | "CE";

/** Whole-submission verdicts (no SKIP; CE when compilation fails). */
export type SubmitVerdict = "AC" | "WA" | "TLE" | "RE" | "ML" | "CE";

export interface TestCase {
  name: string;
  input: string;
  /** null = no expected output (custom input runs). */
  expected: string | null;
}

export interface RunRequest {
  runId: string;
  lang: Lang;
  source: string;
  /** Run a problem package's sample tests… */
  problemId?: string;
  /** …or explicit tests (samples/custom input supplied by the caller). */
  tests?: TestCase[];
  timeLimitMs?: number;
  memoryLimitMb?: number;
}

export interface TestResult {
  name: string;
  verdict: TestVerdict;
  timeMs: number;
  stdout: string;
  stderr: string;
  stdoutTruncated?: boolean;
  stderrTruncated?: boolean;
  checkerNote?: string;
  checkerUnreliable?: boolean;
}

export interface RunResponse {
  runId: string;
  compile: { ok: boolean; stderr: string };
  results: TestResult[];
  /** Set for special-judge problems: token checker may mis-grade samples. */
  checkerUnreliable?: boolean;
}

export interface SubmitRequest {
  submissionId: string;
  lang: Lang;
  source: string;
  problemId: string;
}

export interface SubmitResponse {
  submissionId: string;
  verdict: SubmitVerdict;
  failedTest?: string | null;
  passedCount: number;
  totalCount: number;
  timeMsMax: number;
  compileStderr?: string;
}
