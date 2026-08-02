# Flow PRD: Admin Console

## Goal
One page for booth staff to run the whole show: see station readiness, pick a problem,
launch the countdown, and recover from anything with one click.

## Layout (`/e/<id>/admin`)
1. **Header** — event name + admin badge.
2. **Device links** — copy links for stations/monitors/admin (flow 01).
3. **Stations panel** — live cards for Station 1/2: checked-in contestant
   (name/flag) or "empty", updated in realtime.
4. **Race control**
   - No active race: problem picker (dropdown of the problem bank, shows id, name,
     rating, tourist time, special-judge flag), timer override input (defaults to the
     problem's `race_timer_sec`), and a big **Start race** button (disabled until at
     least one station has checked in). Starting = 5s countdown broadcast to all.
   - Active race: problem name, race phase (countdown/racing/overtime), live per-station
     status (AC at mm:ss / racing / DQ), time remaining, and **Finish & reset** button
     (marks race finished, DQs unsolved, returns stations to check-in).
5. **Recent results** — last few races with solve times (compact list).

## Behaviors
- Poll + realtime like every client; all controls are API calls guarded by the event
  cookie.
- "Start race" errors surface as toasts (e.g. another race active, nobody checked in).
- Reset is idempotent and always available — the panic button.
