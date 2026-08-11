import { redirect } from "next/navigation";
import { getEffectiveUser } from "@/lib/impersonation";
import { db } from "@/lib/db";
import { adminEventIds } from "@/lib/event-admins";
import { CreateEventCard } from "@/components/create-event-card";
import { EventList, type EventListRow } from "@/components/events/event-list";
import { PageHeader, PageShell } from "@/components/shell/page";

export const dynamic = "force-dynamic";

export default async function EventsPage() {
  const user = await getEffectiveUser();
  if (!user) redirect("/?next=/events");

  const adminIds = await adminEventIds(user.id);
  const filter = [
    `created_by.eq.${user.id}`,
    ...(adminIds.length ? [`id.in.(${adminIds.join(",")})`] : []),
  ].join(",");
  const { data: events } = await db()
    .from("events")
    .select("id, name, secret, created_at")
    .or(filter)
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
