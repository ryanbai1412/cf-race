import { authorizeEvent } from "@/lib/event-auth";
import { notFound, redirect } from "next/navigation";
import { MonitorClient } from "@/components/monitor/monitor-client";

export default async function MonitorPage({
  params,
}: {
  params: { eventId: string; m: string };
}) {
  if (params.m !== "a" && params.m !== "b") notFound();
  const event = await authorizeEvent(params.eventId);
  if (!event) redirect("/invalid-link");

  return <MonitorClient eventId={event.id} monitor={params.m} />;
}
