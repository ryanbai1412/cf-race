/** Minimal fetch-based Supabase Storage + PostgREST helpers for repo scripts
 *  (no supabase-js: its realtime client needs Node 22's native WebSocket). */
import { supabaseEnv } from "./env";

function base(): { url: string; headers: Record<string, string> } {
  const { url, serviceKey } = supabaseEnv();
  return { url, headers: { apikey: serviceKey, authorization: `Bearer ${serviceKey}` } };
}

export async function ensureBucket(name: string): Promise<void> {
  const { url, headers } = base();
  const res = await fetch(`${url}/storage/v1/bucket`, {
    method: "POST",
    headers: { ...headers, "content-type": "application/json" },
    body: JSON.stringify({ id: name, name, public: false }),
  });
  if (!res.ok) {
    const text = await res.text();
    if (!/already exists/i.test(text)) throw new Error(`create bucket ${name}: ${res.status} ${text}`);
  }
}

export async function uploadObject(
  bucket: string,
  objectPath: string,
  body: Buffer | string,
  contentType: string
): Promise<void> {
  const { url, headers } = base();
  const res = await fetch(`${url}/storage/v1/object/${bucket}/${objectPath}`, {
    method: "POST",
    headers: { ...headers, "content-type": contentType, "x-upsert": "true" },
    body: typeof body === "string" ? body : new Uint8Array(body),
  });
  if (!res.ok) throw new Error(`upload ${bucket}/${objectPath}: ${res.status} ${await res.text()}`);
}

export async function upsertRows(table: string, rows: unknown): Promise<void> {
  const { url, headers } = base();
  const res = await fetch(`${url}/rest/v1/${table}`, {
    method: "POST",
    headers: {
      ...headers,
      "content-type": "application/json",
      prefer: "resolution=merge-duplicates",
    },
    body: JSON.stringify(rows),
  });
  if (!res.ok) throw new Error(`upsert ${table}: ${res.status} ${await res.text()}`);
}

export async function updateRows(
  table: string,
  filter: string,
  patch: unknown
): Promise<void> {
  const { url, headers } = base();
  const res = await fetch(`${url}/rest/v1/${table}?${filter}`, {
    method: "PATCH",
    headers: { ...headers, "content-type": "application/json" },
    body: JSON.stringify(patch),
  });
  if (!res.ok) throw new Error(`update ${table}: ${res.status} ${await res.text()}`);
}
