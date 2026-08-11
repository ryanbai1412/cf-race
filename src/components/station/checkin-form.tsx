"use client";

import { useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Eyebrow } from "@/components/shell/page";
import { flagEmoji } from "@/lib/countries";
import { IOI_TEAMS } from "@/lib/ioi-contestants";
import { cn } from "@/lib/utils";
import type { Contestant, StationRole } from "@/lib/types";

function Select({ className, ...props }: React.ComponentProps<"select">) {
  return (
    <select
      className={cn(
        "flex h-9 w-full appearance-none rounded-md border border-input bg-transparent px-3 py-1 text-base shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 md:text-sm [&>option]:bg-background",
        className
      )}
      {...props}
    />
  );
}

export function CheckinForm({
  eventId,
  eventName,
  station,
  rival,
  onCheckedIn,
}: {
  eventId: string;
  eventName: string;
  station: StationRole;
  rival: Contestant | undefined;
  onCheckedIn: () => void;
}) {
  const [manual, setManual] = useState(false);
  const [team, setTeam] = useState("");
  const [member, setMember] = useState("");
  const [name, setName] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const selectedTeam = useMemo(
    () => IOI_TEAMS.find((t) => t.team === team),
    [team]
  );
  const canSubmit = manual ? !!name.trim() : !!(selectedTeam && member);

  async function submit() {
    if (!canSubmit || busy) return;
    setBusy(true);
    setError(null);
    try {
      const payload = {
        name: manual ? name : member,
        country: selectedTeam?.country ?? null,
      };
      const res = await fetch("/api/checkin", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ eventId, station, ...payload }),
      });
      if (!res.ok) throw new Error((await res.json()).error ?? "Check-in failed");
      onCheckedIn();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Check-in failed");
      setBusy(false);
    }
  }

  return (
    <main className="relative flex min-h-screen flex-col items-center justify-center gap-8 px-6">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(99,102,241,0.12),transparent_60%)]" />
      <div className="z-10 text-center">
        <Eyebrow>
          {eventName} · Station {station === "station1" ? "1" : "2"}
        </Eyebrow>
        <h1 className="mt-2 text-5xl font-extrabold tracking-tight">
          Ready to race?
        </h1>
        <p className="mt-3 text-sm text-muted-foreground">
          {rival
            ? `Your rival ${rival.name} ${rival.country ? flagEmoji(rival.country) : ""} is checked in.`
            : "Waiting for a rival on the other station…"}
        </p>
      </div>
      <Card className="z-10 w-full max-w-md border-border/60 bg-card/60 backdrop-blur">
        <CardHeader>
          <CardTitle className="text-lg">Check in</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-1.5">
            <Label htmlFor="team">Team{manual ? " (optional)" : ""}</Label>
            <Select
              id="team"
              autoFocus={!manual}
              value={team}
              onChange={(e) => {
                setTeam(e.target.value);
                setMember("");
              }}
            >
              <option value="" disabled={!manual}>
                {manual ? "No team" : "Choose your team…"}
              </option>
              {IOI_TEAMS.map((t) => (
                <option key={t.team} value={t.team}>
                  {t.country ? `${flagEmoji(t.country)} ` : ""}
                  {t.team}
                </option>
              ))}
            </Select>
          </div>
          <div className="space-y-1.5">
            <Label htmlFor={manual ? "name" : "member"}>Name</Label>
            {manual ? (
              <Input
                id="name"
                maxLength={40}
                placeholder="Your name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && submit()}
              />
            ) : (
              <Select
                id="member"
                value={member}
                disabled={!selectedTeam}
                onChange={(e) => setMember(e.target.value)}
              >
                <option value="" disabled>
                  {selectedTeam ? "Choose your name…" : "Choose a team first"}
                </option>
                {selectedTeam?.members.map((m) => (
                  <option key={m} value={m}>
                    {m}
                  </option>
                ))}
              </Select>
            )}
          </div>
          <Button className="w-full" size="lg" onClick={submit} disabled={busy || !canSubmit}>
            {busy ? "Checking in…" : "Continue"}
          </Button>
          {error && <p className="text-sm text-destructive">{error}</p>}
          <button
            className="w-full text-center text-sm text-muted-foreground hover:text-foreground"
            onClick={() => {
              setManual(!manual);
              setError(null);
            }}
          >
            {manual ? "On an IOI team? Pick from the list" : "Not on the list? Enter your name"}
          </button>
        </CardContent>
      </Card>
    </main>
  );
}
