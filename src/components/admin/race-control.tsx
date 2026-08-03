"use client";

import { useEffect, useMemo, useState } from "react";
import { useEventState } from "@/hooks/use-event-state";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { flagEmoji } from "@/lib/countries";
import { cn } from "@/lib/utils";
import { formatMs, formatMsPrecise } from "@/lib/templates";
import type { StationRole } from "@/lib/types";

type ProblemMeta = {
  id: string;
  name: string;
  rating: number | null;
  race_timer_sec: number;
  tourist_time_ms: number | null;
  special_judge: boolean;
};

export function RaceControl({ eventId }: { eventId: string }) {
  const { state, refetch, serverNow } = useEventState(eventId);
  const [problems, setProblems] = useState<ProblemMeta[]>([]);
  const [problemId, setProblemId] = useState("");
  const [timerSec, setTimerSec] = useState<number | "">("");
  const [busy, setBusy] = useState(false);
  const [, forceTick] = useState(0);

  useEffect(() => {
    fetch(`/api/problems?eventId=${eventId}`, { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : { problems: [] }))
      .then((d) => setProblems(d.problems.filter((p: ProblemMeta) => p.id !== "warmup-sum")))
      .catch(() => {});
  }, [eventId]);

  useEffect(() => {
    const iv = setInterval(() => forceTick((n) => n + 1), 1000);
    return () => clearInterval(iv);
  }, []);

  const selected = useMemo(
    () => problems.find((p) => p.id === problemId),
    [problems, problemId]
  );

  async function startRace() {
    if (!problemId || busy) return;
    setBusy(true);
    try {
      const res = await fetch("/api/race/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          eventId,
          problemId,
          timerSec: timerSec === "" ? undefined : Number(timerSec),
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? "Failed to start");
      toast.success("Race starting — countdown is live!");
      void refetch();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed to start race");
    } finally {
      setBusy(false);
    }
  }

  async function finishRace() {
    setBusy(true);
    try {
      await fetch("/api/race/finish", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ eventId }),
      });
      toast.success("Race finished — stations reset to check-in");
      void refetch();
    } finally {
      setBusy(false);
    }
  }

  if (!state) {
    return (
      <p className="animate-pulse py-8 text-center font-mono text-sm text-muted-foreground">
        Connecting…
      </p>
    );
  }
  const race = state.race;
  const anyCheckedIn = Boolean(state.contestants.station1 || state.contestants.station2);
  const raceEndMs = race?.started_at
    ? new Date(race.started_at).getTime() + race.timer_sec * 1000
    : null;
  const raceOver = raceEndMs !== null && serverNow() > raceEndMs;

  return (
    <div className="space-y-6">
      {/* Stations */}
      <div className="grid gap-4 sm:grid-cols-2">
        {(["station1", "station2"] as StationRole[]).map((role) => {
          const c = state.contestants[role];
          const p = race?.participants.find((x) => x.station_role === role);
          const startMs = race?.started_at ? new Date(race.started_at).getTime() : null;
          return (
            <Card key={role}>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm text-muted-foreground">
                  Station {role === "station1" ? "1" : "2"}
                </CardTitle>
              </CardHeader>
              <CardContent>
                {c ? (
                  <div className="flex items-center gap-2">
                    <span className="text-xl">{c.country ? flagEmoji(c.country) : "🏳️"}</span>
                    <span className="text-lg font-semibold">{c.name}</span>
                    {p?.first_ac_at && startMs !== null && (
                      <span className="ml-auto font-mono text-green-400">
                        AC {formatMsPrecise(new Date(p.first_ac_at).getTime() - startMs)}
                      </span>
                    )}
                    {p && !p.first_ac_at && race && (
                      <span
                        className={cn(
                          "ml-auto font-mono",
                          raceOver ? "text-muted-foreground" : "text-amber-400"
                        )}
                      >
                        {raceOver ? "time up — no AC" : "racing…"}
                      </span>
                    )}
                  </div>
                ) : (
                  <p className="text-muted-foreground">Empty — waiting for check-in</p>
                )}
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Race control */}
      <Card>
        <CardHeader>
          <CardTitle>Race control</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {race ? (
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <span className="font-semibold">
                  {race.problem.name}{" "}
                  <span className="font-mono text-xs text-muted-foreground">
                    ({race.problem_id})
                  </span>
                </span>
                {race.started_at &&
                  (raceOver ? (
                    <span className="ml-auto font-mono text-2xl font-bold text-red-400">
                      OVERTIME
                    </span>
                  ) : (
                    <span className="ml-auto font-mono text-2xl tabular-nums">
                      {formatMs(raceEndMs! - serverNow())}
                    </span>
                  ))}
              </div>
              <Button
                variant="destructive"
                size={raceOver ? "lg" : "default"}
                onClick={finishRace}
                disabled={busy}
              >
                Finish &amp; reset stations
              </Button>
              {raceOver && (
                <p className="text-xs text-muted-foreground">
                  Timer expired — finish to return stations to check-in.
                </p>
              )}
            </div>
          ) : (
            <div className="space-y-4">
              <div className="space-y-1.5">
                <Label>Problem</Label>
                <select
                  className="w-full rounded-md border border-border bg-background px-3 py-2 text-sm"
                  value={problemId}
                  onChange={(e) => setProblemId(e.target.value)}
                >
                  <option value="">Select a problem…</option>
                  {problems.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.id} — {p.name}
                      {p.rating ? ` (*${p.rating})` : ""}
                      {p.tourist_time_ms
                        ? ` · tourist ${formatMsPrecise(p.tourist_time_ms)}`
                        : ""}
                      {p.special_judge ? " · special judge" : ""}
                    </option>
                  ))}
                </select>
                {problems.length === 0 && (
                  <p className="text-xs text-muted-foreground">
                    Problem bank is empty — the pipeline hasn&apos;t delivered problems yet.
                  </p>
                )}
              </div>
              <div className="space-y-1.5">
                <Label>Timer (seconds{selected ? `, default ${selected.race_timer_sec}` : ""})</Label>
                <Input
                  type="number"
                  min={30}
                  max={3600}
                  placeholder={selected ? String(selected.race_timer_sec) : "180"}
                  value={timerSec}
                  onChange={(e) =>
                    setTimerSec(e.target.value === "" ? "" : Number(e.target.value))
                  }
                  className="max-w-40"
                />
              </div>
              <Button
                size="lg"
                onClick={startRace}
                disabled={busy || !problemId || !anyCheckedIn}
              >
                {busy ? "Starting…" : "Start race (5s countdown)"}
              </Button>
              {!anyCheckedIn && (
                <p className="text-xs text-muted-foreground">
                  Needs at least one contestant checked in.
                </p>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
