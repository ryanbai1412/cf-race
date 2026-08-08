import { describe, expect, it } from "vitest";
import {
  buildReplayEvents,
  sanitizeEditorEvents,
  type EditorEventRow,
} from "../editor-events";

const row = (partial: Partial<EditorEventRow>): EditorEventRow => ({
  t_ms: 0,
  code: "",
  lang: "cpp",
  kind: "snapshot",
  payload: null,
  ...partial,
});

describe("sanitizeEditorEvents", () => {
  it("normalizes t/code/lang and defaults unknown kinds to snapshot", () => {
    const [e] = sanitizeEditorEvents([
      { t: -5.7, code: "int main(){}", lang: "cpp", kind: "nonsense" },
    ]);
    expect(e).toEqual({
      t_ms: 0,
      code: "int main(){}",
      lang: "cpp",
      kind: "snapshot",
      payload: null,
    });
  });

  it("keeps known kinds and small payloads", () => {
    const [e] = sanitizeEditorEvents([
      {
        t: 1234.4,
        code: "",
        lang: "py",
        kind: "delta",
        payload: { changes: [{ o: 0, l: 0, text: "x" }] },
      },
    ]);
    expect(e.t_ms).toBe(1234);
    expect(e.kind).toBe("delta");
    expect(e.payload).toEqual({ changes: [{ o: 0, l: 0, text: "x" }] });
  });

  it("drops oversized payloads and caps batch size", () => {
    const big = sanitizeEditorEvents([
      { t: 0, code: "", lang: "cpp", kind: "run_result", payload: { s: "x".repeat(30_000) } },
    ]);
    expect(big[0].payload).toBeNull();

    const batch = sanitizeEditorEvents(
      Array.from({ length: 1500 }, (_, i) => ({
        t: i,
        code: "",
        lang: "cpp" as const,
      }))
    );
    expect(batch).toHaveLength(1000);
  });

  it("coerces unknown languages to cpp", () => {
    const [e] = sanitizeEditorEvents([
      { t: 0, code: "", lang: "rust" as unknown as "cpp" },
    ]);
    expect(e.lang).toBe("cpp");
  });
});

describe("buildReplayEvents", () => {
  it("maps every persisted kind to its tourist event", () => {
    const { events } = buildReplayEvents([
      row({ t_ms: 0, code: "a", kind: "snapshot" }),
      row({ t_ms: 10, kind: "delta", payload: { changes: [{ o: 0, l: 0, text: "b" }] } }),
      row({ t_ms: 20, kind: "run" }),
      row({
        t_ms: 30,
        kind: "run_result",
        payload: { target: "samples", compiled: true, verdict: "AC", passed: 1, total: 1 },
      }),
      row({ t_ms: 40, kind: "tab", payload: { tab: "output" } }),
      row({ t_ms: 50, kind: "scroll", payload: { frac: 0.5 } }),
      row({ t_ms: 60, kind: "submit" }),
      row({ t_ms: 70, kind: "verdict", payload: { verdict: "AC" } }),
    ]);
    expect(events.map((e) => e.type)).toEqual([
      "snapshot",
      "delta",
      "run",
      "run_result",
      "tab",
      "scroll",
      "submit",
      "verdict",
    ]);
  });

  it("sorts by time and skips marker kinds with missing payloads", () => {
    const { events } = buildReplayEvents([
      row({ t_ms: 100, kind: "snapshot", code: "late" }),
      row({ t_ms: 5, kind: "run" }),
      row({ t_ms: 50, kind: "verdict", payload: null }),
      row({ t_ms: 60, kind: "delta", payload: null }),
    ]);
    expect(events).toEqual([
      { t: 5, type: "run" },
      { t: 100, type: "snapshot", code: "late", lang: "cpp" },
    ]);
  });

  it("reports the language of the final code state", () => {
    const py = buildReplayEvents([
      row({ t_ms: 0, kind: "snapshot", lang: "cpp" }),
      row({ t_ms: 10, kind: "snapshot", lang: "py" }),
      row({ t_ms: 20, kind: "run", lang: "cpp" }),
    ]);
    expect(py.lang).toBe("py");

    const fallback = buildReplayEvents([row({ t_ms: 0, kind: "run" })], "py");
    expect(fallback.lang).toBe("py");
  });
});
