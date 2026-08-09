"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Segmented } from "@/components/ui/segmented";
import { SoloAuthButton, useSoloAuth } from "@/components/solo/auth-button";
import {
  CenteredMessage,
  EmptyState,
  LoadingScreen,
  PageHeader,
} from "@/components/shell/page";
import { formatMsPrecise } from "@/lib/templates";
import { cn } from "@/lib/utils";
import { ArrowLeft, Ban, RotateCcw } from "lucide-react";
import { toast } from "sonner";

type BankProblem = {
  id: string;
  name: string;
  rating: number | null;
  touristTimeMs: number | null;
  solvedByYouMs?: number | null;
  solvedByAnyone: boolean;
  invalidated: boolean;
  invalidReason: string | null;
};

const VIEWS = ["all", "solved-you", "solved-any", "invalidated"] as const;
type View = (typeof VIEWS)[number];

const VIEW_LABELS: Record<View, string> = {
  all: "All",
  "solved-you": "Solved by you",
  "solved-any": "Solved by anyone",
  invalidated: "Invalidated",
};

export function DuelProblems() {
  const auth = useSoloAuth();
  const { user, loading } = auth;
  const [problems, setProblems] = useState<BankProblem[] | null>(null);
  const [view, setView] = useState<View>("all");
  const [busy, setBusy] = useState<string | null>(null);

  const refresh = useCallback(() => {
    fetch("/api/duel/problems", { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => setProblems(d?.problems ?? null))
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (user) refresh();
  }, [user, refresh]);

  const toggleInvalid = async (p: BankProblem) => {
    setBusy(p.id);
    try {
      let reason: string | null = null;
      if (!p.invalidated) {
        reason = window.prompt("Reason for invalidating (optional):") ?? null;
      }
      const res = await fetch("/api/duel/invalidate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(
          p.invalidated
            ? { problemId: p.id, revoke: true }
            : { problemId: p.id, reason }
        ),
      });
      const d = await res.json();
      if (!res.ok) throw new Error(d.error ?? "Failed");
      refresh();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed");
    } finally {
      setBusy(null);
    }
  };

  if (loading) return <LoadingScreen />;
  if (!user) {
    return (
      <CenteredMessage
        eyebrow="Problem bank"
        title="Sign in to view the duel bank"
        description="The duel problem bank shows what you and your opponents have already solved."
      >
        <SoloAuthButton {...auth} next="/duel/problems" />
      </CenteredMessage>
    );
  }

  const filtered = (problems ?? []).filter((p) => {
    if (view === "solved-you") return p.solvedByYouMs !== undefined;
    if (view === "solved-any") return p.solvedByAnyone;
    if (view === "invalidated") return p.invalidated;
    return true;
  });

  return (
    <main className="relative min-h-full overflow-hidden px-6 py-10">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(99,102,241,0.12),transparent_60%)]" />
      <div className="relative mx-auto w-full max-w-5xl space-y-6">
        <Button asChild size="sm" variant="ghost" className="-ml-3">
          <Link href="/duels">
            <ArrowLeft className="mr-1.5 h-3.5 w-3.5" />
            Duels
          </Link>
        </Button>

        <PageHeader
          eyebrow="Problem bank"
          title="Duel problems"
          description="Problems eligible for duels — invalidate any that leaked."
        />

        <Segmented
          className="w-fit"
          options={VIEWS}
          value={view}
          onChange={setView}
          labelFor={(v) => VIEW_LABELS[v]}
        />

        <Card className="border-border/60 bg-card/60">
          <CardContent className="pt-6">
            {problems === null ? (
              <EmptyState className="animate-pulse">Loading problems…</EmptyState>
            ) : filtered.length === 0 ? (
              <EmptyState>No problems in this view.</EmptyState>
            ) : (
              <div className="space-y-1.5">
                {filtered.map((p) => (
                  <div
                    key={p.id}
                    className={cn(
                      "flex items-center gap-3 rounded-md border border-border/60 px-3 py-2",
                      p.invalidated && "opacity-60"
                    )}
                  >
                    <div className="min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="font-mono text-sm text-primary">
                          {p.id}
                        </span>
                        {p.rating !== null && (
                          <Badge variant="outline" className="font-mono text-xs">
                            {p.rating}
                          </Badge>
                        )}
                        {p.invalidated && (
                          <Badge
                            variant="outline"
                            className="border-amber-500/50 font-mono text-xs text-amber-400"
                          >
                            invalidated
                            {p.invalidReason ? `: ${p.invalidReason}` : ""}
                          </Badge>
                        )}
                      </div>
                      <p className="truncate text-sm text-muted-foreground">
                        {p.name}
                      </p>
                    </div>
                    <div className="ml-auto flex items-center gap-2">
                      {p.solvedByYouMs !== undefined ? (
                        <span className="font-mono text-xs text-green-400">
                          you{" "}
                          {p.solvedByYouMs !== null
                            ? formatMsPrecise(p.solvedByYouMs)
                            : "AC"}
                        </span>
                      ) : p.solvedByAnyone ? (
                        <span className="font-mono text-xs text-muted-foreground">
                          solved
                        </span>
                      ) : null}
                      <Button
                        size="sm"
                        variant="ghost"
                        disabled={busy === p.id}
                        onClick={() => void toggleInvalid(p)}
                      >
                        {p.invalidated ? (
                          <>
                            <RotateCcw className="mr-1.5 h-3.5 w-3.5" />
                            Restore
                          </>
                        ) : (
                          <>
                            <Ban className="mr-1.5 h-3.5 w-3.5" />
                            Invalidate
                          </>
                        )}
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </main>
  );
}
