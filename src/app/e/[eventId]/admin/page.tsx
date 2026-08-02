import { authorizeEvent } from "@/lib/event-auth";
import { redirect } from "next/navigation";
import { DeviceLinks } from "@/components/admin/device-links";

export default async function AdminPage({
  params,
  searchParams,
}: {
  params: { eventId: string };
  searchParams: { k?: string };
}) {
  const event = await authorizeEvent(params.eventId, searchParams.k);
  if (!event) redirect("/invalid-link");

  return (
    <main className="mx-auto max-w-5xl space-y-8 px-6 py-10">
      <header className="space-y-1">
        <p className="font-mono text-xs uppercase tracking-[0.3em] text-primary">
          Admin console
        </p>
        <h1 className="text-3xl font-bold">{event.name}</h1>
      </header>
      <DeviceLinks eventId={event.id} secret={event.secret} />
      <section className="rounded-lg border border-dashed border-border p-6 text-muted-foreground">
        Race controls coming next: problem queue, countdown, DQ/reset.
      </section>
    </main>
  );
}
