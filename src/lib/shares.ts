import { db, logDbError } from "./db";

export type ShareTarget =
  | { kind: "session"; id: string }
  | { kind: "match"; id: string };

function tableFor(target: ShareTarget): { table: string; col: string } {
  return target.kind === "session"
    ? { table: "session_shares", col: "session_id" }
    : { table: "match_shares", col: "match_id" };
}

/** The active (unrevoked) share token for a session/match, if any. */
export async function activeShareToken(
  target: ShareTarget
): Promise<string | null> {
  const { table, col } = tableFor(target);
  const { data } = await db()
    .from(table)
    .select("token")
    .eq(col, target.id)
    .is("revoked_at", null)
    .maybeSingle();
  return data?.token ?? null;
}

/** Mint a share token, reusing the active one (unique-index race safe). */
export async function mintShare(
  target: ShareTarget,
  createdBy: string
): Promise<string | null> {
  const existing = await activeShareToken(target);
  if (existing) return existing;

  const { table, col } = tableFor(target);
  const { data, error } = await db()
    .from(table)
    .insert({ [col]: target.id, created_by: createdBy })
    .select("token")
    .single();
  if (error) {
    // Concurrent mint lost the one-active-share unique-index race: reuse the winner.
    if (error.code === "23505") return activeShareToken(target);
    logDbError("mintShare", error);
    return null;
  }
  return data.token;
}

/** Revoke the active share token for a session/match. */
export async function revokeShare(target: ShareTarget): Promise<boolean> {
  const { table, col } = tableFor(target);
  const { error } = await db()
    .from(table)
    .update({ revoked_at: new Date().toISOString() })
    .eq(col, target.id)
    .is("revoked_at", null);
  logDbError("revokeShare", error);
  return error === null;
}

/** Resolve an unrevoked share token to what it shares. */
export async function lookupShare(
  token: string
): Promise<ShareTarget | null> {
  const [{ data: session }, { data: match }] = await Promise.all([
    db()
      .from("session_shares")
      .select("session_id")
      .eq("token", token)
      .is("revoked_at", null)
      .maybeSingle(),
    db()
      .from("match_shares")
      .select("match_id")
      .eq("token", token)
      .is("revoked_at", null)
      .maybeSingle(),
  ]);
  if (session) return { kind: "session", id: session.session_id };
  if (match) return { kind: "match", id: match.match_id };
  return null;
}
