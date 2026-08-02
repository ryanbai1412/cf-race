# Flow PRD: Contestant Check-in & Warm-up Sandbox

## Goal
A walk-up contestant gets from "stranger at the booth" to "ready to race" in under a
minute, having typed their name/country and touched the editor once.

## Entry
Station page (`/e/<id>/station/<n>`) when no contestant is checked in at this station,
or after the previous race finished and was reset.

## Flow

### Step 1 — Check-in
- Full-screen card, huge heading: "Ready to race?"
- Fields: **Name** (required, ≤40 chars) and **Country** (searchable select of
  ISO countries with flag emojis; optional).
- CTA: "Continue". Creates a `contestants` row bound to this event + station role.
- The other station's check-in state is visible in a subtle status line
  ("Station 2: Alice checked in ✓ / waiting…") via realtime, so staff can see both
  laptops are ready.

### Step 2 — Warm-up sandbox
- Layout identical to the race screen (problem left / editor right) so nothing is new
  at GO, but loaded with a trivial demo problem ("A+B") and a banner: "Warm-up — get
  comfortable. The real race starts when the countdown hits zero."
- Everything works exactly like the race: language picker (C++ / Python), starter
  template, Run on samples, custom test, output panes. Submissions disabled.
- A "I'm ready" button marks the station ready (shown to admin + other station).
- No time pressure; admin launches the countdown when both stations are ready.

### Step 3 — Countdown handoff
- When the admin starts a race, both stations (and monitors) show a full-screen
  3-2-1-GO overlay driven by the server clock; at GO the sandbox is replaced by the
  actual race problem with a fresh editor (template preserved language choice).

## UX details
- Enter key advances; autofocus name field; no dead ends (Back link on warm-up
  returns to check-in to fix a typo).
- Country flags shown next to names everywhere (leaderboard, monitors).
- All state changes broadcast on the event's realtime channel: `contestant_checked_in`,
  `station_ready`, `race_countdown`, `race_started`.

## Data
- `contestants` insert on check-in; `station_ready` kept in channel presence (not DB).
- Active contestant per station = most recent contestant row for (event, station)
  not yet attached to a finished race.
