/**
 * Seed Supabase from local problem packages (see docs/JUDGE_API.md):
 *   - uploads every package under problems/ to the `problems` Storage bucket
 *     (the judge syncs from there on boot);
 *   - upserts the corresponding rows in the `problems` table from
 *     meta.json + statement.html + samples/.
 *
 * Usage:
 *   pnpm seed                 # seed everything under problems/
 *   pnpm seed --only 2024A    # a single package (also dev/aplusb etc.)
 *   pnpm seed --dry-run       # show what would happen without writing
 *
 * Requires NEXT_PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY
 * (read from the environment or .env.local).
 */
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { loadDotEnvLocal } from "./env";
import { ensureBucket, uploadObject, upsertRows } from "./supabase";

const ROOT = path.join(__dirname, "..");
const PROBLEMS_DIR = path.join(ROOT, "problems");
const BUCKET = "problems";

type Meta = {
  id: string;
  name: string;
  rating: number | null;
  timeLimitMs: number;
  memoryLimitMb: number;
  multiTest: boolean;
  specialJudge: boolean;
  floatEps: number | null;
  raceTimerSec: number;
  touristTimeMs: number | null;
  tags?: string[];
};

function findPackages(dir: string, out: string[] = []): string[] {
  if (fs.existsSync(path.join(dir, "meta.json"))) {
    out.push(dir);
    return out;
  }
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.isDirectory()) findPackages(path.join(dir, e.name), out);
  }
  return out;
}

function listFiles(dir: string, out: string[] = []): string[] {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) listFiles(p, out);
    else out.push(p);
  }
  return out;
}

async function main() {
  loadDotEnvLocal(ROOT);
  const only = process.argv.includes("--only")
    ? process.argv[process.argv.indexOf("--only") + 1]
    : null;
  const dryRun = process.argv.includes("--dry-run");

  let pkgs = findPackages(PROBLEMS_DIR);
  if (only) {
    pkgs = pkgs.filter(
      (p) => path.relative(PROBLEMS_DIR, p).split(path.sep).join("/") === only
    );
    if (pkgs.length === 0) {
      console.error(`no package '${only}' under problems/`);
      process.exit(1);
    }
  }

  const gates = pkgs.map((pkgDir) => JSON.parse(execFileSync("python3", [
    path.join(ROOT, "pipeline", "pool_contract.py"), pkgDir,
    ...(dryRun ? ["--dry-run"] : []),
  ], { encoding: "utf8" })) as {
    legacy: boolean;
    files?: Record<string, { sha256: string; bytes: number }>;
  });
  const snapshots = pkgs.map((pkgDir, i) => {
    const files = listFiles(pkgDir).map((file) => ({
      rel: path.relative(pkgDir, file).split(path.sep).join("/"),
      data: fs.readFileSync(file),
    }));
    const gate = gates[i];
    if (!gate.legacy) {
      if (files.length !== Object.keys(gate.files!).length) throw new Error("changed package file set");
      for (const file of files) {
        const expected = gate.files![file.rel];
        if (!expected || file.data.length !== expected.bytes ||
            createHash("sha256").update(file.data).digest("hex") !== expected.sha256) {
          throw new Error(`changed approved bytes: ${file.rel}`);
        }
      }
    }
    return files;
  });

  if (!dryRun) {
    for (const bucket of ["problems", "tourist"]) await ensureBucket(bucket);
  }

  for (const [i] of pkgs.entries()) {
    const snapshot = snapshots[i];
    const meta = JSON.parse(
      snapshot.find((f) => f.rel === "meta.json")!.data.toString("utf8")
    ) as Meta;
    const files = snapshot;
    console.log(`${meta.id}: ${files.length} files${dryRun ? " (dry run)" : ""}`);
    if (dryRun) continue;

    for (const file of files) {
      const rel = file.rel;
      const objectPath = `${meta.id}/${rel}`;
      const contentType = rel.endsWith(".html")
        ? "text/html"
        : rel.endsWith(".json")
          ? "application/json"
          : "text/plain";
      await uploadObject(BUCKET, objectPath, file.data, contentType);
    }

    const row = {
      id: meta.id,
      name: meta.name,
      rating: meta.rating,
      time_limit_ms: meta.timeLimitMs,
      memory_limit_mb: meta.memoryLimitMb,
      special_judge: meta.specialJudge,
      multi_test: meta.multiTest,
      float_eps: meta.floatEps,
      race_timer_sec: meta.raceTimerSec,
      tourist_time_ms: meta.touristTimeMs,
      statement_html: snapshot.find((f) => f.rel === "statement.html")?.data.toString("utf8") ?? null,
      samples: snapshot.filter((f) => /^samples\/.*\.in$/.test(f.rel)).map((f) => ({
        input: f.data.toString("utf8"),
        output: snapshot.find((o) => o.rel === f.rel.replace(/\.in$/, ".out"))!.data.toString("utf8"),
      })),
    };
    await upsertRows("problems", row);
  }

  console.log(`done: ${pkgs.length} package(s) seeded`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
