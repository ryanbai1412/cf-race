"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { loadSoloHistory } from "@/lib/solo";

/**
 * One-time merge of pre-unified-app anonymous runs (tracked in
 * localStorage) into the signed-in account; new anonymous runs are
 * claimed via cookie at OAuth callback instead.
 */
export function LegacyClaim({ userId }: { userId: string }) {
  const router = useRouter();
  useEffect(() => {
    const key = `cfr-solo-claimed-${userId}`;
    if (localStorage.getItem(key)) return;
    const ids = loadSoloHistory().map((e) => e.sessionId);
    if (ids.length === 0) {
      localStorage.setItem(key, "1");
      return;
    }
    fetch("/api/solo/claim", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ sessionIds: ids }),
    })
      .then((r) => {
        if (r.ok) {
          localStorage.setItem(key, "1");
          router.refresh();
        }
      })
      .catch(() => {});
  }, [userId, router]);
  return null;
}
