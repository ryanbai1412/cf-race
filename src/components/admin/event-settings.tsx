"use client";

import { useState } from "react";
import { toast } from "sonner";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";

/** Event-level settings block on the admin console. */
export function EventSettings({
  eventId,
  initialRequireWebcam,
}: {
  eventId: string;
  initialRequireWebcam: boolean;
}) {
  const [requireWebcam, setRequireWebcam] = useState(initialRequireWebcam);
  const [saving, setSaving] = useState(false);

  const toggle = async (next: boolean) => {
    setSaving(true);
    setRequireWebcam(next);
    const res = await fetch("/api/events/settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ eventId, requireWebcam: next }),
    }).catch(() => null);
    setSaving(false);
    if (!res?.ok) {
      setRequireWebcam(!next);
      toast.error("Could not save setting");
      return;
    }
    toast.success(next ? "Webcam required at stations" : "Webcam optional");
  };

  return (
    <Card className="border-border/60 bg-card/60">
      <CardHeader>
        <CardTitle className="text-lg">Settings</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex items-center gap-3">
          <Switch
            id="require-webcam"
            checked={requireWebcam}
            onCheckedChange={toggle}
            disabled={saving}
          />
          <Label htmlFor="require-webcam" className="cursor-pointer">
            Require webcam — stations must grant camera access before racing
          </Label>
        </div>
      </CardContent>
    </Card>
  );
}
