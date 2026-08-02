# Flow PRD: Finish Screen & Leaderboard

## Goal
A satisfying payoff moment: your time, your rank, and how you did against your rival
and against tourist — then a clean reset for the next contestant.

## Trigger
- First AC (win state) — confetti burst, then finish card.
- Timer expiry without AC (DNF state) — sympathetic, no confetti.

## Finish card (station)
- Big verdict: "ACCEPTED" (green, monospace) or "TIME'S UP" (neutral).
- Your time: `01:47.3` huge; below, deltas: "vs <rival name>: −0:12" (green if won)
  and "vs tourist: +1:05" (almost always red — that's the joke).
- Both-station awareness: if the rival is still racing, show "Waiting for <name>…"
  with their live timer; the card completes when both finish or time out.
- Leaderboard section: top-10 fastest solves for THIS problem (name, flag, time,
  delta vs tourist), current contestant's row highlighted; if outside top-10 show
  "#23 of 87" with their row appended.
- Footer: "Next racers — see the staff!" + a subtle reset countdown (admin resets, or
  auto-reset after N minutes idle).

## Leaderboard rules
- Ranked by solve time (first-AC timestamp − race start), ascending; DQ/DNF excluded.
- Tourist's time comes from problem meta (`tourist_time_ms`) and is pinned as a
  ghost row ("tourist 🇧🇾 — 0:41") at its rank position.
- Same leaderboard data feeds the monitor cycling views.

## Reset
- Admin "Reset stations" (or auto-reset) returns both stations to check-in (flow 02).
- Contestant + submission rows are kept forever (event history).
