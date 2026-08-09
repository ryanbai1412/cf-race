"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { SoloAuthButton, useSoloAuth } from "@/components/solo/auth-button";
import { ShareButton } from "@/components/shell/share-button";
import {
  CenteredMessage,
  EmptyState,
  LoadingScreen,
  PageHeader,
} from "@/components/shell/page";
import { formatMsPrecise } from "@/lib/templates";
import { cn } from "@/lib/utils";
import { ListChecks, Swords, Trophy, Video } from "lucide-react";
import { toast } from "sonner";

type HomeData = {
  userId: string;
  matches: {
    id: string;
    roomId: string;
    problemId: string;
    startedAt: string;
    finished: boolean;
    won: boolean;
    winnerIsSet: boolean;
    opponent: string;
  }[];
  solved: { problemId: string; solveMs: number | null; kind: string }[];
  recordings: {
    id: string;
    kind: string;
    problem_id: string;
    started_at: string;
    outcome: string | null;
    solve_ms: number | null;
  }[];
};

export function DuelHome() {
  const auth = useSoloAuth();
  const { user, loading } = auth;
  const router = useRouter();
  const [data, setData] = useState<HomeData | null>(null);
  const [creating, setCreating] = useState(false);
  const [joinLink, setJoinLink] = useState("");
  const [joinError, setJoinError] = useState<string | null>(null);

  const joinByLink = () => {
    const match = joinLink.match(/\/duel\/room\/([0-9a-f-]{36})/i);
    if (match) router.push(`/duel/room/${match[1]}`);
    else setJoinError("That doesn\u2019t look like a duel room link (…/duel/room/…).");
  };

  useEffect(() => {
    if (!user) return;
    fetch("/api/duel/home", { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : null))
      .then(setData)
      .catch(() => {});
  }, [user]);

  const createRoom = async () => {
    setCreating(true);
    try {
      const res = await fetch("/api/duel/create", { method: "POST" });
      const d = await res.json();
      if (!res.ok) throw new Error(d.error ?? "Failed to create room");
      router.push(`/duel/room/${d.roomId}`);
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed to create room");
      setCreating(false);
    }
  };

  if (loading) return <LoadingScreen />;

  if (!user) {
    return (
      <CenteredMessage
        eyebrow="1v1 Duel"
        title="Sign in to duel"
        description="Duels are head-to-head races on a shared problem — everything is recorded. Google login is required."
      >
        <SoloAuthButton {...auth} next="/duels" />
      </CenteredMessage>
    );
  }

  const wins = data?.matches.filter((m) => m.finished && m.won).length ?? 0;
  const played = data?.matches.filter((m) => m.finished).length ?? 0;

  return (
    <main className="relative min-h-screen overflow-hidden px-6 py-10">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(99,102,241,0.12),transparent_60%)]" />
      <div className="relative mx-auto w-full max-w-5xl space-y-8">
        <PageHeader
          eyebrow="1v1 Duel"
          title="Duel arena"
          description={
            <span className="font-mono">
              {played} matches · {wins} wins · {data?.solved.length ?? 0} problems
              solved
            </span>
          }
        />

        <div className="flex flex-wrap gap-2">
          <Button size="lg" onClick={createRoom} disabled={creating}>
            <Swords className="mr-2 h-4 w-4" />
            {creating ? "Creating…" : "Create room"}
          </Button>
          <Button asChild size="lg" variant="secondary">
            <Link href="/duel/problems">
              <ListChecks className="mr-2 h-4 w-4" />
              Problem bank
            </Link>
          </Button>
          <div className="flex items-center gap-2">
            <Input
              placeholder="Paste a room link to join…"
              value={joinLink}
              onChange={(e) => {
                setJoinLink(e.target.value);
                setJoinError(null);
              }}
              onKeyDown={(e) => e.key === "Enter" && joinByLink()}
              className="h-10 w-64 font-mono text-xs"
            />
            <Button
              size="lg"
              variant="secondary"
              onClick={joinByLink}
              disabled={!joinLink.trim()}
            >
              Join
            </Button>
          </div>
        </div>
        {joinError && <p className="text-sm text-destructive">{joinError}</p>}

        <Card className="border-border/60 bg-card/60">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <Swords className="h-4 w-4 text-primary" /> Matches
            </CardTitle>
          </CardHeader>
          <CardContent>
            {!data || data.matches.length === 0 ? (
              <EmptyState>
                No matches yet — create a room and send the link to your opponent.
              </EmptyState>
            ) : (
              <div className="space-y-1.5">
                {data.matches.map((m) => (
                  <div
                    key={m.id}
                    className="flex items-center gap-3 rounded-md border border-border/60 px-3 py-2"
                  >
                    <span className="font-mono text-sm text-primary">
                      {m.problemId}
                    </span>
                    <span className="text-sm text-muted-foreground">
                      vs {m.opponent}
                    </span>
                    {m.finished ? (
                      <Badge
                        variant="outline"
                        className={cn(
                          "font-mono",
                          m.won
                            ? "border-green-500/50 text-green-400"
                            : m.winnerIsSet
                              ? "border-red-500/50 text-red-400"
                              : "text-muted-foreground"
                        )}
                      >
                        {m.won ? "won" : m.winnerIsSet ? "lost" : "both DNF"}
                      </Badge>
                    ) : (
                      <Badge variant="outline" className="animate-pulse font-mono">
                        live
                      </Badge>
                    )}
                    <span className="ml-auto font-mono text-xs text-muted-foreground">
                      {new Date(m.startedAt).toLocaleString()}
                    </span>
                    <Button asChild size="sm" variant="ghost">
                      <Link href={`/duel/review/${m.id}`}>
                        <Video className="mr-1.5 h-3.5 w-3.5" />
                        Review
                      </Link>
                    </Button>
                    {m.finished && <ShareButton matchId={m.id} />}
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        <div className="grid gap-6 md:grid-cols-2">
          <Card className="border-border/60 bg-card/60">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <Trophy className="h-4 w-4 text-green-400" /> Solved by you
              </CardTitle>
            </CardHeader>
            <CardContent>
              {!data || data.solved.length === 0 ? (
                <p className="text-sm text-muted-foreground">Nothing yet.</p>
              ) : (
                <div className="space-y-1">
                  {data.solved.map((s) => (
                    <div
                      key={s.problemId}
                      className="flex items-center gap-2 font-mono text-sm"
                    >
                      <span className="text-primary">{s.problemId}</span>
                      <Badge variant="outline" className="font-mono text-xs">
                        {s.kind}
                      </Badge>
                      {s.solveMs !== null && (
                        <span className="ml-auto text-green-400">
                          {formatMsPrecise(s.solveMs)}
                        </span>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          <Card className="border-border/60 bg-card/60">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <Video className="h-4 w-4 text-primary" /> Recordings
              </CardTitle>
            </CardHeader>
            <CardContent>
              {!data || data.recordings.length === 0 ? (
                <p className="text-sm text-muted-foreground">
                  No webcam recordings yet.
                </p>
              ) : (
                <div className="space-y-1">
                  {data.recordings.map((r) => (
                    <Link
                      key={r.id}
                      href={`/replay/${r.id}`}
                      className="flex items-center gap-2 rounded px-1 py-0.5 font-mono text-sm hover:bg-accent"
                    >
                      <span className="text-primary">{r.problem_id}</span>
                      <Badge variant="outline" className="font-mono text-xs">
                        {r.kind}
                      </Badge>
                      <span
                        className={cn(
                          "text-xs",
                          r.outcome === "solved"
                            ? "text-green-400"
                            : "text-muted-foreground"
                        )}
                      >
                        {r.outcome === "solved" && r.solve_ms !== null
                          ? `AC ${formatMsPrecise(r.solve_ms)}`
                          : (r.outcome ?? "…")}
                      </span>
                      <span className="ml-auto text-xs text-muted-foreground">
                        {new Date(r.started_at).toLocaleDateString()}
                      </span>
                    </Link>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </main>
  );
}
