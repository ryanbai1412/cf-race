# Architecture proposals — round 4 (post-PRD-11 review)

Context: reviewed the PRD 11 code that landed on main (session lifecycle,
replay privacy + share tokens, anon sessions, app shell, problems bank).
Three concrete bugs found in that code are already fixed and pushed
(`/api/duel/review` privacy hole, solo-run supersede abandoning duel/event
sessions, share-token mint race). The items below are structural questions
that need a call from you.

## 1. Centralize replay/review authorization into one policy module

Today access rules live in three places with different semantics:
- `replay-access.ts` (`canViewSession`) — owner / anon cookie / duel
  participant / event cookie, used by `/api/solo/replay`;
- `/api/shares` has its own inline `authorize()` (owner or match
  participant), subtly stricter (no anon-cookie sharing);
- `/api/duel/review` now has its own participant check (added this pass).

Proposal: one `access.ts` with `canViewSession`, `canViewMatch`,
`canShareSession`, `canShareMatch`, and routes only call these. Any future
surface (exports, embeds, admin) reuses the same policy, and a privacy bug
like the duel-review hole can't reappear by forgetting a check.
Cost: small refactor, no behavior change.

## 2. Make lifecycle transitions explicit instead of lazy writes on reads

`sweepStaleSessions` runs an UPDATE inside GET handlers and page renders
(`/sessions`, `/api/solo/history`, `/api/duel/home`, replay loads). It works,
but: reads now have write side effects (harder caching, surprising load
patterns), each read pays a DB round trip, and coverage is accidental — a
session nobody reads stays "active" forever.

Proposal: keep the lazy flip as a cheap correctness backstop but move the
real work to `pg_cron` (Supabase supports it) running the same one-statement
sweep every minute. Reads become pure again and abandonment happens on time
even when nobody is looking. The PRD itself suggests this ("plus a periodic
sweep via pg_cron if available").

## 3. Anonymous-claim flow: cookie is the only record

Anonymous sessions are claimable solely via the `cfr_anon_sessions` cookie
(capped at 50 ids, 1-year expiry). Clearing cookies loses the runs forever;
nothing on the server records which browser created a session. That's
probably acceptable for practice runs, but if you want durable anon→account
claiming later (e.g. device link codes), we'd need a server-side
`browser_id` on sessions now — retrofitting is impossible once cookies are
gone. Decision needed: accept cookie-only (status quo) or add a persistent
browser id column while the data is still young.

## 4. Judge problem sync is boot-only — make it incremental

The judge syncs the whole `problems` bucket only at boot
(`sync-problems.ts`), so newly seeded problems 404 on `/run`/`/submit` until
someone restarts the Fly machines (hit this again today: both machines had a
week-old package set; a restart re-syncs 9.8k files and takes several
minutes of downtime for that machine). Proposal: judge re-checks the
manifest on a timer (e.g. every 5 min) and downloads only missing/changed
packages by hash — no restarts, no full re-downloads, new problems usable
within minutes. Medium effort, all inside `judge/`.

## 5. Route-level duplication in the new API surface

Small cleanups I can do without a decision, listed for visibility:
- `/api/shares` GET/POST share a table/column-picking pattern that belongs
  in a `shares.ts` service next to the other domain modules;
- `/r/[token]` page queries both share tables inline; same service.
I'll fold these in with #1 if you approve it.
