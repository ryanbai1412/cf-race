import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { db } from "@/lib/db";
import { SoloReplay } from "@/components/solo/solo-replay";
import { DuelReview } from "@/components/duel/duel-review";

export const dynamic = "force-dynamic";

// Public share links must never be indexed (PRD 11 §5.4).
export const metadata: Metadata = {
  robots: { index: false, follow: false },
};

/** Public read-only replay behind a share token: session or duel match. */
export default async function SharedReplayPage({
  params,
}: {
  params: { token: string };
}) {
  const token = params.token;
  const [{ data: sessionShare }, { data: matchShare }] = await Promise.all([
    db()
      .from("session_shares")
      .select("session_id")
      .eq("token", token)
      .is("revoked_at", null)
      .maybeSingle(),
    db()
      .from("match_shares")
      .select("match_id")
      .eq("token", token)
      .is("revoked_at", null)
      .maybeSingle(),
  ]);

  if (sessionShare) {
    return (
      <SoloReplay apiUrl={`/api/shared/replay?token=${token}`} readOnly />
    );
  }
  if (matchShare) {
    return (
      <DuelReview apiUrl={`/api/shared/review?token=${token}`} readOnly />
    );
  }
  notFound();
}
