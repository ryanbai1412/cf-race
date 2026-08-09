---
name: testing-cf-race
description: How to run and end-to-end test the cf-race booth app locally (dev server env vars, device links, judge on Fly, Supabase problems bucket, replay data tables).
---

# Testing the cf-race booth app

## Unified app shell (PRD 11) — testing without Google login
- Google OAuth is not possible in the test browser; the shell is still very testable logged-out:
  landing `/` (CTAs "Sign in with Google" + "Just practice"), anonymous solo runs at
  `/problems/<id>/solve`, `/replay/<sessionId>` (anon access via httpOnly cookie
  `cfr_anon_sessions` set by POST `/api/solo/session`), public shares `/r/<token>`.
- Auth-gated pages redirect logged-out: `/problems` → `/?next=/problems` (same for
  /sessions, /duels, /events). Legacy 308s: `/solo`→`/problems`,
  `/solo/<id>`→`/problems/<id>/solve`, `/solo/replay/<id>`→`/replay/<id>`, `/duel`→`/duels`.
- Share mint/revoke needs an owned session (401 logged-out); instead insert/patch
  `session_shares` rows directly via Supabase REST with the service key
  (`POST /rest/v1/session_shares {"session_id":...}` → token; revoke by PATCH `revoked_at`).
  `/r/<token>` should render the replay (with `<meta name="robots" content="noindex, nofollow">`)
  and 404 after revocation.
- Abandoned sweep: insert a `sessions` row (kind solo, outcome null, `last_event_at` 20+ min ago)
  via REST, then hit any server read (`GET /api/solo/replay?sessionId=...` runs the sweep even
  when it returns 404) and confirm `outcome` flipped to `abandoned`.
- Solving warmup-sum anonymously: click Python toggle, Start run, then Ctrl+A and *type* a short
  multi-line solution that has no indented lines (avoids Monaco auto-indent), e.g. read all of
  stdin with `sys.stdin.read().split()` and print joined sums. Submit → ACCEPTED overlay with
  "Watch replay" link containing the session id.
- Chrome address bar aggressively autocompletes previous localhost URLs — after typing a URL,
  press Delete to drop the inline completion before Enter, or you'll navigate to the old page.
- Devin secrets for the dev server env are ORG-scoped (`secret:org:NEXT_PUBLIC_SUPABASE_URL`, ...),
  not repo-scoped as the repo blueprint claims.

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
- node may not be on the default PATH (`corepack: command not found`) — `source ~/.nvm/nvm.sh`
  first; a `~/.local/bin/pnpm` shim may also exist and resolve to the right pnpm.
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
- If `xclip` is missing and there is no sudo, the reliable fallback (works for stations, solo
  and duel) is CDP `Runtime.evaluate` with
  `monaco.editor.getModels().find(m => m.getLanguageId()==='python').setValue(code)`.
  Two gotchas: (a) raw CDP websockets need `suppress_origin=True` (Chrome rejects unknown
  Origins unless launched with `--remote-allow-origins=*`); (b) never embed Python inside a JS
  template literal — `\n` in `print("\n".join(...))` becomes a real newline and the code REs.
  Build the source as a JSON array of lines joined with `"\n"` instead. Click the **Python**
  language toggle in the UI before setValue/submit.
- Wrong answer: submit `print(0)`.
- Admin race control: pick problem, set Timer seconds (default 180 — use 600 to have time for all checks), "Start race (5s countdown)".

## Judge (Fly) gotchas
- Judge syncs problem packages from the Supabase Storage bucket `problems` **on boot only**. If a problem exists in the DB `problems` table but not in the bucket, runs fail with `judge /run failed: 404` (judge ENOENT on `/data/problems/<id>/meta.json`). `warmup-sum` was missing this way once.
- Fix: upload `<id>/meta.json` + `<id>/tests/01.in|01.out` to the bucket (service-role key via storage REST API), then `flyctl machine restart <ids> -a cf-race-judge` (needs FLY_API_TOKEN; install flyctl via `curl -sL https://fly.io/install.sh | sh`).
- Direct judge check: `POST $JUDGE_URL/run` with `Authorization: Bearer $JUDGE_TOKEN`.

## Testing the judge locally (grading correctness / parallelism)
- Two judges side by side make behaviour changes provable: run the branch judge on :8080 and a
  baseline from `origin/main` in a `git worktree` on :8081, both with
  `JUDGE_TOKEN=dev JUDGE_SANDBOX=none PROBLEMS_DIR=<repo>/problems npx tsx src/server.ts`
  (node at `~/.nvm/versions/node/v24.19.0/bin`; sandbox=none avoids needing isolate/cgroups).
  Point the app at the branch judge with `JUDGE_URL=http://localhost:8080 JUDGE_TOKEN=dev`.
- Custom fixtures: any dir under `problems/<id>/{meta.json,tests/NN.in,NN.out,samples/}` is
  loadable as `problemId` (e.g. `dev/pslow`). Make per-test cost measurable by having the
  *submitted solution* `time.sleep()` based on its input, and raise `timeLimitMs` in meta.json
  above that sleep. 12 tests × 1 s ⇒ ~2 s parallel vs ~12 s sequential with 8 workers.
- Adversarial ordering check (catches "first failure to finish" bugs): make the solution wrong on
  a *slow* early test and also wrong on a *fast* later test. Correct CF-style output is the
  lowest-indexed failure (e.g. `failedTest: "03"`, `passedCount: 2`), not the fast one.
  With real CF packages this works too (938A: wrong+sleep on input `b` = test 05, wrong on `ya`
  = test 09 ⇒ UI must show "failed on 05 · 4/26 passed").
- Progress updates: subscribe to `ws://localhost:8080/ws?token=<token>` and collect
  `submit_update` payloads to assert `passedCount` is monotonic and ends at `totalCount`.
- Note: a TLE submission is *not* faster under parallel grading (all queued tests still run out
  their time limit), so don't expect wall-time wins there — only correct verdicts.

## Replay data
- Since the universal-sessions migration (Aug 2026), event races write to the `sessions` tables:
  each `race_participants` row carries a `session_id` (a `sessions` row with kind='event'),
  editor events go to `session_events`, official submissions to `session_submissions`, and the
  webcam path to `sessions.recording_path` (`race/<raceId>-<station>.webm`). Query
  `session_events?session_id=eq.<sid>` (not `race_editor_events`) to verify recording.
  Expected kinds after a full run: snapshot/delta, tab, run, run_result, submit, verdict.
- A per-session submission cap is enforced by a Postgres trigger (50, duels 10): inserting past
  the cap fails with code 23514 "submission limit reached". Cheap way to test: bulk-insert dummy
  rows via REST (`kind:'submit'`, needs `lang` + `source`), try one more, then DELETE the dummies.
- `POST /api/race/start` authorizes via cookie `cfr_<eventId-without-dashes>=<events.secret>`;
  with the secret from the `events` table you can curl it directly (useful to prove the
  409 "a race is already active" invariant while a race is running).
- Legacy note: editor snapshots used to go to `race_editor_events` via `POST /api/replay` (flushed every 5 s from stations). If replays play back empty, check that table. Races intentionally stay in `state="countdown"` in the DB; the recorder in `src/components/station/station-client.tsx` arms whenever the race has `started_at` and `state !== "finished"` (fixed after an earlier bug that required `state === "running"`).
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

## Duel mode (1v1) testing
- `/duel` requires a signed-in Supabase user (Google OAuth in prod). For local testing, skip
  OAuth: create test users via the admin API (`POST $SUPABASE_URL/auth/v1/admin/users` with the
  service-role key, `email_confirm: true` + password), then password-grant login.
  Users `duel-tester-a@example.com` / `duel-tester-b@example.com` already exist; if the password
  is unknown, reset it via `PUT /auth/v1/admin/users/<id>` with the service-role key.
  (`POST /auth/v1/token?grant_type=password` with the anon key) and set the resulting session as
  a cookie named `sb-<projectref>-auth-token` with value `"base64-" + base64url(JSON session)`
  (chunk into `.0`, `.1`… suffixes above ~3180 chars). Setting it via CDP `Network.setCookie`
  for `http://localhost:3100` works; verify by loading `/duel` (signed-in home, not the Google
  button). One session JSON fits in a single cookie chunk.
- Two players: launch two Chrome instances with separate `--user-data-dir`s and distinct
  `--remote-debugging-port`s (9222/9223), both with the fake-media flags. The second instance
  steals focus even with `--window-position=2000,0` — minimize it right away
  (`xdotool windowminimize <winid>`) and keep driving it via CDP. Switch windows with
  `wmctrl -i -a <winid>`; drive the off-screen player headlessly via CDP `Runtime.evaluate`
  (click buttons by textContent) so realtime effects (opponent-AC toast) can be captured on the
  visible window.
- Pasting code: `xclip` may be unavailable and CDP `Input.insertText` still triggers Monaco
  auto-indent (mangles Python). Reliable: `window.monaco.editor.getModels()[0].setValue(<code>)`
  via CDP eval. Remember to click the **Python** language toggle before submitting, else the
  submit goes out as C++ and CEs.
- Deterministic problem pick: `pickDuelProblem` excludes invalidated problems, problems either
  player solved, and problems the pair already played. Pre-seed `problem_invalidations` rows
  (reason `test-fixture`) for all but the target problem via the REST API, then DELETE them
  right after the countdown starts (problem is stamped on `duel_matches` at ready-up).
  Check `duel_matches` for problems the test-user pair already played and pick a target outside
  that list (and with a `pipeline/problems/<id>/ref.py`), else the start silently falls back to
  the lobby with "no problem available"-style behavior.
- Duel data: rooms/matches/players in `duel_rooms`/`duel_matches`/`duel_players`; per-player
  runs are `sessions` rows (kind `duel`) with `session_events`/`session_submissions`.
- Known bugs seen (2026-08): after a match finishes, "Back to lobby" (and even a full page
  reload of the room) keeps showing the TIME'S UP/ACCEPTED finish screen — `/api/duel/state`
  always returns the latest (finished) match with `yourSessionId`, and `duel-room.tsx` re-arms
  `racedSessionId` from it. Workaround: create a fresh room. Also `/duel/review` auto-plays on
  load with `durationMs=1000` before data arrives, so it pauses itself at 0:01.0; press play
  once data is loaded.

## Selection / re-render gotchas (live race screen)
- `RaceScreen` re-renders every 200 ms (timer `setRemaining`). Any prop that is a fresh object literal per render can churn the DOM: with the react-dom bundled in Next 14.2, `dangerouslySetInnerHTML={{ __html: s }}` re-sets `innerHTML` on **every** render (new object reference, even if the string is identical), destroying browser text selections in the statement pane 5×/sec. Fix pattern: `useMemo` the whole `{ __html }` object (see `src/components/race/statement-pane.tsx`).
- Such selection-destruction bugs do NOT reproduce with headless/synthetic drags (they complete between ticks). Test with real GUI mouse: `mouse_move` → `left_mouse_down` → several `mouse_move`s with ~0.5–1 s waits (spanning timer ticks) → screenshot mid-drag → `left_mouse_up`. Diagnose by (a) MutationObserver on the statement subtree (200 ms-period childList mutations = timer-driven DOM churn) and (b) patching the `Element.prototype.innerHTML` setter to capture the stack of whoever re-sets it.

## pnpm gotcha
- If `pnpm` fails with a corepack "Cannot find matching keyid" signature error, run with `COREPACK_INTEGRITY_KEYS=0` exported.
