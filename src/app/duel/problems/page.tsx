import { Navbar } from "@/components/shell/navbar";
import { DuelProblems } from "@/components/duel/duel-problems";

export const dynamic = "force-dynamic";

export default function DuelProblemsPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <div className="flex-1">
        <DuelProblems />
      </div>
    </div>
  );
}
