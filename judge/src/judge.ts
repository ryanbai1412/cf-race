import fs from "node:fs";
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
  TestResult,
  Verdict,
} from "./types.js";

/** A test either inline (wire requests) or on disk (problem packages). */
interface JudgeTest {
  name: string;
  input?: string;
  inputPath?: string;
  expected?: string | null;
  expectedPath?: string | null;
}

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
  test: JudgeTest,
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
    stdinFile: test.inputPath,
    timeLimitMs,
    memoryLimitMb,
    // ASan reserves terabytes of address space; the rlimit-based fallback
    // sandbox must not cap it for sanitized binaries.
    noAddressSpaceLimit: sanitized,
  });

  // A sandbox failure says nothing about the submitted program; surface it as
  // a judge error instead of grading it as RE.
  if (res.internalError) throw new Error(`sandbox failed on ${test.name}: ${res.internalError}`);

  const out = truncateText(res.stdout);
  const err = truncateText(res.stderr);
  let verdict: Verdict;
  let checkerNote: string | undefined;
  const expected =
    test.expected !== undefined
      ? test.expected
      : test.expectedPath
        ? await fs.promises.readFile(test.expectedPath, "utf8")
        : null;
  if (res.status === "TLE") verdict = "TLE";
  else if (res.status === "ML") verdict = "ML";
  else if (res.status === "RE") verdict = "RE";
  else if (expected == null) verdict = "AC";
  else if (res.stdoutCapped) {
    verdict = "WA";
    checkerNote = `output exceeded ${Math.round(config.captureCapBytes / (1024 * 1024))}MB and could not be checked`;
  } else {
    // Check against the full captured output — out.text is truncated for
    // display and would turn large correct outputs into WA.
    const c = check(expected, res.stdout.toString("utf8"), floatEps);
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
  const meta = req.problemId ? await loadMeta(req.problemId) : undefined;
  const timeLimitMs = req.timeLimitMs ?? meta?.timeLimitMs ?? 2000;
  const memoryLimitMb = req.memoryLimitMb ?? meta?.memoryLimitMb ?? 256;
  const tests: JudgeTest[] =
    req.tests ?? (req.problemId ? await loadSamples(req.problemId) : []);

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
  prewarmSubmitBinary(req.lang, req.source);
  return { runId: req.runId, compile: compileInfo, results };
}

/**
 * Build the -O2 binary for this exact source in the background, so a submit of
 * unchanged code hits the compile cache instead of paying ~600ms mid-race.
 * Queued behind the sample runs and deduplicated by `compile`'s cache.
 */
function prewarmSubmitBinary(lang: Lang, source: string): void {
  if (lang !== "cpp") return;
  void pool
    .run(() => compile(lang, "submit", source))
    .catch((e) => console.error("submit prewarm failed:", e));
}

export async function handleSubmit(
  req: SubmitRequest,
  onUpdate?: (partial: SubmitResponse) => void
): Promise<SubmitResponse> {
  const meta = await loadMeta(req.problemId);
  const tests = await loadFullTests(req.problemId);
  const totalCount = tests.length;

  // Nothing to judge against (package not synced to this machine yet, or its
  // tests/ is empty): fail closed rather than reporting a free AC.
  if (totalCount === 0) {
    return internalError(
      req.submissionId,
      `no tests available for ${req.problemId}`
    );
  }

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

  // Tests run concurrently (bounded by the worker pool), but the reported
  // verdict is the one of the lowest-indexed failing test, so results match
  // sequential CF-style judging. Tests queued after that failure is known are
  // skipped.
  const results: (TestResult | undefined)[] = new Array(tests.length);
  let firstFailure = Number.POSITIVE_INFINITY;
  let passedCount = 0;

  /** Number of leading tests that finished AC, for monotonic progress. */
  function acPrefix(): number {
    let n = 0;
    while (n < results.length && results[n]?.verdict === "AC") n++;
    return n;
  }

  await Promise.all(
    tests.map((t, i) =>
      pool.run(async () => {
        if (i > firstFailure) return;
        const r = await runOneTest(
          req.lang,
          compiled.binPath,
          req.source,
          t,
          meta.timeLimitMs,
          meta.memoryLimitMb,
          meta.floatEps,
          false,
          false
        );
        results[i] = r;
        if (r.verdict !== "AC") firstFailure = Math.min(firstFailure, i);
        const prefix = acPrefix();
        if (prefix > passedCount) {
          passedCount = prefix;
          onUpdate?.({
            submissionId: req.submissionId,
            verdict: "AC",
            failedTest: null,
            passedCount,
            totalCount,
            timeMsMax: maxTimeMs(results, firstFailure),
          });
        }
      })
    )
  );

  passedCount = acPrefix();
  const timeMsMax = maxTimeMs(results, firstFailure);
  const failed = Number.isFinite(firstFailure) ? results[firstFailure] : undefined;
  const resp: SubmitResponse = failed
    ? {
        submissionId: req.submissionId,
        // Judging never yields SKIP here, but the per-test type allows it.
        verdict: failed.verdict === "SKIP" ? "RE" : failed.verdict,
        failedTest: failed.name,
        passedCount,
        totalCount,
        timeMsMax,
      }
    : {
        submissionId: req.submissionId,
        verdict: "AC",
        failedTest: null,
        passedCount,
        totalCount,
        timeMsMax,
      };
  if (failed) onUpdate?.(resp);
  return resp;
}

/**
 * The verdict for "the judge could not decide": an unjudged submission must
 * never look like an AC (or a WA) to the app.
 */
export function internalError(
  submissionId: string,
  note: string
): SubmitResponse {
  return {
    submissionId,
    verdict: "IE",
    failedTest: null,
    passedCount: 0,
    totalCount: 0,
    timeMsMax: 0,
    compileStderr: note,
  };
}

/** Max runtime over the tests a sequential judge would have executed. */
function maxTimeMs(
  results: (TestResult | undefined)[],
  firstFailure: number
): number {
  let max = 0;
  for (let i = 0; i < results.length && i <= firstFailure; i++) {
    const r = results[i];
    if (r) max = Math.max(max, r.timeMs);
  }
  return max;
}
