# Flow PRD: Booth Monitors v2 — Race tourist

## Physical setup
Two monitors side by side at the booth. The queue faces the **right monitor**
head-on (the race itself); the **left monitor** is glanced at for context
(leaderboard + problem). Both render full-bleed dark, no navbar, at
`/e/<eventId>/monitor/left` and `/e/<eventId>/monitor/right` (secret-gated
like the existing monitor routes).

## Monitor states
The monitors have exactly **two states: RACING and REVIEWING**. There is no
warm-up state on the monitors — warm-up/ready-up lives on the contestant
laptops only. While contestants warm up for the next race, the monitors stay
in REVIEWING (previous race's results and problem). Before the first race of
an event, show a minimal "waiting for contestants" resting card in the
review slots — don't over-design it.

## Participants
Three columns of racers: **Contestant A**, **Contestant B** (the two live
stations), and **Genna** (tourist), whose "run" is the replay of his
reference session for the active problem (`genna_problems`). The race clock,
statuses, and finish logic treat all three uniformly — Genna's events come
from his recorded session log instead of realtime broadcasts.

---

## Right monitor — the race (three columns)

Layout, top to bottom:
1. **Header row** — the CF problem id (e.g. `1758B`) and the **race timer**
   (giant, mm:ss).
2. **Three equal columns**, one per racer. Each column:
   1. **Name row** — country flag + full name (fallback "Contestant A" /
      "Contestant B"; Genna shows "tourist" LGM-styled and **no Belarus
      flag**), with a status chip: `WORKING` → `AC mm:ss` (green) or
      `TIME UP` (gray).
   2. **Webcam row** — kept small so code stays visible: webcam video on the
      left, **submission log** on the right (newest first: `ran samples ✓`,
      `submitted…`, `submission AC`/`WA`).
      - Contestant webcams: **continuously streamed live** (LiveKit),
        independent of the session recording.
      - **Genna's webcam: streamed from his reference session's webcam
        recording**, played back synced to the race clock (we have the
        recording from his session).
      - Genna's submission log replays his session's run/submit/verdict
        events on the race clock.
   3. **Code** — read-only Monaco filling the rest: live mirror for
      contestants, replayed `session_events` for Genna.

### AC moment
When a racer ACs: status chip flips to green `AC mm:ss` and confetti bursts
over that column (Genna's slightly subtler). The contestant's session keeps
recording (webcam +5s reaction tail) and uploads **in the background** — the
racer's on-screen flow is continuous; no upload UI on monitors, and the
station moves straight to review while chunks finish uploading behind the
scenes.

---

## Left monitor — context (leaderboard + statement)

Layout: 50/50 split.
- **Left half — leaderboard**, visible in both states. Title: **"RACE
  tourist"** with *tourist* in Codeforces LGM styling. Columns: flag ·
  contestant name · problem id (e.g. `1758B` — signals Codeforces) · their
  time · tourist's time · **delta** (green `−0:12` = beat him, red `+0:41`).
  Sorted by delta ascending, best row per contestant+problem.
- **Right half — problem statement**:
  - RACING: the active problem, always fully readable — scale-to-fit or a
    slow auto-scroll loop when too tall; never statically cut off.
  - REVIEWING: keeps showing the **previous race's** statement for review.

---

## Race lifecycle

### 1. Ready-up (contestant laptops; monitors stay in REVIEWING)
Contestants at stations go through the existing warm-up sandbox and click
**Ready**. Monitors do not change state.

### 2. Auto-start — random problem, server-negotiated timestamp
When all occupied stations are ready, the server (no admin intervention):
1. **randomly picks an unplayed Genna problem** (cycle before repeating);
2. writes the race with `started_at = now + ~5s` and sends the problem
   payload immediately (statement pre-delivered, editor gated);
3. every surface counts down to that shared timestamp against the
   server-synced clock — no duel-style latency skew.
Monitors flip to RACING: right monitor full-screen **3-2-1** overlay; left
monitor dims with the same overlay, statement revealed at 0.

### 3. Racing
- Timer: **3:00 default**, configurable on the event admin page (existing
  timer field; default becomes 180s).
- Right monitor: statuses `WORKING`, logs ticking, Genna's replay running.
- A racer is *done* on AC (timestamp marked immediately, even if the race
  continues) or when the timer expires.

### 4. Game over → REVIEWING
When **all three racers are done** → GAME OVER, racing-game style, shown on
the right monitor, the left monitor's right half, AND the station screens:
```
        GAME OVER
  1st  🇵🇱 Marek        1:42   (tourist +0:19)
  2nd  tourist          1:23   —
  3rd  🇯🇵 Yuki         2:31   (no AC)
```
The review layout is a **split**: left — this race's ranking (three racers
by solve time, no-AC last, deltas vs tourist); right — **all-time best times
for this problem** (event leaderboard filtered to the problem). Stations
show the same split. Monitors hold REVIEWING until the next race auto-starts
(next ready-up), keeping the previous problem + results visible.

---

## Architecture / implementation plan

### Data & state
- `races` gains nothing new for state: RACING = a race with
  `started_at <= now < finish`, REVIEWING = latest finished race. Monitors
  derive state from the existing `/api/state` payload (extend it with the
  latest finished race + its results so review needs no extra fetch).
- **Race results**: rank/time/delta computed from `race_participants.
  first_ac_at` + the Genna reference `solve_ms` — no new tables.
- **Genna leaderboard**: `GET /api/leaderboard/genna?eventId=` — solved event
  sessions joined to `genna_problems`→`sessions.solve_ms`; best row per
  contestant+problem, delta-sorted. Event-secret gated.
- **Random pick**: server-side — Genna-ready problems minus this event's
  already-raced `problem_id`s; reset the pool when exhausted.

### Auto-start
- Extend the existing ready flags: when the last occupied station flips
  ready, the API handler (ready endpoint) transactionally creates the race
  (reuse `startRace`, which already sets a future `started_at` and enforces
  the one-active-race partial unique index — double-ready races can't
  double-start). Admin console keeps a manual start as a fallback.
- Stations receive the race + problem payload via the existing realtime
  state broadcast; editors stay locked until `started_at` (server-synced
  clock, same as the current countdown).

### Genna playback (right monitor column 3)
- Reuse the replay engine (`session_events` playback) in a clock-driven
  mode: instead of an internal play head, it renders at
  `raceClock = serverNow() - started_at`, so refreshes/joins mid-race stay
  in sync.
- His webcam video element seeks to `raceClock - recording_offset_ms` and
  plays; on drift > 500ms, re-seek. Recording is fetched via the existing
  signed-URL recordings API.
- Run/submit/verdict events from the log feed his submission log and status
  chip; his `solve_ms` marks him done.

### Contestant webcam streaming
- Stations publish to the event LiveKit room whenever camera permission is
  granted (not just during races). Monitors subscribe per station identity.
  The chunked session recording continues in parallel, unchanged, including
  the +5s AC reaction tail and background upload after the race.

### Components (new/changed)
- `monitor/left-monitor.tsx` — leaderboard pane + statement pane (+ review
  results pane), 3-2-1 dim overlay.
- `monitor/right-monitor.tsx` — header (problem id + timer) + three
  `RacerColumn`s (name row, webcam+log row, code pane), game-over overlay.
- `monitor/racer-column.tsx` — shared by live (broadcast-fed) and replay
  (log-fed) racers.
- Station: review screen becomes the ranking + all-time split; ready-up
  triggers auto-start.
- Routes: `/e/<id>/monitor/left`, `/e/<id>/monitor/right` (keep `/monitor/a`
  and `/monitor/b` redirecting to `right` for compatibility).

### Ordered build
1. Genna leaderboard API + `/api/state` review extension.
2. Auto-start on ready-up (random pick, negotiated timestamp).
3. Right monitor (columns, streams, Genna replay driver, game over).
4. Left monitor (leaderboard + statement + review split).
5. Station review screen split + timer default 180s.

## Design language
Dark full-bleed, monospace numerals, oversized type readable from ~5m:
timer ≥ 120px, status chips ≥ 28px, leaderboard rows ≥ 32px. Country flags
as emoji. Confetti = existing station confetti component. LGM "tourist"
styling: first letter black (on light chip) or white (on dark), remainder
`#ff0000` red, bold.

## Second-pass fixes & UX improvements
1. **Timer-expiry transition** — game over must trigger with zero submissions:
   monitors derive "done" client-side from the server-synced clock (no
   dependence on a final broadcast); the server sweep finalizes the race row.
2. **Genna finishing after the timer** — if his reference solve is slower
   than the race timer, he's `TIME UP` like anyone else; his true time still
   shows in review ("tourist finished in 4:12").
3. **No webcam in Genna's reference session** — show his name card
   placeholder; never a broken video element.
4. **Statement fairness** — payload is pre-sent but statement stays hidden on
   stations AND the left monitor until t=0 (editor unlock and statement
   reveal share the same clock gate).
5. **Confetti idempotence** — fire per racer per race exactly once (track
   fired race+racer), so replays/refetches don't re-burst.
6. **Refresh resilience** — both monitors are stateless views over
   `/api/state` + the race clock: a mid-race refresh reconstructs columns,
   Genna playhead, logs, and overlays with no drift.
7. **Ready-state races** — reset ready flags when a race starts (already
   landed, d5fdc67) so a stale ready can't instantly re-trigger auto-start
   during review.
8. **Empty leaderboard cold start** — before any solve, show a friendly
   "No one has beaten tourist yet — be the first" row instead of an empty
   table.
9. **Genna replay determinism on monitors A/B** — both monitors and any
   admin preview render Genna from the same clock formula, so his code/webcam
   are identical across screens.
10. **Station review parity** — station game-over screen reuses the same
    ranking + all-time components as the monitors (one component, two
    surfaces), preventing drift between what racers and spectators see.
11. **Webcam stream identities** — one publisher per station (`station1`,
    `station2`) reused across warm-up/race/review; monitors keep a persistent
    subscription instead of re-joining per race (avoids join flicker).
12. **Long names/flags** — truncate names at ~24 chars with ellipsis; always
    keep the status chip visible.

## Open questions
1. If only one station is occupied, race solo vs Genna? (Proposed: yes —
   "all racers done" = occupied stations + Genna.)
2. Statement on the left monitor during the 3-2-1: hidden until 0 (fairness)
   or visible early? (Proposed: hidden until 0, matching stations.)
3. Random pick pool: skip problems any current contestant has already raced
   this event, or only globally-unplayed-this-event? (Proposed: per-event
   unplayed only.)
