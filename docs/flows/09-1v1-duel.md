# Flow PRD: 1v1 Duel Mode

## Goal
A head-to-head duel mode: two logged-in players race the same problem in real
time. Serves two purposes: (a) Gennady-vs-Ryan recording sessions, (b) fun.
Everything is recorded (editor keystrokes/events + webcam), and the finish
screen is a side-by-side review of both players.

## Actors
- Two players, each **logged in with Google** (Supabase Auth). Login is
  required — anonymous users are redirected to sign in.
- No admin, no monitors (v1). Either player can create a room.

## Routes
- `/duel` — home: problem pool, solved lists, recordings, create-room button.
- `/duel/problems` — full problem bank view (all / solved-by-you /
  solved-by-either / invalidated), with per-problem detail.
- `/duel/room/[roomId]` — the room: lobby → ready → countdown → race → review.
- `/duel/review/[matchId]` — post-match side-by-side replay (also reachable
  later from the recordings list).

## User flows

### 1. Duel home (`/duel`)
1. Requires login; shows your Google identity + your duel stats.
2. "Create room" → creates a `duel_rooms` row, gives a shareable link
   `/duel/room/[roomId]` to send to the opponent.
3. Lists: past matches (with review links), problems solved by you, and
   recordings.

### 2. Problem tracking
- **Single `sessions` data source**: one row per player-run of a problem
  (user_id, problem_id, started_at, timer_sec, outcome, solve_ms,
  recording_path, recording_offset_ms). Editor events, submissions, and
  webcam recordings all hang off a session id — identical for ALL surfaces:
  solo, duel, and live-event races. Solo's `solo_sessions` is migrated into
  it, duel matches fkey into two sessions (below), and event races fkey into
  one session per station — one recording/replay/submission code path
  everywhere.
- "Solved by user X" = exists a session for (X, problem) with
  outcome='solved'. Replays are always per-session, so solo and duel replays
  share one player and one URL scheme.
- **Random pick**: when a match starts, the server picks a uniformly random
  problem from the bank that (a) neither player has solved, (b) is not
  invalidated, (c) has not been used in a previous match between these two
  players.
- **Invalidate button**: on a problem's detail view (and on the match review
  screen), "Mark invalid" sets `problems.invalidated_at` + `reason`
  (free-text, e.g. "Genna got distracted"). Invalidated problems are excluded
  from random picks and flagged in the list views. Can be un-invalidated.

### 3. Room lobby (`/duel/room/[roomId]`)
1. Creator waits in the lobby; opponent opens the link and joins (must be
   logged in; room holds max 2 players; extra visitors get a spectate-less
   "room full" card).
2. Both players see each other's name/avatar + webcam preview (getUserMedia,
   same optional-camera semantics as solo mode).
3. **Async ready-up**: each player clicks "Ready". State is per-player;
   you can un-ready until both are ready. When both are ready the server
   stamps `started_at = now + 3s` → synchronized 3-2-1-GO countdown on both
   screens (server-authoritative clock, same as event races).
4. Problem is chosen server-side at ready-completion and revealed at GO.

### 4. Race
1. Same `RaceScreen` as solo/event (Monaco, statement, samples/custom/submit,
   per-language buffers), 10-submission cap, standard verdicts.
2. Timer: configurable in the room lobby before ready-up:
   - `total_time_sec` (optional): hard cutoff for the whole match;
   - `grace_after_ac_sec` (optional): once the first player ACs, the other
     has this much additional time before the match ends.
   Defaults: no total cutoff, 60s grace after first AC.
3. No live opponent visibility during the race. The only realtime signal is
   a notification when the opponent ACs (via the `duel-{roomId}` Supabase
   Realtime channel).
4. Recording: full event log per player (keystroke deltas/snapshots, runs,
   run results, tabs, submits, verdicts, statement scroll — the same recorder
   as solo) + webcam via MediaRecorder.
5. Win condition: first AC wins. The other player gets a notification
   ("<name> solved it!") and the grace window keeps running — if they AC
   within it, the problem still counts as solved for them (winner unchanged).
   Both-DNF if the total cutoff expires or both exhaust submissions.

### 5. Finish + upload guard
- On match end each client stops MediaRecorder and uploads the webm (signed
  Supabase Storage URL, progress bar as in solo).
- **Blocking guard**: while upload is in flight, `beforeunload` warns AND an
  in-app modal blocks navigation ("Uploading recording — 63%") until done or
  explicitly abandoned. The review screen link unlocks after upload finishes.

### 6. Review (`/duel/review/[matchId]`)
- Side-by-side: two replay players (editor + mini console + statement scroll)
  with both webcams, all driven by ONE shared clock/scrubber — play, pause,
  speeds, jump-to-event on either player's activity timeline.
- Header: problem, winner, both solve times, submission counts.
- "Mark problem invalid" button here too (retroactively excludes it and voids
  the match from solved-tracking; the recording remains).

## Data
- `duel_rooms` (id, created_by, status `lobby|racing|done`, timer_sec,
  created_at).
- `duel_matches` (id, room_id, problem_id, started_at, winner_user_id,
  finished_at); `duel_players` (match_id, user_id, ready_at, outcome,
  solve_ms, recording_path, recording_offset_ms).
- `duel_solves` as above; `problem_invalidations` (problem_id, by_user,
  reason, created_at, revoked_at).
- Event logs reuse the existing session-event tables keyed per player-match.

## Out of scope (v1)
- Spectator/monitor view of a duel; ratings/ELO; more than 2 players;
  in-race chat.

## Decisions (from review)
1. No live opponent visibility during the race — only a notification when the
   opponent solves.
2. Timer configurable on the duel page: total time and/or additional time
   after the first AC.
3. Any AC counts as solved for that player, regardless of who won.
4. Google-only login for v1; keep the auth layer pluggable for future
   providers.
