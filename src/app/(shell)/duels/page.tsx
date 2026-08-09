import { redirect } from "next/navigation";
import { authUser } from "@/lib/supabase/server";
import { DuelHome } from "@/components/duel/duel-home";

export const dynamic = "force-dynamic";

export default async function DuelsPage() {
  const user = await authUser();
  if (!user) redirect("/?next=/duels");
  return <DuelHome />;
}
