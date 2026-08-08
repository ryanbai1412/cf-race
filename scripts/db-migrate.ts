/**
 * Apply supabase/migrations/*.sql to the live project and track what ran in
 * supabase_migrations.schema_migrations (the same table the Supabase CLI
 * uses), so migration state is visible and re-runs are safe.
 *
 * Usage:
 *   pnpm db:migrate               # apply unapplied migrations in order
 *   pnpm db:migrate --dry-run     # show what would run
 *   pnpm db:migrate --baseline    # mark every file applied without running
 *
 * Requires SUPABASE_ACCESS_TOKEN (Management API) and SUPABASE_PROJECT_REF
 * (or NEXT_PUBLIC_SUPABASE_URL to derive it), read from env or .env.local.
 */
import fs from "node:fs";
import path from "node:path";
import { loadDotEnvLocal } from "./env";

const ROOT = path.join(__dirname, "..");
const MIGRATIONS_DIR = path.join(ROOT, "supabase", "migrations");

function projectRef(): string {
  const explicit = process.env.SUPABASE_PROJECT_REF;
  if (explicit) return explicit;
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? "";
  const m = url.match(/^https:\/\/([a-z0-9]+)\.supabase\.co/);
  if (!m) throw new Error("set SUPABASE_PROJECT_REF or NEXT_PUBLIC_SUPABASE_URL");
  return m[1];
}

async function query(sql: string): Promise<unknown> {
  const token = process.env.SUPABASE_ACCESS_TOKEN;
  if (!token) throw new Error("SUPABASE_ACCESS_TOKEN is required");
  const res = await fetch(
    `https://api.supabase.com/v1/projects/${projectRef()}/database/query`,
    {
      method: "POST",
      headers: {
        authorization: `Bearer ${token}`,
        "content-type": "application/json",
      },
      body: JSON.stringify({ query: sql }),
    }
  );
  if (!res.ok) throw new Error(`query failed: ${res.status} ${await res.text()}`);
  return res.json();
}

const ENSURE_TABLE = `
create schema if not exists supabase_migrations;
create table if not exists supabase_migrations.schema_migrations (
  version text primary key,
  statements text[],
  name text
);
`;

async function main() {
  loadDotEnvLocal(ROOT);
  const dryRun = process.argv.includes("--dry-run");
  const baseline = process.argv.includes("--baseline");

  const files = fs
    .readdirSync(MIGRATIONS_DIR)
    .filter((f) => f.endsWith(".sql"))
    .sort();

  await query(ENSURE_TABLE);
  // Match on name, not version: some early migrations were re-timestamped
  // when they moved into the repo, so the CLI-era versions differ.
  const rows = (await query(
    "select version, name from supabase_migrations.schema_migrations"
  )) as { version: string; name: string | null }[];
  const applied = new Set(rows.map((r) => r.name ?? r.version));

  let ran = 0;
  for (const file of files) {
    const version = file.split("_")[0];
    const name = file.replace(/^\d+_/, "").replace(/\.sql$/, "");
    if (applied.has(name) || applied.has(version)) continue;
    if (dryRun) {
      console.log(`would apply ${file}`);
      continue;
    }
    if (!baseline) {
      console.log(`applying ${file} ...`);
      await query(fs.readFileSync(path.join(MIGRATIONS_DIR, file), "utf8"));
    } else {
      console.log(`baselining ${file} (marked applied, not run)`);
    }
    await query(
      `insert into supabase_migrations.schema_migrations (version, name)
       values ('${version}', '${name.replace(/'/g, "''")}')
       on conflict (version) do nothing`
    );
    ran++;
  }
  console.log(
    `${files.length} migration file(s), ${applied.size} previously applied, ${ran} ${
      baseline ? "baselined" : dryRun ? "pending" : "applied"
    }`
  );
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
