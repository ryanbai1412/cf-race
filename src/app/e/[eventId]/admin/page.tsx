import { authorizeEvent } from "@/lib/event-auth";
import { listEventAdmins } from "@/lib/event-admins";
import { redirect } from "next/navigation";
import { EventAdmins } from "@/components/admin/event-admins";
import { DeviceLinks } from "@/components/admin/device-links";
import { RaceControl } from "@/components/admin/race-control";
import { RaceHistory } from "@/components/admin/race-history";
import { EventSettings } from "@/components/admin/event-settings";
import { eventTimerSec, gennaOnly, requireWebcam, selfServe } from "@/lib/event-settings";
import { PageHeader, PageShell } from "@/components/shell/page";

export default async function AdminPage({
  params,
}: {
  params: { eventId: string };
}) {
  const event = await authorizeEvent(params.eventId);
  if (!event) redirect("/invalid-link");
  const admins = await listEventAdmins(event);

  return (
    <PageShell>
      <PageHeader eyebrow="Admin console" title={event.name} />
      <RaceControl eventId={event.id} gennaOnly={gennaOnly(event.settings)} />
      <EventSettings
        eventId={event.id}
        initialRequireWebcam={requireWebcam(event.settings)}
        initialSelfServe={selfServe(event.settings)}
        initialGennaOnly={gennaOnly(event.settings)}
        initialTimerSec={eventTimerSec(event.settings)}
      />
      <RaceHistory eventId={event.id} />
      <EventAdmins eventId={event.id} initialAdmins={admins} />
      <DeviceLinks eventId={event.id} secret={event.secret} />
    </PageShell>
  );
}
