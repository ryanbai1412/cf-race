"use client";

import { cn } from "@/lib/utils";

/**
 * Segmented filter control shared by the problem bank, the session list and
 * the duel problem bank so equivalent filters look identical everywhere.
 */
export function Segmented<T extends string>({
  options,
  value,
  onChange,
  className,
  labelFor,
}: {
  options: readonly T[];
  value: T;
  onChange: (value: T) => void;
  className?: string;
  labelFor?: (option: T) => string;
}) {
  return (
    <div
      className={cn(
        "flex overflow-hidden rounded-md border border-border/60",
        className
      )}
    >
      {options.map((o) => (
        <button
          key={o}
          type="button"
          aria-pressed={value === o}
          onClick={() => onChange(o)}
          className={cn(
            "px-3 py-1.5 font-mono text-xs capitalize transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-inset focus-visible:ring-ring",
            value === o
              ? "bg-primary text-primary-foreground"
              : "text-muted-foreground hover:bg-accent hover:text-foreground"
          )}
        >
          {labelFor ? labelFor(o) : o}
        </button>
      ))}
    </div>
  );
}
