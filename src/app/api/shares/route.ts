import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { authUser } from "@/lib/supabase/server";

export const dynamic = "force-dynamic";

/**
 * Share tokens for replays (PRD 11 §5.4). Sessions are shared by their
 * owner; duel matches (side-by-side review) by either participant.
 * GET  ?sessionId= | ?matchId=   -> { token | null }
 * POST { sessionId | matchId }               -> mint (reuses active token)
 * POST { sessionId | matchId, revoke: true } -> revoke active token
 */

async function authorize(args: {
  sessionId?: string;
  matchId?: string;
}): Promise<{ ok: true; userId: string } | { ok: false; status: number }> {
  const user = await authUser();
  if (!user) return { ok: false, status: 401 };

  if (args.sessionId) {
    const { data: session } = await db()
      .from("sessions")
      .select("id, user_id")
      .eq("id", args.sessionId)
      .maybeSingle();
    if (!session) return { ok: false, status: 404 };
    if (session.user_id !== user.id) return { ok: false, status: 404 };
    return { ok: true, userId: user.id };
  }

  if (args.matchId) {
    const { data: player } = await db()
      .from("duel_players")
      .select("match_id")
      .eq("match_id", args.matchId)
      .eq("user_id", user.id)
      .maybeSingle();
    if (!player) return { ok: false, status: 404 };
    return { ok: true, userId: user.id };
  }

  return { ok: false, status: 400 };
}

function parseIds(input: unknown): { sessionId?: string; matchId?: string } {
  const body = input as { sessionId?: unknown; matchId?: unknown } | null;
  return {
    sessionId:
      typeof body?.sessionId === "string" ? body.sessionId : undefined,
    matchId: typeof body?.matchId === "string" ? body.matchId : undefined,
  };
}

export async function GET(req: NextRequest) {
  const ids = {
    sessionId: req.nextUrl.searchParams.get("sessionId") ?? undefined,
    matchId: req.nextUrl.searchParams.get("matchId") ?? undefined,
  };
  const auth = await authorize(ids);
  if (!auth.ok) {
    return NextResponse.json({ error: "not found" }, { status: auth.status });
  }

  const table = ids.sessionId ? "session_shares" : "match_shares";
  const col = ids.sessionId ? "session_id" : "match_id";
  const { data } = await db()
    .from(table)
    .select("token")
    .eq(col, ids.sessionId ?? ids.matchId!)
    .is("revoked_at", null)
    .maybeSingle();
  return NextResponse.json({ token: data?.token ?? null });
}

export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  const ids = parseIds(body);
  const revoke = (body as { revoke?: unknown } | null)?.revoke === true;

  const auth = await authorize(ids);
  if (!auth.ok) {
    return NextResponse.json({ error: "not found" }, { status: auth.status });
  }

  const table = ids.sessionId ? "session_shares" : "match_shares";
  const col = ids.sessionId ? "session_id" : "match_id";
  const id = ids.sessionId ?? ids.matchId!;

  if (revoke) {
    const { error } = await db()
      .from(table)
      .update({ revoked_at: new Date().toISOString() })
      .eq(col, id)
      .is("revoked_at", null);
    if (error) return NextResponse.json({ error: error.message }, { status: 500 });
    return NextResponse.json({ token: null });
  }

  const { data: existing } = await db()
    .from(table)
    .select("token")
    .eq(col, id)
    .is("revoked_at", null)
    .maybeSingle();
  if (existing) return NextResponse.json({ token: existing.token });

  const { data, error } = await db()
    .from(table)
    .insert({ [col]: id, created_by: auth.userId })
    .select("token")
    .single();
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ token: data.token });
}
