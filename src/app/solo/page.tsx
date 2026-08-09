import { permanentRedirect } from "next/navigation";

/** Legacy route — the bank moved to /problems (PRD 11 §10). */
export default function LegacySoloPage() {
  permanentRedirect("/problems");
}
