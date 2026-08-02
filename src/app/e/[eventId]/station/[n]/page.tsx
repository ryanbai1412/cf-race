import { authorizeEvent } from "@/lib/event-auth";
import { notFound, redirect } from "next/navigation";
import { StationClient } from "@/components/station/station-client";

export default async function StationPage({
  params,
  searchParams,
}: {
  params: { eventId: string; n: string };
  searchParams: { k?: string };
}) {
  if (params.n !== "1" && params.n !== "2") notFound();
  const event = await authorizeEvent(params.eventId, searchParams.k);
  if (!event) redirect("/invalid-link");

  return (
    <StationClient
      eventId={event.id}
      station={params.n === "1" ? "station1" : "station2"}
    />
  );
}
