"use client";

import { PROBLEM_RATINGS, type ProblemRating } from "@/lib/problem-rating";
import { cn } from "@/lib/utils";

export function RatingPicker({ value, onChange, counts, disabled = false }: {
  value: ProblemRating;
  onChange: (rating: ProblemRating) => void;
  counts?: Partial<Record<ProblemRating, number>>;
  disabled?: boolean;
}) {
  return (
    <fieldset disabled={disabled} className="min-w-0 space-y-2">
      <legend className="mb-2 text-xs font-medium text-muted-foreground">Codeforces rating</legend>
      <div className="grid grid-cols-5 gap-1.5">
        {PROBLEM_RATINGS.map((rating) => (
          <button key={rating} type="button" aria-pressed={value === rating}
            onClick={() => onChange(rating)}
            className={cn("min-w-0 rounded-md border px-2 py-2 font-mono text-sm font-semibold tabular-nums transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50",
              value === rating ? "border-primary bg-primary/15 text-primary" : "border-border/60 text-muted-foreground hover:bg-accent hover:text-foreground")}
          >
            {rating}
            {counts?.[rating] !== undefined && <span className="mt-0.5 block text-[10px] font-normal">{counts[rating]} problems</span>}
          </button>
        ))}
      </div>
      <p className="text-xs text-muted-foreground">Exact rating, not a range. Higher ratings are harder.</p>
    </fieldset>
  );
}
