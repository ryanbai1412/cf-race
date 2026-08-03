"use client";

/** localStorage history for solo practice runs (docs/flows/07-solo-practice.md). */

export type SoloOutcome = "pending" | "solved" | "timeout" | "abandoned";

export type SoloHistoryEntry = {
  sessionId: string;
  problemId: string;
  startedAt: number; // epoch ms
  outcome: SoloOutcome;
  solveMs: number | null;
};

const KEY = "cfr-solo-history";

export function loadSoloHistory(): SoloHistoryEntry[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = localStorage.getItem(KEY);
    const parsed = raw ? JSON.parse(raw) : [];
    return Array.isArray(parsed) ? (parsed as SoloHistoryEntry[]) : [];
  } catch {
    return [];
  }
}

export function upsertSoloHistory(entry: SoloHistoryEntry) {
  const list = loadSoloHistory().filter((e) => e.sessionId !== entry.sessionId);
  list.push(entry);
  localStorage.setItem(KEY, JSON.stringify(list));
}

export function bestSolve(
  history: SoloHistoryEntry[],
  problemId: string
): SoloHistoryEntry | null {
  let best: SoloHistoryEntry | null = null;
  for (const e of history) {
    if (e.problemId !== problemId || e.outcome !== "solved" || e.solveMs === null)
      continue;
    if (!best || e.solveMs < (best.solveMs ?? Infinity)) best = e;
  }
  return best;
}
