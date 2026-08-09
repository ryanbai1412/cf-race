"use client";

import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { CalendarPlus, Play, Swords } from "lucide-react";
import { toast } from "sonner";

/** Home quick actions: practice, start a duel, create event (PRD §3). */
export function QuickActions({
  practiceProblemId,
}: {
  practiceProblemId: string | null;
}) {
  const router = useRouter();
  const [creating, setCreating] = useState(false);

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
    <div className="flex flex-wrap gap-3">
      {practiceProblemId && (
        <Button asChild size="lg">
          <Link href={`/problems/${practiceProblemId}/solve`}>
            <Play className="mr-2 h-4 w-4" />
            Practice
          </Link>
        </Button>
      )}
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
  );
}
