import type { Lang } from "./types";

export type TouristEvent =
  | { t: number; type: "snapshot"; code: string; lang?: Lang }
  | { t: number; type: "run" }
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
