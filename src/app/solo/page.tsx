import { db } from "@/lib/db";
import { SoloHome } from "@/components/solo/solo-home";

export const dynamic = "force-dynamic";

export default async function SoloPage() {
  const { data: problems } = await db()
    .from("problems")
    .select("id, name, rating, tourist_time_ms")
    .neq("id", "warmup-sum")
    .order("id", { ascending: true });

  return <SoloHome problems={problems ?? []} />;
}
