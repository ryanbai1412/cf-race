import { DuelReview } from "@/components/duel/duel-review";
import { Navbar } from "@/components/shell/navbar";

export const dynamic = "force-dynamic";

export default function DuelReviewPage({
  params,
}: {
  params: { matchId: string };
}) {
  return (
    <div className="flex h-screen flex-col">
      <Navbar />
      <div className="min-h-0 flex-1">
        <DuelReview matchId={params.matchId} />
      </div>
    </div>
  );
}
