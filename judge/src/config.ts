import os from "node:os";

export const config = {
  port: Number(process.env.PORT ?? 8080),
  judgeToken: process.env.JUDGE_TOKEN ?? "",
  problemsDir: process.env.PROBLEMS_DIR ?? "/data/problems",
  cacheDir: process.env.CACHE_DIR ?? "/tmp/judge-cache",
  // "isolate" (cgroup v2), "isolate-nocg" (isolate with rlimits only, for
  // hosts without cgroup v2 controllers; multi-process runs like compiles
  // fall back to plain subprocesses), or "none" (dev fallback, plain
  // subprocesses — NOT safe for untrusted code).
  sandbox: (process.env.JUDGE_SANDBOX ?? "isolate") as
    | "isolate"
    | "isolate-nocg"
    | "none",
  workers: Number(process.env.JUDGE_WORKERS ?? os.cpus().length),
  outputCapBytes: Number(process.env.OUTPUT_CAP_BYTES ?? 64 * 1024),
  // How much of a program's stdout is captured for checking (display is
  // truncated to outputCapBytes). Must comfortably exceed the largest
  // legitimate answer, otherwise correct big outputs would be judged WA.
  captureCapBytes: Number(process.env.CAPTURE_CAP_BYTES ?? 16 * 1024 * 1024),
};

if (!config.judgeToken) {
  console.warn("WARNING: JUDGE_TOKEN is not set; all requests will be rejected");
}
