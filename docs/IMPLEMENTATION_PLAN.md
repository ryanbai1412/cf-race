# Code Voices Racing — Implementation Plan

## Workstreams
- **A. App skeleton** — Next.js + Supabase schema, event creation, secret-link join, role routing (station/monitor/admin), theming baseline.
- **B. Judge service** — VM + isolate sandbox, C++/Python runners (debug + submit modes), CF-style checker, run/submit API, compile cache.
- **C. Race UX** — check-in, sandbox warm-up, race screen (Monaco, statement pane, run/custom/submit UI, verdict + stdout/stderr views), timer/DQ, congrats + leaderboard.
- **D. Realtime** — WS server, server-authoritative clock/countdown, editor streaming, leaderboard/confetti events.
- **E. Monitors** — spectator layouts, editor mirrors, tourist event-log playback, webcam feeds (LiveKit), idle slides.
- **F. Problem pipeline** — scrape/generate/validate **10 randomly picked problems** (sub-agent batch; 200-problem selection deferred), storage + judge sync.
- **G. Polish & dry-run** — latency tuning, design pass, e2e tests, venue rehearsal.

## Dependency graph
```
A (skeleton) ──────┬──> C (race UX) ──┬──> G (polish/dry-run)
B (judge) ─────────┘        │         │
        │                   v         │
        │              D (realtime) ──┤
        │                   │         │
        │                   v         │
        │              E (monitors) ──┘
        └──> F (problem pipeline) ────┘   (F only needs judge's run format + storage schema;
                                           validated problems land continuously)
```
- A and B are fully independent → start both day 1.
- C needs A (pages/auth) + B's API contract (can start against a mocked judge; swap in real one).
- D needs A; E needs D (+ C's race state).
- F needs only B's test-data format — runs as a background batch in parallel with C/D/E, using 3 hand-made problems as fixtures until it delivers.
- Tourist playback rides on D's editor-streaming renderer (same component replays the event log) — so it lands with E, no extra dependency.
- G integrates everything.

## Parallelization plan
- **Phase 1 (parallel)**: main session builds A; child session builds B (judge VM). Agree the judge API + problem/test-data format up front so C and F can mock against it.
- **Phase 2 (parallel)**: C (main session) + D (same session, tightly coupled to C) while a child session kicks off F's pipeline scaffolding; B session moves to latency tuning.
- **Phase 3 (parallel)**: E (monitors, incl. tourist replay + LiveKit webcams) + F fan-out — ~5 sub-agents over the 10 problems (scrape → gen → validate vs AC/WA/TLE); flagged failures reviewed manually.
- **Phase 4**: G — integration, Playwright e2e in CI, testing-agent click-throughs on preview deploys, dry-run with tourist recordings.

Critical path: **A/B → C → D → G** (roughly: skeleton+judge, then race loop, then sync/monitors, then polish). F (now just 10 problems) blocks nothing — it streams validated problems in as they finish.
