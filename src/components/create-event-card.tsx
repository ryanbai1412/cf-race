"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";

export function CreateEventCard() {
  const [name, setName] = useState("");
  const [busy, setBusy] = useState(false);
  const router = useRouter();

  async function createEvent() {
    if (!name.trim()) return;
    setBusy(true);
    try {
      const res = await fetch("/api/events", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? "Failed to create event");
      router.push(`/e/${data.id}/join?k=${data.secret}&to=/admin`);
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed to create event");
      setBusy(false);
    }
  }

  return (
    <Card className="w-full max-w-md border-border/60 bg-card/60">
      <CardHeader>
        <CardTitle className="text-lg">Create an event</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <Input
          placeholder="Event name — e.g. IOI 2026 Booth"
          value={name}
          onChange={(e) => setName(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && createEvent()}
          maxLength={80}
        />
        <Button className="w-full" onClick={createEvent} disabled={busy || !name.trim()}>
          {busy ? "Creating…" : "Create event"}
        </Button>
      </CardContent>
    </Card>
  );
}
