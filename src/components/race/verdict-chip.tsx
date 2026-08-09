import { cn } from "@/lib/utils";

const STYLES: Record<string, string> = {
  AC: "bg-green-500/15 text-green-400 border-green-500/40",
  WA: "bg-red-500/15 text-red-400 border-red-500/40",
  TLE: "bg-amber-500/15 text-amber-400 border-amber-500/40",
  ML: "bg-amber-500/15 text-amber-400 border-amber-500/40",
  RE: "bg-orange-500/15 text-orange-400 border-orange-500/40",
  CE: "bg-purple-500/15 text-purple-400 border-purple-500/40",
  IE: "bg-fuchsia-500/15 text-fuchsia-400 border-fuchsia-500/40",
  PENDING: "bg-blue-500/15 text-blue-400 border-blue-500/40 animate-pulse",
  SKIP: "bg-muted text-muted-foreground border-border",
};

export function VerdictChip({ verdict, className }: { verdict: string; className?: string }) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded border px-1.5 py-0.5 font-mono text-xs font-bold",
        STYLES[verdict] ?? STYLES.SKIP,
        className
      )}
    >
      {verdict === "PENDING" ? "JUDGING" : verdict}
    </span>
  );
}
