import { DuelReview } from "@/components/duel/duel-review";

export const dynamic = "force-dynamic";

export default function DuelReviewPage({
  params,
}: {
  params: { matchId: string };
}) {
  return <DuelReview matchId={params.matchId} />;
}
