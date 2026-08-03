/** Shared helpers for repo scripts: .env.local loading + Supabase env. */
import fs from "node:fs";
import path from "node:path";

/** Load KEY=value pairs from .env.local (if present) into process.env. */
export function loadDotEnvLocal(root: string): void {
  const file = path.join(root, ".env.local");
  if (!fs.existsSync(file)) return;
  for (const line of fs.readFileSync(file, "utf8").split("\n")) {
    const m = line.match(/^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$/);
    if (!m || line.trim().startsWith("#")) continue;
    const [, key, raw] = m;
    if (process.env[key] !== undefined) continue;
    process.env[key] = raw.replace(/^["']|["']$/g, "");
  }
}

export function supabaseEnv(): { url: string; serviceKey: string } {
  const url = process.env.SUPABASE_URL ?? process.env.NEXT_PUBLIC_SUPABASE_URL;
  const serviceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !serviceKey) {
    console.error(
      "Missing NEXT_PUBLIC_SUPABASE_URL (or SUPABASE_URL) and/or SUPABASE_SERVICE_ROLE_KEY.\n" +
        "Set them in .env.local (see .env.example)."
    );
    process.exit(1);
  }
  return { url, serviceKey };
}
