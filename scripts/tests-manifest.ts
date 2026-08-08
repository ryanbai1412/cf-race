/**
 * Regenerate problems/tests-manifest.json from the local problems/ tree.
 *
 * Test packages (problems/<id>/tests/) are gitignored — Supabase Storage is
 * their source of truth (docs/OVERVIEW.md). This manifest is what git tracks
 * instead: one entry per problem with a file count and a content hash, so
 * test changes still show up in review and the judge sync can be verified.
 *
 * Run after generating/uploading tests:
 *   pnpm tests:manifest
 */
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const ROOT = path.join(__dirname, "..");
const PROBLEMS_DIR = path.join(ROOT, "problems");
const MANIFEST = path.join(PROBLEMS_DIR, "tests-manifest.json");

type Entry = { files: number; bytes: number; sha256: string };

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

function hashTests(testsDir: string): Entry {
  const files = fs.readdirSync(testsDir).sort();
  const hash = crypto.createHash("sha256");
  let bytes = 0;
  for (const f of files) {
    const buf = fs.readFileSync(path.join(testsDir, f));
    bytes += buf.length;
    hash.update(f);
    hash.update("\0");
    hash.update(buf);
    hash.update("\0");
  }
  return { files: files.length, bytes, sha256: hash.digest("hex") };
}

function main() {
  const existing: Record<string, Entry> = fs.existsSync(MANIFEST)
    ? (JSON.parse(fs.readFileSync(MANIFEST, "utf8")) as Record<string, Entry>)
    : {};
  const manifest: Record<string, Entry> = {};
  let hashed = 0;
  let kept = 0;

  for (const pkgDir of findPackages(PROBLEMS_DIR).sort()) {
    const id = path.relative(PROBLEMS_DIR, pkgDir).split(path.sep).join("/");
    const testsDir = path.join(pkgDir, "tests");
    if (fs.existsSync(testsDir) && fs.readdirSync(testsDir).length > 0) {
      manifest[id] = hashTests(testsDir);
      hashed++;
    } else if (existing[id]) {
      // Tests only live in Storage on this machine — keep the known entry.
      manifest[id] = existing[id];
      kept++;
    }
  }

  fs.writeFileSync(MANIFEST, JSON.stringify(manifest, null, 2) + "\n");
  console.log(
    `wrote ${MANIFEST}: ${Object.keys(manifest).length} entries ` +
      `(${hashed} hashed locally, ${kept} kept from previous manifest)`
  );
}

main();
