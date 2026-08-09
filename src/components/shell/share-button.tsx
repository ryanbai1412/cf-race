"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Link2, Link2Off } from "lucide-react";
import { toast } from "sonner";

/**
 * Mint / copy / revoke a public share link for a session or duel match
 * (PRD 11 §5.4). Owner-only — the server 404s for anyone else, in which
 * case the button hides itself.
 */
export function ShareButton(props: { sessionId: string } | { matchId: string }) {
  const ids =
    "sessionId" in props
      ? { sessionId: props.sessionId }
      : { matchId: props.matchId };
  const query =
    "sessionId" in props
      ? `sessionId=${props.sessionId}`
      : `matchId=${props.matchId}`;

  const [token, setToken] = useState<string | null>(null);
  const [allowed, setAllowed] = useState(false);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    fetch(`/api/shares?${query}`, { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : null))
      .then((d: { token: string | null } | null) => {
        if (d) {
          setAllowed(true);
          setToken(d.token);
        }
      })
      .catch(() => {});
  }, [query]);

  if (!allowed) return null;

  const shareUrl = (t: string) => `${window.location.origin}/r/${t}`;

  const mint = async () => {
    setBusy(true);
    try {
      const res = await fetch("/api/shares", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(ids),
      });
      const d = await res.json();
      if (!res.ok) throw new Error(d.error ?? "Share failed");
      setToken(d.token);
      await navigator.clipboard.writeText(shareUrl(d.token));
      toast.success("Share link copied to clipboard");
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Share failed");
    } finally {
      setBusy(false);
    }
  };

  const revoke = async () => {
    setBusy(true);
    try {
      const res = await fetch("/api/shares", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ ...ids, revoke: true }),
      });
      if (!res.ok) throw new Error("Revoke failed");
      setToken(null);
      toast.success("Share link revoked");
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Revoke failed");
    } finally {
      setBusy(false);
    }
  };

  if (token) {
    return (
      <span className="flex items-center gap-1">
        <Button
          size="sm"
          variant="secondary"
          disabled={busy}
          onClick={async () => {
            await navigator.clipboard.writeText(shareUrl(token));
            toast.success("Share link copied");
          }}
        >
          <Link2 className="mr-1.5 h-3.5 w-3.5" />
          Copy link
        </Button>
        <Button size="sm" variant="ghost" disabled={busy} onClick={revoke}>
          <Link2Off className="mr-1.5 h-3.5 w-3.5" />
          Revoke
        </Button>
      </span>
    );
  }
  return (
    <Button size="sm" variant="secondary" disabled={busy} onClick={mint}>
      <Link2 className="mr-1.5 h-3.5 w-3.5" />
      {busy ? "Sharing…" : "Share"}
    </Button>
  );
}
