"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { flagEmoji } from "@/lib/countries";
import { formatMsPrecise } from "@/lib/templates";
import { PlayCircle } from "lucide-react";

type RaceRow = {
  id: string;
  problem_id: string;
  state: string;
  started_at: string;
  problem: { name: string } | null;
  participants: {
    station_role: string;
    first_ac_at: string | null;
    dq: boolean;
    contestant: { name: string; country: string | null } | null;
  }[];
};

export function RaceHistory({ eventId }: { eventId: string }) {
  const [races, setRaces] = useState<RaceRow[]>([]);

  useEffect(() => {
    const load = () =>
      fetch(`/api/races?eventId=${eventId}`, { cache: "no-store" })
        .then((r) => (r.ok ? r.json() : { races: [] }))
        .then((d) => setRaces(d.races ?? []))
        .catch(() => {});
    load();
    const iv = setInterval(load, 15000);
    return () => clearInterval(iv);
  }, [eventId]);

  if (races.length === 0) return null;

  return (
    <Card className="border-border/60 bg-card/60">
      <CardHeader>
        <CardTitle className="text-lg">Race history &amp; replays</CardTitle>
      </CardHeader>
      <CardContent className="space-y-2">
        {races.map((race) => {
          const startMs = new Date(race.started_at).getTime();
          return (
            <div
              key={race.id}
              className="flex flex-wrap items-center gap-3 rounded-md border border-border/60 px-3 py-2"
            >
              <div className="min-w-40">
                <p className="text-sm font-semibold">
                  {race.problem?.name ?? race.problem_id}
                </p>
                <p className="font-mono text-xs text-muted-foreground">
                  {new Date(race.started_at).toLocaleTimeString()} · {race.state}
                </p>
              </div>
              <div className="flex flex-1 flex-wrap items-center gap-2">
                {race.participants.map((p) => (
                  <Button
                    key={p.station_role}
                    asChild
                    size="sm"
                    variant="secondary"
                    className="gap-1.5"
                  >
                    <Link
                      href={`/e/${eventId}/replay/${race.id}/${p.station_role}`}
                      target="_blank"
                    >
                      <PlayCircle className="h-3.5 w-3.5" />
                      {p.contestant?.country ? flagEmoji(p.contestant.country) + " " : ""}
                      {p.contestant?.name ?? p.station_role}
                      {p.first_ac_at && (
                        <span className="font-mono text-green-400">
                          {formatMsPrecise(new Date(p.first_ac_at).getTime() - startMs)}
                        </span>
                      )}
                    </Link>
                  </Button>
                ))}
              </div>
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
}
