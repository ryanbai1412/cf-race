"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { eventChannel } from "@/lib/realtime";
import type { RealtimeChannel } from "@supabase/supabase-js";
import type { BroadcastMsg, ClientState } from "@/lib/types";

const POLL_MS = 2500;

/**
 * Single source of truth for client-side event state.
 * Polls /api/state and refetches instantly on realtime `state_changed`.
 * Also exposes a server-clock offset and a raw broadcast subscription.
 */
export function useEventState(
  eventId: string,
  onMessage?: (msg: BroadcastMsg) => void,
  onSubscribed?: (ch: RealtimeChannel) => void
) {
  const [state, setState] = useState<ClientState | null>(null);
  const [clockOffset, setClockOffset] = useState(0); // serverNow - clientNow
  const onMessageRef = useRef(onMessage);
  onMessageRef.current = onMessage;
  const onSubscribedRef = useRef(onSubscribed);
  onSubscribedRef.current = onSubscribed;
  // The poll interval, realtime nudges and manual refetches overlap, so
  // responses can arrive out of order. Only apply the newest one, or a slow
  // reply would resurrect state the app has already moved past.
  const appliedNow = useRef(0);

  const refetch = useCallback(async () => {
    try {
      const t0 = Date.now();
      const res = await fetch(`/api/state?eventId=${eventId}`, {
        cache: "no-store",
      });
      if (!res.ok) return;
      const data: ClientState = await res.json();
      if (data.serverNow < appliedNow.current) return;
      appliedNow.current = data.serverNow;
      const rtt = Date.now() - t0;
      setClockOffset(data.serverNow + rtt / 2 - Date.now());
      setState(data);
    } catch {
      // transient network error; next poll will retry
    }
  }, [eventId]);

  // A new event means a fresh state stream; don't hold the old one's clock.
  useEffect(() => {
    appliedNow.current = 0;
  }, [eventId]);

  useEffect(() => {
    void refetch();
    const iv = setInterval(refetch, POLL_MS);
    const ch = eventChannel(eventId);
    ch.on("broadcast", { event: "msg" }, ({ payload }) => {
      const msg = payload as BroadcastMsg;
      if (msg.type === "state_changed") void refetch();
      onMessageRef.current?.(msg);
    });
    ch.subscribe((status) => {
      if (status === "SUBSCRIBED") onSubscribedRef.current?.(ch);
    });
    return () => {
      clearInterval(iv);
      void ch.unsubscribe();
    };
  }, [eventId, refetch]);

  const serverNow = useCallback(() => Date.now() + clockOffset, [clockOffset]);

  return { state, refetch, serverNow };
}
