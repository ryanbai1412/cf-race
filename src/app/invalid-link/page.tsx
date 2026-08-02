import Link from "next/link";

export default function InvalidLink() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4">
      <h1 className="text-3xl font-bold">Invalid or expired event link</h1>
      <p className="text-muted-foreground">
        Ask the organizer for a fresh device link.
      </p>
      <Link href="/" className="underline text-primary">
        Back to home
      </Link>
    </main>
  );
}
