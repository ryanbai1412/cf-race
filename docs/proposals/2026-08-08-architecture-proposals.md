# Architecture proposals (2026-08-08)

Higher-order changes worth discussing before more features land. Ordered by
expected payoff. None of these are started — this is a review doc.

## 1. Finish the "universal sessions" migration; fold event races in

The `sessions` / `session_events` / `session_submissions` tables (added for
duel mode) already model exactly what event races store in the older
`races` / `race_editor_events` / `submissions` tables. Today the codebase has
two parallel stacks:

| Concern            | Event races                      | Solo + duel            |
|--------------------|----------------------------------|------------------------|
| Playback stream    | `race_editor_events`             | `session_events`       |
| Submissions        | `submissions`                    | `session_submissions`  |
| Replay assembly    | `/api/replay` (custom)           | `src/lib/session-log.ts` |
| Recordings         | `race_recordings` table          | `sessions.recording_path` |

Proposal: give each race participant a `sessions` row (`kind='event'` — the
enum already allows it) and delete the race-specific tables and the
`/api/replay` assembly path. One recording/replay/submission code path for
every mode, and future modes (team relay, lockout, etc.) come for free.
This is the direction docs/flows/09 already states; the remaining work is a
data migration for the event-race tables plus updating `/api/submit`,
`/api/state`, and the replay routes.

## 2. Split route handlers from domain logic

API routes increasingly mix HTTP parsing/authz with business rules (e.g.
`duel/ready` builds matches, `duel/state` lazily resolves matches). Proposal:
keep `src/app/api/**` as thin parse→authorize→call→serialize wrappers and move
match lifecycle, race lifecycle, and session lifecycle into `src/lib/`
services (duel.ts is already halfway there). This makes the invariants
(time windows, submission caps, first-AC-wins) unit-testable without HTTP.

## 3. Server-enforced concurrency invariants in Postgres

Several invariants are enforced by read-then-write sequences that race under
concurrency:

- one active race per event (`/api/race/start` checks then inserts),
- submission caps (count then insert — two simultaneous submits can exceed
  the cap),
- first AC / winner stamping (partially guarded with `.is(null)` filters).

Proposal: enforce in the database — partial unique index for "one unfinished
race per event", a `check_submission_cap` trigger or an RPC that counts and
inserts in one statement, and rely on the existing conditional-update guards
for winner stamping. Low effort, removes a whole class of heisenbugs.

## 4. Move judging to an async queue

`/api/submit` (and duel/solo submit) hold an HTTP request open for the full
judge run (`maxDuration = 120`). Under load this ties up serverless function
time and duplicates "pending row + verdict update + failure cleanup" logic in
every route. Proposal: insert the submission, return immediately, have the
judge (or a small worker) update the verdict, and let clients get the verdict
via the Realtime subscription they already hold for state changes. This also
makes retries/idempotency natural (the judge already accepts a
`submissionId`).

## 5. Shared types package for the judge wire contract

`src/lib/judge.ts` (web) and `judge/src/server.ts` each declare the
run/submit request+response shapes; they can drift silently. Now that the
repo is a single pnpm workspace, proposal: a tiny `packages/judge-protocol`
(types only) imported by both sides.

## 6. Testing gap

The judge has good tests; the web app has none — the trickiest logic
(time windows, grace periods, match resolution, replay event assembly) is
exactly what regressed most easily during recent refactors. Proposal: start
with pure-function tests for `src/lib/` (duel matchEndMs/resolveMatch,
editor-events sanitize/build, submission caps) using vitest, which is already
in the workspace via the judge.

## Smaller notes

- `/api/solo/*` is now really "session API" shared by solo + duel (duel
  routes re-export the handlers). Consider renaming to `/api/session/*` with
  the duel aliases kept for compatibility.
- `sessions` rows are capability-addressed (unguessable UUID grants access).
  Fine for now, but if session IDs ever leak into URLs/analytics, reads of
  code + webcam URLs leak with them. Worth an explicit decision.
- `problems/` packages in git make the repo heavy (tests are large text
  files). If it keeps growing, move test data to Supabase Storage only and
  keep just statements/manifests in git.
