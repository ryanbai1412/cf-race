import { describe, expect, it } from "vitest";
import type { RunResult } from "../types";
import { applyDeltaChanges, summarizeRun } from "../tourist";

const runResult = (
  verdicts: ("AC" | "WA" | "RE" | "TLE" | "ML" | "SKIP")[],
  compileOk = true
): RunResult => ({
  runId: "r1",
  compile: { ok: compileOk, stderr: compileOk ? "" : "boom" },
  results: verdicts.map((v, i) => ({
    name: `sample${i + 1}`,
    verdict: v,
    timeMs: 10,
    stdout: "",
    stderr: "",
  })),
});

describe("summarizeRun", () => {
  it("is AC when all tests pass", () => {
    const s = summarizeRun(runResult(["AC", "AC"]), "samples");
    expect(s.verdict).toBe("AC");
    expect(s.passed).toBe(2);
    expect(s.total).toBe(2);
    expect(s.compileStderr).toBeUndefined();
  });

  it("picks the worst verdict across tests", () => {
    expect(summarizeRun(runResult(["AC", "WA", "TLE"]), "samples").verdict).toBe("TLE");
    expect(summarizeRun(runResult(["WA", "RE"]), "samples").verdict).toBe("RE");
  });

  it("is CE when compilation failed, with truncated stderr", () => {
    const s = summarizeRun(runResult([], false), "custom");
    expect(s.verdict).toBe("CE");
    expect(s.compiled).toBe(false);
    expect(s.compileStderr).toBe("boom");
  });
});

describe("applyDeltaChanges", () => {
  it("applies inserts, replacements, and deletions", () => {
    expect(applyDeltaChanges("hello", [{ o: 5, l: 0, text: "!" }])).toBe("hello!");
    expect(applyDeltaChanges("hello", [{ o: 0, l: 5, text: "bye" }])).toBe("bye");
    expect(applyDeltaChanges("hello", [{ o: 1, l: 3, text: "" }])).toBe("ho");
  });

  it("applies multiple changes relative to the pre-event document", () => {
    // Monaco batches: both offsets are relative to "abcdef" before the event.
    expect(
      applyDeltaChanges("abcdef", [
        { o: 0, l: 1, text: "X" },
        { o: 5, l: 1, text: "Y" },
      ])
    ).toBe("XbcdeY");
  });

  it("throws on out-of-bounds changes", () => {
    expect(() => applyDeltaChanges("ab", [{ o: 1, l: 5, text: "" }])).toThrow();
    expect(() => applyDeltaChanges("ab", [{ o: -1, l: 0, text: "x" }])).toThrow();
  });
});
