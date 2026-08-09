"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { formatMsPrecise } from "@/lib/templates";
import { cn } from "@/lib/utils";
import { Play, Shuffle, Video } from "lucide-react";
import { StarRating } from "@/components/problems/star-rating";

export type ProblemStatus = "unsolved" | "solved" | "attempted" | "invalidated";

export type ProblemBankRow = {
  id: string;
  name: string;
  rating: number | null;
  tags: string[];
  touristTimeMs: number | null;
  status: ProblemStatus;
  bestSolveMs: number | null;
  sessionCount: number;
  myStars: number | null;
};

const FILTERS = ["all", "unsolved", "solved", "attempted", "invalidated"] as const;
type Filter = (typeof FILTERS)[number];
type Sort = "id" | "rating" | "time";

const FILTER_KEY = "cfr-problems-filter";

/** The problem bank table: filters, /-to-search, sortable columns. */
export function ProblemsTable({ problems }: { problems: ProblemBankRow[] }) {
  const [filter, setFilter] = useState<Filter>("all");
  const [search, setSearch] = useState("");
  const [sort, setSort] = useState<Sort>("id");
  const searchRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    const saved = localStorage.getItem(FILTER_KEY) as Filter | null;
    if (saved && (FILTERS as readonly string[]).includes(saved)) setFilter(saved);
  }, []);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "/" && document.activeElement?.tagName !== "INPUT") {
        e.preventDefault();
        searchRef.current?.focus();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  const setAndSaveFilter = (f: Filter) => {
    setFilter(f);
    localStorage.setItem(FILTER_KEY, f);
  };

  const rows = useMemo(() => {
    const q = search.trim().toLowerCase();
    let out = problems.filter(
      (p) =>
        (filter === "all" || p.status === filter) &&
        (!q ||
          p.id.toLowerCase().includes(q) ||
          p.name.toLowerCase().includes(q))
    );
    out = [...out].sort((a, b) => {
      if (sort === "rating")
        return (a.rating ?? Infinity) - (b.rating ?? Infinity);
      if (sort === "time")
        return (a.bestSolveMs ?? Infinity) - (b.bestSolveMs ?? Infinity);
      return a.id.localeCompare(b.id);
    });
    return out;
  }, [problems, filter, search, sort]);

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-2">
        <div className="flex overflow-hidden rounded-md border border-border">
          {FILTERS.map((f) => (
            <button
              key={f}
              onClick={() => setAndSaveFilter(f)}
              className={cn(
                "px-3 py-1.5 font-mono text-xs capitalize",
                filter === f
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-accent"
              )}
            >
              {f}
            </button>
          ))}
        </div>
        <Input
          ref={searchRef}
          placeholder="Search ( / )"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="h-8 w-48 font-mono text-sm"
        />
        <Button
          size="sm"
          variant="secondary"
          className="h-8 shrink-0"
          onClick={() => {
            const pool = problems.filter((p) => p.status === "unsolved");
            if (pool.length === 0) return;
            const pick = pool[Math.floor(Math.random() * pool.length)];
            window.location.href = `/problems/${pick.id}/solve`;
          }}
        >
          <Shuffle className="mr-1.5 h-3.5 w-3.5" />
          Random unsolved
        </Button>
        <div className="ml-auto flex items-center gap-1 font-mono text-xs text-muted-foreground">
          sort:
          {(["id", "rating", "time"] as Sort[]).map((s) => (
            <button
              key={s}
              onClick={() => setSort(s)}
              className={cn(
                "rounded px-2 py-1",
                sort === s ? "bg-accent text-foreground" : "hover:bg-accent"
              )}
            >
              {s}
            </button>
          ))}
        </div>
      </div>

      <div className="divide-y divide-border/60 rounded-lg border border-border/60 bg-card/60">
        {rows.map((p) => (
          <div key={p.id} className="flex items-center gap-3 px-4 py-3">
            <Link
              href={`/problems/${p.id}`}
              className="w-20 shrink-0 font-mono text-sm font-bold text-primary hover:underline"
            >
              {p.id}
            </Link>
            <Link
              href={`/problems/${p.id}`}
              className="min-w-0 truncate text-sm hover:underline"
            >
              {p.name}
            </Link>
            {p.rating !== null && (
              <Badge variant="outline" className="shrink-0 font-mono text-xs">
                {p.rating}
              </Badge>
            )}
            {p.status === "invalidated" && (
              <Badge
                variant="outline"
                className="shrink-0 border-amber-500/50 font-mono text-xs text-amber-400"
              >
                invalidated
              </Badge>
            )}
            <span className="ml-auto shrink-0 font-mono text-xs">
              {p.status === "solved" && p.bestSolveMs !== null ? (
                <span className="text-green-400">
                  solved · {formatMsPrecise(p.bestSolveMs)}
                </span>
              ) : p.status === "attempted" ? (
                <span className="text-amber-400">attempted</span>
              ) : p.status === "unsolved" ? (
                <span className="text-muted-foreground">unsolved</span>
              ) : null}
            </span>
            <Button asChild size="sm" className="shrink-0">
              <Link href={`/problems/${p.id}/solve`}>
                <Play className="mr-1.5 h-3.5 w-3.5" />
                Solve
              </Link>
            </Button>
            <div className="shrink-0">
              <StarRating problemId={p.id} initial={p.myStars} size="sm" />
            </div>
            {p.sessionCount > 0 && (
              <Button asChild size="sm" variant="ghost" className="shrink-0">
                <Link href={`/problems/${p.id}`}>
                  <Video className="mr-1.5 h-3.5 w-3.5" />
                  {p.sessionCount}
                </Link>
              </Button>
            )}
          </div>
        ))}
        {rows.length === 0 && (
          <p className="px-4 py-8 text-center font-mono text-sm text-muted-foreground">
            No problems match.
          </p>
        )}
      </div>
    </div>
  );
}
