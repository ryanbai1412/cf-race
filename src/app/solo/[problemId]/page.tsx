import { notFound } from "next/navigation";
import { db } from "@/lib/db";
import { SoloClient } from "@/components/solo/solo-client";
import type { Problem } from "@/lib/types";

export const dynamic = "force-dynamic";

export default async function SoloProblemPage({
  params,
}: {
  params: { problemId: string };
}) {
  const [{ data: problem }, { data: all }] = await Promise.all([
    db().from("problems").select("*").eq("id", params.problemId).maybeSingle<Problem>(),
    db()
      .from("problems")
      .select("id")
      .neq("id", "warmup-sum")
      .order("id", { ascending: true }),
  ]);
  if (!problem) notFound();

  return (
    <SoloClient problem={problem} problemIds={(all ?? []).map((p) => p.id)} />
  );
}
