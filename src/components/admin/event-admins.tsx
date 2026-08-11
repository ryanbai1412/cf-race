"use client";

import { useState } from "react";
import { toast } from "sonner";
import { X } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import type { EventAdmin } from "@/lib/event-admins";

/** Who can open this event's admin console while logged in. */
export function EventAdmins({
  eventId,
  initialAdmins,
}: {
  eventId: string;
  initialAdmins: EventAdmin[];
}) {
  const [admins, setAdmins] = useState(initialAdmins);
  const [email, setEmail] = useState("");
  const [busy, setBusy] = useState(false);

  const post = async (
    body: Record<string, string>
  ): Promise<EventAdmin[] | null> => {
    setBusy(true);
    const res = await fetch("/api/events/admins", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ eventId, ...body }),
    }).catch(() => null);
    setBusy(false);
    const json = (await res?.json().catch(() => null)) as {
      admins?: EventAdmin[];
      error?: string;
    } | null;
    if (!res?.ok) {
      toast.error(json?.error ?? "Something went wrong");
      return null;
    }
    return json?.admins ?? null;
  };

  const add = async () => {
    const next = await post({ action: "add", email });
    if (!next) return;
    setAdmins(next);
    setEmail("");
    toast.success("Admin added");
  };

  const remove = async (admin: EventAdmin) => {
    const next = await post({ action: "remove", userId: admin.userId });
    if (!next) return;
    setAdmins(next);
    toast.success(`Removed ${admin.email ?? admin.userId}`);
  };

  return (
    <Card className="border-border/60 bg-card/60">
      <CardHeader>
        <CardTitle className="text-lg">Admins</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <ul className="space-y-2 text-sm">
          {admins.map((a) => (
            <li key={a.userId} className="flex items-center gap-2">
              <span className="truncate">{a.email ?? a.userId}</span>
              {a.isCreator ? (
                <Badge variant="muted" className="text-xs">
                  creator
                </Badge>
              ) : (
                <Button
                  size="sm"
                  variant="ghost"
                  className="ml-auto"
                  disabled={busy}
                  onClick={() => remove(a)}
                >
                  <X className="h-3.5 w-3.5" />
                </Button>
              )}
            </li>
          ))}
        </ul>
        <form
          className="flex items-center gap-2"
          onSubmit={(e) => {
            e.preventDefault();
            if (email.trim()) void add();
          }}
        >
          <Input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="teammate@example.com"
            className="max-w-xs"
          />
          <Button size="sm" type="submit" disabled={busy || !email.trim()}>
            Add admin
          </Button>
        </form>
        <p className="text-xs text-muted-foreground">
          Admins can open this console when signed in — no secret link needed.
          They must have signed in to the app at least once.
        </p>
      </CardContent>
    </Card>
  );
}
