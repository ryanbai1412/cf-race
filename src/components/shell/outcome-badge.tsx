import { Badge, type BadgeProps } from "@/components/ui/badge";

export type SessionOutcome = "solved" | "timeout" | "abandoned" | null;

/**
 * Outcome badge shared across session lists. Abandoned runs get a distinct
 * neutral badge — they must never look like losses (PRD §9 pass 3).
 */
export function OutcomeBadge({ outcome }: { outcome: SessionOutcome }) {
  const variants: Record<string, BadgeProps["variant"]> = {
    solved: "success",
    timeout: "danger",
    abandoned: "muted",
    active: "outline",
  };
  const key = outcome ?? "active";
  const label =
    outcome === "solved"
      ? "Solved"
      : outcome === "timeout"
        ? "Unsolved"
        : outcome === "abandoned"
          ? "Abandoned"
          : "Active";
  return (
    <Badge
      variant={variants[key]}
      className={key === "active" ? "border-primary/50 font-mono text-xs text-primary" : "font-mono text-xs"}
    >
      {label}
    </Badge>
  );
}
