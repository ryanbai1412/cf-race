# Code Voices Racing — High-Level Architecture Plan (v1 draft)

## Recommended stack (TL;DR)
| Layer | Choice | Why |
|---|---|---|
| Web app | **Next.js (App Router) + TypeScript** on Vercel | One app, many pages (contestant / monitor / admin); fast to build, easy deploys |
| UI | **Tailwind + shadcn/ui**, Monaco editor, framer-motion, canvas-confetti | Polished look without inventing a design system; Monaco = VS Code editor feel |
| Realtime | **WebSockets on the judge server** (socket.io or plain ws) | Countdown sync, editor streaming to monitors, live leaderboard |
| DB | **Supabase (Postgres)** | Events, contestants, submissions, leaderboard; Supabase Realtime as a fallback channel; Storage for test data + tourist recordings |
| Judge / code exec | **Dedicated VM (Fly.io machine or a Hetzner/EC2 box) running our own runner with `isolate`** (the actual IOI sandbox) or nsjail | Lowest latency + full control over debug flags (ASan/UBSan), stdout/stderr capture, concurrency. Hosted judges (Judge0 etc.) are too slow/rigid for the "instant sample run" bar |
| Test-gen pipeline | Offline scripts + Devin sub-agents, results committed to repo / Supabase Storage | Batch job (v1: 10 problems), validated against real CF verdicts |
| Tourist playback | **Timestamped editor-event log** (JSON: keystrokes/snapshots, cursor, run/submit events) replayed through the same editor renderer as live streaming | Restyle/scrub/speed-adjust without re-recording; one rendering path for live + replay |
| Webcams (v1) | WebRTC via **LiveKit Cloud** | Contestant faces on the monitors with low latency |

**Accounts you'd create for me**: Vercel, Supabase, Fly.io (or give me a VM), and LiveKit.

## Components

### 1. Web app (Next.js, single deployment)
Pages/roles, all joined to an event via secret link (`/e/<eventId>?k=<secret>&role=...`):
- `/e/.../station/1|2` — contestant station: check-in → sandbox → countdown → race screen → congrats/leaderboard.
- `/e/.../monitor/a|b` — spectator screens: configurable layout panels (problem, editor streams, timer, tourist playback, leaderboard, idle slides).
- `/e/.../admin` — organizer: create event, pick/queue problems, start countdown, DQ/reset, tweak timer.
- Race screen: Monaco (C++/Python modes), Run / Run custom / Submit; verdict panel with per-sample results, split & combined stdout/stderr, CF-style diff highlighting, constructive-problem warning banner.

### 2. Realtime layer
- One WS connection per device to the judge server.
- Server-authoritative clock: countdown + race timer broadcast from server (devices render offsets), so laptops, monitors, and tourist playback all start on the same "GO".
- Editor streaming: contestant page sends debounced code snapshots (+ cursor) over WS; monitors render them in a read-only Monaco. Crisp, cheap, no screen capture.
- Leaderboard/verdict events pushed to all screens; confetti trigger on AC.

### 3. Judge service (the critical path)
- Node/Go service on a dedicated 8–16 core VM, colocated region.
- Sandboxing via `isolate` (cgroups): per-run CPU/memory/time limits, no network.
- **Sample runs ("debug mode")**: C++ compiled with `-O1 -g -fsanitize=address,undefined`; Python run directly. Warm compile cache keyed on source hash (samples then submit = one compile). Target: Python samples < 300ms, C++ ~1–2s (compile-dominated).
- **Submissions**: compile with `-O2`, run against full generated tests, short-circuit on first failure per CF convention; up to ~10 submissions per contestant, concurrent runs OK (queue with per-station fairness).
- **Checker**: CF-style token comparison (trailing whitespace, case-insensitive YES/NO, float eps option); special-judge problems flagged in problem metadata → warning on samples.
- API: `POST /run` (samples/custom), `POST /submit`, WS for streaming verdicts as tests complete.

### 4. Problem bank + offline test-gen pipeline
- Repo directory `problems/<cfId>/` with `statement.html`, `meta.json` (limits, multi-test flag, special-judge flag, timer), `samples/`, `tests/`, `gen/` (generator + validator source).
- Pipeline (Devin sub-agents; **v1: 10 randomly picked problems**, same machinery scales to the eventual ~200):
  1. Randomly pick CF problems rated 800 from recent years (prefer multi-tested).
  2. Scrape statement + samples; write a generator (incl. max tests) and reference solution.
  3. Validate: run ~5 AC / 5 WA / 5 TLE real CF submissions against our tests; require expected verdicts; flag mismatches for manual review.
- Final test data uploaded to Supabase Storage and pre-synced onto the judge VM before the event (no network dependency at race time).

### 5. Tourist playback (event-log format)
- One event-log JSON per problem: `{t_ms, type, payload}` entries — editor deltas/snapshots, cursor moves, run/submit actions and verdicts — normalized to start at "GO".
- Stored in Supabase Storage, preloaded on monitor pages; replay driven by the synchronized race clock through the same read-only editor component used for live contestant streaming (so live and tourist look identical and can be overlaid/styled freely).
- Capture: a capture-enabled instance of the race editor (preferred) or transcription from a screen recording. Solve time stored in problem meta for the leaderboard diff.

### 5b. Webcam streaming (v1)
- Contestant laptops publish webcam via LiveKit; monitor pages subscribe and composite the feeds next to the editor mirrors.

### 6. Data model (Postgres)
`events` (id, name, secret, settings) → `stations` (event, role/device) → `contestants` (name, country, station, event) → `races` (event, problem, started_at, state) → `submissions` (race, contestant, lang, source, verdict, submitted_at, is_first_ac) → `leaderboard` = view over first-AC times + tourist times.

## Feedback loop / testing
- Playwright e2e for the golden path (check-in → run samples → submit → leaderboard) run in CI on every PR.
- Judge correctness suite: replay known AC/WA/TLE submissions per problem in CI.
- Periodic Devin testing-agent sessions that click through the app on preview deploys and report issues.
- Vercel preview deploys per PR for quick review on real hardware.

## Build order (rough milestones)
1. **Skeleton**: Next.js app + Supabase + event creation/join links + role pages.
2. **Judge v1** on a VM: run C++/Python samples with debug flags, CF checker, custom tests.
3. **Race loop**: countdown sync, timer/DQ, submit + full-test judging, congrats + leaderboard, 3 hand-made problems for testing.
4. **Monitors**: editor streaming, timer, leaderboard, idle slides, confetti; tourist playback.
5. **Problem pipeline**: sub-agent batch over 10 problems + validation (200-problem selection deferred).
6. **Webcams + polish**: LiveKit face streaming, theming pass, latency tuning, venue dry-run.

## Key risks
- **Sample-run latency** (C++ compile) — mitigated by warm VM, compile cache, `-O1` debug builds; measure early.
- **Generated-test quality** — the AC/WA/TLE validation step is the safety net; manual review of flagged problems.
- **Venue Wi-Fi** — everything the race needs at runtime lives on our own server + preloaded assets; graceful WS reconnect; worst case the judge VM could be swapped for an on-site box.
- **Clock sync** — server-authoritative time with offset estimation, not device clocks.
