import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { eventCookieName } from "@/lib/event-auth";

const ALLOWED_PATHS = /^\/(station\/[12]|monitor\/[ab]|admin)$/;

export async function GET(
  req: NextRequest,
  { params }: { params: { eventId: string } }
) {
  const k = req.nextUrl.searchParams.get("k") ?? "";
  const to = req.nextUrl.searchParams.get("to") ?? "/admin";

  const { data: event } = await db()
    .from("events")
    .select("id, secret")
    .eq("id", params.eventId)
    .maybeSingle();

  if (!event || event.secret !== k) {
    return NextResponse.redirect(new URL("/invalid-link", req.url));
  }
  const dest = ALLOWED_PATHS.test(to) ? to : "/admin";
  const res = NextResponse.redirect(
    new URL(`/e/${params.eventId}${dest}`, req.url)
  );
  res.cookies.set(eventCookieName(params.eventId), k, {
    httpOnly: true,
    sameSite: "lax",
    maxAge: 60 * 60 * 24 * 30,
    path: `/`,
  });
  return res;
}
