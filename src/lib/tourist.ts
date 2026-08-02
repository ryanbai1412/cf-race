import type { Lang } from "./types";

export type TouristEvent =
  | { t: number; type: "snapshot"; code: string }
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
  log: TouristLog,
  clockMs: number
): { code: string; solved: boolean; submitted: boolean } {
  let code = "";
  let solved = false;
  let submitted = false;
  for (const ev of log.events) {
    if (ev.t > clockMs) break;
    if (ev.type === "snapshot") code = ev.code;
    else if (ev.type === "submit") submitted = true;
    else if (ev.type === "verdict" && ev.verdict === "AC") solved = true;
  }
  return { code, solved, submitted };
}
