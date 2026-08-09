import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { authUser } from "@/lib/supabase/server";

export const dynamic = "force-dynamic";

/** Upsert (or clear with stars=0) the signed-in user's 1-5 star rating. */
export async function POST(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  const user = await authUser();
  if (!user)
    return NextResponse.json({ error: "sign in to rate" }, { status: 401 });

  const body = (await req.json().catch(() => null)) as { stars?: number } | null;
  const stars = body?.stars;
  if (typeof stars !== "number" || !Number.isInteger(stars) || stars < 0 || stars > 5)
    return NextResponse.json({ error: "invalid stars" }, { status: 400 });

  if (stars === 0) {
    const { error } = await db()
      .from("problem_ratings")
      .delete()
      .eq("user_id", user.id)
      .eq("problem_id", params.id);
    if (error) return NextResponse.json({ error: error.message }, { status: 500 });
    return NextResponse.json({ ok: true, stars: null });
  }

  const { error } = await db()
    .from("problem_ratings")
    .upsert({ user_id: user.id, problem_id: params.id, stars, rated_at: new Date().toISOString() });
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ ok: true, stars });
}
