import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

export type SessionOutcome = "solved" | "timeout" | "abandoned" | null;

/**
 * Outcome badge shared across session lists. Abandoned runs get a distinct
 * neutral badge — they must never look like losses (PRD §9 pass 3).
 */
export function OutcomeBadge({ outcome }: { outcome: SessionOutcome }) {
  const styles: Record<string, string> = {
    solved: "border-green-500/50 text-green-400",
    timeout: "border-red-500/50 text-red-400",
    abandoned: "border-border text-muted-foreground",
    active: "border-primary/50 text-primary",
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
    <Badge variant="outline" className={cn("font-mono text-xs", styles[key])}>
      {label}
    </Badge>
  );
}
