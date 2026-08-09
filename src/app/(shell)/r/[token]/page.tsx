import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { lookupShare } from "@/lib/shares";
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
  const share = await lookupShare(token);

  if (share?.kind === "session") {
    return (
      <SoloReplay apiUrl={`/api/shared/replay?token=${token}`} readOnly />
    );
  }
  if (share?.kind === "match") {
    return (
      <DuelReview apiUrl={`/api/shared/review?token=${token}`} readOnly />
    );
  }
  notFound();
}
