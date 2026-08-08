# Architecture proposals — round 2 (2026-08-08)

Follow-ups after the universal-sessions migration, DB invariants, shared
judge protocol, and the new test/ownership work. Ordered by expected value.

## 1. Move problem test packages out of git

`problems/` is already 231 MB across 399 problems and every pipeline batch
adds more (~40 batch commits landed today alone). Git history keeps every
version forever, so the repo (`.git` is 69 MB packed and growing) will get
slow to clone and CI-hostile.

Supabase Storage is already the runtime source of truth — `pnpm seed`
uploads packages and the judge syncs them to its disk. Git only needs what
humans edit/review:

- Keep in git: `meta.json`, `statement.html`, `samples/` (small, reviewable).
- Move out of git: `tests/` (the bulk). Pipeline uploads them straight to
  Storage; a manifest (problem id → content hash, test count) is committed
  so changes are still reviewable and the judge can verify integrity.
- One-time history rewrite is optional; even without it, stopping the
  growth now is the main win.

Alternative: git-lfs for `problems/*/tests/**`. Less moving parts, but adds
LFS quota/cost and the judge still pulls from Storage anyway, so the
manifest approach removes duplication.

## 2. Atomic first-AC / winner stamping (Postgres RPC)

Event submit does read-check → conditional `race_participants` update →
`sessions` update → confetti notify as four separate calls; duel submit
similarly stamps `first_ac_at`/`winner_user_id` then calls `resolveMatch`.
The conditional `.is(..., null)` updates prevent double-stamping, but the
side effects (session outcome, notify) can still fire when the stamp lost
the race, and a crash between calls leaves half-applied state.

Proposal: one `plpgsql` function per mode, e.g.
`record_event_ac(session_id, race_id, contestant_id, solve_ms)` /
`record_duel_ac(session_id, match_id, user_id, solve_ms)`, doing the stamp +
session update in a single transaction and returning whether this AC was
the first. The route then only fires confetti/notify when the RPC says so.

## 3. Track applied migrations

Migrations in `supabase/migrations/` are applied ad hoc via the Management
API; nothing records what has run against the live DB, so drift is invisible
and re-running relies on every migration being hand-written idempotent.

Proposal: adopt the Supabase CLI flow (`supabase migration up` /
`supabase db push`), which maintains `supabase_migrations.schema_migrations`
in the database. Add a `make db-migrate` target and note it in
docs/OVERVIEW.md. No schema change needed — the CLI can baseline the
existing files.

## 4. Stop swallowing write errors on hot paths

Several important writes ignore their errors: the submit/verdict
`session_events` inserts in all three submit routes, the first-AC
`sessions`/`race_participants` updates, and `resolveMatch` internals. A
failed insert silently produces a replay with no submit marker.

Proposal: a tiny `logDbError(context, error)` helper (console.error → shows
up in Vercel logs) applied to fire-and-forget writes, and propagate (500)
where the write is essential to the response. Cheap, mechanical, and makes
live incidents diagnosable.

## 5. Codify the e2e flows as a Playwright suite

Today's manual e2e pass (event race, replay, backfilled replay, solo, duel,
DB invariants) is exactly the golden-path set worth automating. The testing
skill already documents the setup (dev server env, device links, judge on
Fly, duel test users). A Playwright project with those five specs, run
against a local dev server + live judge in CI (or a nightly job), would
catch regressions in the session pipeline that unit tests can't — the
replay/recording plumbing spans browser APIs, routes, and Postgres.
