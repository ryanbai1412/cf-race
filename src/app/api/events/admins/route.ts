import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/event-auth";
import { listEventAdmins, userIdByEmail } from "@/lib/event-admins";

export const dynamic = "force-dynamic";

/** Admins of an event (admin console, event-cookie or event-admin authorized). */
export async function GET(req: NextRequest) {
  const eventId = req.nextUrl.searchParams.get("eventId") ?? "";
  const event = await requireEvent(eventId);
  if (!event)
    return NextResponse.json({ error: "unauthorized" }, { status: 401 });
  return NextResponse.json({ admins: await listEventAdmins(event) });
}

/** Add an admin by email, or remove one by user id. */
export async function POST(req: NextRequest) {
  const body = (await req.json().catch(() => null)) as {
    eventId?: string;
    action?: "add" | "remove";
    email?: string;
    userId?: string;
  } | null;
  const event = await requireEvent(body?.eventId ?? "");
  if (!event)
    return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  if (body?.action === "add") {
    const email = typeof body.email === "string" ? body.email.trim() : "";
    if (!email)
      return NextResponse.json({ error: "Email required" }, { status: 400 });
    const userId = await userIdByEmail(email);
    if (!userId) {
      return NextResponse.json(
        { error: "No account with that email — they must sign in once first" },
        { status: 404 }
      );
    }
    if (userId !== event.created_by) {
      const { error } = await db()
        .from("event_admins")
        .upsert({ event_id: event.id, user_id: userId });
      if (error)
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
  } else if (body?.action === "remove") {
    const userId = typeof body.userId === "string" ? body.userId : "";
    if (!userId)
      return NextResponse.json({ error: "bad request" }, { status: 400 });
    if (userId === event.created_by) {
      return NextResponse.json(
        { error: "The event creator is always an admin" },
        { status: 400 }
      );
    }
    const { error } = await db()
      .from("event_admins")
      .delete()
      .eq("event_id", event.id)
      .eq("user_id", userId);
    if (error)
      return NextResponse.json({ error: error.message }, { status: 500 });
  } else {
    return NextResponse.json({ error: "bad request" }, { status: 400 });
  }

  return NextResponse.json({ admins: await listEventAdmins(event) });
}
