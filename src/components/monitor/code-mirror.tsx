"use client";

import dynamic from "next/dynamic";
import type { Lang } from "@/lib/types";

const MonacoEditor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

/** Read-only editor renderer shared by live contestant mirrors and tourist replay. */
export function CodeMirror({
  code,
  lang,
  fontSize = 16,
}: {
  code: string;
  lang: Lang;
  fontSize?: number;
}) {
  return (
    <MonacoEditor
      height="100%"
      theme="vs-dark"
      language={lang === "cpp" ? "cpp" : "python"}
      value={code}
      options={{
        readOnly: true,
        domReadOnly: true,
        fontSize,
        fontFamily: "var(--font-geist-mono), 'JetBrains Mono', monospace",
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        renderLineHighlight: "none",
        occurrencesHighlight: "off",
        cursorBlinking: "solid",
        automaticLayout: true,
        scrollbar: { verticalScrollbarSize: 6 },
      }}
    />
  );
}
