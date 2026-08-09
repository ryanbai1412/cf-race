"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Ban, Undo2 } from "lucide-react";
import { toast } from "sonner";

/** Invalidate / un-invalidate a problem (excludes it from random picks). */
export function InvalidateToggle({
  problemId,
  invalidated,
}: {
  problemId: string;
  invalidated: boolean;
}) {
  const router = useRouter();
  const [busy, setBusy] = useState(false);

  const toggle = async () => {
    const reason = invalidated
      ? null
      : window.prompt("Why is this problem invalid? (optional)") ?? undefined;
    setBusy(true);
    try {
      const res = await fetch("/api/duel/invalidate", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(
          invalidated ? { problemId, revoke: true } : { problemId, reason }
        ),
      });
      const d = await res.json();
      if (!res.ok) throw new Error(d.error ?? "Failed");
      router.refresh();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed");
    } finally {
      setBusy(false);
    }
  };

  return (
    <Button size="sm" variant="outline" onClick={toggle} disabled={busy}>
      {invalidated ? (
        <>
          <Undo2 className="mr-1.5 h-3.5 w-3.5" />
          Un-invalidate
        </>
      ) : (
        <>
          <Ban className="mr-1.5 h-3.5 w-3.5" />
          Invalidate
        </>
      )}
    </Button>
  );
}
