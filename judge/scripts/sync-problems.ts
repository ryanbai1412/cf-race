/**
 * Sync the `problems` bucket from Supabase Storage to $PROBLEMS_DIR
 * (default /data/problems). Requires SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY.
 *
 * Usage: npx tsx scripts/sync-problems.ts
 */
import fs from "node:fs";
import path from "node:path";

const SUPABASE_URL = process.env.SUPABASE_URL;
const KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;
const BUCKET = process.env.PROBLEMS_BUCKET ?? "problems";
const DEST = process.env.PROBLEMS_DIR ?? "/data/problems";

if (!SUPABASE_URL || !KEY) {
  console.error("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required");
  process.exit(1);
}

const headers = { apikey: KEY, authorization: `Bearer ${KEY}` };

async function list(prefix: string): Promise<{ name: string; id: string | null }[]> {
  const res = await fetch(
    `${SUPABASE_URL}/storage/v1/object/list/${BUCKET}`,
    {
      method: "POST",
      headers: { ...headers, "content-type": "application/json" },
      body: JSON.stringify({ prefix, limit: 10000, offset: 0 }),
    }
  );
  if (!res.ok) throw new Error(`list ${prefix} failed: ${res.status} ${await res.text()}`);
  return (await res.json()) as { name: string; id: string | null }[];
}

async function walk(prefix: string, out: string[]): Promise<void> {
  const entries = await list(prefix);
  for (const e of entries) {
    const full = prefix ? `${prefix}/${e.name}` : e.name;
    // Folders come back with id === null in Supabase Storage listings.
    if (e.id === null) await walk(full, out);
    else out.push(full);
  }
}

async function download(objectPath: string): Promise<void> {
  const dest = path.join(DEST, objectPath);
  await fs.promises.mkdir(path.dirname(dest), { recursive: true });
  const res = await fetch(
    `${SUPABASE_URL}/storage/v1/object/${BUCKET}/${objectPath}`,
    { headers }
  );
  if (!res.ok) throw new Error(`download ${objectPath} failed: ${res.status}`);
  await fs.promises.writeFile(dest, Buffer.from(await res.arrayBuffer()));
}

async function main() {
  const files: string[] = [];
  await walk("", files);
  console.log(`syncing ${files.length} files from bucket '${BUCKET}' to ${DEST}`);
  const CONC = 16;
  let i = 0;
  await Promise.all(
    Array.from({ length: CONC }, async () => {
      while (i < files.length) {
        const f = files[i++];
        await download(f);
      }
    })
  );
  console.log("done");
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
