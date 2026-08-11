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
  initialGennaOnly,
}: {
  eventId: string;
  initialRequireWebcam: boolean;
  initialGennaOnly: boolean;
}) {
  const [requireWebcam, setRequireWebcam] = useState(initialRequireWebcam);
  const [gennaOnly, setGennaOnly] = useState(initialGennaOnly);
  const [saving, setSaving] = useState(false);

  const save = async (patch: Record<string, boolean>): Promise<boolean> => {
    setSaving(true);
    const res = await fetch("/api/events/settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ eventId, ...patch }),
    }).catch(() => null);
    setSaving(false);
    if (!res?.ok) toast.error("Could not save setting");
    return Boolean(res?.ok);
  };

  const toggle = async (next: boolean) => {
    setRequireWebcam(next);
    if (!(await save({ requireWebcam: next }))) {
      setRequireWebcam(!next);
      return;
    }
    toast.success(next ? "Webcam required at stations" : "Webcam optional");
  };

  const toggleGenna = async (next: boolean) => {
    setGennaOnly(next);
    if (!(await save({ gennaOnly: next }))) {
      setGennaOnly(!next);
      return;
    }
    toast.success(next ? "Genna problems only" : "All problems allowed");
  };

  return (
    <Card className="border-border/60 bg-card/60">
      <CardHeader>
        <CardTitle className="text-lg">Settings</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
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
        <div className="flex items-center gap-3">
          <Switch
            id="genna-only"
            checked={gennaOnly}
            onCheckedChange={toggleGenna}
            disabled={saving}
          />
          <Label htmlFor="genna-only" className="cursor-pointer">
            Genna problems only — races limited to problems with a Genna
            reference solve
          </Label>
        </div>
      </CardContent>
    </Card>
  );
}
