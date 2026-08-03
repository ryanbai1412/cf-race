-- Statement-pane scroll events: payload {frac} (0..1 scroll fraction), so
-- replays can mirror what part of the problem the contestant was reading.
alter table public.solo_editor_events
  drop constraint if exists solo_editor_events_kind_check;
alter table public.solo_editor_events
  add constraint solo_editor_events_kind_check
    check (kind in ('snapshot','run','run_result','tab','scroll'));

alter table public.race_editor_events
  drop constraint if exists race_editor_events_kind_check;
alter table public.race_editor_events
  add constraint race_editor_events_kind_check
    check (kind in ('snapshot','run','run_result','tab','scroll'));
