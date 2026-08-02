# Code Voices Racing — PRD (v1 draft)

## Overview
A booth experience for the IOI (International Olympiad in Informatics) sponsorship. Two contestants on two laptops race head-to-head to solve the same easy Codeforces problem as fast as possible — while also racing against Gennady "tourist" Korotkevich, whose pre-recorded solve of the same problem is played back live. Two overhead monitors show the race to spectators.

Everything is a single web app with multiple screen/pages (contestant screens, spectator/monitor screens, admin/event screens).

## Physical setup
- 2 laptops (contestant stations), side by side.
- Monitor A: directly above the two laptops (roughly the width of both).
- Monitor B: to the left of Monitor A.
- Exact monitor layouts TBD; both are driven by spectator pages of the web app.

## Contestant experience (golden path)
1. **Check-in**: Contestant enters their **name** and **country**.
2. **Sandbox / warm-up (~30s)**: A quick throwaway playground so they can get familiar with the editor, keybindings/VM setup, run button, etc. Skippable once familiar. (No heavy tutorial mode.)
3. **Countdown**: "3, 2, 1, GO" — synchronized across both laptops and the tourist playback.
4. **Race screen**:
   - **Left**: the Codeforces problem statement.
   - **Right**: code editor.
   - Languages: **C++ and Python only**.
   - **Run on samples** (default: debug mode; C++ debug builds include ASan/UBSan etc.). Runs all sample tests and gives a quick verdict per sample.
   - stdout and stderr are automatically captured and shown — both **split** and **combined** views.
   - **Custom test case**: contestant can add and run their own input.
   - **Submit**: up to ~10 submissions; multiple submissions may run concurrently. Judged against our own full generated test data (not via Codeforces). **The timestamp of the first AC is what counts.**
   - **Timer**: hard per-problem cap (~3 min, maybe 4 — configurable per problem). Exceeding it = DQ.
   - Sample-run latency must be as fast as possible — the run/submit UX is the single most important thing to get right.
5. **Finish**: On AC → congratulations screen + confetti, then the leaderboard: fastest solves on this problem, including your time vs tourist's time.

## Judging & checkers
- Codeforces-style output comparison:
  - Token-based diff, trailing whitespace / trailing newlines ignored.
  - Case-insensitive YES/NO handling.
- **Constructive / special-judge problems**: when running samples, show a warning — "this is a constructive problem; the sample checker may not be accurate" — instead of pretending the diff checker is authoritative.
- Verdicts: AC / WA / TLE / RE / CE (with compiler output surfaced nicely).

## Problem bank & test generation (offline pipeline)
- Eventual target: ~**200 Codeforces problems, ~800 rated**, randomly sampled from the past few years; prefer multi-tested problems.
- **v1 scope: 10 randomly picked problems** — enough to build and validate the pipeline; how the 200 get selected is decided later.
- For each problem, an offline (sub-agent-driven) pipeline:
  1. Scrape statement + samples.
  2. Generate full test data ourselves, including max-size tests.
  3. Validate the generated tests: take ~5 random AC, ~5 WA, ~5 TLE (etc.) submissions from Codeforces and confirm our tests reproduce the expected verdicts.
- Test data stored with the problem in our own storage; submissions never touch Codeforces at event time.

## Spectator screens (monitors)
- Show, in some cycling/split arrangement (final layout TBD, iterate later):
  - The current problem statement.
  - Live view of each contestant's **editor** (stream code, not necessarily pixels), cycling between the two contestants, plus their **faces** via webcam (in v1).
  - The race **timer**.
  - Tourist's playback progress.
  - **Leaderboard** — ranked by fastest solve time and time-diff vs tourist.
- **Idle mode**: when no race is running, cycle through explainer slides ("what's going on here") and the leaderboard.
- On a solve: big confetti moment on the monitors.

## Tourist playback
- Tourist solves all problems offline; each solve is captured as a **timestamped event log** (editor keystrokes/snapshots, cursor movement, run/submit events and their verdicts) rather than a video file.
- During a race, the event log for the current problem is replayed synchronized with the countdown, so contestants are "racing him live".
- The event format gives flexibility: replay in the same editor UI as live contestants, scrub/speed-adjust, overlay timers/verdicts, and restyle without re-recording. (A screen recording can still be kept as a backup artifact.)

## Events & access control
- **Custom events**: an organizer creates an event; the event has a password / secret link. Laptops and monitors join the event via that link (the link auths the device and assigns its role: contestant-1, contestant-2, monitor-A, monitor-B, admin).
- Threat model is light — defend against casual bad-faith abuse, not determined attackers; it's a supervised live event.
- **Future (out of scope for v1)**: public standalone website where anyone can race on a leaderboard without a custom event or the streaming features. Don't over-invest now, but don't paint ourselves into a corner.

## Design
- Must look **very polished**. Don't invent a design system — adopt a good existing template/theme (component library + tasteful theming) and follow it consistently.

## Non-functional requirements
- Sample runs feel instant (target sub-second for typical 800-rated sample runs; C++ compile is the long pole).
- Submissions judged fast; multiple concurrent submissions supported.
- Countdown/timer sync across laptops, monitors, and tourist playback.
- Reliable on flaky venue Wi-Fi as much as possible (prefer one local-ish backend; graceful reconnects).

## Success criteria
- A contestant can walk up, check in, warm up, race, and see themselves on the leaderboard with zero staff intervention.
- Sample-run loop feels great (fast, clear output, nice diffs).
- Spectator screens are legible and exciting from a few meters away.

## Open questions
1. Per-problem timer: fixed 3 min vs per-problem (3–4 min)?
2. Exact monitor layouts — iterate at the booth?
3. Do both contestants always get the *same* problem, chosen randomly from the bank per race? (Assumed yes.)
4. Tourist event-log capture: instrument an editor he's happy to use (e.g. a capture-enabled instance of our race editor), or transcribe from a screen recording afterwards?
