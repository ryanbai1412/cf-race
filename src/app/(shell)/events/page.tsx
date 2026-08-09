import { redirect } from "next/navigation";
import { authUser } from "@/lib/supabase/server";
import { db } from "@/lib/db";
import { CreateEventCard } from "@/components/create-event-card";
import { EventList, type EventListRow } from "@/components/events/event-list";

export const dynamic = "force-dynamic";

export default async function EventsPage() {
  const user = await authUser();
  if (!user) redirect("/?next=/events");

  const { data: events } = await db()
    .from("events")
    .select("id, name, secret, created_at")
    .eq("created_by", user.id)
    .order("created_at", { ascending: false });

  const rows: EventListRow[] = (events ?? []).map((e) => ({
    id: e.id,
    name: e.name,
    secret: e.secret,
    createdAt: e.created_at,
  }));

  return (
    <main className="mx-auto max-w-4xl space-y-8 px-6 py-10">
      <div className="space-y-1">
        <h1 className="text-3xl font-bold tracking-tight">Events</h1>
        <p className="text-sm text-muted-foreground">
          Booth events — stations, monitors, and an admin console behind one
          secret link.
        </p>
      </div>
      <CreateEventCard />
      <EventList events={rows} />
    </main>
  );
}
