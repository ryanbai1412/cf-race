-- Editor events arrive in batches (up to 1000 rows per insert); the row-level
-- bump trigger did one sessions update per event row. Statement-level with a
-- transition table does one update per batch per session instead.

drop trigger if exists session_events_bump_last_event on public.session_events;

create or replace function public.bump_session_last_event()
returns trigger
language plpgsql
as $$
begin
  update public.sessions s
  set last_event_at = greatest(s.last_event_at, x.max_at)
  from (
    select session_id, max(created_at) as max_at
    from new_events
    group by session_id
  ) x
  where s.id = x.session_id;
  return null;
end;
$$;

create trigger session_events_bump_last_event
  after insert on public.session_events
  referencing new table as new_events
  for each statement execute function public.bump_session_last_event();
