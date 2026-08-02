export type Lang = "cpp" | "py";

export type Verdict = "AC" | "WA" | "TLE" | "RE" | "ML" | "CE" | "PENDING";

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

export type RunTestResult = {
  name: string;
  verdict: "AC" | "WA" | "RE" | "TLE" | "ML" | "SKIP";
  timeMs: number;
  stdout: string;
  stderr: string;
  checkerNote?: string;
};

export type RunResult = {
  runId: string;
  compile: { ok: boolean; stderr: string };
  results: RunTestResult[];
  checkerUnreliable?: boolean;
};

/** Full state for a station/monitor client, returned by GET /api/state. */
export type ClientState = {
  serverNow: number; // epoch ms, for clock sync
  event: { id: string; name: string };
  contestants: Partial<Record<StationRole, Contestant>>;
  race:
    | (Race & {
        problem: Problem;
        participants: {
          contestant_id: string;
          station_role: StationRole;
          first_ac_at: string | null;
          dq: boolean;
        }[];
      })
    | null;
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
  | { type: "confetti"; station: StationRole };
