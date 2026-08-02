import { CreateEventCard } from "@/components/create-event-card";

export default function Home() {
  return (
    <main className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(99,102,241,0.15),transparent_60%)]" />
      <div className="z-10 flex flex-col items-center gap-8 px-6 text-center">
        <div className="space-y-3">
          <p className="font-mono text-sm uppercase tracking-[0.3em] text-primary">
            Code vs Racing
          </p>
          <h1 className="max-w-2xl text-5xl font-extrabold tracking-tight sm:text-6xl">
            Race the fastest coders alive.
          </h1>
          <p className="mx-auto max-w-xl text-lg text-muted-foreground">
            Head-to-head competitive programming sprints — solve a Codeforces
            problem faster than the person next to you, and faster than tourist.
          </p>
        </div>
        <CreateEventCard />
      </div>
    </main>
  );
}
