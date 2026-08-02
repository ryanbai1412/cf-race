import { check } from "./checker.js";
import { compile, CompileMode } from "./compile.js";
import { config } from "./config.js";
import { loadFullTests, loadMeta, loadSamples } from "./problems.js";
import { sandboxRun } from "./sandbox.js";
import {
  Lang,
  RunRequest,
  RunResponse,
  SubmitRequest,
  SubmitResponse,
  TestCase,
  TestResult,
  Verdict,
} from "./types.js";

/** Simple counting semaphore for the worker pool. */
class Semaphore {
  private queue: (() => void)[] = [];
  private n: number;
  constructor(n: number) {
    this.n = n;
  }
  get pending(): number {
    return this.queue.length;
  }
  async run<T>(fn: () => Promise<T>): Promise<T> {
    if (this.n <= 0) await new Promise<void>((res) => this.queue.push(res));
    else this.n--;
    try {
      return await fn();
    } finally {
      const next = this.queue.shift();
      if (next) next();
      else this.n++;
    }
  }
}

export const pool = new Semaphore(config.workers);

function truncateText(buf: Buffer): { text: string; truncated: boolean } {
  const truncated = buf.length > config.outputCapBytes;
  return {
    text: buf.subarray(0, config.outputCapBytes).toString("utf8"),
    truncated,
  };
}

async function runOneTest(
  lang: Lang,
  binPath: string | undefined,
  source: string,
  test: TestCase,
  timeLimitMs: number,
  memoryLimitMb: number,
  floatEps: number | null | undefined,
  specialJudge: boolean,
  sanitized: boolean
): Promise<TestResult> {
  const spec: Pick<Parameters<typeof sandboxRun>[0], "argv" | "files" | "env"> =
    lang === "cpp"
      ? {
          argv: ["./prog"],
          files: { prog: { fromPath: binPath! } },
          env: {
            ASAN_OPTIONS: "detect_leaks=0:exitcode=97",
            UBSAN_OPTIONS: "halt_on_error=1",
          },
        }
      : {
          argv: ["/usr/bin/python3", "-I", "main.py"],
          files: { "main.py": source },
        };

  const res = await sandboxRun({
    ...spec,
    stdin: test.input,
    timeLimitMs,
    memoryLimitMb,
    // ASan reserves terabytes of address space; the rlimit-based fallback
    // sandbox must not cap it for sanitized binaries.
    noAddressSpaceLimit: sanitized,
  });

  const out = truncateText(res.stdout);
  const err = truncateText(res.stderr);
  let verdict: Verdict;
  let checkerNote: string | undefined;
  if (res.status === "TLE") verdict = "TLE";
  else if (res.status === "ML") verdict = "ML";
  else if (res.status === "RE") verdict = "RE";
  else if (test.expected == null) verdict = "AC";
  else {
    const c = check(test.expected, out.text, floatEps);
    verdict = c.ok ? "AC" : "WA";
    checkerNote = c.note;
  }
  const result: TestResult = {
    name: test.name,
    verdict,
    timeMs: res.timeMs,
    stdout: out.text,
    stderr: err.text,
  };
  if (out.truncated) result.stdoutTruncated = true;
  if (err.truncated) result.stderrTruncated = true;
  if (checkerNote) result.checkerNote = checkerNote;
  if (specialJudge) result.checkerUnreliable = true;
  return result;
}

export async function handleRun(
  req: RunRequest,
  onUpdate?: (partial: Partial<RunResponse> & { runId: string }) => void
): Promise<RunResponse> {
  const meta = req.problemId ? loadMeta(req.problemId) : undefined;
  const timeLimitMs = req.timeLimitMs ?? meta?.timeLimitMs ?? 2000;
  const memoryLimitMb = req.memoryLimitMb ?? meta?.memoryLimitMb ?? 256;
  const tests: TestCase[] =
    req.tests ?? (req.problemId ? loadSamples(req.problemId) : []);

  const compiled = await pool.run(() => compile(req.lang, "debug", req.source));
  const compileInfo = { ok: compiled.ok, stderr: compiled.stderr };
  onUpdate?.({ runId: req.runId, compile: compileInfo });
  if (!compiled.ok) {
    return {
      runId: req.runId,
      compile: compileInfo,
      results: tests.map((t) => ({
        name: t.name,
        verdict: "SKIP" as Verdict,
        timeMs: 0,
        stdout: "",
        stderr: "",
      })),
    };
  }

  const results: TestResult[] = new Array(tests.length);
  await Promise.all(
    tests.map((t, i) =>
      pool.run(async () => {
        const r = await runOneTest(
          req.lang,
          compiled.binPath,
          req.source,
          t,
          timeLimitMs,
          memoryLimitMb,
          meta?.floatEps,
          meta?.specialJudge ?? false,
          req.lang === "cpp"
        );
        results[i] = r;
        onUpdate?.({ runId: req.runId, compile: compileInfo, results: [r] });
      })
    )
  );
  return { runId: req.runId, compile: compileInfo, results };
}

export async function handleSubmit(
  req: SubmitRequest,
  onUpdate?: (partial: SubmitResponse) => void
): Promise<SubmitResponse> {
  const meta = loadMeta(req.problemId);
  const tests = loadFullTests(req.problemId);
  const totalCount = tests.length;

  const compiled = await pool.run(() =>
    compile(req.lang, "submit" as CompileMode, req.source)
  );
  if (!compiled.ok) {
    return {
      submissionId: req.submissionId,
      verdict: "CE",
      failedTest: null,
      passedCount: 0,
      totalCount,
      timeMsMax: 0,
      compileStderr: compiled.stderr,
    };
  }

  let passedCount = 0;
  let timeMsMax = 0;
  // Sequential with short-circuit on first failure (CF convention).
  for (const t of tests) {
    const r = await pool.run(() =>
      runOneTest(
        req.lang,
        compiled.binPath,
        req.source,
        t,
        meta.timeLimitMs,
        meta.memoryLimitMb,
        meta.floatEps,
        false,
        false
      )
    );
    timeMsMax = Math.max(timeMsMax, r.timeMs);
    if (r.verdict !== "AC") {
      const resp: SubmitResponse = {
        submissionId: req.submissionId,
        verdict: r.verdict,
        failedTest: t.name,
        passedCount,
        totalCount,
        timeMsMax,
      };
      onUpdate?.(resp);
      return resp;
    }
    passedCount++;
    onUpdate?.({
      submissionId: req.submissionId,
      verdict: "AC",
      failedTest: null,
      passedCount,
      totalCount,
      timeMsMax,
    });
  }
  return {
    submissionId: req.submissionId,
    verdict: "AC",
    failedTest: null,
    passedCount,
    totalCount,
    timeMsMax,
  };
}
