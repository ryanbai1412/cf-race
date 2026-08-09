"use client";

import { useMemo, useState } from "react";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { toast } from "sonner";

export type AdminUserRow = {
  id: string;
  email: string | null;
  name: string | null;
  avatarUrl: string | null;
  createdAt: string;
  lastSignInAt: string | null;
  sessionCount: number;
  builtInAdmin: boolean;
  grantedAdmin: boolean;
};

export type AdminOverview = {
  users: number;
  sessions: number;
  sessionsByKind: Record<string, number>;
  sessionsByOutcome: Record<string, number>;
  problemsVisible: number;
  problemsHidden: number;
  duels: number;
};

function fmt(date: string | null): string {
  return date ? new Date(date).toLocaleString() : "—";
}

/** Hidden admin console: overview counts + user list with impersonation. */
export function AdminPanel({
  users,
  overview,
  realUserId,
  impersonatingUserId,
}: {
  users: AdminUserRow[];
  overview: AdminOverview;
  realUserId: string;
  impersonatingUserId: string | null;
}) {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [pending, setPending] = useState<string | null>(null);
  const [confirming, setConfirming] = useState<AdminUserRow | null>(null);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return users;
    return users.filter(
      (u) =>
        (u.email ?? "").toLowerCase().includes(q) ||
        (u.name ?? "").toLowerCase().includes(q)
    );
  }, [users, query]);

  const impersonate = async (user: AdminUserRow) => {
    setPending(user.id);
    const res = await fetch("/api/admin/impersonate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ userId: user.id }),
    });
    setPending(null);
    setConfirming(null);
    if (!res.ok) {
      toast.error("Could not start impersonation");
      return;
    }
    toast.success(`Now viewing as ${user.email ?? user.id}`);
    router.refresh();
  };

  const stopImpersonating = async () => {
    setPending("stop");
    await fetch("/api/admin/impersonate", { method: "DELETE" });
    setPending(null);
    router.refresh();
  };

  const setAdmin = async (user: AdminUserRow, action: "grant" | "revoke") => {
    setPending(user.id);
    const res = await fetch("/api/admin/admins", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ userId: user.id, action }),
    });
    setPending(null);
    if (!res.ok) {
      const body = (await res.json().catch(() => ({}))) as { error?: string };
      toast.error(body.error ?? "Failed");
      return;
    }
    toast.success(action === "grant" ? "Admin granted" : "Admin revoked");
    router.refresh();
  };

  return (
    <main className="mx-auto max-w-6xl space-y-6 px-6 py-10">
      <div className="space-y-1">
        <h1 className="text-3xl font-bold tracking-tight">Admin</h1>
        <p className="text-sm text-muted-foreground">
          Unlisted console — visible only to admins.
        </p>
      </div>

      <Tabs defaultValue="users">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="users">Users</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="mt-4">
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            {[
              { label: "Users", value: overview.users },
              { label: "Sessions", value: overview.sessions },
              { label: "Duels", value: overview.duels },
              {
                label: "Problems (visible / hidden)",
                value: `${overview.problemsVisible} / ${overview.problemsHidden}`,
              },
            ].map((s) => (
              <Card key={s.label} className="border-border/60 bg-card/60">
                <CardContent className="p-4">
                  <p className="font-mono text-2xl font-bold tabular-nums">
                    {s.value}
                  </p>
                  <p className="text-xs text-muted-foreground">{s.label}</p>
                </CardContent>
              </Card>
            ))}
          </div>
          <div className="mt-4 grid gap-3 sm:grid-cols-2">
            {[
              { title: "Sessions by kind", data: overview.sessionsByKind },
              {
                title: "Sessions by outcome",
                data: overview.sessionsByOutcome,
              },
            ].map((group) => (
              <Card key={group.title} className="border-border/60 bg-card/60">
                <CardContent className="space-y-1 p-4">
                  <p className="text-sm font-semibold">{group.title}</p>
                  {Object.entries(group.data).length === 0 && (
                    <p className="text-xs text-muted-foreground">none</p>
                  )}
                  {Object.entries(group.data)
                    .sort((a, b) => b[1] - a[1])
                    .map(([k, v]) => (
                      <p
                        key={k}
                        className="flex justify-between font-mono text-xs"
                      >
                        <span className="text-muted-foreground">{k}</span>
                        <span className="tabular-nums">{v}</span>
                      </p>
                    ))}
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="users" className="mt-4 space-y-3">
          <Input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by email or name…"
            className="max-w-sm"
          />
          <div className="divide-y divide-border/60 rounded-lg border border-border/60 bg-card/60">
            {filtered.map((u) => {
              const isImpersonated = impersonatingUserId === u.id;
              return (
                <div
                  key={u.id}
                  className="flex flex-wrap items-center gap-3 px-4 py-3"
                >
                  {u.avatarUrl ? (
                    <Image
                      src={u.avatarUrl}
                      alt=""
                      width={28}
                      height={28}
                      className="rounded-full"
                      unoptimized
                    />
                  ) : (
                    <span className="flex h-7 w-7 items-center justify-center rounded-full bg-primary/20 font-mono text-xs uppercase">
                      {(u.email ?? u.name ?? "?")[0]?.toUpperCase()}
                    </span>
                  )}
                  <div className="min-w-0">
                    <p className="truncate font-mono text-sm">
                      {u.email ?? u.id}
                    </p>
                    <p className="truncate text-xs text-muted-foreground">
                      {u.name ?? "—"} · joined {fmt(u.createdAt)} · last sign-in{" "}
                      {fmt(u.lastSignInAt)} · {u.sessionCount} sessions
                    </p>
                  </div>
                  {u.builtInAdmin && (
                    <Badge variant="outline" className="font-mono text-xs">
                      built-in admin
                    </Badge>
                  )}
                  {u.grantedAdmin && !u.builtInAdmin && (
                    <Badge variant="outline" className="font-mono text-xs">
                      admin
                    </Badge>
                  )}
                  {isImpersonated && (
                    <Badge className="font-mono text-xs">
                      currently impersonating
                    </Badge>
                  )}
                  <div className="ml-auto flex items-center gap-2">
                    {isImpersonated ? (
                      <Button
                        size="sm"
                        variant="secondary"
                        disabled={pending !== null}
                        onClick={stopImpersonating}
                      >
                        Stop impersonating
                      </Button>
                    ) : (
                      <Button
                        size="sm"
                        variant="secondary"
                        disabled={pending !== null || u.id === realUserId}
                        onClick={() => setConfirming(u)}
                      >
                        Impersonate
                      </Button>
                    )}
                    {!u.builtInAdmin && (
                      <Button
                        size="sm"
                        variant="ghost"
                        disabled={pending !== null}
                        onClick={() =>
                          setAdmin(u, u.grantedAdmin ? "revoke" : "grant")
                        }
                      >
                        {u.grantedAdmin ? "Revoke admin" : "Make admin"}
                      </Button>
                    )}
                  </div>
                </div>
              );
            })}
            {filtered.length === 0 && (
              <p className="px-4 py-6 text-sm text-muted-foreground">
                No users match “{query}”.
              </p>
            )}
          </div>
        </TabsContent>
      </Tabs>

      <Dialog
        open={confirming !== null}
        onOpenChange={(open) => !open && setConfirming(null)}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Impersonate user?</DialogTitle>
            <DialogDescription>
              All app pages will act as{" "}
              <span className="font-mono">
                {confirming?.email ?? confirming?.id}
              </span>{" "}
              for up to 1 hour. Admin access stays tied to your own account.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="ghost" onClick={() => setConfirming(null)}>
              Cancel
            </Button>
            <Button
              disabled={pending !== null}
              onClick={() => confirming && impersonate(confirming)}
            >
              Impersonate
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </main>
  );
}
