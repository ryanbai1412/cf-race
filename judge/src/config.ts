import os from "node:os";

export const config = {
  port: Number(process.env.PORT ?? 8080),
  judgeToken: process.env.JUDGE_TOKEN ?? "",
  problemsDir: process.env.PROBLEMS_DIR ?? "/data/problems",
  cacheDir: process.env.CACHE_DIR ?? "/tmp/judge-cache",
  // "isolate" (production, requires ioi/isolate) or "none" (dev fallback,
  // plain subprocesses with rlimits — NOT safe for untrusted code).
  sandbox: (process.env.JUDGE_SANDBOX ?? "isolate") as "isolate" | "none",
  workers: Number(process.env.JUDGE_WORKERS ?? os.cpus().length),
  outputCapBytes: Number(process.env.OUTPUT_CAP_BYTES ?? 64 * 1024),
};

if (!config.judgeToken) {
  console.warn("WARNING: JUDGE_TOKEN is not set; all requests will be rejected");
}
