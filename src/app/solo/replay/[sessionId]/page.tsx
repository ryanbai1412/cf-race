import { SoloReplay } from "@/components/solo/solo-replay";

export default function SoloReplayPage({
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
