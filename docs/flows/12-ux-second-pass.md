# UX Second Pass: Unified App — Every User Flow

A systematic walk of every persona and journey through the unified app
(shipped per `11-unified-app-detailed.md`), auditing what exists today,
what's rough, and what's missing. Each flow lists **State** (what the code
does now), **Friction** (observed or predicted pain), and **Proposals**
(ranked: P0 = fix soon, P1 = high-value, P2 = nice-to-have).

Personas used throughout:

| Persona | Description |
|---|---|
| **Visitor** | Logged-out, first touch, maybe from a shared link |
| **Anon practicer** | Practices without an account, same browser |
| **Grinder** | Signed-in returning user, practices daily, cares about times |
| **Duelist** | Signed-in, races friends 1v1 |
| **Organizer** | Creates booth events, runs the admin console |
| **Contestant** | Booth participant at an event station (no login) |
| **Spectator** | Follows a share link `/r/<token>`; may never sign in |
| **Curator** | Logged-in user policing the problem bank (invalidations) |

---

## 1. First touch & onboarding

### 1.1 Visitor lands on `/`
**State:** Hero pitch, "Sign in with Google", "Just practice" → random
visible problem's solve page. Auth-gated pages redirect here with `?next=`.

**Friction:**
- The landing shows zero product: no screenshot, no live replay, no sample
  race. "Race the fastest coders alive" is a claim without proof.
- "Just practice" throws the visitor straight into a pre-run screen with a
  camera permission prompt — the scariest possible first interaction.
- No explanation of what a "run" is (3-minute timer, recording) until the
  pre-run card.
- If Google OAuth fails, `?auth_error=1` is appended but nothing renders it.

**Proposals:**
- **P0** Render a visible error toast/banner when `auth_error=1` is present.
- **P1** Embed a looping muted demo (a real replay of a fast solve, or a
  15-second screen capture) on the landing — the replay player already
  exists; a hardcoded shared token would do.
- **P1** "Just practice" should land on a *problem picker lite* (3 curated
  easy problems + "random") rather than a random pre-run screen, so the
  first decision is "which problem", not "allow camera?".
- **P2** Add a "How it works" strip: solve → replay → share, three icons.

### 1.2 Visitor arrives via a share link `/r/<token>`
**State:** Read-only replay (or duel review), noindex, no navbar CTA beyond
the logo.

**Friction:**
- This is the app's single best acquisition surface and it dead-ends: no
  "try this problem yourself" and no sign-in prompt anywhere.
- No OG/social meta — a pasted link into Discord/Twitter renders as a bare
  URL, wasting the wow factor.
- Revoked/invalid token → generic 404 page with no path back into the app.

**Proposals:**
- **P0** Footer CTA on `/r/<token>`: "Race this problem yourself →
  `/problems/<id>/solve`" + "Sign in to keep your own replays".
- **P1** OG meta tags on `/r/<token>`: problem name, outcome, solve time
  ("AC 1:23 on 1681B — cf racing"). Static text is enough; an OG image can
  come later. Keep noindex.
- **P1** Custom 404 for dead share tokens: "This replay link was revoked or
  never existed" + Practice/Home buttons.

### 1.3 First signed-in session (empty account)
**State:** Home shows zeroed stats and "solve your first problem" CTA.

**Friction:** Stats strip of `0 / 0–0 / 0` is demoralizing; the three quick
actions have equal visual weight even though a new user should practice
first.

**Proposals:**
- **P2** Hide the stats strip until ≥1 finished session; replace with a
  short checklist (solve one problem → watch your replay → share it).

---

## 2. Anonymous practice lifecycle

### 2.1 Run → result → replay
**State:** Anonymous runs work end-to-end; session ids stored in the
httpOnly `cfr_anon_sessions` cookie (last 50); replay accessible in-browser;
cookieless access to the replay API 404s.

**Friction:**
- The result page for an anonymous run has **no sign-in nudge** — the PRD
  (§9 pass 1) explicitly calls for "Sign in to keep your history" here, and
  it's the moment of highest motivation.
- No Share button for anonymous runs (correct — shares need an owner), but
  nothing explains *why* they can't share, which reads like a missing
  feature.
- The 50-session cookie cap silently drops the oldest replays; no user has
  been told this exists.

**Proposals:**
- **P0** Result page (anonymous): add a card — "Sign in with Google to keep
  this run, see your history, and share replays." Sign-in `next` should
  return to the result/replay so the user sees claiming worked.
- **P1** Replay page (anonymous session): same nudge in the header where the
  Share button would be.
- **P2** When the cookie is ≥40 ids, surface "your oldest anonymous runs
  will stop being replayable — sign in to keep them permanently".

### 2.2 Claiming on sign-in
**State:** OAuth callback stamps `user_id` on cookie ids and clears the
cookie; legacy localStorage ids claimed once from home.

**Friction:**
- Claiming is silent. The user never learns their anonymous runs were saved.
- Legacy localStorage claiming only fires on `/` (home) — a user who signs
  in from a replay page and never visits home won't get their old runs.

**Proposals:**
- **P1** Post-claim toast/banner on first page after OAuth: "Claimed N
  practice runs from this browser" (callback can set a short-lived cookie
  the shell reads once).
- **P2** Mount `LegacyClaim` in the shell layout (fires for any signed-in
  page view), not just home.

### 2.3 Cross-device reality check
**State:** Anonymous history is browser-bound (cookie); replay on another
device 404s, which is correct but surprising.

**Proposal:** **P2** Anonymous replay pages could show "only viewable in the
browser that recorded it — sign in to access anywhere".

---

## 3. Practice: problems bank & solving

### 3.1 `/problems` discovery
**State:** Table with status filters (all/unsolved/solved/attempted/
invalidated), `/`-to-search, sort by id/rating/time, remembered filter.

**Friction:**
- Tags are fetched but not rendered — `multitest` matters to solvers
  (multi-test-case parsing changes the template you start from).
- No rating-range filter; sort-by-rating with mixed 800s and 1600s is a poor
  substitute for "show me 1000–1200".
- "attempted" conflates timeout-DNF with abandoned; a grinder wants to retry
  real DNFs, not runs they walked away from.
- Best-time column exists only inside the status text; no tourist-time
  comparison ("you: 1:45 / tourist: 0:52") even though `tourist_time_ms` is
  already selected.
- No indication which problem the "Practice" quick-action would pick, so the
  bank and the home button feel disconnected.

**Proposals:**
- **P1** Render tag chips per row; make them click-to-filter.
- **P1** Show tourist time next to your best ("you 1:45 · tourist 0:52") —
  it's the product's core fantasy and the data is already loaded.
- **P2** Rating bucket filter (Div2 A/B/C style buckets or a range slider).
- **P2** Split "attempted" visual state: DNF (red-ish) vs abandoned (grey).

### 3.2 `/problems/<id>` detail
**State:** Statement preview, your session list, invalidate toggle with
reason banner, Solve button.

**Friction:**
- The statement pane is a fixed `60vh` box; long statements scroll inside a
  small window while the page around them is mostly empty.
- Session history shows only your runs — no global context (fastest solve,
  how many people solved it). Fine for now (small userbase) but the columns
  exist.
- Invalidate uses `window.prompt` — jarring, unstyled, and easy to dismiss
  accidentally.

**Proposals:**
- **P1** Replace `window.prompt` with a small inline form/popover (existing
  Input + Button components).
- **P2** Make the statement pane fill available height (flex) instead of
  fixed `60vh`.
- **P2** "Best solves" mini-leaderboard per problem (top 5 solve times) —
  cheap query, high grinder value.

### 3.3 Solve flow `/problems/<id>/solve`
**State:** Pre-run card (language, camera preview, Start), countdown, race
screen, result page with replay/run-again/next/back links.

**Friction:**
- **Navigating away mid-run is silent data loss.** No `beforeunload` guard;
  the session becomes abandoned 15 minutes later. A misclick on the logo
  (not shown in-race, but browser back is one gesture away) kills the run.
- The pre-run screen requests the camera immediately on mount; a user who
  wanted to read the problem first can't (statement isn't visible pre-run).
- Result page next-problem is the next id in sequence, not "next unsolved" —
  a grinder who solved 1236A gets pushed to 1236B regardless of status.
- After AC, there's no immediate time comparison vs your previous best or
  the tourist time — the single most motivating number.

**Proposals:**
- **P0** `beforeunload` confirm while a run is active ("Your run will be
  abandoned").
- **P1** Result page: show delta vs your previous best and vs tourist time
  ("new PB! 0:26.7, tourist 0:19.4").
- **P1** "Next problem" → next *unsolved* visible problem (fall back to next
  id).
- **P2** Let the pre-run screen show the statement (read-before-start
  changes what "3-minute timer" means competitively — decide deliberately:
  either show it and start the timer on reveal, or explicitly label "the
  statement is revealed when the clock starts").

### 3.4 Session timeout semantics (user-facing)
**State:** 15-min lazy abandon on server reads; abandoned badge is neutral
grey; abandoned never counts as solved.

**Friction:**
- A user who leaves a tab open >15 min and comes back can keep typing into a
  dead session — the client doesn't know it was abandoned; submits will
  still work against an `outcome=abandoned` row (finish overwrites outcome).
- Nothing in the UI explains what "Abandoned" means.

**Proposals:**
- **P1** Client-side idle check on the race screen: after 15 min without
  events, show "this run timed out" and route to the result state instead of
  letting a zombie run continue.
- **P2** Tooltip on the Abandoned badge: "run was inactive for 15+ minutes;
  replay kept, doesn't count as a solve".

---

## 4. Sessions & replays

### 4.1 `/sessions` history
**State:** Filter chips (kind, outcome), 25/page pagination, shared badge,
replay links.

**Friction:**
- No problem-name search; finding "that run of 1681B last week" means
  paging.
- Duration column was speced (PRD §5.2) but only solve time renders.
- The `shared` badge is informational only — you can't manage the share from
  the list (must open the replay).
- No date grouping; a wall of 25 uniform rows.

**Proposals:**
- **P1** Text filter by problem id/name (client-side, data is loaded).
- **P2** Make the `shared` badge a popover with Copy link / Revoke (reuse
  `ShareButton`).
- **P2** Group rows by day ("Today", "Yesterday", date headers).

### 4.2 `/replay/<sessionId>` private replay
**State:** Full replay player; Share button (owner); back-link to problems.

**Friction:**
- Back link is always "← problems", even when you arrived from `/sessions`
  or a duel — breadcrumb amnesia.
- No "run this problem again" action from a replay — watching a failed run
  is the exact moment to retry.
- Owner viewing an *abandoned* replay gets no explanation banner.

**Proposals:**
- **P1** Add "Race again" button on the replay header →
  `/problems/<id>/solve`.
- **P2** Back link respects a `?from=` param (sessions/problems/duels).

### 4.3 Sharing lifecycle
**State:** Owner mint/copy/revoke on replays; match shares on duel review;
public `/r/<token>` with noindex; revoke → 404; re-share mints fresh token.

**Friction:**
- Mint copies the link and toasts, but there's no persistent visual state on
  the page showing "this replay is public" beyond the button swap.
- No share management overview — a user who shared 10 replays has no single
  place to see/revoke them all.
- Result page after a run has no Share button (PRD §5.4 wanted share on
  result pages too); the user must click into the replay first.

**Proposals:**
- **P1** Add `ShareButton` to the post-run result page (logged-in, owner).
- **P2** "Shared replays" section or filter on `/sessions` (share status
  already fetched).

---

## 5. Duels

### 5.1 `/duels` arena
**State:** Create room, join-by-pasted-link input, match history with
review/share, solved list, recordings list.

**Friction:**
- Join-by-link requires a full URL paste; friends on voice chat want a short
  code ("room 7f3a").
- Match history rows don't show solve times — "won" without "by how much"
  buries the drama.
- No pending-invite state: after creating a room and sending a link, the
  creator sits in the lobby with no way back to /duels without abandoning
  context (does leaving the lobby kill the room? unclear to users).
- "Problem bank" button routes to the *duel* problems page
  (`/duel/problems`) which now overlaps confusingly with `/problems`.

**Proposals:**
- **P1** Show both players' times on finished match rows ("you 1:12 · them
  1:45").
- **P1** Merge `/duel/problems` into `/problems` (it predates the unified
  bank; one bank should serve both) — or relabel the button "Pick-score
  bank" if it stays.
- **P2** Room short-codes (first 6 hex chars) accepted in the join box.

### 5.2 Lobby & in-duel
**State:** Existing flow untouched: ready-up → countdown → race → AC
notifications → review. 15-min abandon applies per session.

**Friction:**
- Opponent disconnect mid-race is only discovered via silence; the 15-min
  timeout is an eternity in a 3-minute race format.
- No rematch: the review page dead-ends the pair who just raced (PRD §9 pass
  2 explicitly wants this).
- Lobby has no "copy invite link" affordance re-surfaced after creation (it
  copies once on create).

**Proposals:**
- **P0** "Rematch" button on `/duel/review/<matchId>` and on the duel-end
  screen: creates a room and (if possible) notifies via the existing
  realtime channel; at minimum it pre-copies the new invite link.
- **P1** In-race presence indicator using existing LiveKit/webcam signal —
  "opponent disconnected" after ~30s of silence, with their timer still
  running (they can rejoin).
- **P2** Persistent "copy invite" button in the lobby.

### 5.3 Review & match sharing
**State:** Side-by-side synced replay, navbar shown, invalidate toggle,
match-level Share.

**Friction:**
- The invalidate control sits in the review header next to Share — a
  spectator-facing screen exposes a destructive curator tool with equal
  prominence.
- Winner banner shows time but not the margin.

**Proposals:**
- **P2** Move invalidate behind an overflow ("⋯") menu on review.
- **P2** Show margin in the winner chip ("won by 0:33").

---

## 6. Events (organizer + contestant)

### 6.1 `/events` organizer console
**State:** Create form, list of own events with admin link + device-links
panel; legacy events (null `created_by`) hidden but functional.

**Friction:**
- No event status (upcoming/live/done) — the PRD speced a status column;
  currently only a created date renders.
- Device links are copy-only; on-site setup means emailing yourself links or
  QR-scanning nothing. Booth setup is done from a laptop to N machines.
- No indication of activity (races run, contestants checked in) per event.
- A legacy event owner has no way to claim their old events.

**Proposals:**
- **P1** Per-event activity summary (races count, last race time) — one
  query against `races`.
- **P1** QR codes for device links (client-side QR lib, no backend) — the
  actual booth workflow is pointing a station's browser at a link.
- **P2** Derived status chip: "live" if a race ran in the last 2h, else
  "idle".
- **P2** "Claim event" via secret: pasting an admin link while logged in
  offers to stamp `created_by`.

### 6.2 Booth contestant flow
**State:** Untouched, correctly navbar-free, secret-cookie gated.

**Friction:** A contestant who enjoyed the booth has no bridge to the
product: the station result screen doesn't mention that this exists as an
app they can use at home.

**Proposal:** **P2** Post-race station screen: small QR → landing page
("race again at home"). Booth is the funnel; use it.

---

## 7. Cross-cutting

### 7.1 Navigation coherence
- Navbar active state works; but `/replay/<id>` and `/duel/review/<id>`
  highlight nothing — acceptable, they're leaf pages.
- **P2** The logo → `/` for signed-in users renders the dashboard; for
  anonymous *practicers* it renders the marketing landing every time.
  Consider: anonymous user with ≥1 cookie session gets a slim "your recent
  anonymous runs" strip on the landing instead of pure marketing.

### 7.2 Loading, empty, error states
- Replay/review loading states exist ("Loading replay…"). Problems/sessions
  server pages have no skeletons but render fast; fine.
- **P1** Global error toast for failed fetches in `DuelHome`/`SoloReplay`
  (currently silent `catch(() => {})` in places — a dead API looks like an
  empty account).

### 7.3 Mobile
- Navbar collapses; tables (problems/sessions) will overflow on narrow
  screens — rows have 6+ inline elements.
- Solving on mobile is not a real use case (Monaco + camera), but *viewing*
  is: replays and share links will be opened on phones from chat apps.
- **P1** Ensure `/r/<token>` and `/replay/<id>` degrade usably on mobile
  (stack video above editor; the editor pane readable). Test at 390px.
- **P2** Problems/sessions rows: collapse metadata under the title line on
  small screens.

### 7.4 Permissions honesty
- Anyone logged-in can invalidate problems (deliberate booth-team decision,
  PRD §4.2) — fine at current scale, but the affordance appears on every
  problem page for every user.
- **P2** Gate invalidate UI behind a `curator` flag (env allowlist of user
  ids is enough) before any public launch.

### 7.5 Stats integrity
- Abandoned excluded from solves ✓. But home "Duel record" counts only
  finished matches with a winner; both-DNF matches vanish from W–L (correct)
  yet also from "matches played" on /duels (shows played = finished ones
  including DNF — inconsistent denominators between home and /duels).
- **P2** Unify: played = finished matches (any result); record = W–L–D.

---

## 8. Prioritized backlog (rollup)

**P0 — do next**
1. Anonymous result-page sign-in nudge (§2.1) — the PRD's own pass-1 item.
2. `beforeunload` guard during active runs (§3.3).
3. Rematch button on duel review/end (§5.2) — PRD pass-2 item.
4. Share-link landing CTA on `/r/<token>` (§1.2).
5. Render `auth_error=1` (§1.1).

**P1 — high value**
6. Post-run PB/tourist time deltas (§3.3).
7. Share button on the result page (§4.3).
8. Tag chips + tourist-time column in `/problems` (§3.1).
9. OG meta on share links (§1.2).
10. Claim-success feedback after OAuth (§2.2).
11. Client-side idle timeout on the race screen (§3.4).
12. Opponent-disconnect indicator in duels (§5.2).
13. Both players' times in duel match history (§5.1).
14. QR codes + activity summary on `/events` (§6.1).
15. Mobile-usable replay pages (§7.3).
16. Merge or relabel `/duel/problems` vs `/problems` (§5.1).
17. Next-unsolved "next problem" (§3.3); sessions text filter (§4.1);
    landing demo replay (§1.1); inline invalidate form (§3.2); surface
    silent fetch errors (§7.2).

**P2 — later**
Everything else above: rating buckets, per-problem leaderboards, share
management view, room short-codes, curator gating, date-grouped sessions,
booth→app QR funnel, stats denominator unification, empty-state checklist,
statement-pane sizing, breadcrumbs.
