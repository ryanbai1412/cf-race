import { permanentRedirect } from "next/navigation";

/** Legacy route — solving moved to /problems/[id]/solve (PRD 11 §10). */
export default function LegacySoloSolvePage({
  params,
}: {
  params: { problemId: string };
}) {
  permanentRedirect(`/problems/${params.problemId}/solve`);
}
