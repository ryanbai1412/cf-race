"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { OutcomeBadge, type SessionOutcome } from "@/components/shell/outcome-badge";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Segmented } from "@/components/ui/segmented";
import { EmptyState } from "@/components/shell/page";
import { formatMsPrecise } from "@/lib/templates";
import { ChevronLeft, ChevronRight, Video } from "lucide-react";

export type SessionListRow = {
  id: string;
  kind: string;
  problemId: string;
  startedAt: string;
  outcome: SessionOutcome;
  solveMs: number | null;
  timerSec: number | null;
  shared: boolean;
};

const KINDS = ["all", "solo", "duel", "event"] as const;
const OUTCOMES = ["all", "solved", "timeout", "abandoned"] as const;
const PAGE_SIZE = 25;

/** /sessions history list: kind + outcome filters, pagination (PRD §5.2). */
export function SessionsList({ sessions }: { sessions: SessionListRow[] }) {
  const [kind, setKind] = useState<(typeof KINDS)[number]>("all");
  const [outcome, setOutcome] = useState<(typeof OUTCOMES)[number]>("all");
  const [page, setPage] = useState(0);

  const filtered = useMemo(
    () =>
      sessions.filter(
        (s) =>
          (kind === "all" || s.kind === kind) &&
          (outcome === "all" || s.outcome === outcome)
      ),
    [sessions, kind, outcome]
  );
  const pages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const rows = filtered.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE);

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-2">
        <Segmented
          options={KINDS}
          value={kind}
          onChange={(k) => {
            setKind(k);
            setPage(0);
          }}
        />
        <Segmented
          options={OUTCOMES}
          value={outcome}
          onChange={(o) => {
            setOutcome(o);
            setPage(0);
          }}
        />
        <span className="ml-auto font-mono text-xs text-muted-foreground">
          {filtered.length} sessions
        </span>
      </div>

      <div className="divide-y divide-border/60 rounded-lg border border-border/60 bg-card/60">
        {rows.map((s) => (
          <div key={s.id} className="flex items-center gap-3 px-4 py-3">
            <span className="w-36 shrink-0 font-mono text-xs text-muted-foreground">
              {new Date(s.startedAt).toLocaleString()}
            </span>
            <Link
              href={`/problems/${s.problemId}`}
              className="font-mono text-sm text-primary hover:underline"
            >
              {s.problemId}
            </Link>
            <Badge variant="muted" className="font-mono text-xs">
              {s.kind}
            </Badge>
            <OutcomeBadge outcome={s.outcome} />
            {s.outcome === "solved" && s.solveMs !== null && (
              <span className="font-mono text-xs text-green-400 tabular-nums">
                {formatMsPrecise(s.solveMs)}
              </span>
            )}
            {s.shared && (
              <Badge variant="muted" className="font-mono text-xs">
                shared
              </Badge>
            )}
            <Button asChild size="sm" variant="ghost" className="ml-auto">
              <Link href={`/replay/${s.id}`}>
                <Video className="mr-1.5 h-3.5 w-3.5" />
                Replay
              </Link>
            </Button>
          </div>
        ))}
        {rows.length === 0 && (
          <EmptyState>
            {sessions.length === 0
              ? "No sessions yet \u2014 solve a problem to start your history."
              : "No sessions match these filters."}
          </EmptyState>
        )}
      </div>

      {pages > 1 && (
        <div className="flex items-center justify-center gap-2">
          <Button
            size="sm"
            variant="ghost"
            disabled={page === 0}
            onClick={() => setPage((p) => p - 1)}
          >
            <ChevronLeft className="mr-1.5 h-3.5 w-3.5" />
            Prev
          </Button>
          <span className="font-mono text-xs text-muted-foreground">
            {page + 1} / {pages}
          </span>
          <Button
            size="sm"
            variant="ghost"
            disabled={page >= pages - 1}
            onClick={() => setPage((p) => p + 1)}
          >
            Next
            <ChevronRight className="ml-1.5 h-3.5 w-3.5" />
          </Button>
        </div>
      )}
    </div>
  );
}
