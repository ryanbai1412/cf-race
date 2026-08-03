"use client";

import { useMemo } from "react";
import katex from "katex";
import "katex/dist/katex.min.css";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { Copy } from "lucide-react";
import type { Problem } from "@/lib/types";

const TEX_ENTITIES: [RegExp, string][] = [
  [/&lt;/g, "<"],
  [/&gt;/g, ">"],
  [/&amp;/g, "&"],
];

function renderTex(tex: string, displayMode: boolean): string {
  const decoded = TEX_ENTITIES.reduce((s, [re, ch]) => s.replace(re, ch), tex);
  return katex.renderToString(decoded, { throwOnError: false, displayMode });
}

/** Replace \(...\) and \[...\] TeX delimiters in scraped statement HTML with KaTeX markup. */
function renderStatementMath(html: string): string {
  return html
    .replace(/\\\[([\s\S]+?)\\\]/g, (m, tex) => {
      try {
        return renderTex(tex, true);
      } catch {
        return m;
      }
    })
    .replace(/\\\(([\s\S]+?)\\\)/g, (m, tex) => {
      try {
        return renderTex(tex, false);
      } catch {
        return m;
      }
    });
}

export function StatementPane({ problem }: { problem: Problem }) {
  const statementHtml = useMemo(
    () => (problem.statement_html ? renderStatementMath(problem.statement_html) : null),
    [problem.statement_html]
  );

  return (
    <div className="flex h-full flex-col overflow-y-auto border-r border-border/60 bg-card/30 px-6 py-5">
      <div className="mb-3 flex items-baseline gap-3">
        <h2 className="text-xl font-bold">{problem.name}</h2>
        <span className="font-mono text-xs text-muted-foreground">
          {problem.time_limit_ms / 1000}s · {problem.memory_limit_mb}MB
        </span>
      </div>
      {statementHtml ? (
        <div
          className="cf-statement prose prose-invert prose-sm max-w-none"
          dangerouslySetInnerHTML={{ __html: statementHtml }}
        />
      ) : (
        <p className="text-muted-foreground">Statement unavailable.</p>
      )}
      <div className="mt-6 space-y-4">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">
          Sample tests
        </h3>
        {problem.samples.map((s, i) => (
          <div key={i} className="grid grid-cols-2 gap-2">
            {(["input", "output"] as const).map((kind) => (
              <div key={kind} className="rounded-md border border-border/60">
                <div className="flex items-center justify-between border-b border-border/60 px-2 py-1">
                  <span className="text-xs font-medium text-muted-foreground">
                    {kind === "input" ? `Input ${i + 1}` : `Output ${i + 1}`}
                  </span>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="h-6 px-1.5"
                    onClick={() => {
                      navigator.clipboard.writeText(kind === "input" ? s.input : s.output);
                      toast.success("Copied");
                    }}
                  >
                    <Copy className="h-3 w-3" />
                  </Button>
                </div>
                <pre className="max-h-48 overflow-auto p-2 font-mono text-xs">
                  {kind === "input" ? s.input : s.output}
                </pre>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
