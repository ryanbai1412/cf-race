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
      `submitted…`, `submission AC`/`WA`). Contestant webcams are
      **continuously streamed** (LiveKit) independent of session recording;
      Genna's webcam is blank for now. Genna's log replays his reference
      session's run/submit/verdict events on the race clock.
   3. **Code** — read-only Monaco filling the rest: live mirror for
      contestants, replayed `session_events` for Genna.

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

The monitors are always in one of two primary states: **racing** or
**reviewing** (the previous race). Before the first race ever, show a minimal
"waiting for contestants" resting view — don't over-design it: labels shown,
webcams streaming if live (else blank card), editors show template or last
code, statement half dimmed on the left monitor.

### 2. Warm-up (contestants entered, readying up)
Entering a station puts the contestant into warm-up mode (existing sandbox).
- Right monitor: header shows **WARM-UP MODE**; each contestant column shows
  `READY` (green) / `NOT READY` (gray) chips; editors mirror warm-up typing;
  webcams streaming.
- Left monitor: right half shows the **warm-up problem** while they ready up;
  leaderboard stays.

### 3. Start — auto, server-negotiated timestamp
When all required contestants are ready, the server **randomly selects an
unplayed Genna problem** and auto-starts the race — no admin intervention.
It picks a single start timestamp (now + a few seconds) and broadcasts it
with the problem payload early; every surface (stations, monitors) counts down to that shared
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
  occupied stations are ready (admin console keeps a manual override).
- Timer default: 180s; editable in event admin settings.
- Game-over rank includes Genna as a first-class row.

## Design language
Dark full-bleed, monospace numerals, oversized type readable from ~5m:
timer ≥ 120px, status chips ≥ 28px, leaderboard rows ≥ 32px. Country flags as
emoji. Confetti = existing station confetti component. LGM "tourist"
styling: first letter black (on light chip) or white (on dark), remainder
`#ff0000` red, bold.

## Open questions
1. If only one station is occupied, race solo vs Genna? (Proposed: yes —
   "all racers done" = occupied stations + Genna.)
2. Game-over hold time: stay until next warm-up starts? (Proposed: yes, no
   auto-timeout.)
3. Random pick pool: exclude problems already raced at this event?
   (Proposed: yes, cycle before repeating.)
