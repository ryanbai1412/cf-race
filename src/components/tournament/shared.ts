"use client";

import type { MatchView, MemberView, TournamentStateView } from "@/lib/tournament-view";

export type { MatchView, MemberView, TournamentStateView };

export function memberMap(state: TournamentStateView | null): Map<string, MemberView> {
  return new Map((state?.members ?? []).map((m) => [m.id, m]));
}

const POST_TIMEOUT_MS = 20_000;
const BUSY = "Server is busy, please try again";

export async function postJson(url: string, body: unknown): Promise<{ ok: boolean; error?: string; data?: Record<string, unknown> }> {
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(POST_TIMEOUT_MS),
    });
    const data = await res.json().catch(() => ({}));
    if (res.ok) return { ok: true, data };
    const error = (data as { error?: string }).error;
    return { ok: false, error: error ?? (res.status >= 500 ? BUSY : `Error ${res.status}`) };
  } catch (e) {
    return { ok: false, error: e instanceof DOMException && e.name === "TimeoutError" ? BUSY : "Network error" };
  }
}

export function fmtClock(ms: number): string {
  const s = Math.max(0, Math.ceil(ms / 1000));
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

/** Short two-tone chime for "your match is ready" reminders. */
export function chime(): void {
  try {
    const Ctx = window.AudioContext ?? (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
    const ctx = new Ctx();
    [880, 1320].forEach((f, i) => {
      const o = ctx.createOscillator();
      const g = ctx.createGain();
      o.frequency.value = f;
      o.connect(g);
      g.connect(ctx.destination);
      const t0 = ctx.currentTime + i * 0.18;
      g.gain.setValueAtTime(0.0001, t0);
      g.gain.exponentialRampToValueAtTime(0.25, t0 + 0.02);
      g.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.35);
      o.start(t0);
      o.stop(t0 + 0.4);
    });
    setTimeout(() => void ctx.close(), 1200);
  } catch {}
}

export function notify(title: string, body: string): void {
  try {
    if (typeof Notification !== "undefined" && Notification.permission === "granted" && document.hidden) {
      new Notification(title, { body });
    }
  } catch {}
}

/** Games won as shown on a bracket card (single games show 1/0 once decided). */
export function scoreOf(m: MatchView, side: "a" | "b"): string {
  if (m.decidedBy === "bye") return "";
  if (m.format === "single") {
    if (m.status !== "done") return "";
    return m.winner && m.winner === (side === "a" ? m.a : m.b) ? "W" : "L";
  }
  return String(side === "a" ? m.aWins : m.bWins);
}
