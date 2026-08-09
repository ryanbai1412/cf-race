/**
 * Diff every stored problem statement against its sanitized form, so the
 * sanitizer allowlist can be verified not to strip legitimate statement
 * markup. Reports any problem whose rendered text content changes, plus the
 * tags/attributes that were removed.
 *
 *   pnpm tsx scripts/check-statement-sanitize.ts            # local problems/
 *   pnpm tsx scripts/check-statement-sanitize.ts --remote   # Supabase rows
 */
import fs from "node:fs";
import path from "node:path";
import { JSDOM } from "jsdom";
import { sanitizeStatementHtml } from "../src/lib/statement-html";

type Statement = { id: string; html: string };

function localStatements(): Statement[] {
  const dir = path.join(process.cwd(), "problems");
  return fs
    .readdirSync(dir)
    .flatMap((id) => {
      const file = path.join(dir, id, "statement.html");
      return fs.existsSync(file)
        ? [{ id, html: fs.readFileSync(file, "utf8") }]
        : [];
    });
}

async function remoteStatements(): Promise<Statement[]> {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) throw new Error("Supabase env vars are required for --remote");
  const res = await fetch(
    `${url}/rest/v1/problems?select=id,statement_html&order=id.asc`,
    { headers: { apikey: key, Authorization: `Bearer ${key}` } }
  );
  if (!res.ok) throw new Error(`problems fetch failed: ${res.status}`);
  const rows = (await res.json()) as { id: string; statement_html: string | null }[];
  return rows.flatMap((r) => (r.statement_html ? [{ id: r.id, html: r.statement_html }] : []));
}

/** Normalized visible text, so whitespace/attribute noise isn't flagged. */
function textOf(html: string): string {
  const { document } = new JSDOM(`<body>${html}</body>`).window;
  return (document.body.textContent ?? "").replace(/\s+/g, " ").trim();
}

function shapeOf(html: string): { tags: Map<string, number>; attrs: Map<string, number> } {
  const { document } = new JSDOM(`<body>${html}</body>`).window;
  const tags = new Map<string, number>();
  const attrs = new Map<string, number>();
  for (const el of Array.from(document.body.querySelectorAll("*"))) {
    const tag = el.tagName.toLowerCase();
    tags.set(tag, (tags.get(tag) ?? 0) + 1);
    for (const a of Array.from(el.attributes)) {
      const k = `${tag}[${a.name}]`;
      attrs.set(k, (attrs.get(k) ?? 0) + 1);
    }
  }
  return { tags, attrs };
}

function lost(before: Map<string, number>, after: Map<string, number>): string[] {
  const out: string[] = [];
  for (const [k, n] of before) {
    const m = after.get(k) ?? 0;
    if (m < n) out.push(`${k} ${n}\u2192${m}`);
  }
  return out;
}

async function main() {
  const statements = process.argv.includes("--remote")
    ? await remoteStatements()
    : localStatements();

  let textChanged = 0;
  const removedTags = new Map<string, number>();
  const removedAttrs = new Map<string, number>();

  for (const s of statements) {
    const clean = sanitizeStatementHtml(s.html);
    if (textOf(s.html) !== textOf(clean)) {
      textChanged++;
      console.log(`TEXT CHANGED: ${s.id}`);
    }
    const a = shapeOf(s.html);
    const b = shapeOf(clean);
    for (const entry of lost(a.tags, b.tags)) {
      const name = entry.split(" ")[0];
      removedTags.set(name, (removedTags.get(name) ?? 0) + 1);
      console.log(`  ${s.id}: tag ${entry}`);
    }
    for (const entry of lost(a.attrs, b.attrs)) {
      const name = entry.split(" ")[0];
      removedAttrs.set(name, (removedAttrs.get(name) ?? 0) + 1);
      console.log(`  ${s.id}: attr ${entry}`);
    }
  }

  console.log(
    `\nchecked ${statements.length} statements; ${textChanged} with changed text`
  );
  console.log("tags removed:", Object.fromEntries(removedTags));
  console.log("attrs removed:", Object.fromEntries(removedAttrs));
  if (textChanged > 0) process.exitCode = 1;
}

void main();
