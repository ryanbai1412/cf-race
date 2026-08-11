# Flow PRD: Genna Problems & Event Monitors v2

## Goal
Event races should only use problems Genna (Gennady "tourist" Korotkevich) has
solved on this platform, and the booth monitors should show contestants racing
Genna head-to-head — his webcam + code replay next to theirs — with a leaderboard
of best solve-time deltas vs Genna. A passer-by seeing a monitor from across the
room should immediately get: *people are racing the world champion, and here's
who's come closest.*

## Part 1 — Genna problems (build first)

### Concept
A **Genna problem** is a problem with a designated *Genna reference session*: a
`sessions` row (solved outcome) recorded by Genna's account, whose replay
(session_events) and webcam recording become the "ghost" shown on monitors, and
whose `solve_ms` is the reference time for the leaderboard delta.

Genna logs in with Google like any user, solves problems in solo mode, and his
runs land in `sessions` with his `user_id`. Admins then bless those sessions as
reference sessions.

### Data model
```sql
-- One designated reference session per problem.
create table public.genna_problems (
  problem_id text primary key references public.problems(id),
  session_id uuid not null references public.sessions(id),
  created_at timestamptz not null default now()
);
```
- One row per problem (PK) — remarking replaces the row (upsert), so "which
  session is the ghost" is never ambiguous. No explicit "Genna user" flag:
  admins act on sessions (usually via a per-user bulk action), not identities.
- `sessions.solve_ms` on the referenced session is the Genna time. No copy —
  single source of truth.
- The legacy `problems.tourist_time_ms` + `tourist/<id>.json` storage path stays
  as a fallback for problems with scripted tourist logs but no real Genna
  session; new code prefers `genna_problems`.

### Admin flows (in /admin, new "Genna" tab)
1. **Pick a user** (search by email/name — Genna's Google account) → see all
   their solved sessions: problem, solve time, date, has-webcam, replay link.
2. **Bulk: "Mark all as Genna references"** — for every problem where this user
   has ≥1 solved session, set the **fastest** one (ties → latest) as the
   reference. Preview before confirm; existing references are replaced only
   when the checkbox "overwrite existing" is on.
3. **Per-row**: `Set as reference` / `Replace` / `Remove reference`.
4. **Coverage view** — which problems are Genna-ready, which this user solved
   but aren't blessed, which have no solve. The "what can this event run" list.
5. **Guard rails** — only solved sessions with replay events can be referenced;
   references cascade-delete with their problem/session; warn (not block) when
   the session has no webcam recording.

### API
- `GET /api/admin/genna?userId=` — a user's solved sessions + current references.
- `POST /api/admin/genna/reference` — `{problemId, sessionId}` set/replace;
  `{problemId, remove: true}` to clear.
- `POST /api/admin/genna/bulk` — `{userId, overwrite, dryRun}`.
All admin-gated (same guard as /admin).

### Event problem picking
- `startRace` rejects problems without a Genna reference when the event requires
  one (event setting `gennaOnly`, default **on** for new events).
- The event admin console's problem dropdown filters to Genna-ready problems
  (with a toggle to show all, disabled when gennaOnly).

## Part 2 — Monitors v2 (spec, build after Part 1)

Two physical monitors, positioned for a queue that faces the **right** monitor
head-on and glances **left** for context.

### Left monitor — context: leaderboard + problem statement
Split 50/50:
- **Left half: leaderboard** titled **"RACE tourist"** with *tourist* stylized
  in Codeforces Legendary Grandmaster style (black first letter, red rest —
  `t`ourist with LGM colors). Columns: contestant flag · contestant name ·
  problem id (e.g. `1234A`, signalling Codeforces) · their time · tourist's
  time · **delta** (green negative = beat him, red positive).
  Sorted by delta ascending; one best row per contestant+problem.
- **Right half: problem statement** of the active race — must ALWAYS be fully
  visible: auto-fit (scale text down to fit height) or slow auto-scroll loop if
  it can't fit; never a cut-off statement.

### Right monitor — the race: webcams + code, three-way split
- **Top row: webcams** — contestant's live webcam next to Genna's recorded
  webcam (replay synced to race clock), each labeled (name/flag vs
  "tourist 🇧🇾").
- **Bottom: code** — contestant's live editor mirror and Genna's replayed
  editor side by side.
- Layout is a three-way split (webcam strip on top, two code panes below).
- Verdict moments: contestant AC → confetti + delta vs Genna; Genna's replay
  AC → subtle flash + "tourist solved it".

### Idle mode (no active race)
Cycles: explainer ("RACE THE WORLD CHAMPION…" + how to join) → leaderboard →
warm-up mirror.

### Genna leaderboard data
- Event sessions with outcome=solved joined to `genna_problems` → reference
  `solve_ms`; delta = contestant solve_ms − genna solve_ms.
- API: `GET /api/leaderboard/genna?eventId=` (event-secret gated).

## Implementation order
1. Migration: `genna_problems`.
2. Admin APIs + /admin Genna tab (flows 1–4).
3. `startRace` gennaOnly gating + admin console filter.
4. Monitor right pane: reference-session replay + recording playback.
5. Genna leaderboard API + idle-mode slide.

## Open questions
1. Genna's webcam on monitors: replay his recorded webcam (synced to race
   clock), or static photo if no recording? (Proposed: recording when present,
   else his avatar + name card.)
2. Should solo/duel surfaces also show "Genna's time" once a reference exists
   (replacing tourist_time_ms)? (Proposed: yes, unified.)
3. Leaderboard scope: per-event only, or global across all events? (Proposed:
   per-event on monitors, global later on /problems.)
