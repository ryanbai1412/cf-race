import { DuelReview } from "@/components/duel/duel-review";
import { ShellFrame } from "@/components/shell/shell-frame";

export const dynamic = "force-dynamic";

export default function DuelReviewPage({
  params,
}: {
  params: { matchId: string };
}) {
  return (
    <ShellFrame>
      <DuelReview matchId={params.matchId} />
    </ShellFrame>
  );
}
