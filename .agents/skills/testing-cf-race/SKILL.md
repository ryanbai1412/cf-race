---
name: testing-cf-race
description: How to run and end-to-end test the cf-race booth app locally (dev server env vars, device links, judge on Fly, Supabase problems bucket, replay data tables).
---

# Testing the cf-race booth app

## Run locally
- Next.js app at repo root, pnpm. Start with: `pnpm exec next dev -p 3100` and env vars
  `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`,
  `NEXT_PUBLIC_LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`,
  `JUDGE_URL=https://cf-race-judge.fly.dev`, `JUDGE_TOKEN`.
- Vercel prod may be behind SSO; test against localhost.
- pnpm must be v10 (`packageManager: pnpm@10.18.3`): pnpm 9 fails on `pnpm-workspace.yaml`'s
  `minimumReleaseAge` key with "ERROR packages field missing or empty". Use
  `COREPACK_INTEGRITY_KEYS=0 corepack pnpm@10.18.3 install`, then run
  `./node_modules/.bin/next dev -p 3100` directly. Run the dev server in a persistent/tty
  shell — one-shot backgrounded shells may get reaped and the server silently dies.
- Beware Next.js fetch caching of supabase-js GETs in API routes (`.next/cache/fetch-cache/`):
  a route can keep returning stale data (e.g. empty `/api/solo/submissions`) even with
  `dynamic = "force-dynamic"`. If an API returns stale/empty data that the DB clearly has,
  restart the dev server (or clear `.next/cache/fetch-cache`) before concluding it's a bug
  in the change under test.

## Navigation / auth model
- Landing `/` → "Create event" → `/e/<eventId>/admin`.
- Device links are `/e/<id>/join?k=<secret>&to=/station/1|/station/2|/monitor/a|/monitor/b|/admin`; the join route sets an httpOnly cookie with path `/`, so after joining once in a browser you can navigate directly to `/e/<id>/station/2`, `/e/<id>/monitor/a`, etc. in other tabs — no need to copy each link.
- Simulate the booth with multiple tabs: admin, station 1, station 2, monitor A.

## Test data
- Reference AC solutions: `pipeline/problems/<id>/ref.py` (e.g. 2024A). Paste via clipboard (`xclip -selection clipboard`, then Ctrl+A/Ctrl+V in Monaco) — typing Python by keystrokes breaks due to Monaco auto-indent.
- Wrong answer: submit `print(0)`.
- Admin race control: pick problem, set Timer seconds (default 180 — use 600 to have time for all checks), "Start race (5s countdown)".

## Judge (Fly) gotchas
- Judge syncs problem packages from the Supabase Storage bucket `problems` **on boot only**. If a problem exists in the DB `problems` table but not in the bucket, runs fail with `judge /run failed: 404` (judge ENOENT on `/data/problems/<id>/meta.json`). `warmup-sum` was missing this way once.
- Fix: upload `<id>/meta.json` + `<id>/tests/01.in|01.out` to the bucket (service-role key via storage REST API), then `flyctl machine restart <ids> -a cf-race-judge` (needs FLY_API_TOKEN; install flyctl via `curl -sL https://fly.io/install.sh | sh`).
- Direct judge check: `POST $JUDGE_URL/run` with `Authorization: Bearer $JUDGE_TOKEN`.

## Replay data
- Editor snapshots go to table `race_editor_events` via `POST /api/replay` (flushed every 5 s from stations). If replays play back empty, check that table. Races intentionally stay in `state="countdown"` in the DB; the recorder in `src/components/station/station-client.tsx` arms whenever the race has `started_at` and `state !== "finished"` (fixed after an earlier bug that required `state === "running"`).
- To verify recording during a test: type/edit code during the race, wait >5 s for the flush, then query the table. Direct `psql` to `db.<ref>.supabase.co:5432` may fail (IPv6-only DNS, unreachable from some boxes) — use the Supabase REST API instead: `curl "$SUPABASE_URL/rest/v1/race_editor_events?race_id=eq.<raceId>&select=station_role,t_ms,lang,code" -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY"`.

## Devin Secrets Needed
`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `NEXT_PUBLIC_LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, `JUDGE_TOKEN`, `FLY_API_TOKEN`.

## Webcam
- Webcam publishing needs a camera; in a VM launch Chrome fresh with `--use-fake-ui-for-media-stream --use-fake-device-for-media-stream` **before** any Chrome instance is running, else the pane renders black.
- Webcam **recording** (solo runs + event races) uploads webm to the private Storage bucket `recordings` via `POST /api/recordings` (`?sessionId=` for solo, `?eventId=&raceId=&station=` for races); replay APIs return a 1-h signed `recordingUrl` + `recordingOffsetMs`. Without a camera everything still works — recording is skipped.

## Solo practice mode
- `/solo` (list) → `/solo/<problemId>` (3-min run) → `/solo/replay/<sessionId>`. No auth/cookies needed.
- API smoke test without a browser: `POST /api/solo/session {problemId}` → `POST /api/solo/events {sessionId, events:[{t,code,lang}]}` (a `kind:"run"` event = run-samples marker) → `POST /api/solo/submit {sessionId, lang, source}` (use `pipeline/problems/<id>/ref.py` for AC) → `GET /api/solo/replay?sessionId=`.
- History/replay links live in localStorage key `cfr-solo-history`; active run in sessionStorage `cfr-solo-active`.

## pnpm gotcha
- If `pnpm` fails with a corepack "Cannot find matching keyid" signature error, run with `COREPACK_INTEGRITY_KEYS=0` exported.
