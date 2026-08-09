"use client";

import { useState } from "react";
import { Star } from "lucide-react";
import { cn } from "@/lib/utils";

/**
 * Interactive 1-5 star widget. Clicking your current rating clears it.
 * Read-only when `disabled` (e.g. logged out).
 */
export function StarRating({
  problemId,
  initial,
  disabled,
  size = "md",
  onRated,
}: {
  problemId: string;
  initial: number | null;
  disabled?: boolean;
  size?: "sm" | "md";
  onRated?: (stars: number | null) => void;
}) {
  const [stars, setStars] = useState<number | null>(initial);
  const [hover, setHover] = useState<number | null>(null);
  const [saving, setSaving] = useState(false);

  const rate = async (n: number) => {
    if (disabled || saving) return;
    const next = stars === n ? 0 : n;
    setSaving(true);
    const prev = stars;
    setStars(next === 0 ? null : next);
    const res = await fetch(`/api/problems/${problemId}/rate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ stars: next }),
    }).catch(() => null);
    if (!res?.ok) setStars(prev);
    else onRated?.(next === 0 ? null : next);
    setSaving(false);
  };

  const px = size === "sm" ? "h-4 w-4" : "h-5 w-5";
  const shown = hover ?? stars ?? 0;
  return (
    <div
      className="flex items-center gap-0.5"
      onMouseLeave={() => setHover(null)}
      title={disabled ? "Sign in to rate" : "Rate this problem"}
    >
      {[1, 2, 3, 4, 5].map((n) => (
        <button
          key={n}
          type="button"
          disabled={disabled || saving}
          onClick={() => rate(n)}
          onMouseEnter={() => !disabled && setHover(n)}
          className={cn(
            "rounded p-0.5 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring",
            disabled ? "cursor-default" : "cursor-pointer"
          )}
          aria-label={`${n} star${n > 1 ? "s" : ""}`}
        >
          <Star
            className={cn(
              px,
              n <= shown
                ? "fill-yellow-400 text-yellow-400"
                : "text-muted-foreground/40"
            )}
          />
        </button>
      ))}
    </div>
  );
}
