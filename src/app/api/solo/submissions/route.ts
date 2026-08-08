import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";

export const dynamic = "force-dynamic";

export async function GET(req: NextRequest) {
  const sessionId = req.nextUrl.searchParams.get("sessionId") ?? "";
  if (!sessionId) {
    return NextResponse.json({ error: "bad request" }, { status: 400 });
  }
  const { data, error } = await db()
    .from("session_submissions")
    .select("id, session_id, lang, verdict, details, submitted_at")
    .eq("session_id", sessionId)
    .eq("kind", "submit")
    .order("submitted_at", { ascending: false });
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ submissions: data });
}
