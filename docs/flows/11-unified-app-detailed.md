# Flow PRD v2: Unified App — Detailed Flows

Supersedes the outline in `10-unified-app.md`. Decisions locked in:
- Replays are **private by default**; an explicit **Share** button mints a
  public share link (separate token URL — the session UUID URL itself never
  becomes public).
- **Anonymous solo** practice (and its replay) stays allowed.
- **Sessions time out after 15 minutes** of inactivity → marked `abandoned`.

---

## 1. Auth & identity

### 1.1 Rules
- Google login via Supabase Auth (pluggable providers later).
- Auth-gated: `/`, `/problems`, `/sessions`, `/duels`, `/events` and their
  subroutes — EXCEPT solo solving + solo replay, which work anonymously.
- Secret-link gated (no login): all `/e/<id>/...` booth pages.
- Share-token gated: `/r/<shareToken>` public replays.

### 1.2 Flows
- Logged-out user hits an auth-gated page → landing hero with product pitch,
  "Sign in with Google", and a "Just practice" button (anonymous solo).
- After login, return to the page they were heading to (`?next=` param).
- Sign out from the avatar menu; returns to landing.
- Anonymous user finishes a solo run → result page nudges "Sign in to keep
  your history"; if they sign in within the same browser session, we
  **claim** their anonymous sessions (cookie holds anonymous session ids;
  claiming stamps `user_id`).

## 2. App shell / navbar

- Persistent navbar: logo → `/`; links Problems, Sessions, Duels, Events;
  right side avatar menu or "Sign in".
- Active-link highlight; mobile: collapses to a menu button.
- Booth pages (`/e/...`) and the race/duel screens themselves do NOT show the
  navbar (full-screen focus); replay and review pages do.

## 3. Home `/`

- Quick actions row:
  - **Practice** → random unsolved non-hidden problem, straight into solve.
  - **Start a duel** → creates room, copies link, goes to lobby.
  - **Create event** → new event + admin console.
- **Recent activity**: last 10 of your sessions (any kind): problem, kind
  badge (solo/duel/event), outcome (solved / unsolved / abandoned), solve
  time, replay link, share status.
- **Stats strip**: problems solved, duel W–L, solo solves this week.
- Empty states: fresh account sees a friendly "solve your first problem" CTA.

## 4. Problems

### 4.1 `/problems` — bank
- Table of non-hidden problems: id, name, rating, tags, pick_score (admin
  only?), your status (unsolved / solved w/ best time / attempted /
  invalidated).
- Filters: unsolved | solved | attempted | invalidated | all; text search;
  sort by id / rating / your solve time.
- Row actions: **Solve** (solo), **Your replays** (if any).

### 4.2 `/problems/<id>` — detail
- Statement preview (same renderer as race view).
- Your history on this problem: every session (kind, date, outcome, time,
  replay link).
- **Invalidate** toggle (logged-in): sets invalidated + reason; excluded from
  random picks (duel + practice); banner shows who/why; un-invalidate
  available. (Anyone logged-in can invalidate for now — booth-team tool.)
- **Solve** button → `/problems/<id>/solve`.

### 4.3 `/problems/<id>/solve` — solo run (replaces `/solo/<id>`)
- Identical to today's solo flow (camera optional, 3-min timer default, 50
  submissions, per-language buffers, full recording).
- Works anonymously; logged-in runs get `user_id`.
- On finish → session result page with replay + (if logged in) Share button.
- Old routes `/solo`, `/solo/<id>`, `/solo/replay/<id>` 301-redirect.

## 5. Sessions

### 5.1 Session lifecycle (all kinds)
- States: `active` → `finished` (solved/out-of-time/gave-up) or `abandoned`.
- **15-minute timeout**: a session with no new `session_events` for 15
  minutes is treated as abandoned. Enforced lazily: any read that encounters
  an `active` session whose `last_event_at < now()-15min` flips it to
  `abandoned` (plus a periodic sweep via pg_cron if available). Abandoned
  sessions keep their events/recording; replay still works; they show as
  "abandoned" everywhere and don't count as solves.
- A user starting a new run of the same problem while another `active`
  session exists: old one is abandoned immediately.

### 5.2 `/sessions` — your history
- All your sessions, newest first; columns: date, problem, kind, outcome,
  solve time, duration, replay, share status.
- Filters: kind, outcome; pagination.

### 5.3 `/replay/<sessionId>` — private replay (replaces `/solo/replay/<id>`)
- Access: session owner, or anyone for anonymous sessions created in that
  browser (cookie), or any participant's opponent for duel sessions, or the
  event secret cookie for event sessions. Otherwise 404 (no existence leak).
- Existing replay UI (editor playback, webcam, console re-render, scroll
  follow, jump-to-time) unchanged.

### 5.4 Sharing
- **Share** button on replay + result pages (owner only): creates
  `session_shares` row `{token, session_id, created_at, revoked_at}` →
  public URL `/r/<token>`.
- `/r/<token>`: read-only replay, no auth required, noindex. Owner can revoke
  (revoked token → 404). Re-sharing after revoke mints a new token.
- Duel review sharing: shares BOTH sessions of the match via one token
  (`match_shares`), since the review is side-by-side.

## 6. Duels

### 6.1 `/duels`
- **Create room** → `/duel/room/<id>` lobby (existing flow).
- Join by pasted link.
- Match history: date, opponent, problem, result (you won / lost / both
  unsolved), review link, share button.

### 6.2 In-duel (existing, unchanged)
- Lobby ready-up → countdown → race → notification on opponent AC → review.
- 15-min timeout applies per-session: an abandoned player forfeits.

### 6.3 Review `/duel/review/<matchId>`
- Side-by-side replay (existing) + Share button (match-level).

## 7. Events

### 7.1 `/events`
- **Create event** (moves off the public landing page; requires login) —
  `events.created_by = user`.
- List of your events: name, created date, status, links: admin console,
  device links panel.
- Events created before this change (null `created_by`) are visible to no
  one's list but keep working via secret links.

### 7.2 Booth flows (unchanged)
- `/e/<id>/join?k=...` cookie gate; stations, monitors, admin as today.
- Event sessions attribute `user_id` only if the contestant happens to be
  logged in (not required).

## 8. Data changes

- `sessions.last_event_at timestamptz` — bumped by event writes (trigger on
  `session_events` insert); backfill from latest event.
- `sessions.state` gains `abandoned` (or reuse outcome enum — implementer's
  choice, keep one source of truth).
- `session_shares (token pk, session_id fk, created_by, created_at,
  revoked_at)`; `match_shares` likewise for duels.
- `events.created_by uuid null` fkey auth.users.
- `problems.tags` (done) — `hidden` excluded from all listings and random
  picks.
- RLS/API: replay reads go through server routes that enforce §5.3 rules.

## 9. UX pass notes (three passes)

**Pass 1 — first-time & anonymous UX:** landing pitch must let people try
without login (anonymous practice) but every post-run screen nudges sign-in
with a concrete benefit ("keep history", "share replays"). Claiming
anonymous sessions on login avoids punishing users who tried first.

**Pass 2 — returning power user (Ryan/Gennady):** home = launcher; every list
links directly into action (solve/replay/review) in one click; duel rematch
button on review page ("Rematch" pre-creates a room with the same opponent);
problems list remembers filter; keyboard-first (/-to-search on problems).

**Pass 3 — failure/edge cases:** abandoned sessions must never look like
losses (distinct badge + excluded from stats); share revocation immediate;
duel opponent disconnecting mid-race → their session times out and review
shows partial replay; event pages must never require login even if the same
browser is logged in as someone else; replay 404s never leak session
existence; camera-denied and upload-pending states already handled — carry
them into the unified result page.

## 10. Rollout

1. Migrations (shares, last_event_at, created_by, abandoned state).
2. Session timeout logic + abandon semantics (server).
3. App shell + navbar + landing/auth.
4. `/problems` (+detail/solve moves), `/sessions`, `/replay/<id>` + `/r/<t>`.
5. `/duels`, `/events` wrappers around existing flows.
6. Redirects from old routes; update internal links.
7. Verify booth flows untouched end-to-end.
