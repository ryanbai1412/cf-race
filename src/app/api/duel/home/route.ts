import { NextResponse } from "next/server";
import { db } from "@/lib/db";
import { getEffectiveUser } from "@/lib/impersonation";
import { invalidatedProblemIds } from "@/lib/duel";
import { sweepStaleSessions } from "@/lib/session-lifecycle";

export const dynamic = "force-dynamic";

/** Data for /duel home: your matches, solved problems, and recordings. */
export async function GET() {
  const user = await getEffectiveUser();
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  await sweepStaleSessions({ userId: user.id });
  const { data: myPlayers } = await db()
    .from("duel_players")
    .select("match_id, session_id")
    .eq("user_id", user.id);
  const matchIds = (myPlayers ?? []).map((p) => p.match_id);

  const [{ data: matches }, { data: solved }, { data: recordings }, invalidated] =
    await Promise.all([
      matchIds.length > 0
        ? db()
            .from("duel_matches")
            .select("id, room_id, problem_id, started_at, winner_user_id, finished_at")
            .in("id", matchIds)
            .order("started_at", { ascending: false })
            .limit(100)
        : Promise.resolve({ data: [] }),
      db()
        .from("sessions")
        .select("problem_id, kind, solve_ms, started_at")
        .eq("user_id", user.id)
        .eq("outcome", "solved")
        .order("started_at", { ascending: false })
        .limit(500),
      db()
        .from("sessions")
        .select("id, kind, problem_id, started_at, outcome, solve_ms")
        .eq("user_id", user.id)
        .not("recording_path", "is", null)
        .order("started_at", { ascending: false })
        .limit(100),
      invalidatedProblemIds(),
    ]);

  // Opponent names per match.
  let opponents: Record<string, string> = {};
  if (matchIds.length > 0) {
    const { data: others } = await db()
      .from("duel_players")
      .select("match_id, user_id")
      .in("match_id", matchIds)
      .neq("user_id", user.id);
    const otherIds = Array.from(new Set((others ?? []).map((o) => o.user_id)));
    const { data: names } = otherIds.length
      ? await db()
          .from("duel_room_players")
          .select("user_id, name")
          .in("user_id", otherIds)
      : { data: [] };
    const nameById = new Map((names ?? []).map((n) => [n.user_id, n.name]));
    opponents = Object.fromEntries(
      (others ?? []).map((o) => [o.match_id, nameById.get(o.user_id) ?? "Opponent"])
    );
  }

  const solvedByProblem = new Map<string, { solveMs: number | null; kind: string }>();
  for (const s of solved ?? []) {
    if (invalidated.has(s.problem_id)) continue;
    const prev = solvedByProblem.get(s.problem_id);
    if (!prev || (s.solve_ms ?? Infinity) < (prev.solveMs ?? Infinity)) {
      solvedByProblem.set(s.problem_id, { solveMs: s.solve_ms, kind: s.kind });
    }
  }

  return NextResponse.json({
    userId: user.id,
    matches: (matches ?? []).map((m) => ({
      id: m.id,
      roomId: m.room_id,
      problemId: m.problem_id,
      startedAt: m.started_at,
      finished: m.finished_at !== null,
      won: m.winner_user_id === user.id,
      winnerIsSet: m.winner_user_id !== null,
      opponent: opponents[m.id] ?? "Opponent",
    })),
    solved: Array.from(solvedByProblem.entries()).map(([problemId, v]) => ({
      problemId,
      solveMs: v.solveMs,
      kind: v.kind,
    })),
    recordings: recordings ?? [],
  });
}
