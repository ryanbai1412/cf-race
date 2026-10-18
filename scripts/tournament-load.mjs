#!/usr/bin/env node
// Load test for GET /api/tournament/state.
//
// Creates a throwaway tournament (service role), joins N clients through
// POST /api/tournament/join, optionally starts it, then has every client poll
// the state route like the room page does (one request in flight, ~3s +-20%
// between polls). Prints latency percentiles and error rate, and REST calls
// per poll when the server runs with scripts/count-supabase-fetches.cjs.
// The tournament and its game sessions are deleted at the end (or on Ctrl-C);
// rows go to whatever Supabase project the env points at.
//
//   BASE_URL=http://localhost:3100 node scripts/tournament-load.mjs \
//     --clients 100 --duration 300 --start [--rest-count-dir /tmp/rest-counts]
//
// Needs NEXT_PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY. Against a
// deployed URL the join rate limit (per IP) kicks in; members past it are
// inserted directly with their own tokens, which polls the same way.
import { createHash, randomBytes, randomInt } from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

const { values: args } = parseArgs({
  options: {
    clients: { type: "string", default: "100" },
    duration: { type: "string", default: "300" },
    interval: { type: "string", default: "3000" },
    start: { type: "boolean", default: false },
    "rest-count-dir": { type: "string" },
    "report-every": { type: "string", default: "30" },
    "allow-prod-site": { type: "boolean", default: false },
  },
});

const BASE_URL = (process.env.BASE_URL ?? "http://localhost:3100").replace(/\/$/, "");
if (/(^|\.)cfrace\.com$/.test(new URL(BASE_URL).hostname) && !args["allow-prod-site"]) {
  console.error(`refusing to load-test ${BASE_URL} without --allow-prod-site`);
  process.exit(1);
}
const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const SERVICE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;
if (!SUPABASE_URL || !SERVICE_KEY) {
  console.error("NEXT_PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required");
  process.exit(1);
}
const CLIENTS = Number(args.clients);
const DURATION_MS = Number(args.duration) * 1000;
const INTERVAL_MS = Number(args.interval);
const MAX_PARTICIPANTS = 64;
const CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
const CODE_LENGTH = 6;

async function rest(method, pathAndQuery, body) {
  const res = await fetch(`${SUPABASE_URL}/rest/v1/${pathAndQuery}`, {
    method,
    headers: {
      apikey: SERVICE_KEY,
      Authorization: `Bearer ${SERVICE_KEY}`,
      "Content-Type": "application/json",
      Prefer: "return=representation",
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`${method} ${pathAndQuery}: ${res.status} ${text}`);
  return text ? JSON.parse(text) : null;
}

function mintToken() {
  const token = randomBytes(24).toString("base64url");
  return { token, hash: createHash("sha256").update(token).digest("hex") };
}

const fakeIp = (i) => `10.${(i >> 16) & 255}.${(i >> 8) & 255}.${i & 255}`;

function readRestCounts() {
  const dir = args["rest-count-dir"];
  if (!dir || !fs.existsSync(dir)) return null;
  const total = { rest: 0, auth: 0, byPath: {} };
  for (const f of fs.readdirSync(dir)) {
    if (!f.endsWith(".json")) continue;
    try {
      const c = JSON.parse(fs.readFileSync(path.join(dir, f), "utf8"));
      total.rest += c.rest;
      total.auth += c.auth;
      for (const [k, v] of Object.entries(c.byPath)) total.byPath[k] = (total.byPath[k] ?? 0) + v;
    } catch {
      // A file mid-write; the next read picks it up.
    }
  }
  return total;
}

function pct(sorted, p) {
  if (!sorted.length) return 0;
  return sorted[Math.min(sorted.length - 1, Math.floor((p / 100) * sorted.length))];
}

function summarize(samples, elapsedMs) {
  const lat = samples.map((s) => s.ms).sort((a, b) => a - b);
  const errors = samples.filter((s) => s.status !== 200);
  const byStatus = {};
  for (const s of samples) byStatus[s.status] = (byStatus[s.status] ?? 0) + 1;
  return {
    polls: samples.length,
    rps: +(samples.length / (elapsedMs / 1000)).toFixed(1),
    p50: Math.round(pct(lat, 50)),
    p95: Math.round(pct(lat, 95)),
    p99: Math.round(pct(lat, 99)),
    max: Math.round(lat[lat.length - 1] ?? 0),
    errorRate: samples.length ? +((errors.length / samples.length) * 100).toFixed(2) : 0,
    byStatus,
  };
}

let tournamentId = null;
let cleaned = false;
async function cleanup() {
  if (cleaned || !tournamentId) return;
  cleaned = true;
  const games = await rest("GET", `tournament_games?select=session_a,session_b&tournament_id=eq.${tournamentId}`);
  const sessionIds = games.flatMap((g) => [g.session_a, g.session_b]).filter(Boolean);
  await rest("DELETE", `tournaments?id=eq.${tournamentId}`);
  if (sessionIds.length) await rest("DELETE", `sessions?id=in.(${sessionIds.join(",")})&kind=eq.tournament`);
  console.log(`cleaned up tournament ${tournamentId} and ${sessionIds.length} sessions`);
}
process.on("SIGINT", () =>
  cleanup()
    .catch((e) => console.error(`cleanup failed; delete tournament ${tournamentId} by hand`, e))
    .finally(() => process.exit(130))
);

async function main() {
  let code = "";
  for (let i = 0; i < CODE_LENGTH; i++) code += CODE_ALPHABET[randomInt(CODE_ALPHABET.length)];
  const [t] = await rest("POST", "tournaments", { code, name: `Load test ${new Date().toISOString()}` });
  tournamentId = t.id;
  const owner = mintToken();
  await rest("POST", "tournament_members", {
    tournament_id: t.id,
    token_hash: owner.hash,
    name: "Load host",
    role: "participant",
    is_admin: true,
    is_owner: true,
  });
  console.log(`tournament ${code} (${t.id}) at ${BASE_URL}`);

  const clients = [{ cookie: `cfr_tm_${t.id}=${owner.token}`, ip: fakeIp(1) }];
  let direct = 0;
  for (let i = 1; i < CLIENTS; i++) {
    const name = `load-${i}`;
    const role = i < MAX_PARTICIPANTS ? "participant" : "spectator";
    const ip = fakeIp(i + 1);
    const res = await fetch(`${BASE_URL}/api/tournament/join`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-Forwarded-For": ip },
      body: JSON.stringify({ code, name, role }),
    });
    const setCookie = res.headers.get("set-cookie") ?? "";
    const match = setCookie.match(new RegExp(`cfr_tm_${t.id}=([^;]+)`));
    if (res.ok && match) {
      clients.push({ cookie: `cfr_tm_${t.id}=${match[1]}`, ip });
      continue;
    }
    if (res.status !== 429) throw new Error(`join ${name}: ${res.status} ${await res.text()}`);
    const m = mintToken();
    await rest("POST", "tournament_members", { tournament_id: t.id, token_hash: m.hash, name, role });
    clients.push({ cookie: `cfr_tm_${t.id}=${m.token}`, ip });
    direct++;
  }
  console.log(`${clients.length} clients joined (${direct} inserted directly after a 429)`);

  if (args.start) {
    const res = await fetch(`${BASE_URL}/api/tournament/admin`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Cookie: clients[0].cookie },
      body: JSON.stringify({ code, action: "start" }),
    });
    console.log(`start: ${res.status} ${await res.text()}`);
  }

  const before = readRestCounts();
  const samples = [];
  const startedAt = Date.now();
  const deadline = startedAt + DURATION_MS;
  let windowStart = startedAt;
  let windowFrom = 0;
  const reporter = setInterval(() => {
    const now = Date.now();
    const s = summarize(samples.slice(windowFrom), now - windowStart);
    console.log(`[${Math.round((now - startedAt) / 1000)}s] ${JSON.stringify(s)}`);
    windowFrom = samples.length;
    windowStart = now;
  }, Number(args["report-every"]) * 1000);

  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  await Promise.all(
    clients.map(async (c) => {
      await sleep(randomInt(INTERVAL_MS));
      while (Date.now() < deadline) {
        const t0 = performance.now();
        let status = 0;
        try {
          const res = await fetch(`${BASE_URL}/api/tournament/state?code=${code}`, {
            headers: { Cookie: c.cookie, "X-Forwarded-For": c.ip },
            signal: AbortSignal.timeout(15_000),
          });
          status = res.status;
          await res.arrayBuffer();
        } catch {
          status = -1;
        }
        samples.push({ ms: performance.now() - t0, status });
        await sleep(INTERVAL_MS * (0.8 + Math.random() * 0.4));
      }
    })
  );
  clearInterval(reporter);

  const elapsed = Date.now() - startedAt;
  const result = { clients: clients.length, durationSec: Math.round(elapsed / 1000), ...summarize(samples, elapsed) };
  const after = readRestCounts();
  if (before && after) {
    const rest = after.rest - before.rest;
    result.restCalls = rest;
    result.restPerPoll = +(rest / Math.max(1, samples.length)).toFixed(3);
    result.restPerSec = +(rest / (elapsed / 1000)).toFixed(2);
    result.authCalls = after.auth - before.auth;
    const byPath = {};
    for (const [k, v] of Object.entries(after.byPath)) {
      const d = v - (before.byPath[k] ?? 0);
      if (d) byPath[k] = d;
    }
    result.restByPath = byPath;
  }
  console.log(`RESULT ${JSON.stringify(result, null, 2)}`);
}


main()
  .catch((e) => {
    console.error(e);
    process.exitCode = 1;
  })
  .finally(() =>
    cleanup().catch((e) => console.error(`cleanup failed; delete tournament ${tournamentId} by hand`, e))
  );
