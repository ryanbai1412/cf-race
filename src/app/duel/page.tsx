import { permanentRedirect } from "next/navigation";

/** Legacy route — the duel arena moved to /duels (PRD 11 §10). */
export default function LegacyDuelPage() {
  permanentRedirect("/duels");
}
