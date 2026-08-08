# Architecture proposals — round 3 (2026-08-08)

Round 2 items 1, 3, 4 shipped; the atomic first-AC RPC (item 2) also shipped
(`record_event_ac` / `record_duel_ac`). New decisions needed:

## 1. Implement PRD v2 session lifecycle (recommended next)

The `20260809010000_unified_app` migration already added `session_shares`,
`sessions.last_event_at` (+ bump trigger, now batched), and
`events.created_by` — but no app code uses them yet. Implementing the PRD's
core lifecycle is now unblocked:

- **15-min abandonment**: lazy flip `active → abandoned` on any read that
  sees `last_event_at < now() - 15min`, in `requireSessionAccess` /
  `buildSessionReplay`, plus a small `pg_cron` sweep.
- **Private replays + share tokens**: `/api/solo/replay` (and the future
  `/replay/<id>` page) currently serves any session by UUID. Gate it on
  owner / anonymous-cookie / duel-opponent / event-cookie per PRD §5.3, and
  add mint-share-token + `/r/<token>` public reads against `session_shares`.
- **Anonymous session claim**: cookie holds anonymous session ids; signing in
  stamps `user_id` on them (endpoint exists as `/api/solo/claim` — extend to
  the cookie flow).

Each is small on its own; together they complete the PRD's auth model.
Decision: should I start on these, or is another session already building the
unified app UI (in which case I'll stay on backend/cleanup)?

## 2. Playwright e2e suite (carried over from round 2)

Golden paths (solo run → replay, duel, event race) are currently verified
manually per release. A headless Playwright suite against a local dev server
+ live Supabase test rows would make regressions cheap to catch. Medium
effort. Decision: worth it now, or after the PRD v2 UI churn settles?

## 3. Storage-side manifest verification in CI

`problems/tests-manifest.json` hashes local test packages, but nothing
verifies the Storage bucket matches the manifest. A small CI/pipeline step
(`pnpm tests:verify`) that HEADs each package in the bucket and compares
hashes would catch drift between git's manifest and Storage's truth.
Low effort.
