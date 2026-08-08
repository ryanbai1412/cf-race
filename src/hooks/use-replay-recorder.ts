"use client";

import { useCallback, useEffect, useMemo, useRef } from "react";
import {
  createEditorRecorder,
  type RecordedEditorEvent,
} from "@/lib/replay-recorder";
import { summarizeRun } from "@/lib/tourist";
import type { Lang, RunResult } from "@/lib/types";

/**
 * Client-side replay recording shared by race stations and solo runs: buffers
 * per-keystroke editor events plus run/tab/scroll timeline markers, and
 * periodically flushes them to the caller's persistence endpoint.
 *
 * - `now` returns ms since the recording started, or null when no recording
 *   is active (events are dropped). Countdown-time events clamp to t=0.
 * - `send` posts one batch; return false to requeue the events (e.g. the
 *   recording context isn't known yet).
 * - `autoFlush` enables the 5s flush interval + beforeunload/unmount flush.
 */
export function useReplayRecorder({
  now,
  send,
  autoFlush,
}: {
  now: () => number | null;
  send: (events: RecordedEditorEvent[]) => boolean;
  autoFlush: boolean;
}) {
  const buffer = useRef<RecordedEditorEvent[]>([]);
  const nowRef = useRef(now);
  nowRef.current = now;
  const sendRef = useRef(send);
  sendRef.current = send;

  const editorRecorder = useMemo(
    () =>
      createEditorRecorder({
        now: () => {
          const t = nowRef.current();
          return t === null ? null : Math.max(0, t);
        },
        push: (ev) => buffer.current.push(ev),
      }),
    []
  );

  const push = useCallback(
    (
      lang: Lang,
      kind: RecordedEditorEvent["kind"],
      payload?: RecordedEditorEvent["payload"]
    ) => {
      const t = nowRef.current();
      if (t === null) return;
      buffer.current.push({ t: Math.max(0, t), code: "", lang, kind, payload });
    },
    []
  );

  const recordRun = useCallback((lang: Lang) => push(lang, "run"), [push]);
  const recordRunResult = useCallback(
    (result: RunResult, target: "samples" | "custom", lang: Lang) =>
      push(lang, "run_result", summarizeRun(result, target)),
    [push]
  );
  const recordTab = useCallback(
    (tab: string, lang: Lang) => push(lang, "tab", { tab }),
    [push]
  );
  const recordScroll = useCallback(
    (frac: number, lang: Lang) => push(lang, "scroll", { frac }),
    [push]
  );

  const flush = useCallback(() => {
    const events = buffer.current;
    if (events.length === 0) return;
    buffer.current = [];
    if (!sendRef.current(events)) {
      buffer.current = [...events, ...buffer.current];
    }
  }, []);

  useEffect(() => {
    if (!autoFlush) return;
    const id = setInterval(flush, 5000);
    window.addEventListener("beforeunload", flush);
    return () => {
      clearInterval(id);
      window.removeEventListener("beforeunload", flush);
      flush();
    };
  }, [autoFlush, flush]);

  return { editorRecorder, recordRun, recordRunResult, recordTab, recordScroll, flush };
}
