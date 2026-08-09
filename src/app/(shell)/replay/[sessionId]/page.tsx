import { SoloReplay } from "@/components/solo/solo-replay";

export const dynamic = "force-dynamic";

/** Private replay (PRD 11 §5.3) — access enforced by /api/solo/replay. */
export default function ReplayPage({
  params,
  searchParams,
}: {
  params: { sessionId: string };
  searchParams: { export?: string };
}) {
  return (
    <SoloReplay
      sessionId={params.sessionId}
      showExport={searchParams.export === "1"}
    />
  );
}
