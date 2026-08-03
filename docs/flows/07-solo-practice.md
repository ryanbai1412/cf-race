# Flow PRD: Solo Practice / Gauntlet

## Goal
A single-player practice mode with no live event: open a problem, solve it against a
3-minute clock, then replay the run or move on to the next problem. Every run records
**everything** — all editor snapshots *and* webcam video — so the same rig doubles as
the tourist-recording setup: a Gennady solo run can be promoted, unchanged, to the
tourist ghost the monitors play back during the live event.

## Actors & devices
- A solo player (practice) or Gennady (recording session) on any laptop with a webcam.
- No event, no stations, no admin. `/solo` is reachable directly from the landing page.

## Routes
- `/solo` — the gauntlet: problem list with solved/unsolved state and replay links.
- `/solo/[problemId]` — the solo race screen (pre-race → countdown → race → finish).
- `/solo/replay/[sessionId]` — replay: editor playback + webcam video, synced.

## User flows

### 1. The gauntlet (`/solo`)
1. Header: "Solo practice" + progress line ("7 / 43 solved").
2. Grid/list of all problems in the bank (id, name, rating, tourist time if known),
   ordered by id. Each card shows:
   - **Solved** badge (green, with best solve time) or **Unsolved** (muted).
   - "Race" button → `/solo/[problemId]`.
   - "Replays (N)" link per past session → `/solo/replay/[sessionId]`.
3. Solved-state + session history live in `localStorage` key `cfr-solo-history`
   (array of `{sessionId, problemId, startedAt, outcome, solveMs}`), so the list is
   personal to the machine — perfect for a booth laptop or Gennady's recording rig.
   The authoritative data (events, video, verdicts) lives server-side keyed by
   session id, so replay links can be shared across machines.

### 2. Pre-race (`/solo/[problemId]`, before start)
1. Card with problem id/name/rating and the run rules ("3:00 on the clock, 10
   submissions, C++ or Python").
2. Webcam preview pane: `getUserMedia` on mount. States:
   - granted → live preview + "camera ready" tag;
   - denied/absent → amber note "No camera — the run will be recorded without video."
     **Everything else still works**; recording video is optional, editor events are
     always recorded.
3. "Start run" button → `POST /api/solo/session` creates a `solo_sessions` row with
   `started_at = now + 3s` (countdown baked into the server timestamp) and
   `timer_sec = 180`. Client stores the session in `cfr-solo-history` immediately
   (outcome `pending`) and enters the countdown.

### 3. Countdown & race
1. Reuses `CountdownOverlay` (3-2-1-GO) driven by the server `started_at`.
2. Race screen is the **same `RaceScreen` component** as the event stations — Monaco,
   statement pane, samples/custom/submit console, timer chrome — running in `solo`
   mode: run/submit/submissions go to `/api/solo/*` (no event cookie), timer counts
   down from 180s.
3. **Editor recording**: identical pattern to the station recorder — debounced (300ms)
   full-code snapshots buffered client-side and flushed to
   `POST /api/solo/events` every 5s (and on unload), stored in `solo_editor_events`
   (`session_id, t_ms, code, lang` — same shape as `race_editor_events`).
4. **Webcam recording**: `MediaRecorder` (webm) starts when the countdown begins;
   the offset between recorder start and GO is stored (`recording_offset_ms`) so
   replay can sync video to the race clock exactly.
5. Submits: max 10, judged like event submits, stored in `solo_submissions`.
   Server enforces the time window (`started_at + timer_sec + grace`).

### 4. Finish
- **AC** → confetti; server sets `outcome='solved'`, `solve_ms`. Finish card: big
  "ACCEPTED", solve time, delta vs tourist (`tourist_time_ms`), buttons:
  **Watch replay** · **Run again** · **Next problem** (first unsolved after this one)
  · **Back to list**.
- **Timer expiry** → "TIME'S UP" card, same buttons, no confetti;
  `outcome='timeout'`.
- Either way the client stops the MediaRecorder, uploads the webm via
  `POST /api/recordings?sessionId=…` (server route → Supabase Storage bucket
  `recordings`, path `solo/<sessionId>.webm`, service-role only; the same route
  handles event-race recordings keyed by raceId+station), and updates
  `cfr-solo-history`. Upload failure is non-fatal (toast; replay works without video).
- Leaving mid-run marks the session `abandoned` (best-effort on unload).

### 5. Replay (`/solo/replay/[sessionId]`)
1. Layout: replay player (read-only Monaco fed by `touristStateAt`, scrubber,
   play/pause, 1/2/4/8× speed — same controls as the event replay) with the **webcam
   video beside it**, synced to the same clock: scrubbing/seeking/speed changes drive
   `video.currentTime`/`playbackRate` through `recording_offset_ms`.
2. Header: problem id/name, outcome (AC time in green / DNF), run date.
3. No video recorded → editor-only replay, video pane hidden.
4. Data: `GET /api/solo/replay?sessionId=…` returns the log in the exact
   `TouristLog` shape (`{problemId, lang, solveMs, events: TouristEvent[]}` —
   snapshots from `solo_editor_events`, submit/verdict moments from
   `solo_submissions`) plus outcome metadata and a short-lived signed URL for the
   video.

### 6. Tourist export (the Gennady path)
- The solo event log **is** the tourist format — no conversion needed.
- Replay page footer, `?export=1` (kept out of casual view): **Download tourist
  JSON** (the `TouristLog`) and **Promote to tourist ghost** →
  `POST /api/solo/promote` uploads the log to the `tourist` storage bucket as
  `<problemId>.json` (with a confirm dialog — it overwrites the ghost monitors play).
- Recording day: Gennady runs the gauntlet top to bottom on `/solo`; each AC run is
  reviewed via its replay and promoted. Webcam webms stay in `recordings` for the
  video team.

## UX details
- Same design system as the rest of the app: dark theme, mono accents, shadcn/ui
  cards/badges/buttons, the station race chrome untouched.
- `/solo` cards use the landing-page gradient aesthetic; solved cards get a green
  ring + trophy time, replay links are quiet ghost buttons.
- Timer colors follow flow 03 (amber <60s, pulsing red <15s).

## States
`idle` (pre-race) → `countdown` → `racing` → (`solved` | `timeout`) → finish card.
Reload mid-run: the session id is kept in `sessionStorage`; the race resumes against
the server `started_at` (code restored from the flow-03 localStorage draft). Webcam
recording does not survive a reload (note shown on the finish card).

## Data
- `solo_sessions` (id uuid, problem_id, lang, started_at, timer_sec, solve_ms,
  outcome `solved|timeout|abandoned`, recording_path, recording_offset_ms).
- `solo_editor_events` (session_id, t_ms, code, lang) — mirrors `race_editor_events`.
- `solo_submissions` (session_id, lang, source, verdict, details, submitted_at,
  judged_at) — mirrors `submissions` without race/contestant.
- Storage: `recordings` bucket (private; webcam webms), `tourist` bucket (ghost JSON,
  written by promote).
- All tables RLS-enabled, service-role access only (as with the rest of the schema).

## Out of scope (future)
- ~~Accounts / cross-device solved state~~ — added: "Log in with Google"
  (Supabase Auth, `@supabase/ssr`). Signed-in runs are tagged with
  `solo_sessions.user_id` (RLS: users read their own rows); `/api/solo/history`
  serves the account history and `/api/solo/claim` merges anonymous localStorage
  runs into the account on first login. localStorage remains the anonymous
  fallback and cache.
- Multi-problem timed gauntlet sessions with aggregate scoring.
- Audio commentary recording.
