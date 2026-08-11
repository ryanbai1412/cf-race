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
  initialSelfServe,
}: {
  eventId: string;
  initialRequireWebcam: boolean;
  initialSelfServe: boolean;
}) {
  const [requireWebcam, setRequireWebcam] = useState(initialRequireWebcam);
  const [selfServe, setSelfServe] = useState(initialSelfServe);
  const [saving, setSaving] = useState(false);

  const save = async (
    patch: { requireWebcam?: boolean; selfServe?: boolean },
    rollback: () => void,
    okMsg: string
  ) => {
    setSaving(true);
    const res = await fetch("/api/events/settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ eventId, ...patch }),
    }).catch(() => null);
    setSaving(false);
    if (!res?.ok) {
      rollback();
      toast.error("Could not save setting");
      return;
    }
    toast.success(okMsg);
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
            onCheckedChange={(next) => {
              setRequireWebcam(next);
              void save(
                { requireWebcam: next },
                () => setRequireWebcam(!next),
                next ? "Webcam required at stations" : "Webcam optional"
              );
            }}
            disabled={saving}
          />
          <Label htmlFor="require-webcam" className="cursor-pointer">
            Require webcam — stations must grant camera access before racing
          </Label>
        </div>
        <div className="flex items-center gap-3">
          <Switch
            id="self-serve"
            checked={selfServe}
            onCheckedChange={(next) => {
              setSelfServe(next);
              void save(
                { selfServe: next },
                () => setSelfServe(!next),
                next ? "Self-serve: races auto-start" : "Races start from admin"
              );
            }}
            disabled={saving}
          />
          <Label htmlFor="self-serve" className="cursor-pointer">
            Self-serve — auto-start a random problem 10s after both stations
            ready up
          </Label>
        </div>
      </CardContent>
    </Card>
  );
}
