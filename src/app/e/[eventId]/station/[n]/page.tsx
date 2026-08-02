import { authorizeEvent } from "@/lib/event-auth";
import { notFound, redirect } from "next/navigation";

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
    <main className="flex min-h-screen flex-col items-center justify-center gap-3">
      <p className="font-mono text-xs uppercase tracking-[0.3em] text-primary">
        Station {params.n}
      </p>
      <h1 className="text-3xl font-bold">{event.name}</h1>
      <p className="text-muted-foreground">Check-in flow coming next.</p>
    </main>
  );
}
