import { permanentRedirect } from "next/navigation";

/** Legacy route — replays moved to /replay/[sessionId] (PRD 11 §10). */
export default function LegacySoloReplayPage({
  params,
}: {
  params: { sessionId: string };
}) {
  permanentRedirect(`/replay/${params.sessionId}`);
}
