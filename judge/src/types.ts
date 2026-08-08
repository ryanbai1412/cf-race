// Wire types are shared with the web app via @cf-race/judge-protocol
// (types-only workspace package); ProblemMeta is judge-internal.
export type {
  Lang,
  TestCase,
  TestResult,
  RunRequest,
  RunResponse,
  SubmitRequest,
  SubmitResponse,
} from "@cf-race/judge-protocol";
export type { TestVerdict as Verdict } from "@cf-race/judge-protocol";

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
