import { NextRequest, NextResponse } from "next/server";
import { randomBytes } from "crypto";
import { db } from "@/lib/db";

export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  const name = typeof body?.name === "string" ? body.name.trim() : "";
  if (!name || name.length > 80) {
    return NextResponse.json({ error: "Invalid event name" }, { status: 400 });
  }
  const secret = randomBytes(18).toString("base64url");
  const { data, error } = await db()
    .from("events")
    .insert({ name, secret })
    .select("id, secret")
    .single();
  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
  return NextResponse.json({ id: data.id, secret: data.secret });
}
