/**
 * Upload a tourist event log (src/lib/tourist.ts TouristLog JSON) to the
 * `tourist` Storage bucket as <problemId>.json, and update the problem's
 * tourist_time_ms from the log's solveMs.
 *
 * Usage:
 *   pnpm seed:tourist <problemId> <path/to/log.json>
 *   pnpm seed:tourist 2024A recordings/2024A.json
 *
 * Requires NEXT_PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY
 * (read from the environment or .env.local).
 */
import fs from "node:fs";
import path from "node:path";
import { loadDotEnvLocal } from "./env";
import { updateRows, uploadObject } from "./supabase";

async function main() {
  const [problemId, file] = process.argv.slice(2);
  if (!problemId || !file) {
    console.error("usage: pnpm seed:tourist <problemId> <log.json>");
    process.exit(1);
  }
  loadDotEnvLocal(path.join(__dirname, ".."));
  const raw = fs.readFileSync(file, "utf8");
  const log = JSON.parse(raw) as {
    problemId?: string;
    solveMs?: number;
    events?: unknown[];
  };
  if (!Array.isArray(log.events) || typeof log.solveMs !== "number") {
    console.error("log must be a TouristLog JSON with 'events' and 'solveMs'");
    process.exit(1);
  }
  if (log.problemId && log.problemId !== problemId) {
    console.error(
      `log.problemId is '${log.problemId}' but uploading as '${problemId}'`
    );
    process.exit(1);
  }

  await uploadObject("tourist", `${problemId}.json`, raw, "application/json");
  await updateRows("problems", `id=eq.${encodeURIComponent(problemId)}`, {
    tourist_time_ms: log.solveMs,
  });

  console.log(
    `uploaded tourist/${problemId}.json (${log.events.length} events, solveMs=${log.solveMs})`
  );
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
