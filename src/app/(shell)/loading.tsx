/** Instant shell-route loading state so navs feel immediate. */
export default function Loading() {
  return (
    <main className="mx-auto max-w-4xl px-6 py-10">
      <div className="space-y-4">
        <div className="h-8 w-48 animate-pulse rounded bg-muted" />
        <div className="h-4 w-72 animate-pulse rounded bg-muted" />
        <div className="mt-6 space-y-2">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="h-12 animate-pulse rounded bg-muted/60" />
          ))}
        </div>
      </div>
    </main>
  );
}
