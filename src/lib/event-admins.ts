import { db } from "./db";

export type EventAdmin = {
  userId: string;
  email: string | null;
  isCreator: boolean;
};

/** Is this user the event creator or a row in `event_admins`? */
export async function isEventAdmin(
  event: { id: string; created_by?: string | null },
  userId: string
): Promise<boolean> {
  if (event.created_by && event.created_by === userId) return true;
  const { data } = await db()
    .from("event_admins")
    .select("user_id")
    .eq("event_id", event.id)
    .eq("user_id", userId)
    .maybeSingle();
  return data !== null;
}

/** Event ids this user administers through `event_admins`. */
export async function adminEventIds(userId: string): Promise<string[]> {
  const { data } = await db()
    .from("event_admins")
    .select("event_id")
    .eq("user_id", userId);
  return (data ?? []).map((r) => r.event_id as string);
}

/** The event's admins — creator first, then granted admins. */
export async function listEventAdmins(event: {
  id: string;
  created_by?: string | null;
}): Promise<EventAdmin[]> {
  const { data } = await db()
    .from("event_admins")
    .select("user_id, created_at")
    .eq("event_id", event.id)
    .order("created_at", { ascending: true });

  const ids = [
    ...(event.created_by ? [event.created_by] : []),
    ...(data ?? [])
      .map((r) => r.user_id as string)
      .filter((id) => id !== event.created_by),
  ];
  return Promise.all(
    ids.map(async (userId) => ({
      userId,
      email: await userEmail(userId),
      isCreator: userId === event.created_by,
    }))
  );
}

async function userEmail(userId: string): Promise<string | null> {
  const { data, error } = await db().auth.admin.getUserById(userId);
  if (error || !data.user) return null;
  return data.user.email ?? null;
}

/** Look up an auth user id by email (case-insensitive), or null. */
export async function userIdByEmail(email: string): Promise<string | null> {
  const target = email.trim().toLowerCase();
  if (!target) return null;
  const { data, error } = await db().auth.admin.listUsers({
    page: 1,
    perPage: 1000,
  });
  if (error) return null;
  const match = data.users.find(
    (u) => (u.email ?? "").toLowerCase() === target
  );
  return match?.id ?? null;
}
