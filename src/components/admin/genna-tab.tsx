"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";
import type { AdminUserRow } from "./admin-panel";

type SolvedSession = {
  id: string;
  problem_id: string;
  kind: string;
  solve_ms: number | null;
  started_at: string;
  recording_path: string | null;
  lang: string | null;
};

type Reference = { problem_id: string; session_id: string };

type BulkPick = { problemId: string; sessionId: string; solveMs: number };

function fmtMs(ms: number | null): string {
  if (ms === null) return "—";
  const s = Math.round(ms / 1000);
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

/**
 * Genna references: pick a user, view their solved sessions, and bless them
 * (individually or in bulk) as per-problem Genna reference sessions.
 */
export function GennaTab({ users }: { users: AdminUserRow[] }) {
  const [query, setQuery] = useState("");
  const [userId, setUserId] = useState<string | null>(null);
  const [sessions, setSessions] = useState<SolvedSession[]>([]);
  const [references, setReferences] = useState<Reference[]>([]);
  const [loading, setLoading] = useState(false);
  const [pending, setPending] = useState(false);
  const [overwrite, setOverwrite] = useState(false);
  const [preview, setPreview] = useState<BulkPick[] | null>(null);

  const candidates = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return [];
    return users
      .filter(
        (u) =>
          (u.email ?? "").toLowerCase().includes(q) ||
          (u.name ?? "").toLowerCase().includes(q)
      )
      .slice(0, 8);
  }, [users, query]);

  const selected = users.find((u) => u.id === userId) ?? null;
  const refByProblem = useMemo(
    () => new Map(references.map((r) => [r.problem_id, r.session_id])),
    [references]
  );

  const load = useCallback(async (uid: string) => {
    setLoading(true);
    const res = await fetch(`/api/admin/genna?userId=${uid}`, {
      cache: "no-store",
    });
    setLoading(false);
    if (!res.ok) {
      toast.error("Could not load sessions");
      return;
    }
    const data = (await res.json()) as {
      sessions: SolvedSession[];
      references: Reference[];
    };
    setSessions(data.sessions);
    setReferences(data.references);
  }, []);

  useEffect(() => {
    if (userId) void load(userId);
  }, [userId, load]);

  const setReference = async (s: SolvedSession, remove: boolean) => {
    setPending(true);
    const res = await fetch("/api/admin/genna/reference", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        problemId: s.problem_id,
        sessionId: s.id,
        remove,
      }),
    });
    setPending(false);
    if (!res.ok) {
      const body = (await res.json().catch(() => ({}))) as { error?: string };
      toast.error(body.error ?? "Failed");
      return;
    }
    toast.success(remove ? "Reference removed" : "Reference set");
    if (userId) void load(userId);
  };

  const bulk = async (dryRun: boolean) => {
    if (!userId) return;
    setPending(true);
    const res = await fetch("/api/admin/genna/bulk", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ userId, overwrite, dryRun }),
    });
    setPending(false);
    if (!res.ok) {
      const body = (await res.json().catch(() => ({}))) as { error?: string };
      toast.error(body.error ?? "Failed");
      return;
    }
    const data = (await res.json()) as { picks: BulkPick[]; applied?: number };
    if (dryRun) {
      setPreview(data.picks);
      return;
    }
    setPreview(null);
    toast.success(`Set ${data.applied} reference${data.applied === 1 ? "" : "s"}`);
    void load(userId);
  };

  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <Input
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setUserId(null);
          }}
          placeholder="Find Genna's account by email or name…"
          className="max-w-sm"
        />
        {!selected && candidates.length > 0 && (
          <div className="max-w-sm divide-y divide-border/60 rounded-lg border border-border/60 bg-card/60">
            {candidates.map((u) => (
              <button
                key={u.id}
                className="block w-full px-3 py-2 text-left font-mono text-sm hover:bg-accent"
                onClick={() => setUserId(u.id)}
              >
                {u.email ?? u.id}
                <span className="ml-2 text-xs text-muted-foreground">
                  {u.sessionCount} sessions
                </span>
              </button>
            ))}
          </div>
        )}
      </div>

      {selected && (
        <>
          <div className="flex flex-wrap items-center gap-3">
            <p className="font-mono text-sm">{selected.email ?? selected.id}</p>
            <Badge variant="outline" className="font-mono text-xs">
              {sessions.length} solved
            </Badge>
            <div className="ml-auto flex items-center gap-3">
              <label className="flex items-center gap-1.5 text-xs text-muted-foreground">
                <Switch checked={overwrite} onCheckedChange={setOverwrite} />
                overwrite existing
              </label>
              <Button
                size="sm"
                disabled={pending || sessions.length === 0}
                onClick={() => bulk(true)}
              >
                Mark all as Genna references…
              </Button>
            </div>
          </div>

          {loading ? (
            <p className="text-sm text-muted-foreground">Loading…</p>
          ) : (
            <div className="divide-y divide-border/60 rounded-lg border border-border/60 bg-card/60">
              {sessions.map((s) => {
                const ref = refByProblem.get(s.problem_id);
                const isRef = ref === s.id;
                const otherRef = ref !== undefined && !isRef;
                return (
                  <div
                    key={s.id}
                    className="flex flex-wrap items-center gap-3 px-4 py-2.5"
                  >
                    <span className="w-16 font-mono text-sm font-semibold">
                      {s.problem_id}
                    </span>
                    <span className="font-mono text-sm tabular-nums">
                      {fmtMs(s.solve_ms)}
                    </span>
                    <span className="text-xs text-muted-foreground">
                      {new Date(s.started_at).toLocaleString()} · {s.kind}
                      {s.lang ? ` · ${s.lang}` : ""}
                      {s.recording_path ? " · webcam" : " · no webcam"}
                    </span>
                    {isRef && <Badge className="font-mono text-xs">reference</Badge>}
                    <div className="ml-auto flex items-center gap-2">
                      <Link
                        href={`/replay/${s.id}`}
                        target="_blank"
                        className="text-xs text-muted-foreground underline-offset-2 hover:underline"
                      >
                        replay
                      </Link>
                      {isRef ? (
                        <Button
                          size="sm"
                          variant="ghost"
                          disabled={pending}
                          onClick={() => setReference(s, true)}
                        >
                          Remove reference
                        </Button>
                      ) : (
                        <Button
                          size="sm"
                          variant="secondary"
                          disabled={pending}
                          onClick={() => setReference(s, false)}
                        >
                          {otherRef ? "Replace reference" : "Set as reference"}
                        </Button>
                      )}
                    </div>
                  </div>
                );
              })}
              {sessions.length === 0 && (
                <p className="px-4 py-6 text-sm text-muted-foreground">
                  No solved sessions for this user.
                </p>
              )}
            </div>
          )}
        </>
      )}

      {!selected && !query && (
        <p className="text-sm text-muted-foreground">
          Search for the account Genna signed in with, then bless his solved
          sessions as per-problem reference times for events and monitors.
        </p>
      )}

      <Dialog open={preview !== null} onOpenChange={(o) => !o && setPreview(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Set Genna references?</DialogTitle>
            <DialogDescription>
              {preview?.length === 0
                ? "Nothing to set — every solved problem already has a reference."
                : `Fastest solve per problem for ${selected?.email ?? "this user"}:`}
            </DialogDescription>
          </DialogHeader>
          {preview && preview.length > 0 && (
            <div className="max-h-64 overflow-y-auto rounded border border-border/60 font-mono text-sm">
              {preview.map((p) => (
                <p key={p.problemId} className="flex justify-between px-3 py-1.5">
                  <span>{p.problemId}</span>
                  <span className="tabular-nums">{fmtMs(p.solveMs)}</span>
                </p>
              ))}
            </div>
          )}
          <DialogFooter>
            <Button variant="ghost" onClick={() => setPreview(null)}>
              Cancel
            </Button>
            <Button
              disabled={pending || preview?.length === 0}
              onClick={() => bulk(false)}
            >
              Set {preview?.length ?? 0} reference{preview?.length === 1 ? "" : "s"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
