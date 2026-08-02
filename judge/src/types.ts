export type Lang = "cpp" | "py";
export type Verdict = "AC" | "WA" | "RE" | "TLE" | "ML" | "SKIP" | "CE";

export interface TestCase {
  name: string;
  input: string;
  expected: string | null;
}

export interface RunRequest {
  runId: string;
  lang: Lang;
  source: string;
  problemId?: string;
  tests?: TestCase[];
  timeLimitMs?: number;
  memoryLimitMb?: number;
}

export interface TestResult {
  name: string;
  verdict: Verdict;
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
}

export interface SubmitRequest {
  submissionId: string;
  lang: Lang;
  source: string;
  problemId: string;
}

export interface SubmitResponse {
  submissionId: string;
  verdict: Verdict;
  failedTest: string | null;
  passedCount: number;
  totalCount: number;
  timeMsMax: number;
  compileStderr?: string;
}

export interface ProblemMeta {
  id: string;
  name: string;
  rating?: number;
  timeLimitMs: number;
  memoryLimitMb: number;
  multiTest?: boolean;
  specialJudge?: boolean;
  floatEps?: number | null;
  raceTimerSec?: number;
  touristTimeMs?: number | null;
}
