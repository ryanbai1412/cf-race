# Flow PRD: Spectator Monitors

## Goal
Passers-by instantly understand what's happening: two people racing to solve a
problem, live code on screen, a ghost of tourist racing them, and a countdown clock.

## Setup
Two monitors: Monitor A mirrors Station 1, Monitor B mirrors Station 2 (`/monitor/a`,
`/monitor/b`). Both show the shared race clock and tourist replay.

## Modes

### Race mode (race active)
Full-bleed dark layout:
- **Header bar**: event name · problem name · giant race timer (server-synced).
- **Main area (2 columns)**:
  - Left (60%): contestant's live editor mirror — read-only Monaco fed by realtime
    `editor` broadcasts (code updates ~300ms cadence), contestant name/flag overlay,
    webcam feed (LiveKit) in a corner picture-in-picture card.
  - Right (40%): **tourist ghost** — event-log replay of tourist solving the same
    problem, rendered in the same read-only editor style, synced to the race clock,
    with a "tourist 🇧🇾" header and his elapsed/solve time. If no recording exists for
    the problem, show the tourist time as a countdown chip instead ("tourist would
    finish in 0:41").
- **Verdict moments**: on submission AC of the mirrored station → full-screen confetti
  + "<name> SOLVED IT — mm:ss.d"; tourist "solving" moment shows a subtle flash.
- Countdown overlay (3-2-1-GO) identical to stations.

### Idle mode (no active race)
Cycles every ~12s between:
1. **Explainer slide** — "Race a Codeforces problem. Beat your rival. Beat tourist." +
   how to join (see staff).
2. **Leaderboard** — top solves across all problems (or per-problem cycling).
3. **Warm-up mirror** — if a contestant is checked in and typing in the sandbox,
   show their editor live ("warming up…").

## Tourist event-log format (`tourist/<problemId>.json` in Supabase Storage)
```jsonc
{
  "problemId": "1927A",
  "lang": "cpp",
  "solveMs": 41000,
  "events": [
    {"t": 0, "type": "snapshot", "code": ""},
    {"t": 1200, "type": "snapshot", "code": "#include..."},   // full-code snapshots
    {"t": 39500, "type": "submit"},
    {"t": 41000, "type": "verdict", "verdict": "AC"}
  ]
}
```
Full-code snapshots (not deltas) keep the player trivial and scrub-safe; at 1-2
snapshots/sec a 4-minute solve is ~a few hundred KB, fine to preload.

## Player behavior
- Binary-search the snapshot at `raceClock` and render it; on `verdict: AC` show the
  solved banner + freeze the ghost editor.
- Works for countdown (clock < 0 → empty editor, "waiting at the start line…").
