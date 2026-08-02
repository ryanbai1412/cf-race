import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/api-auth";

export const dynamic = "force-dynamic";

/** Fetch the tourist event log for a problem from Supabase Storage. */
export async function GET(
  req: NextRequest,
  { params }: { params: { problemId: string } }
) {
  const eventId = req.nextUrl.searchParams.get("eventId") ?? "";
  const event = await requireEvent(eventId);
  if (!event) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const { data, error } = await db()
    .storage.from("tourist")
    .download(`${params.problemId}.json`);
  if (error || !data) {
    return NextResponse.json({ error: "no recording" }, { status: 404 });
  }
  const text = await data.text();
  return new NextResponse(text, {
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "public, max-age=300",
    },
  });
}
