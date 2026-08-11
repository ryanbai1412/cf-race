import { authorizeEvent } from "@/lib/event-auth";
import { redirect } from "next/navigation";
import { DeviceLinks } from "@/components/admin/device-links";
import { RaceControl } from "@/components/admin/race-control";
import { RaceHistory } from "@/components/admin/race-history";
import { EventSettings } from "@/components/admin/event-settings";
import { gennaOnly, requireWebcam } from "@/lib/event-settings";
import { PageHeader, PageShell } from "@/components/shell/page";

export default async function AdminPage({
  params,
}: {
  params: { eventId: string };
}) {
  const event = await authorizeEvent(params.eventId);
  if (!event) redirect("/invalid-link");

  return (
    <PageShell>
      <PageHeader eyebrow="Admin console" title={event.name} />
      <RaceControl eventId={event.id} gennaOnly={gennaOnly(event.settings)} />
      <EventSettings
        eventId={event.id}
        initialRequireWebcam={requireWebcam(event.settings)}
        initialGennaOnly={gennaOnly(event.settings)}
      />
      <RaceHistory eventId={event.id} />
      <DeviceLinks eventId={event.id} secret={event.secret} />
    </PageShell>
  );
}
