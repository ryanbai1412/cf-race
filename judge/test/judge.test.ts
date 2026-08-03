import path from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";

const dirname = path.dirname(fileURLToPath(import.meta.url));
process.env.JUDGE_SANDBOX = process.env.JUDGE_SANDBOX ?? "none";
process.env.PROBLEMS_DIR = path.resolve(dirname, "../../problems");
process.env.CACHE_DIR = "/tmp/judge-test-cache";

const { handleRun, handleSubmit } = await import("../src/judge.js");

const PY_AC = `
t=int(input())
for _ in range(t):
    a,b=map(int,input().split())
    print(a+b)
`;
const PY_WA = `
t=int(input())
for _ in range(t):
    a,b=map(int,input().split())
    print(a+b+1)
`;
const PY_TLE = `
while True:
    pass
`;
const PY_RE = `
raise RuntimeError("boom")
`;

const CPP_AC = `
#include <bits/stdc++.h>
int main(){int t;scanf("%d",&t);while(t--){long long a,b;scanf("%lld %lld",&a,&b);printf("%lld\\n",a+b);}return 0;}
`;

describe("run (samples)", () => {
  it("python AC on dev/aplusb samples", async () => {
    const r = await handleRun({ runId: "r1", lang: "py", source: PY_AC, problemId: "dev/aplusb" });
    expect(r.compile.ok).toBe(true);
    expect(r.results.length).toBeGreaterThan(0);
    expect(r.results.every((x) => x.verdict === "AC")).toBe(true);
  });

  it("python WA with checker note", async () => {
    const r = await handleRun({ runId: "r2", lang: "py", source: PY_WA, problemId: "dev/aplusb" });
    expect(r.results[0].verdict).toBe("WA");
    expect(r.results[0].checkerNote).toBeTruthy();
  });

  it("python RE surfaces stderr", async () => {
    const r = await handleRun({ runId: "r3", lang: "py", source: PY_RE, problemId: "dev/aplusb" });
    expect(r.results[0].verdict).toBe("RE");
    expect(r.results[0].stderr).toContain("boom");
  });

  it("custom test with expected=null is AC and shows output", async () => {
    const r = await handleRun({
      runId: "r4",
      lang: "py",
      source: "print(int(input())*2)",
      tests: [{ name: "custom1", input: "21\n", expected: null }],
      timeLimitMs: 1000,
      memoryLimitMb: 256,
    });
    expect(r.results[0].verdict).toBe("AC");
    expect(r.results[0].stdout.trim()).toBe("42");
  });

  it("large correct output is AC, with display truncated", async () => {
    const n = 200_000; // ~1.2MB, far beyond the 64KB display cap
    let expected = "";
    for (let i = 0; i < n; i++) expected += `${i}\n`;
    const r = await handleRun({
      runId: "r7",
      lang: "py",
      source: `import sys\nsys.stdout.write("".join(f"{i}\\n" for i in range(${n})))`,
      tests: [{ name: "big", input: "", expected }],
      timeLimitMs: 5000,
      memoryLimitMb: 512,
    });
    expect(r.results[0].checkerNote).toBeUndefined();
    expect(r.results[0].verdict).toBe("AC");
    expect(r.results[0].stdoutTruncated).toBe(true);
    expect(r.results[0].stdout.length).toBeLessThan(expected.length);
  }, 60000);

  it("cpp compiles (debug) and passes samples", async () => {
    const r = await handleRun({ runId: "r5", lang: "cpp", source: CPP_AC, problemId: "dev/aplusb" });
    expect(r.compile.ok).toBe(true);
    expect(r.results.every((x) => x.verdict === "AC")).toBe(true);
  }, 60000);

  it("cpp CE reports compiler stderr and SKIPs tests", async () => {
    const r = await handleRun({ runId: "r6", lang: "cpp", source: "int main( {", problemId: "dev/aplusb" });
    expect(r.compile.ok).toBe(false);
    expect(r.compile.stderr).toMatch(/error/i);
    expect(r.results.every((x) => x.verdict === "SKIP")).toBe(true);
  }, 60000);
});

describe("submit (full tests)", () => {
  it("AC", async () => {
    const r = await handleSubmit({ submissionId: "s1", lang: "py", source: PY_AC, problemId: "dev/aplusb" });
    expect(r.verdict).toBe("AC");
    expect(r.passedCount).toBe(r.totalCount);
  }, 60000);

  it("WA short-circuits", async () => {
    const r = await handleSubmit({ submissionId: "s2", lang: "py", source: PY_WA, problemId: "dev/aplusb" });
    expect(r.verdict).toBe("WA");
    expect(r.failedTest).toBe("01");
    expect(r.passedCount).toBe(0);
  }, 60000);

  it("TLE", async () => {
    const r = await handleSubmit({ submissionId: "s3", lang: "py", source: PY_TLE, problemId: "dev/aplusb" });
    expect(r.verdict).toBe("TLE");
  }, 60000);

  it("RE", async () => {
    const r = await handleSubmit({ submissionId: "s4", lang: "py", source: PY_RE, problemId: "dev/aplusb" });
    expect(r.verdict).toBe("RE");
  }, 60000);

  it("CE for cpp", async () => {
    const r = await handleSubmit({ submissionId: "s5", lang: "cpp", source: "int main( {", problemId: "dev/aplusb" });
    expect(r.verdict).toBe("CE");
    expect(r.compileStderr).toMatch(/error/i);
  }, 60000);

  it("floatEps problem accepts close output", async () => {
    const src = `
n=int(input())
xs=list(map(int,input().split()))
print(sum(xs)/n)
`;
    const r = await handleSubmit({ submissionId: "s6", lang: "py", source: src, problemId: "dev/floatavg" });
    expect(r.verdict).toBe("AC");
  }, 60000);

  it("YES/NO case-insensitive on parity", async () => {
    const src = `
t=int(input())
for _ in range(t):
    print("yes" if int(input())%2==0 else "No")
`;
    const r = await handleSubmit({ submissionId: "s7", lang: "py", source: src, problemId: "dev/parity" });
    expect(r.verdict).toBe("AC");
  }, 60000);
});
