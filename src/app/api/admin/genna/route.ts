import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireAdmin } from "@/lib/admin-api";

export const dynamic = "force-dynamic";

/**
 * A user's solved sessions (candidates for Genna references) plus the current
 * reference map. Only sessions with replay events qualify.
 */
export async function GET(req: NextRequest) {
  const gate = await requireAdmin();
  if (!gate.ok) return gate.response;

  const userId = req.nextUrl.searchParams.get("userId") ?? "";
  if (!userId) return NextResponse.json({ error: "userId required" }, { status: 400 });

  const [{ data: sessions, error }, { data: refs }] = await Promise.all([
    db()
      .from("sessions")
      .select("id, problem_id, kind, solve_ms, started_at, recording_path, lang")
      .eq("user_id", userId)
      .eq("outcome", "solved")
      .order("started_at", { ascending: false }),
    db().from("genna_problems").select("problem_id, session_id"),
  ]);
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });

  return NextResponse.json({
    sessions: sessions ?? [],
    references: refs ?? [],
  });
}
