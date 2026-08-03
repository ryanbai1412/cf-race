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

function readSamples(pkgDir: string): { input: string; output: string }[] {
  const dir = path.join(pkgDir, "samples");
  if (!fs.existsSync(dir)) return [];
  const samples: { input: string; output: string }[] = [];
  const ins = fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(".in"))
    .sort();
  for (const inFile of ins) {
    const outFile = inFile.replace(/\.in$/, ".out");
    if (!fs.existsSync(path.join(dir, outFile))) continue;
    samples.push({
      input: fs.readFileSync(path.join(dir, inFile), "utf8"),
      output: fs.readFileSync(path.join(dir, outFile), "utf8"),
    });
  }
  return samples;
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

  if (!dryRun) {
    for (const bucket of ["problems", "tourist"]) await ensureBucket(bucket);
  }

  for (const pkgDir of pkgs) {
    const meta = JSON.parse(
      fs.readFileSync(path.join(pkgDir, "meta.json"), "utf8")
    ) as Meta;
    const files = listFiles(pkgDir);
    console.log(`${meta.id}: ${files.length} files${dryRun ? " (dry run)" : ""}`);
    if (dryRun) continue;

    for (const file of files) {
      const rel = path.relative(pkgDir, file).split(path.sep).join("/");
      const objectPath = `${meta.id}/${rel}`;
      const contentType = rel.endsWith(".html")
        ? "text/html"
        : rel.endsWith(".json")
          ? "application/json"
          : "text/plain";
      await uploadObject(BUCKET, objectPath, fs.readFileSync(file), contentType);
    }

    const statementPath = path.join(pkgDir, "statement.html");
    const row = {
      id: meta.id,
      name: meta.name,
      rating: meta.rating,
      time_limit_ms: meta.timeLimitMs,
      memory_limit_mb: meta.memoryLimitMb,
      special_judge: meta.specialJudge,
      race_timer_sec: meta.raceTimerSec,
      tourist_time_ms: meta.touristTimeMs,
      statement_html: fs.existsSync(statementPath)
        ? fs.readFileSync(statementPath, "utf8")
        : null,
      samples: readSamples(pkgDir),
    };
    await upsertRows("problems", row);
  }

  console.log(`done: ${pkgs.length} package(s) seeded`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
