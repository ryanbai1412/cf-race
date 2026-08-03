"use client";

import { createClient, RealtimeChannel, SupabaseClient } from "@supabase/supabase-js";
import type { BroadcastMsg } from "./types";

let client: SupabaseClient | null = null;

export function supabase(): SupabaseClient {
  if (!client) {
    client = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
      { auth: { persistSession: false } }
    );
  }
  return client;
}

export function eventChannel(eventId: string): RealtimeChannel {
  return supabase().channel(`event:${eventId}`, {
    config: { broadcast: { self: true } },
  });
}

export function sendBroadcast(ch: RealtimeChannel, msg: BroadcastMsg): void {
  void ch.send({ type: "broadcast", event: "msg", payload: msg });
}
