-- Per-keystroke editor deltas: payload {changes:[{o,l,text}]} relative to the
-- previous editor state, with periodic full snapshots as keyframes.
alter table public.solo_editor_events
  drop constraint if exists solo_editor_events_kind_check;
alter table public.solo_editor_events
  add constraint solo_editor_events_kind_check
    check (kind in ('snapshot','delta','run','run_result','tab','scroll'));

alter table public.race_editor_events
  drop constraint if exists race_editor_events_kind_check;
alter table public.race_editor_events
  add constraint race_editor_events_kind_check
    check (kind in ('snapshot','delta','run','run_result','tab','scroll'));
