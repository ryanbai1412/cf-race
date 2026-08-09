import { NextRequest, NextResponse } from "next/server";
import { canShareMatch, canShareSession } from "@/lib/access";
import {
  activeShareToken,
  mintShare,
  revokeShare,
  type ShareTarget,
} from "@/lib/shares";

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
}): Promise<
  { ok: true; userId: string; target: ShareTarget } | { ok: false; status: number }
> {
  if (args.sessionId) {
    const grant = await canShareSession(args.sessionId);
    if (!grant) return { ok: false, status: 404 };
    return {
      ok: true,
      userId: grant.userId,
      target: { kind: "session", id: args.sessionId },
    };
  }
  if (args.matchId) {
    const grant = await canShareMatch(args.matchId);
    if (!grant) return { ok: false, status: 404 };
    return {
      ok: true,
      userId: grant.userId,
      target: { kind: "match", id: args.matchId },
    };
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
  const auth = await authorize({
    sessionId: req.nextUrl.searchParams.get("sessionId") ?? undefined,
    matchId: req.nextUrl.searchParams.get("matchId") ?? undefined,
  });
  if (!auth.ok) {
    return NextResponse.json({ error: "not found" }, { status: auth.status });
  }
  return NextResponse.json({ token: await activeShareToken(auth.target) });
}

export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  const revoke = (body as { revoke?: unknown } | null)?.revoke === true;

  const auth = await authorize(parseIds(body));
  if (!auth.ok) {
    return NextResponse.json({ error: "not found" }, { status: auth.status });
  }

  if (revoke) {
    const ok = await revokeShare(auth.target);
    if (!ok) return NextResponse.json({ error: "revoke failed" }, { status: 500 });
    return NextResponse.json({ token: null });
  }

  const token = await mintShare(auth.target, auth.userId);
  if (!token) return NextResponse.json({ error: "mint failed" }, { status: 500 });
  return NextResponse.json({ token });
}
