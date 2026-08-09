import type { ReactNode } from "react";
import { Navbar } from "@/components/shell/navbar";

/** Navbar over full-height content, for pages outside the (shell) route group. */
export function ShellFrame({ children }: { children: ReactNode }) {
  return (
    <div className="flex h-screen flex-col">
      <Navbar />
      <div className="min-h-0 flex-1 overflow-y-auto">{children}</div>
    </div>
  );
}
