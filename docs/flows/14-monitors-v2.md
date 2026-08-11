# Flow PRD: Booth Monitors v2 — Race tourist

## Physical setup
Two monitors side by side at the booth. The queue faces the **right monitor**
head-on (the race itself); the **left monitor** is glanced at for context
(leaderboard + problem). Both render full-bleed dark, no navbar, at
`/e/<eventId>/monitor/left` and `/e/<eventId>/monitor/right` (secret-gated
like the existing monitor routes).

## Participants
Three columns of racers: **Contestant A**, **Contestant B** (the two live
stations), and **Genna** (tourist), whose "run" is the replay of his reference
session for the active problem (`genna_problems`). The race clock, statuses,
and finish logic treat all three uniformly — Genna's events just come from a
recorded log instead of realtime broadcasts.

---

## Right monitor — the race (three columns)

Layout: full-height three equal columns, one per racer. A header bar spans the
top with the event name and the **race timer** (giant, mm:ss, centered).

Each column, top to bottom:
1. **Label bar** — "CONTESTANT A" / "CONTESTANT B" / "tourist" (LGM-styled:
   first letter black, rest red, on a light chip so it reads from afar), plus
   the checked-in name + country flag once known. Right-aligned **status
   chip**: `WORKING` (default during race) → `AC mm:ss` (green) or
   `TIME UP` (gray).
2. **Webcam** (~40% of column height) — 16:9 video.
   - Contestants: **continuously streamed live** (LiveKit), independent of the
     save-to-session recording which keeps happening as today. Streams run
     whenever the station has camera access — even before/between races.
   - Genna: blank/empty placeholder for now (dark card with the tourist mark).
3. **Activity feed** (thin strip next to/under the webcam) — most recent
   submission/run events, newest first, e.g. `ran samples ✓`, `submitted…`,
   `submission AC` (green), `submission WA` (red). Genna's feed is driven by
   his replay log (run/submit/verdict events) synced to the race clock.
4. **Code editor** (rest of the column) — read-only Monaco.
   - Contestants: live mirror from realtime editor broadcasts.
   - Genna: replayed from the reference session's `session_events`, synced to
     the race clock.

### AC moment
When a racer ACs: status chip flips to green `AC mm:ss`, and **confetti
bursts over that column**. Genna's replay AC does the same for his column
(slightly subtler flash is fine).

---

## Left monitor — context (leaderboard + statement)

Layout: 50/50 split.
- **Left half — leaderboard**, always visible in every phase. Title:
  **"RACE tourist"** with *tourist* in Codeforces LGM styling. Columns:
  flag · contestant name · problem id (e.g. `1758B` — signals Codeforces) ·
  their time · tourist's time · **delta** (green `−0:12` = beat him, red
  `+0:41`). Sorted by delta ascending, best row per contestant+problem.
  Data: solved event sessions joined to `genna_problems` reference times via
  `GET /api/leaderboard/genna?eventId=`.
- **Right half — problem statement** of the active race. Must always be fully
  readable: scale-to-fit, or a slow auto-scroll loop when too tall — never a
  statically cut-off statement.

---

## Phase-by-phase flows

### 1. Idle (no one checked in / nothing happening)
- Right monitor: three columns in resting state — labels shown, webcams
  streaming if a station's camera is live (else blank card), editors show
  template code (or last race's final code), status chips hidden.
- Left monitor: leaderboard on the left; statement half **hidden/dimmed**
  (show a subtle "waiting for the next race" card instead of an empty pane).

### 2. Warm-up (contestants entered, readying up)
Entering a station puts the contestant into warm-up mode (existing sandbox).
- Right monitor: header shows **WARM-UP MODE**; each contestant column shows
  `READY` (green) / `NOT READY` (gray) chips; editors mirror warm-up typing;
  webcams streaming.
- Left monitor: right half shows the **warm-up problem** while they ready up;
  leaderboard stays.

### 3. Start — server-negotiated timestamp
When all required contestants are ready, the **server picks a single start
timestamp** (now + a few seconds) and broadcasts it with the problem payload
early; every surface (stations, monitors) counts down to that shared
timestamp locally against the server-synced clock. This kills the duel-style
latency skew — nobody starts a second early.
- Right monitor: full-screen **3-2-1** overlay, then the race timer starts.
- Left monitor: dimmed with the same 3-2-1 overlaid; at 0 the statement
  appears (payload was pre-sent).

### 4. Racing
- Timer: **3:00 default**, configurable per event on the event admin page
  (existing timer field; default moves to 180s).
- Right monitor: statuses `WORKING`, feeds ticking, Genna's replay running.
- Left monitor: statement fully visible, leaderboard live.

### 5. Finish — when all three racers are done
A racer is *done* when they AC (timestamp marked) or the timer expires.
When **all three** (A, B, Genna) are done → **GAME OVER** screen, racing-game
style, shown on the right monitor AND the right half of the left monitor AND
the contestant stations:
```
        GAME OVER
  1st  🇵🇱 Marek        1:42   (tourist +0:19)
  2nd  tourist          1:23   —
  3rd  🇯🇵 Yuki         2:31   (tourist +1:08)
```
- Ranks over the three racers by solve time (no-AC ranks last, "no solve").
- Deltas vs Genna shown per contestant.
- Below/beside: **all-time best times for this problem** (event-wide
  leaderboard filtered to the problem) — same panel on station screens.

### 6. Review / between races
Stations show the game-over/review screen; contestants can click **Next
problem** / **Go to warm-up**.
- While they warm up for the next race, the right monitor keeps showing the
  **previous problem's** game-over/review state, and the left monitor's right
  half keeps the previous statement; leaderboard stays.
- When both click Ready again → phase 3 (3-2-1 on both monitors) → next race.

---

## Implementation notes
- Webcam streaming: reuse the LiveKit room per event; stations publish
  whenever camera is granted (not just during races); monitors subscribe.
  Session recordings (chunked upload) continue unchanged in parallel.
- Genna replay driver: reuse the replay engine (session_events playback)
  clamped to the shared race clock; expose his run/submit/verdict events to
  the activity feed and status chip.
- Server-negotiated start: `races.started_at` already is a future timestamp
  (countdown); extend the same mechanism so stations receive the problem
  payload at ready-time and gate the editor until `started_at`.
- Ready-up state: reuse warm-up ready flags; race auto-starts when all
  stations are ready (or admin forces start from the console).
- Timer default: 180s; editable in event admin settings.
- Game-over rank includes Genna as a first-class row.

## Design language
Dark full-bleed, monospace numerals, oversized type readable from ~5m:
timer ≥ 120px, status chips ≥ 28px, leaderboard rows ≥ 32px. Country flags as
emoji. Confetti = existing station confetti component. LGM "tourist"
styling: first letter black (on light chip) or white (on dark), remainder
`#ff0000` red, bold.

## Open questions
1. Auto-start when both stations are ready, or admin always pulls the
   trigger? (Proposed: auto when both ready AND admin has armed a problem.)
2. If only one station is occupied, race solo vs Genna? (Proposed: yes —
   "all racers done" = occupied stations + Genna.)
3. Game-over hold time: stay until next warm-up starts? (Proposed: yes, no
   auto-timeout.)
