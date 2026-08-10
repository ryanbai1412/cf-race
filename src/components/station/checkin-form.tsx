"use client";

import { useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Eyebrow } from "@/components/shell/page";
import { COUNTRIES, flagEmoji } from "@/lib/countries";
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
  const [country, setCountry] = useState("");
  const [query, setQuery] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const selectedTeam = useMemo(
    () => IOI_TEAMS.find((t) => t.team === team),
    [team]
  );
  const canSubmit = manual ? !!name.trim() : !!(selectedTeam && member);

  const matches = useMemo(() => {
    if (!query.trim()) return [];
    const q = query.trim().toLowerCase();
    return COUNTRIES.filter((c) => c.name.toLowerCase().includes(q)).slice(0, 6);
  }, [query]);

  async function submit() {
    if (!canSubmit || busy) return;
    setBusy(true);
    setError(null);
    try {
      const payload = manual
        ? { name, country: country || null }
        : { name: member, country: selectedTeam?.country ?? null };
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
          {manual ? (
            <>
              <div className="space-y-1.5">
                <Label htmlFor="name">Name</Label>
                <Input
                  id="name"
                  autoFocus
                  maxLength={40}
                  placeholder="Your name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && submit()}
                />
              </div>
              <div className="space-y-1.5">
                <Label htmlFor="country">Country (optional)</Label>
                {country ? (
                  <div className="flex items-center justify-between rounded-md border border-border/60 px-3 py-2">
                    <span>
                      {flagEmoji(country)}{" "}
                      {COUNTRIES.find((c) => c.code === country)?.name ?? country}
                    </span>
                    <button
                      className="text-sm text-muted-foreground hover:text-foreground"
                      onClick={() => {
                        setCountry("");
                        setQuery("");
                      }}
                    >
                      change
                    </button>
                  </div>
                ) : (
                  <>
                    <Input
                      id="country"
                      placeholder="Start typing — e.g. Japan"
                      value={query}
                      onChange={(e) => setQuery(e.target.value)}
                    />
                    {matches.length > 0 && (
                      <div className="overflow-hidden rounded-md border border-border/60">
                        {matches.map((c) => (
                          <button
                            key={c.code}
                            className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm hover:bg-accent"
                            onClick={() => setCountry(c.code)}
                          >
                            <span>{flagEmoji(c.code)}</span> {c.name}
                          </button>
                        ))}
                      </div>
                    )}
                  </>
                )}
              </div>
            </>
          ) : (
            <>
              <div className="space-y-1.5">
                <Label htmlFor="team">Team</Label>
                <Select
                  id="team"
                  autoFocus
                  value={team}
                  onChange={(e) => {
                    setTeam(e.target.value);
                    setMember("");
                  }}
                >
                  <option value="" disabled>
                    Choose your team…
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
                <Label htmlFor="member">Name</Label>
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
              </div>
            </>
          )}
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
