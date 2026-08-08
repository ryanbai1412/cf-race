import { describe, expect, it } from "vitest";
import { createEditorRecorder, type RecordedEditorEvent } from "../replay-recorder";

function makeRecorder(startT = 0) {
  let t: number | null = startT;
  const pushed: RecordedEditorEvent[] = [];
  const rec = createEditorRecorder({
    now: () => t,
    push: (ev) => pushed.push(ev),
  });
  return {
    rec,
    pushed,
    setT: (next: number | null) => {
      t = next;
    },
  };
}

describe("createEditorRecorder", () => {
  it("records a snapshot keyframe then deltas", () => {
    const { rec, pushed, setT } = makeRecorder();
    rec.snapshot("", "cpp");
    setT(100);
    rec.delta([{ o: 0, l: 0, text: "a" }], "a", "cpp");
    setT(200);
    rec.delta([{ o: 1, l: 0, text: "b" }], "ab", "cpp");

    expect(pushed).toHaveLength(3);
    expect(pushed[0]).toMatchObject({ t: 0, code: "" });
    expect(pushed[0].kind).toBeUndefined();
    expect(pushed[1]).toMatchObject({ t: 100, kind: "delta" });
    expect(pushed[2]).toMatchObject({ t: 200, kind: "delta" });
  });

  it("falls back to a keyframe when the shadow copy diverges", () => {
    const { rec, pushed, setT } = makeRecorder();
    rec.snapshot("", "cpp");
    setT(50);
    // Claim the editor now contains text the delta can't produce.
    rec.delta([{ o: 0, l: 0, text: "a" }], "different", "cpp");
    const last = pushed[pushed.length - 1];
    expect(last.kind).toBeUndefined();
    expect(last.code).toBe("different");
  });

  it("emits a keyframe on language switch", () => {
    const { rec, pushed, setT } = makeRecorder();
    rec.snapshot("int main(){}", "cpp");
    setT(10);
    rec.delta([{ o: 0, l: 0, text: "x" }], "print(1)", "py");
    const last = pushed[pushed.length - 1];
    expect(last.kind).toBeUndefined();
    expect(last.lang).toBe("py");
  });

  it("records nothing when the clock is off", () => {
    const { rec, pushed, setT } = makeRecorder();
    setT(null);
    rec.snapshot("code", "cpp");
    rec.delta([{ o: 0, l: 0, text: "a" }], "a", "cpp");
    expect(pushed).toHaveLength(0);
  });
});
