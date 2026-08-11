import { authorizeEvent } from "@/lib/event-auth";
import { notFound, redirect } from "next/navigation";
import { LeftMonitor } from "@/components/monitor/left-monitor";
import { RightMonitor } from "@/components/monitor/right-monitor";

export default async function MonitorPage({
  params,
}: {
  params: { eventId: string; m: string };
}) {
  // Legacy monitor names: a = the race monitor, b = the leaderboard monitor.
  const m =
    params.m === "a" ? "right" : params.m === "b" ? "left" : params.m;
  if (m !== "left" && m !== "right") notFound();
  const event = await authorizeEvent(params.eventId);
  if (!event) redirect("/invalid-link");

  return m === "right" ? (
    <RightMonitor eventId={event.id} />
  ) : (
    <LeftMonitor eventId={event.id} />
  );
}
