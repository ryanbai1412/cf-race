# Flow 08 — Replay activity history

## Goal

Replays (solo and event races) should show not just the code and webcam, but
*what the contestant did*: every compile/run of the samples or custom input,
every submission, and which console tab they were looking at — with the
ability to jump the replay to any of those moments.

## Recording

The station/solo recorders already persist timestamped editor snapshots and
`run` markers. This flow adds two richer event kinds to the same event logs
(`solo_editor_events`, `race_editor_events`):

- `run_result` — written when a run finishes, with a compact JSON `payload`
  (`RunSummary`): target (samples/custom), compile ok, overall verdict,
  passed/total, per-test verdicts + times, compile stderr (capped).
- `tab` — written whenever the console tab changes (user click or the
  auto-switch on Run/Submit), payload `{ tab }`.

Submissions/verdicts continue to come from the submissions tables, so the
replay log merges: snapshots, run, run_result, tab, submit, verdict.

## Replay UI

- **Right sidebar** (under the webcam video): a scrollable "Runs &
  submissions" list of every run, compile, and submission in the session.
  Each row is an accordion: collapsed it shows label + verdict + passed/total
  + timestamp; expanded it shows per-test verdicts/times or the compile
  error. Rows after the current playback position are dimmed. Clicking a
  row's timestamp jumps the replay clock (editor + webcam) to that moment.
- **Bottom-left status strip** (above the transport controls): the console
  state at the current playback moment — which tab the contestant was
  viewing, a pulsing "running…" indicator between a run and its result, and
  the most recent run/compile summary (label, verdict, samples passed).
- Timeline markers stay as before (run/submit/verdict); tab and run_result
  events don't add markers to avoid clutter.

## Edge cases

- Old sessions without run_result/tab events: the list falls back to
  submissions only; the status strip shows "no runs yet".
- Submissions still pending at recording end render as PENDING.
- Payloads are capped (20 KB) server-side; compile stderr capped at 4 KB.
