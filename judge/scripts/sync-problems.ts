/**
 * Incremental sync of the `problems` bucket from Supabase Storage to
 * $PROBLEMS_DIR (default /data/problems). Requires SUPABASE_URL and
 * SUPABASE_SERVICE_ROLE_KEY. The server also runs this on a timer
 * (PROBLEM_SYNC_INTERVAL_SEC); this CLI covers boot and manual use.
 *
 * Usage: npx tsx scripts/sync-problems.ts
 */
import { syncProblems } from "../src/sync.js";

if (!process.env.SUPABASE_URL || !process.env.SUPABASE_SERVICE_ROLE_KEY) {
  console.error("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required");
  process.exit(1);
}

syncProblems()
  .then((n) => console.log(`done (${n} objects downloaded)`))
  .catch((e) => {
    console.error(e);
    process.exit(1);
  });
