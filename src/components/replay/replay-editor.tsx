"use client";

import { useEffect, useRef } from "react";
import dynamic from "next/dynamic";
import type { OnMount } from "@monaco-editor/react";
import type { Lang } from "@/lib/types";
import type { TouristPlayer } from "@/lib/tourist";

const MonacoEditor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

type Editor = Parameters<OnMount>[0];
type Monaco = Parameters<OnMount>[1];

/**
 * Read-only Monaco view driven imperatively by a TouristPlayer: forward
 * playback applies delta events via `model.applyEdits` (per-keystroke smooth,
 * no per-frame React value churn); seeks, keyframes, and language switches
 * replace the document wholesale.
 */
export function ReplayEditor({
  player,
  clockMs,
  fallbackLang,
  fontSize = 16,
}: {
  player: TouristPlayer;
  clockMs: number;
  fallbackLang: Lang;
  fontSize?: number;
}) {
  const editorRef = useRef<Editor | null>(null);
  const monacoRef = useRef<Monaco | null>(null);
  const langRef = useRef<Lang | null>(null);
  const clockRef = useRef(clockMs);
  clockRef.current = clockMs;

  const sync = (clock: number) => {
    const editor = editorRef.current;
    const monaco = monacoRef.current;
    const model = editor?.getModel();
    if (!editor || !monaco || !model) return;

    const frame = player.advance(clock);
    const lang = frame.lang ?? fallbackLang;
    if (lang !== langRef.current) {
      langRef.current = lang;
      monaco.editor.setModelLanguage(model, lang === "cpp" ? "cpp" : "python");
    }

    if (frame.reset) {
      if (model.getValue() !== frame.code) model.setValue(frame.code);
      return;
    }
    let lastOffset: number | null = null;
    for (const changes of frame.deltas) {
      // All ranges within one batch are relative to the document before it.
      const edits = changes.map((c) => ({
        range: monaco.Range.fromPositions(
          model.getPositionAt(c.o),
          model.getPositionAt(c.o + c.l)
        ),
        text: c.text,
      }));
      model.applyEdits(edits);
      const last = changes[changes.length - 1];
      if (last) lastOffset = Math.min(model.getValueLength(), c0End(last));
    }
    // Drift safety net: if the mirrored document ever diverges, resync.
    if (model.getValueLength() !== frame.code.length) {
      model.setValue(frame.code);
      return;
    }
    if (lastOffset !== null) {
      editor.revealPositionInCenterIfOutsideViewport(
        model.getPositionAt(lastOffset)
      );
    }
  };

  const handleMount: OnMount = (editor, monaco) => {
    editorRef.current = editor;
    monacoRef.current = monaco;
    langRef.current = null;
    sync(clockRef.current);
  };

  useEffect(() => {
    sync(clockMs);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [clockMs, player]);

  return (
    <MonacoEditor
      height="100%"
      theme="vs-dark"
      language={fallbackLang === "cpp" ? "cpp" : "python"}
      defaultValue=""
      onMount={handleMount}
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

function c0End(c: { o: number; text: string }): number {
  return c.o + c.text.length;
}
