"use client";

import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { CalendarPlus, Play, Swords } from "lucide-react";
import { toast } from "sonner";
import { RatingPicker } from "@/components/problems/rating-picker";
import { usePracticeSettings } from "@/hooks/use-practice-settings";
import { requestPracticeProblem } from "@/lib/practice-client";
import type { ProblemRating } from "@/lib/problem-rating";

/** Home quick actions: practice, start a duel, create event (PRD §3). */
export function QuickActions({
  counts,
}: {
  counts: Record<ProblemRating, number>;
}) {
  const router = useRouter();
  const [creating, setCreating] = useState(false);
  const [picking, setPicking] = useState(false);
  const [pickError, setPickError] = useState<string | null>(null);
  const { rating, chooseRating } = usePracticeSettings();

  const practice = async () => {
    setPicking(true);
    setPickError(null);
    try {
      const id = await requestPracticeProblem(rating);
      router.push(`/problems/${id}/solve`);
    } catch (e) {
      setPickError(e instanceof Error ? e.message : "Could not pick a problem");
      setPicking(false);
    }
  };

  const startDuel = async () => {
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

  return (
    <div className="space-y-4">
      <div className="max-w-lg rounded-lg border border-border/60 bg-card/60 p-4">
        <RatingPicker value={rating} onChange={(r) => { chooseRating(r); setPickError(null); }} counts={counts} disabled={picking} />
        {counts[rating] === 0 && <p className="mt-3 text-sm text-muted-foreground" role="status">This pool is not available yet. Choose another rating.</p>}
        {pickError && <p className="mt-3 text-sm text-destructive" role="alert">{pickError}</p>}
      </div>
      <div className="flex flex-wrap gap-3">
        <Button size="lg" onClick={practice} disabled={picking || counts[rating] === 0}>
            <Play className="mr-2 h-4 w-4" />
            {picking ? "Picking…" : `Practice · ${rating}`}
        </Button>
      <Button size="lg" variant="secondary" onClick={startDuel} disabled={creating}>
        <Swords className="mr-2 h-4 w-4" />
        {creating ? "Creating…" : "Start a duel"}
      </Button>
      <Button asChild size="lg" variant="secondary">
        <Link href="/events">
          <CalendarPlus className="mr-2 h-4 w-4" />
          Create event
        </Link>
      </Button>
      </div>
    </div>
  );
}
