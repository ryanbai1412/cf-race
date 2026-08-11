import type {
  Lang as ProtocolLang,
  SubmitVerdict,
  RunResponse,
  TestResult,
} from "@cf-race/judge-protocol";

export type Lang = ProtocolLang;

/** DB verdicts: the judge's submit verdicts plus a pre-judging PENDING. */
export type Verdict = SubmitVerdict | "PENDING";

export type SampleTest = { input: string; output: string };

export type Problem = {
  id: string;
  name: string;
  rating: number | null;
  time_limit_ms: number;
  memory_limit_mb: number;
  special_judge: boolean;
  race_timer_sec: number;
  tourist_time_ms: number | null;
  statement_html: string | null;
  samples: SampleTest[];
};

export type Contestant = {
  id: string;
  event_id: string;
  station_role: StationRole;
  name: string;
  country: string | null;
  retired_at: string | null;
  ready_at: string | null;
};

export type StationRole = "station1" | "station2";

export type RaceState = "waiting" | "countdown" | "running" | "finished";

export type Race = {
  id: string;
  event_id: string;
  problem_id: string;
  state: RaceState;
  started_at: string | null;
  timer_sec: number;
};

export type Submission = {
  id: string;
  race_id: string;
  contestant_id: string;
  lang: Lang;
  verdict: Verdict | null;
  details: {
    failedTest?: string;
    passedCount?: number;
    totalCount?: number;
    timeMsMax?: number;
    compileError?: string;
  };
  submitted_at: string;
};

// Judge wire types, shared with judge/src via the workspace package.
export type RunTestResult = TestResult;
export type RunResult = RunResponse;

export type RaceParticipantState = {
  contestant_id: string;
  station_role: StationRole;
  first_ac_at: string | null;
  dq: boolean;
};

export type RaceWithProblem = Race & {
  problem: Problem;
  participants: RaceParticipantState[];
};

/** Full state for a station/monitor client, returned by GET /api/state. */
export type ClientState = {
  serverNow: number; // epoch ms, for clock sync
  event: { id: string; name: string; requireWebcam: boolean; selfServe: boolean };
  contestants: Partial<Record<StationRole, Contestant>>;
  /** Self-serve auto-start moment (epoch ms) while both stations are ready. */
  autoStartAt: number | null;
  race: RaceWithProblem | null;
  /** Most recent finished race, for the REVIEWING monitor/station state. */
  lastRace:
    | (RaceWithProblem & {
        /** Names/countries of that race's participants, keyed by contestant. */
        contestants: Record<string, { name: string; country: string | null }>;
        /** Genna reference time for the raced problem, if any. */
        gennaSolveMs: number | null;
      })
    | null;
  /** Genna reference time for the active race problem, if any. */
  gennaSolveMs: number | null;
};

/** Realtime broadcast payloads on channel `event:<eventId>`. */
export type BroadcastMsg =
  | { type: "state_changed" } // any station/race change: clients refetch /api/state
  | {
      type: "editor";
      station: StationRole;
      code: string;
      lang: Lang;
      cursorLine: number;
    }
  | { type: "confetti"; station: StationRole }
  // A monitor asks the station to rebroadcast its current editor snapshot
  // (e.g. after a monitor refresh mid-race).
  | { type: "request_editor"; station: StationRole };
