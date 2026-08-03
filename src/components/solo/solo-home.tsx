"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatMsPrecise } from "@/lib/templates";
import { loadSoloHistory, bestSolve, type SoloHistoryEntry } from "@/lib/solo";
import { cn } from "@/lib/utils";
import { Play, Trophy, Video } from "lucide-react";

type ProblemRow = {
  id: string;
  name: string;
  rating: number | null;
  tourist_time_ms: number | null;
};

export function SoloHome({ problems }: { problems: ProblemRow[] }) {
  const [history, setHistory] = useState<SoloHistoryEntry[]>([]);
  useEffect(() => setHistory(loadSoloHistory()), []);

  const solvedCount = problems.filter((p) => bestSolve(history, p.id)).length;

  return (
    <main className="relative min-h-screen overflow-hidden px-6 py-10">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(99,102,241,0.12),transparent_60%)]" />
      <div className="relative mx-auto max-w-4xl space-y-8">
        <div className="space-y-2">
          <p className="font-mono text-sm uppercase tracking-[0.3em] text-primary">
            Solo practice
          </p>
          <h1 className="text-4xl font-extrabold tracking-tight">The gauntlet</h1>
          <p className="text-muted-foreground">
            One problem, 3 minutes on the clock. Every run records your editor and
            webcam — replay any run below.
          </p>
          <p className="font-mono text-sm text-muted-foreground">
            {solvedCount} / {problems.length} solved on this machine
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          {problems.map((p) => {
            const best = bestSolve(history, p.id);
            const sessions = history
              .filter((h) => h.problemId === p.id && h.outcome !== "pending")
              .sort((a, b) => b.startedAt - a.startedAt);
            return (
              <Card
                key={p.id}
                className={cn(
                  "border-border/60 bg-card/60",
                  best && "ring-1 ring-green-500/50"
                )}
              >
                <CardHeader className="pb-2">
                  <div className="flex items-center gap-2">
                    <CardTitle className="truncate text-base">
                      <span className="font-mono text-primary">{p.id}</span>{" "}
                      {p.name}
                    </CardTitle>
                    {p.rating !== null && (
                      <Badge variant="outline" className="ml-auto shrink-0 font-mono">
                        {p.rating}
                      </Badge>
                    )}
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex items-center gap-2 text-sm">
                    {best ? (
                      <span className="flex items-center gap-1.5 font-mono text-green-400">
                        <Trophy className="h-3.5 w-3.5" />
                        Solved · {formatMsPrecise(best.solveMs ?? 0)}
                      </span>
                    ) : (
                      <span className="font-mono text-muted-foreground">Unsolved</span>
                    )}
                    {p.tourist_time_ms !== null && (
                      <span className="ml-auto font-mono text-xs text-muted-foreground">
                        tourist {formatMsPrecise(p.tourist_time_ms)}
                      </span>
                    )}
                  </div>
                  <div className="flex flex-wrap items-center gap-2">
                    <Button asChild size="sm">
                      <Link href={`/solo/${p.id}`}>
                        <Play className="mr-1.5 h-3.5 w-3.5" />
                        Race
                      </Link>
                    </Button>
                    {sessions.slice(0, 3).map((s, i) => (
                      <Button key={s.sessionId} asChild size="sm" variant="ghost">
                        <Link href={`/solo/replay/${s.sessionId}`}>
                          <Video className="mr-1.5 h-3.5 w-3.5" />
                          Replay{sessions.length > 1 ? ` #${sessions.length - i}` : ""}
                        </Link>
                      </Button>
                    ))}
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {problems.length === 0 && (
          <p className="font-mono text-muted-foreground">No problems in the bank yet.</p>
        )}
      </div>
    </main>
  );
}
