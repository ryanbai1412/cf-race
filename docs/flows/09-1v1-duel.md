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
2. Timer: none by default (first AC wins); optional room setting
   `timer_sec` (e.g. 5/10 min) as a cutoff → both DNF if it expires.
3. Live opponent presence: a slim status strip (not a full editor mirror in
   v1): opponent's language, last run/submit + verdict, and a "typing"
   heartbeat via the existing Supabase Realtime channel pattern
   (`duel-{roomId}`).
4. Recording: full event log per player (keystroke deltas/snapshots, runs,
   run results, tabs, submits, verdicts, statement scroll — the same recorder
   as solo) + webcam via MediaRecorder.
5. Win condition: first AC ends the match for both (loser's screen shows
   "<name> solved it first" and locks after a short grace to finish typing a
   pending submit). Both-DNF if timer expires or both exhaust submissions.

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

## Open questions
1. Live opponent visibility during the race: none, a status strip (proposed),
   or full live editor mirror of the opponent?
2. Race timer: pure first-AC-wins with no cutoff, or a default cutoff
   (e.g. 10 min)?
3. Should a duel loser's problem count as "solved" for them if they AC after
   the winner (within grace), or only the winner's solve recorded?
4. Login: Google-only, or also allow the booth secret-link identities?
