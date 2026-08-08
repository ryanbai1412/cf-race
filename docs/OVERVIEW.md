# cf-race — Architecture & Data Model Overview

A competitive-programming race platform: two contestants race head-to-head on a
Codeforces-style problem at a live event, with spectator monitors, webcam feeds,
a "tourist" ghost replay, and a single-player solo practice mode. This doc
describes the system as built (see `docs/ARCHITECTURE.md` for the original
design plan and `docs/flows/` for per-screen UX flows).

## System components

```
Browser clients                     Vercel (Next.js app)              External services
┌─────────────────┐   HTTPS   ┌──────────────────────────┐   ┌──────────────────────────┐
│ Station 1 / 2   │──────────▶│ src/app/  (pages + API   │──▶│ Supabase                 │
│ Monitor A / B   │           │ route handlers, service- │   │  Postgres (data)         │
│ Admin console   │           │ role Supabase client)    │   │  Storage (tests, webcam, │
│ /solo player    │           └───────────┬──────────────┘   │   tourist logs)          │
└───────┬─────────┘                       │ HTTPS+token      │  Realtime (broadcast)    │
        │  Supabase Realtime             ▼                  │  Auth (Google, solo)     │
        │  (state_changed, editor,  ┌──────────────┐        └──────────────────────────┘
        │   confetti broadcasts)    │ Judge service │        ┌──────────────────────────┐
        └─────────────────────────▶ │ (Fly.io VM,   │        │ LiveKit Cloud (webcam    │
           LiveKit WebRTC           │ judge/, isolate│        │  publish + view)         │
                                    │ sandbox)      │        └──────────────────────────┘
                                    └──────────────┘
```

### Web app (`src/`)
Next.js 14 App Router + TypeScript + Tailwind/shadcn, Monaco editor.

- **Pages** (`src/app/`):
  - `/e/[eventId]/station/[n]` — contestant station: check-in → warm-up sandbox
    → countdown → race screen → finish screen.
  - `/e/[eventId]/monitor/[m]` — spectator monitors: live editor mirrors,
    webcams, tourist ghost playback, leaderboard.
  - `/e/[eventId]/admin` — organizer console: start/finish races, pick
    problems, manage contestants.
  - `/e/[eventId]/replay/[raceId]/[station]` — race replay (editor + webcam).
  - `/solo`, `/solo/[problemId]`, `/solo/replay/[sessionId]` — solo practice.
- **API route handlers** (`src/app/api/`): all data access goes through these;
  browsers never talk to Postgres directly. They use a service-role Supabase
  client (`src/lib/db.ts`), so Postgres RLS does not apply to them — access
  control is enforced in the handlers.
- **Shared server libs** (`src/lib/`): `event-auth.ts` (event secret / cookie
  auth), `judge.ts` (judge HTTP client), `run-route.ts` + `submission-route.ts`
  (shared run/submit lifecycle), `editor-events.ts` (replay event
  sanitization + reconstruction), `limits.ts` (shared request limits),
  `tourist.ts` (replay event types + player).
- **Client hooks/components**: `use-event-state` (poll `/api/state` + realtime
  refetch), `use-replay-recorder` (per-keystroke recording + periodic flush),
  `race-screen.tsx` (the editor/run/submit UI shared by races, warm-up, and
  solo), `replay-player.tsx` (synced editor + webcam playback).

### Judge service (`judge/`)
A standalone Node/TypeScript HTTP service on a dedicated VM (Fly.io app
`cf-race-judge`), authenticated with a bearer token (`JUDGE_TOKEN`).

- `POST /run` — compile + run against sample tests or custom input; returns
  per-test stdout/stderr/verdicts (used for the editor's "Run" button).
- `POST /submit` — compile + run against the full hidden test set; returns a
  single verdict (`AC/WA/TLE/RE/ML/CE`) with pass counts.
- Sandboxing: `isolate` (IOI sandbox, cgroups) in production; `JUDGE_SANDBOX=none`
  subprocess mode for local dev. A `BoxPool` manages concurrent sandbox ids and
  a semaphore caps parallel executions.
- C++ is compiled with a SHA-256 source-keyed binary cache; debug mode
  (`-O1` + ASan/UBSan) for runs, `-O2` for submissions. Python runs directly.
- Checker: token-based comparator (whitespace-insensitive, float epsilon,
  YES/NO case-insensitive); `special_judge` problems flag results as
  potentially unreliable rather than shipping per-problem checkers.
- Test data lives on the VM disk, synced from the Supabase Storage `problems`
  bucket via `judge/scripts/sync-problems.ts`.

### Problem pipeline (`pipeline/`, `problems/`, `scripts/`)
Offline tooling that scrapes/generates problem statements and test data into
`problems/<id>/` packages, then seeds them into Supabase (`pnpm seed`) and onto
the judge VM. `scripts/upload-tourist.ts` uploads tourist ghost replay logs.

CF test packages (`problems/<id>/tests/`) are gitignored — Supabase Storage is
their source of truth. Git tracks `problems/tests-manifest.json` instead (file
count + content hash per problem, regenerated with `pnpm tests:manifest` after
uploading new tests). Dev fixtures under `problems/dev/` keep their tests in
git for local judge work.

## Runtime data flows

- **Event auth**: every event URL carries `?k=<secret>`; the join page sets an
  httpOnly cookie (`cfr_<eventId>`), and every event API call re-validates it
  (constant-time compare) against `events.secret`.
- **State sync**: clients poll `GET /api/state` (event, active contestants,
  active race + participants, `serverNow` for clock offset). A Supabase
  Realtime broadcast channel `event:<eventId>` carries `state_changed`
  (refetch), `editor` (debounced code mirror for monitors), `confetti`, and
  `request_editor` messages. Timers are server-authoritative: clients render
  offsets from `serverNow`, and the server re-checks deadlines on submit.
- **Race lifecycle**: admin starts a race → row in `races` with
  `state=countdown` and `started_at` a few seconds in the future; participants
  snapshot the currently checked-in contestants, and each participant gets a
  universal `sessions` row (`kind='event'`) that carries its replay stream,
  submissions, and webcam recording. `/api/state` lazily flips countdown →
  running. First `AC` sets `race_participants.first_ac_at`; finishing the race
  DQs unsolved participants and retires contestants back to check-in. A
  partial unique index guarantees at most one unfinished race per event.
- **Run vs submit**: "Run samples"/custom input goes to `/api/judge/run` (or
  `/api/solo/run`) → judge `/run`, no persistence. "Submit" goes to
  `/api/submit` (or `/api/solo/submit`) → inserts a `PENDING` row in
  `session_submissions`, judges on full tests, records the verdict; caps are
  50 submissions per session, 10 for duels (`src/lib/limits.ts`), enforced
  atomically by a Postgres trigger (`session_submission_cap`).
- **Replay recording**: the station/solo client records every keystroke as
  editor deltas with periodic full-code keyframes, plus run / run-result /
  console-tab / statement-scroll markers, and flushes batches every 5s to
  `/api/replay` or `/api/solo/events`. Webcam video is recorded locally
  (MediaRecorder) and uploaded to Storage when the run ends, with a clock
  offset so replays sync video to the editor timeline.
- **Replay playback**: `/api/replay` (GET) / `/api/solo/replay` rebuild a
  normalized event timeline (snapshots, deltas, runs, verdicts, tab/scroll)
  from the DB plus signed Storage URLs for the video; `replay-player.tsx`
  plays both in lockstep. Solved solo runs can be promoted to the tourist
  ghost for a problem (`/api/solo/promote`).
- **Solo practice**: sessions are anonymous by default (the session UUID is
  the capability); Google sign-in lets a user claim their anonymous sessions
  (`/api/solo/claim`) and read their history via RLS.

## Data model (Supabase Postgres)

Base tables (`supabase/schema.sql`-era) plus migrations in
`supabase/migrations/`:

```
events                          problems
  id uuid PK                      id text PK          (e.g. "1794C")
  name text                       name text
  secret text                     rating int?
  settings jsonb                  time_limit_ms int
  created_at                      memory_limit_mb int
                                  special_judge bool
contestants                       race_timer_sec int
  id uuid PK                      tourist_time_ms int?
  event_id → events               statement_html text?
  station_role 'station1|2'       samples jsonb [{input,output}]
  name, country
  retired_at timestamptz?      ── "active" contestant per station =
                                  most recent non-retired row

races                           race_participants
  id uuid PK                      race_id → races
  event_id → events               contestant_id → contestants
  problem_id → problems           station_role
  state waiting|countdown|        first_ac_at timestamptz?
        running|finished          dq bool
  started_at timestamptz?
  timer_sec int

```

`race_participants.session_id` links each participant to a universal session.

All modes (solo, duel, event) share the universal session tables:

```
sessions                        session_events        session_submissions
  id uuid PK (capability)         session_id → sessions (cascade)
  kind solo|duel|event            t_ms, code, lang      kind run|submit
  problem_id → problems           kind snapshot|delta|  lang, source
  user_id → auth.users?                run|run_result|  verdict? (PENDING→…)
  lang cpp|py?                         tab|scroll|      details jsonb
  started_at, timer_sec                submit|verdict   submitted_at,
  solve_ms int?                   payload jsonb?        judged_at
  outcome solved|timeout|abandoned
  recording_path, recording_offset_ms
```

The legacy `submissions`, `race_editor_events`, `race_recordings`, and
`solo_*` tables are frozen archives — backfilled into the universal tables by
migrations, no longer written.

RLS is enabled everywhere; the app's service-role client bypasses it, and the
only anon/authenticated policy is `solo_sessions_select_own` (signed-in users
reading their own history). Storage holds problem test data, webcam
recordings, and tourist replay logs.

## Environment variables

| Variable | Used by | Purpose |
|---|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` / `NEXT_PUBLIC_SUPABASE_ANON_KEY` | app (client+server) | Supabase project + realtime/auth |
| `SUPABASE_SERVICE_ROLE_KEY` | app (server only) | service-role DB/Storage access |
| `JUDGE_URL` / `JUDGE_TOKEN` | app (server only) | judge service endpoint + bearer token |
| `LIVEKIT_API_KEY` / `LIVEKIT_API_SECRET` / `NEXT_PUBLIC_LIVEKIT_URL` | app | webcam publish/view tokens |
| `JUDGE_TOKEN`, `JUDGE_SANDBOX`, `PROBLEMS_DIR`, … | judge | see `judge/src/config.ts` |

## Dev commands

`make setup` (prereqs + `.env.local` + deps), `make dev` (web app),
`make judge-dev` (local judge, no sandbox), `make check`
(lint + typecheck + build), `make judge-test`, `make seed`, `make smoke`.
