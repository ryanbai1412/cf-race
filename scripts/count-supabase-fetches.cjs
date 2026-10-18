// Preload for load tests: counts this process's fetches to Supabase REST
// (PostgREST) and Auth, and writes the totals to
// $SUPABASE_FETCH_COUNT_DIR/<pid>.json once a second.
//
//   SUPABASE_FETCH_COUNT_DIR=/tmp/rest-counts \
//   NODE_OPTIONS="--require ./scripts/count-supabase-fetches.cjs" pnpm start
const fs = require("node:fs");
const path = require("node:path");

const dir = process.env.SUPABASE_FETCH_COUNT_DIR;
const base = process.env.NEXT_PUBLIC_SUPABASE_URL;
if (dir && base && typeof globalThis.fetch === "function") {
  fs.mkdirSync(dir, { recursive: true });
  const counts = { rest: 0, auth: 0, other: 0, byPath: {} };
  const original = globalThis.fetch;
  globalThis.fetch = function countedFetch(input, init) {
    const url = typeof input === "string" ? input : input instanceof URL ? input.href : input.url;
    if (url.startsWith(base)) {
      const { pathname } = new URL(url);
      const kind = pathname.startsWith("/rest/") ? "rest" : pathname.startsWith("/auth/") ? "auth" : "other";
      counts[kind] += 1;
      const key = `${(init && init.method) || "GET"} ${pathname}`;
      counts.byPath[key] = (counts.byPath[key] || 0) + 1;
    }
    return original.call(this, input, init);
  };
  const file = path.join(dir, `${process.pid}.json`);
  setInterval(() => fs.writeFileSync(file, JSON.stringify(counts)), 1000).unref();
}
