"use client";

import { useState } from "react";
import { toast } from "sonner";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

/** Event-level settings block on the admin console. */
export function EventSettings({
  eventId,
  initialRequireWebcam,
  initialSelfServe,
  initialGennaOnly,
  initialTimerSec,
}: {
  eventId: string;
  initialRequireWebcam: boolean;
  initialSelfServe: boolean;
  initialGennaOnly: boolean;
  initialTimerSec: number;
}) {
  const [requireWebcam, setRequireWebcam] = useState(initialRequireWebcam);
  const [selfServe, setSelfServe] = useState(initialSelfServe);
  const [gennaOnly, setGennaOnly] = useState(initialGennaOnly);
  const [timerSec, setTimerSec] = useState(String(initialTimerSec));
  const [saving, setSaving] = useState(false);

  const save = async (patch: Record<string, boolean | number>): Promise<boolean> => {
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

  const toggleSelfServe = async (next: boolean) => {
    setSelfServe(next);
    if (!(await save({ selfServe: next }))) {
      setSelfServe(!next);
      return;
    }
    toast.success(next ? "Self-serve: races auto-start" : "Races start from admin");
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
            id="self-serve"
            checked={selfServe}
            onCheckedChange={toggleSelfServe}
            disabled={saving}
          />
          <Label htmlFor="self-serve" className="cursor-pointer">
            Self-serve — auto-start a random problem 5s after both stations
            ready up
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
        <div className="flex items-center gap-3">
          <Label htmlFor="timer-sec">Race timer (seconds)</Label>
          <Input
            id="timer-sec"
            type="number"
            min={30}
            max={3600}
            value={timerSec}
            onChange={(e) => setTimerSec(e.target.value)}
            className="w-28"
          />
          <Button
            size="sm"
            variant="secondary"
            disabled={saving || Number(timerSec) === initialTimerSec}
            onClick={async () => {
              const n = Number(timerSec);
              if (!Number.isFinite(n) || n < 30 || n > 3600) {
                toast.error("Timer must be 30–3600 seconds");
                return;
              }
              if (await save({ timerSec: n })) {
                toast.success(`Race timer: ${n}s`);
              }
            }}
          >
            Save
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
