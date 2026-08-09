import { notFound } from "next/navigation";
import { db } from "@/lib/db";
import { SoloClient } from "@/components/solo/solo-client";
import type { Problem } from "@/lib/types";

export const dynamic = "force-dynamic";

/** Solo run screen (full-screen, no navbar) — replaces /solo/[problemId]. */
export default async function SolvePage({
  params,
}: {
  params: { id: string };
}) {
  const [{ data: problem }, { data: all }] = await Promise.all([
    db()
      .from("problems")
      .select("*")
      .eq("id", params.id)
      .maybeSingle<Problem & { tags: string[] | null }>(),
    db()
      .from("problems")
      .select("id, tags")
      .neq("id", "warmup-sum")
      .order("id", { ascending: true }),
  ]);
  if (!problem || (problem.tags ?? []).includes("hidden")) notFound();

  const ids = (all ?? [])
    .filter((p) => !((p.tags as string[] | null) ?? []).includes("hidden"))
    .map((p) => p.id);
  return <SoloClient problem={problem} problemIds={ids} />;
}
