-- Rich replay events: run/compile results and console-tab views, so replays
-- can show what the contestant ran and which tab they were looking at.
alter table public.solo_editor_events
  drop constraint if exists solo_editor_events_kind_check;
alter table public.solo_editor_events
  add constraint solo_editor_events_kind_check
    check (kind in ('snapshot','run','run_result','tab'));
alter table public.solo_editor_events
  add column if not exists payload jsonb;

alter table public.race_editor_events
  drop constraint if exists race_editor_events_kind_check;
alter table public.race_editor_events
  add constraint race_editor_events_kind_check
    check (kind in ('snapshot','run','run_result','tab'));
alter table public.race_editor_events
  add column if not exists payload jsonb;
