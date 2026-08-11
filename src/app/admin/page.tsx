import { notFound } from "next/navigation";
import { db } from "@/lib/db";
import { authUser } from "@/lib/supabase/server";
import { grantedAdminIds, isAdmin, isBuiltInAdminEmail } from "@/lib/admin";
import { impersonatedUserIdFromCookie } from "@/lib/impersonation";
import { AdminPanel, type AdminUserRow, type AdminOverview } from "@/components/admin/admin-panel";

export const dynamic = "force-dynamic";

/** Hidden admin panel — non-admins (and logged-out visitors) get a plain 404. */
export default async function AdminPage() {
  // Admin gating always uses the REAL user, never the impersonated one.
  const real = await authUser();
  if (!(await isAdmin(real))) notFound();

  const [{ data: userList }, granted, { data: sessions }, { data: problems }, { count: duelCount }] =
    await Promise.all([
      db().auth.admin.listUsers({ page: 1, perPage: 1000 }),
      grantedAdminIds(),
      db().from("sessions").select("user_id, kind, outcome"),
      db().from("problems").select("tags"),
      db().from("duel_matches").select("id", { count: "exact", head: true }),
    ]);

  const sessionCounts = new Map<string, number>();
  const byKind: Record<string, number> = {};
  const byOutcome: Record<string, number> = {};
  for (const s of sessions ?? []) {
    if (s.user_id) {
      sessionCounts.set(s.user_id, (sessionCounts.get(s.user_id) ?? 0) + 1);
    }
    byKind[s.kind] = (byKind[s.kind] ?? 0) + 1;
    const outcome = (s.outcome as string | null) ?? "active";
    byOutcome[outcome] = (byOutcome[outcome] ?? 0) + 1;
  }

  const hiddenProblems = (problems ?? []).filter((p) =>
    ((p.tags as string[] | null) ?? []).includes("hidden")
  ).length;

  const users: AdminUserRow[] = (userList?.users ?? []).map((u) => ({
    id: u.id,
    email: u.email ?? null,
    name: (u.user_metadata?.full_name as string | undefined) ?? null,
    avatarUrl: (u.user_metadata?.avatar_url as string | undefined) ?? null,
    createdAt: u.created_at,
    lastSignInAt: u.last_sign_in_at ?? null,
    sessionCount: sessionCounts.get(u.id) ?? 0,
    builtInAdmin: isBuiltInAdminEmail(u.email),
    grantedAdmin: granted.has(u.id),
  }));
  users.sort((a, b) => (a.createdAt < b.createdAt ? 1 : -1));

  const { count: gennaCount } = await db()
    .from("genna_problems")
    .select("problem_id", { count: "exact", head: true });

  const overview: AdminOverview = {
    users: users.length,
    sessions: (sessions ?? []).length,
    sessionsByKind: byKind,
    sessionsByOutcome: byOutcome,
    problemsVisible: (problems ?? []).length - hiddenProblems,
    problemsHidden: hiddenProblems,
    duels: duelCount ?? 0,
    gennaProblems: gennaCount ?? 0,
  };

  return (
    <AdminPanel
      users={users}
      overview={overview}
      realUserId={real!.id}
      impersonatingUserId={impersonatedUserIdFromCookie()}
    />
  );
}
