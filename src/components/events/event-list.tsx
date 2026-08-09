"use client";

import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { EmptyState, SectionTitle } from "@/components/shell/page";
import { toast } from "sonner";
import { ChevronDown, ChevronUp, Copy, ExternalLink } from "lucide-react";

export type EventListRow = {
  id: string;
  name: string;
  secret: string;
  createdAt: string;
};

const DEVICES: { label: string; to: string }[] = [
  { label: "Station 1", to: "/station/1" },
  { label: "Station 2", to: "/station/2" },
  { label: "Monitor A", to: "/monitor/a" },
  { label: "Monitor B", to: "/monitor/b" },
  { label: "Admin", to: "/admin" },
];

/** Your events with admin + device links (PRD 11 §7.1). */
export function EventList({ events }: { events: EventListRow[] }) {
  const [expanded, setExpanded] = useState<string | null>(null);

  const linkFor = (e: EventListRow, to: string) =>
    `${window.location.origin}/e/${e.id}/join?k=${e.secret}&to=${encodeURIComponent(to)}`;

  if (events.length === 0) {
    return (
      <div className="space-y-3">
        <SectionTitle>Your events</SectionTitle>
        <div className="rounded-lg border border-border/60 bg-card/60">
          <EmptyState>No events yet — create one above.</EmptyState>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <SectionTitle>Your events</SectionTitle>
      {events.map((e) => (
        <Card key={e.id} className="border-border/60 bg-card/60">
          <CardContent className="space-y-3 p-4">
            <div className="flex flex-wrap items-center gap-3">
              <span className="font-semibold">{e.name}</span>
              <Badge variant="outline" className="font-mono text-xs">
                {new Date(e.createdAt).toLocaleDateString()}
              </Badge>
              <div className="ml-auto flex items-center gap-2">
                <Button
                  size="sm"
                  onClick={() => window.open(linkFor(e, "/admin"), "_blank")}
                >
                  <ExternalLink className="mr-1.5 h-3.5 w-3.5" />
                  Admin console
                </Button>
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={() => setExpanded(expanded === e.id ? null : e.id)}
                >
                  Device links
                  {expanded === e.id ? (
                    <ChevronUp className="ml-1 h-3.5 w-3.5" />
                  ) : (
                    <ChevronDown className="ml-1 h-3.5 w-3.5" />
                  )}
                </Button>
              </div>
            </div>
            {expanded === e.id && (
              <div className="grid gap-2 sm:grid-cols-2">
                {DEVICES.map((d) => (
                  <div
                    key={d.to}
                    className="flex items-center justify-between rounded-md border border-border/60 px-3 py-2"
                  >
                    <span className="text-sm">{d.label}</span>
                    <Button
                      size="sm"
                      variant="secondary"
                      onClick={() => {
                        navigator.clipboard.writeText(linkFor(e, d.to));
                        toast.success(`${d.label} link copied`);
                      }}
                    >
                      <Copy className="mr-1.5 h-3.5 w-3.5" />
                      Copy link
                    </Button>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
