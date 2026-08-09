"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";
import { Copy } from "lucide-react";

const DEVICES: { label: string; to: string }[] = [
  { label: "Station 1", to: "/station/1" },
  { label: "Station 2", to: "/station/2" },
  { label: "Monitor A", to: "/monitor/a" },
  { label: "Monitor B", to: "/monitor/b" },
  { label: "Admin", to: "/admin" },
];

export function DeviceLinks({
  eventId,
  secret,
}: {
  eventId: string;
  secret: string;
}) {
  function linkFor(to: string): string {
    const origin = typeof window !== "undefined" ? window.location.origin : "";
    return `${origin}/e/${eventId}/join?k=${secret}&to=${encodeURIComponent(to)}`;
  }

  return (
    <Card className="border-border/60 bg-card/60">
      <CardHeader>
        <CardTitle className="text-lg">Device links</CardTitle>
      </CardHeader>
      <CardContent className="grid gap-3 sm:grid-cols-2">
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
                navigator.clipboard.writeText(linkFor(d.to));
                toast.success(`${d.label} link copied`);
              }}
            >
              <Copy className="mr-1.5 h-3.5 w-3.5" /> Copy link
            </Button>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
