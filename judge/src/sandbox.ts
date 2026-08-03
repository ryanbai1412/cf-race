import { spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { config } from "./config.js";

export interface ExecSpec {
  /** argv to execute inside the box (paths relative to the box dir). */
  argv: string[];
  /** Files to place in the working dir before running: name -> content/path. */
  files?: Record<string, string | { fromPath: string }>;
  stdin?: string;
  timeLimitMs: number;
  memoryLimitMb: number;
  wallTimeMs?: number;
  /** max processes (compilers need more than 1) */
  procs?: number;
  /** extra size for fsize in KB */
  fsizeKb?: number;
  /** Extra host directories to bind read-only into the sandbox. */
  dirs?: string[];
  /** skip the address-space rlimit in non-cg mode (needed for ASan binaries) */
  noAddressSpaceLimit?: boolean;
  env?: Record<string, string>;
}

export type ExecStatus = "OK" | "TLE" | "ML" | "RE";

export interface ExecResult {
  status: ExecStatus;
  exitCode: number;
  timeMs: number;
  stdout: Buffer;
  stderr: Buffer;
  /** stdout hit the capture cap, so it is incomplete even for checking */
  stdoutCapped?: boolean;
  /** copy a file out of the box after the run (set via outFiles) */
  outFiles?: Record<string, Buffer>;
}

export interface RunOptions {
  /** file names (relative to box) to copy out after a successful run */
  collect?: string[];
}

function spawnCollect(
  cmd: string,
  args: string[],
  opts: { stdin?: string; cwd?: string; killAfterMs?: number; env?: NodeJS.ProcessEnv }
): Promise<{
  code: number | null;
  signal: string | null;
  stdout: Buffer;
  stderr: Buffer;
  stdoutCapped: boolean;
}> {
  return new Promise((resolve, reject) => {
    const child = spawn(cmd, args, {
      cwd: opts.cwd,
      env: opts.env ?? process.env,
      stdio: ["pipe", "pipe", "pipe"],
    });
    const out: Buffer[] = [];
    const err: Buffer[] = [];
    let outLen = 0;
    let errLen = 0;
    let outCapped = false;
    // stdout must be kept in full for the checker; stderr is display-only.
    const outCap = config.captureCapBytes;
    const errCap = config.outputCapBytes * 4;
    child.stdout.on("data", (d: Buffer) => {
      if (outLen < outCap) {
        out.push(d);
        outLen += d.length;
      } else {
        outCapped = true;
      }
    });
    child.stderr.on("data", (d: Buffer) => {
      if (errLen < errCap) {
        err.push(d);
        errLen += d.length;
      }
    });
    let killed = false;
    let timer: NodeJS.Timeout | undefined;
    if (opts.killAfterMs) {
      timer = setTimeout(() => {
        killed = true;
        child.kill("SIGKILL");
      }, opts.killAfterMs);
    }
    child.on("error", (e) => {
      if (timer) clearTimeout(timer);
      reject(e);
    });
    child.on("close", (code, signal) => {
      if (timer) clearTimeout(timer);
      resolve({
        code: killed && code === null ? null : code,
        signal,
        stdout: Buffer.concat(out),
        stderr: Buffer.concat(err).subarray(0, errCap),
        stdoutCapped: outCapped,
      });
    });
    if (opts.stdin !== undefined) child.stdin.write(opts.stdin);
    child.stdin.end();
  });
}

/** Pool of isolate box ids. */
class BoxPool {
  private free: number[] = [];
  private waiters: ((id: number) => void)[] = [];
  constructor(n: number) {
    for (let i = 0; i < n; i++) this.free.push(i);
  }
  acquire(): Promise<number> {
    const id = this.free.pop();
    if (id !== undefined) return Promise.resolve(id);
    return new Promise((res) => this.waiters.push(res));
  }
  release(id: number) {
    const w = this.waiters.shift();
    if (w) w(id);
    else this.free.push(id);
  }
}

const boxPool = new BoxPool(Math.max(config.workers * 2, 4));

// isolate --init instances race on mounting the shared tmpfs at
// /var/local/lib/isolate ("Unexpected mountpoint" errors); serialize them.
let initChain: Promise<unknown> = Promise.resolve();
function serializedInit(args: string[]) {
  const p = initChain.then(() => spawnCollect("isolate", args, {}));
  initChain = p.catch(() => {});
  return p;
}

async function placeFiles(dir: string, files?: ExecSpec["files"]) {
  if (!files) return;
  for (const [name, content] of Object.entries(files)) {
    const dest = path.join(dir, name);
    if (typeof content === "string") {
      await fs.promises.writeFile(dest, content);
    } else {
      await fs.promises.copyFile(content.fromPath, dest);
    }
    await fs.promises.chmod(dest, 0o755);
  }
}

function parseIsolateMeta(metaPath: string): Record<string, string> {
  const out: Record<string, string> = {};
  try {
    for (const line of fs.readFileSync(metaPath, "utf8").split("\n")) {
      const i = line.indexOf(":");
      if (i > 0) out[line.slice(0, i)] = line.slice(i + 1);
    }
  } catch {
    /* meta may be missing on hard failures */
  }
  return out;
}

async function runIsolate(
  spec: ExecSpec,
  opts: RunOptions,
  cg: boolean
): Promise<ExecResult> {
  const boxId = await boxPool.acquire();
  const metaPath = path.join(os.tmpdir(), `isolate-meta-${boxId}-${Date.now()}`);
  const cgArgs = cg ? ["--cg"] : [];
  try {
    let init = await serializedInit([...cgArgs, "-b", String(boxId), "--init"]);
    if (init.code !== 0) {
      // A crashed previous run can leave the box dirty; clean and retry once.
      await spawnCollect("isolate", [...cgArgs, "-b", String(boxId), "--cleanup"], {});
      init = await serializedInit([...cgArgs, "-b", String(boxId), "--init"]);
      if (init.code !== 0) {
        throw new Error(`isolate --init failed: ${init.stderr.toString()}`);
      }
    }
    const boxDir = init.stdout.toString().trim() + "/box";
    await placeFiles(boxDir, spec.files);

    const timeSec = spec.timeLimitMs / 1000;
    const wallSec = (spec.wallTimeMs ?? spec.timeLimitMs * 2 + 2000) / 1000;
    const args = [
      ...cgArgs,
      "-b",
      String(boxId),
      "-M",
      metaPath,
      "-t",
      timeSec.toFixed(3),
      "-w",
      wallSec.toFixed(3),
      "-x",
      "0.5", // extra time so we can distinguish TLE cleanly
      "-f",
      String(spec.fsizeKb ?? 16384),
      "-E",
      "PATH=/usr/local/bin:/usr/bin:/bin",
      "-E",
      "HOME=/box",
      "-s",
    ];
    if (cg) {
      args.push("--cg-mem", String(spec.memoryLimitMb * 1024));
      args.push("-p" + String(spec.procs ?? 1));
    } else if (!spec.noAddressSpaceLimit) {
      args.push("-m", String(spec.memoryLimitMb * 1024));
    }
    for (const d of spec.dirs ?? []) args.push(`--dir=${d}=${d}`);
    for (const [k, v] of Object.entries(spec.env ?? {})) args.push("-E", `${k}=${v}`);
    args.push("--run", "--", ...spec.argv);

    const res = await spawnCollect("isolate", args, { stdin: spec.stdin ?? "" });
    const meta = parseIsolateMeta(metaPath);
    const timeMs = Math.round(Number(meta["time"] ?? 0) * 1000);
    let status: ExecStatus = "OK";
    if (meta["status"] === "TO") status = "TLE";
    else if (meta["status"] === "SG" || meta["status"] === "RE") {
      status =
        meta["cg-oom-killed"] === "1" || /oom/i.test(meta["message"] ?? "")
          ? "ML"
          : "RE";
    } else if (meta["status"] === "XX") status = "RE";
    else if (Number(meta["time"] ?? 0) * 1000 > spec.timeLimitMs) status = "TLE";

    const outFiles: Record<string, Buffer> = {};
    if (opts.collect && status === "OK") {
      for (const f of opts.collect) {
        const p = path.join(boxDir, f);
        if (fs.existsSync(p)) outFiles[f] = await fs.promises.readFile(p);
      }
    }
    return {
      status,
      exitCode: Number(meta["exitcode"] ?? res.code ?? 0),
      timeMs,
      stdout: res.stdout,
      stderr: res.stderr,
      stdoutCapped: res.stdoutCapped,
      outFiles,
    };
  } finally {
    spawnCollect("isolate", [...cgArgs, "-b", String(boxId), "--cleanup"], {}).finally(
      () => boxPool.release(boxId)
    );
    fs.promises.unlink(metaPath).catch(() => {});
  }
}

/** Dev fallback: plain subprocess with a wall-clock kill. NOT a real sandbox. */
async function runPlain(spec: ExecSpec, opts: RunOptions): Promise<ExecResult> {
  const dir = await fs.promises.mkdtemp(path.join(os.tmpdir(), "judge-run-"));
  try {
    await placeFiles(dir, spec.files);
    const start = process.hrtime.bigint();
    const res = await spawnCollect(spec.argv[0], spec.argv.slice(1), {
      stdin: spec.stdin ?? "",
      cwd: dir,
      killAfterMs: spec.wallTimeMs ?? spec.timeLimitMs * 2 + 2000,
      env: { ...process.env, ...spec.env },
    });
    const timeMs = Number(process.hrtime.bigint() - start) / 1e6;
    let status: ExecStatus = "OK";
    if (res.code === null || timeMs > spec.timeLimitMs) status = "TLE";
    else if (res.code !== 0) status = "RE";
    const outFiles: Record<string, Buffer> = {};
    if (opts.collect && status === "OK") {
      for (const f of opts.collect) {
        const p = path.join(dir, f);
        if (fs.existsSync(p)) outFiles[f] = await fs.promises.readFile(p);
      }
    }
    return {
      status,
      exitCode: res.code ?? -1,
      timeMs: Math.round(timeMs),
      stdout: res.stdout,
      stderr: res.stderr,
      stdoutCapped: res.stdoutCapped,
      outFiles,
    };
  } finally {
    fs.promises.rm(dir, { recursive: true, force: true }).catch(() => {});
  }
}

export function sandboxRun(spec: ExecSpec, opts: RunOptions = {}): Promise<ExecResult> {
  if (config.sandbox === "isolate") return runIsolate(spec, opts, true);
  if (config.sandbox === "isolate-nocg") {
    // Non-cg isolate can't host multi-process runs (compilers); those run as
    // trusted-ish plain subprocesses instead.
    if ((spec.procs ?? 1) > 1) return runPlain(spec, opts);
    return runIsolate(spec, opts, false);
  }
  return runPlain(spec, opts);
}
