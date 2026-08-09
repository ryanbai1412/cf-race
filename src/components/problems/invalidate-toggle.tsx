"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
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
  const [open, setOpen] = useState(false);
  const [reason, setReason] = useState("");

  const submit = async (body: Record<string, unknown>) => {
    setBusy(true);
    try {
      const res = await fetch("/api/duel/invalidate", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(body),
      });
      const d = await res.json();
      if (!res.ok) throw new Error(d.error ?? "Failed");
      setOpen(false);
      setReason("");
      router.refresh();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed");
    } finally {
      setBusy(false);
    }
  };

  if (invalidated) {
    return (
      <Button
        size="sm"
        variant="outline"
        onClick={() => submit({ problemId, revoke: true })}
        disabled={busy}
      >
        <Undo2 className="mr-1.5 h-3.5 w-3.5" />
        Un-invalidate
      </Button>
    );
  }

  return (
    <>
      <Button size="sm" variant="outline" onClick={() => setOpen(true)} disabled={busy}>
        <Ban className="mr-1.5 h-3.5 w-3.5" />
        Invalidate
      </Button>
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Invalidate problem</DialogTitle>
            <DialogDescription>
              Excludes <span className="font-mono">{problemId}</span> from
              random picks and duels. You can un-invalidate it later.
            </DialogDescription>
          </DialogHeader>
          <Input
            placeholder="Reason (optional)"
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            autoFocus
          />
          <DialogFooter>
            <Button variant="ghost" onClick={() => setOpen(false)} disabled={busy}>
              Cancel
            </Button>
            <Button
              variant="destructive"
              onClick={() =>
                submit({ problemId, reason: reason.trim() || undefined })
              }
              disabled={busy}
            >
              <Ban className="mr-1.5 h-3.5 w-3.5" />
              Invalidate
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
