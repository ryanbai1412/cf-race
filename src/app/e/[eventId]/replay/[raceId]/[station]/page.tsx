import { authorizeEvent } from "@/lib/event-auth";
import { notFound, redirect } from "next/navigation";
import { ReplayPlayer } from "@/components/replay/replay-player";

export default async function ReplayPage({
  params,
}: {
  params: { eventId: string; raceId: string; station: string };
}) {
  if (params.station !== "station1" && params.station !== "station2") notFound();
  const event = await authorizeEvent(params.eventId);
  if (!event) redirect("/invalid-link");

  return (
    <ReplayPlayer
      eventId={event.id}
      raceId={params.raceId}
      station={params.station}
    />
  );
}
