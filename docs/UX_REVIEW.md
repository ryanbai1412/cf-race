# UX Review — booth walkthrough (all personas)

Method: walked every flow locally in the browser as admin, contestant (station 1/2),
and spectator (monitor A/B): create event → check-in → warm-up → race start →
run/submit → AC finish → DNF timeout → reset → idle monitors.

## P0 — fixed in this pass

1. **Math renders as raw LaTeX in problem statements.**
   `\(a_1, a_2, \ldots, a_n\)` shown literally in every scraped statement — the
   single biggest readability problem for a first-time contestant.
   → Render with KaTeX (auto-render on the statement container).

2. **DNF finish screen shows backwards copy.**
   When you time out and your rival solved it, the card said
   "vs Alice: *you finished, they didn't*". Insulting *and* wrong.
   → Correct copy for all four outcomes (both solved / you only / them only / neither).

3. **Scraped statement cruft.**
   The CF header block (title/limits, duplicated by our own pane header) and the
   "epigraph" (random SoundCloud song link) render inside the statement.
   → Hidden via `.cf-statement .header` / `.epigraph` CSS.

4. **Dead black webcam box on monitors.**
   When a station has no camera (or permission denied), the monitor shows a solid
   black rectangle that looks broken.
   → PiP card now hidden until a live video track is actually attached.

## P1 — fixed in this pass

5. **No rival awareness during the race.**
   A contestant can't tell whether their rival has already solved it — the key
   dramatic tension of the format.
   → Station top bar now shows "vs Bob — racing…" / green "Bob ✓ AC 1:33.6".

6. **Admin shows "racing…" + frozen 00:00 after the timer expires.**
   Staff can't tell the race is over and stations are stuck on "TIME'S UP".
   → Timer shows red "OVERTIME"; station chips show "time up — no AC"; the
   finish button is visually promoted once the race is over.

7. **No way to swap contestants between races.**
   After a reset the previous contestant stays checked in on the warm-up screen;
   a new walk-up visitor sees someone else's name with no way to fix it.
   → "Not Alice? Switch player" button in the warm-up banner returns to check-in.

8. **Monitor idle leaderboard too small to read from a distance.**
   Rows were laptop-sized (~16px) on a screen meant to attract passers-by.
   → `size="lg"` leaderboard variant on monitors (bigger flags, names, times).

9. **Admin console blank while loading.**
   First paint shows only device links, then stations/race control pop in.
   → Explicit "Connecting…" placeholder.

## P2 — recommended next (not done; needs product decisions or bigger changes)

- **Post-AC overlay on the monitor never clears** — "ALICE SOLVED IT" covers the
  code until reset; consider auto-fading to the leaderboard after ~15s.
- **Auto-reset after N idle minutes** (PRD flow 04) isn't implemented — booth
  relies entirely on staff remembering to hit reset.
- **QR codes next to device links** (PRD flow 01, v1.1) would remove the
  copy/paste dance during booth setup.
- **Ready state not surfaced to admin** — "I'm ready" toggles only local state;
  the admin stations panel should show ready/warming-up badges (needs presence).
- **Editor font-size control on stations** — a 15px default is fine but an
  A−/A+ toggle would help on shared booth laptops.
- **Custom-test tab has no sample prefill** — a "copy sample 1" shortcut would
  save contestants the round trip to the statement pane.
- **Countdown overlay is only 1.2s of "GO"** — consider a real 3-2-1-GO with
  audio for the booth (PRD flow 02/03 describes 3-2-1).
- **Idle explainer could show a live QR / "how to join" step list** — currently
  it says "ask the booth staff", which is fine but passive.
