import { redirect } from "next/navigation";
import { getEffectiveUser } from "@/lib/impersonation";
import { DuelHome } from "@/components/duel/duel-home";

export const dynamic = "force-dynamic";

export default async function DuelsPage() {
  const user = await getEffectiveUser();
  if (!user) redirect("/?next=/duels");
  return <DuelHome />;
}
