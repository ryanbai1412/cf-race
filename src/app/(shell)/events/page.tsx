import { redirect } from "next/navigation";
import { getEffectiveUser } from "@/lib/impersonation";
import { db } from "@/lib/db";
import { CreateEventCard } from "@/components/create-event-card";
import { EventList, type EventListRow } from "@/components/events/event-list";
import { PageHeader, PageShell } from "@/components/shell/page";

export const dynamic = "force-dynamic";

export default async function EventsPage() {
  const user = await getEffectiveUser();
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
    <PageShell>
      <PageHeader
        eyebrow="Booth"
        title="Events"
        description="Booth events — stations, monitors, and an admin console behind one secret link."
      />
      <CreateEventCard />
      <EventList events={rows} />
    </PageShell>
  );
}
