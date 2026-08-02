import { authorizeEvent } from "@/lib/event-auth";
import { notFound, redirect } from "next/navigation";

export default async function MonitorPage({
  params,
  searchParams,
}: {
  params: { eventId: string; m: string };
  searchParams: { k?: string };
}) {
  if (params.m !== "a" && params.m !== "b") notFound();
  const event = await authorizeEvent(params.eventId, searchParams.k);
  if (!event) redirect("/invalid-link");

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-3">
      <p className="font-mono text-xs uppercase tracking-[0.3em] text-primary">
        Monitor {params.m.toUpperCase()}
      </p>
      <h1 className="text-3xl font-bold">{event.name}</h1>
      <p className="text-muted-foreground">Spectator screen coming next.</p>
    </main>
  );
}
