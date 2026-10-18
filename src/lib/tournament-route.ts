import { NextResponse } from "next/server";
import { db } from "./db";
import { getEffectiveUser } from "./impersonation";
import {
  loadSnapshotByCode,
  type TournamentMemberRow,
  type TournamentRow,
  type TournamentSnapshot,
} from "./tournament";
import { memberFromList } from "./tournament-auth";
import { MAX_PARTICIPANTS, normalizeCode } from "./tournament-format";

export const bad = (error: string, status = 400) => NextResponse.json({ error }, { status });

export const unavailable = () =>
  NextResponse.json(
    { error: "Server is busy, please retry" },
    { status: 503, headers: { "Retry-After": "3" } }
  );

export async function readJson(req: Request): Promise<Record<string, unknown>> {
  const body = await req.json().catch(() => null);
  return body && typeof body === "object" ? (body as Record<string, unknown>) : {};
}

export function codeParam(raw: unknown): string {
  return typeof raw === "string" ? normalizeCode(raw) : "";
}

export const noSuchTournament = () => bad("No tournament with that code", 404);

/** Resolve a fresh snapshot by code plus the caller's membership (for mutations). */
export async function tournamentFromCode(
  raw: unknown
): Promise<
  | { ok: true; t: TournamentRow; me: TournamentMemberRow | null; snap: TournamentSnapshot }
  | { ok: false; response: NextResponse }
> {
  const code = codeParam(raw);
  if (!code) return { ok: false, response: bad("missing code") };
  try {
    const snap = await loadSnapshotByCode(code);
    if (!snap) return { ok: false, response: noSuchTournament() };
    const { me } = await memberFromList(snap.tournament.id, snap.members, async () => {
      const user = await getEffectiveUser();
      return user?.id ?? null;
    });
    return { ok: true, t: snap.tournament, me, snap };
  } catch (e) {
    console.error(e);
    return { ok: false, response: unavailable() };
  }
}

export async function nameTaken(
  tournamentId: string,
  name: string,
  exceptMemberId?: string
): Promise<boolean> {
  const { data } = await db()
    .from("tournament_members")
    .select("id, name")
    .eq("tournament_id", tournamentId)
    .is("kicked_at", null)
    .ilike("name", name.replace(/[%_\\]/g, "\\$&"));
  return (data ?? []).some((m) => m.id !== exceptMemberId);
}

/** Whether the player list is full (ignoring `exceptMemberId`'s own seat). */
export async function participantsFull(
  tournamentId: string,
  exceptMemberId: string
): Promise<boolean> {
  const { count } = await db()
    .from("tournament_members")
    .select("id", { count: "exact", head: true })
    .eq("tournament_id", tournamentId)
    .eq("role", "participant")
    .is("kicked_at", null)
    .neq("id", exceptMemberId);
  return (count ?? 0) >= MAX_PARTICIPANTS;
}
