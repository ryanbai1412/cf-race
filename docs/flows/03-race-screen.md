# Flow PRD: Race Screen (run / custom test / submit / timer)

## Goal
The core experience. It must feel like a serious competitive-programming setup:
instant feedback, clear verdicts, zero confusion under adrenaline.

## Layout (station, fullscreen)
- Top bar: problem id+name · race timer (mm:ss, turns amber <60s, red <15s, pulsing) ·
  contestant name/flag · language picker · status pill (Running / Judging / AC …).
- Left pane (45%): problem statement (scrollable, CF-style formatting, MathJax),
  sample tests inline with copy buttons.
- Right pane (55%): Monaco editor (vs-dark, C++/Python syntax, sensible defaults:
  tab=4 for C++, autoindent; font: Geist Mono / JetBrains Mono).
- Bottom of right pane, tabbed console:
  - **Samples** tab: per-sample verdict chips (AC/WA/RE/TLE) + expandable rows showing
    input, expected, got, stderr — split and combined stdout/stderr views.
  - **Custom** tab: textarea for custom input + Run button; output split/combined.
  - **Submit** tab: submission history list (verdict, time, failed test #, counter
    "N/50 submissions used").
- Action buttons: `Run samples` (Ctrl+Enter), `Run custom`, `Submit` (Ctrl+Shift+Enter),
  all with busy states; concurrent submits allowed, run disabled while a run is active.

## Behaviors
- **Run samples**: POST /api/judge/run → per-test streaming updates; debug-mode note
  shown for C++ ("ASan/UBSan enabled — slower but catches UB").
- **Special-judge problems**: amber banner above sample results: "This problem may
  accept multiple answers — sample checking here can report false WA."
- **Custom test**: same path with tests=[{custom input, expected:null}] → output only.
- **Submit**: max 10 per contestant per race; optimistic row appears instantly with
  PENDING, updates as judge streams verdict. First AC freezes contestant's clock:
  full-screen confetti + transition to Finish screen (flow 04). Later submissions after
  AC are blocked.
- **Timer expiry**: hard stop — editor locks, "Time's up" overlay, DQ recorded, then
  transition to Finish screen (as DNF).
- Starter templates: C++ (bits/stdc++, fast IO, `int t; cin>>t; while(t--) solve();`
  skeleton) and Python (`import sys; input=sys.stdin.readline`, t-loop skeleton).
- Editor content is broadcast (debounced ~300ms) on the realtime channel for monitors.
- Language switch swaps template only if the editor is untouched; otherwise keeps code.

## States
`racing` → (`AC` | `timeout-DQ` | `out-of-submissions` stays racing until timer ends)
→ finish screen. Reconnect-safe: reload restores race state from server (code is kept
in localStorage keyed by race+station).

## Data
- `submissions` rows with verdict/details (failed test, counts, times).
- `race_participants.first_ac_at` set on first AC (server-side, authoritative).
- Runs are ephemeral (not persisted) except a counter in memory for rate limiting.
