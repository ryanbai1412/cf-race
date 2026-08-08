-- Concurrency invariants enforced in Postgres instead of read-then-write
-- application code.

-- At most one unfinished race per event: two concurrent /api/race/start
-- calls can both pass the "already active?" read, but only one insert wins.
create unique index if not exists races_one_active_per_event
  on public.races (event_id)
  where state <> 'finished';

-- Per-session submission caps: counting then inserting in the app races
-- under concurrent submits, so serialize per session with an advisory lock
-- and enforce the cap where the row is created. Caps mirror
-- src/lib/limits.ts (MAX_SUBMISSIONS / DUEL_MAX_SUBMISSIONS).
create or replace function public.enforce_session_submission_cap()
returns trigger
language plpgsql
as $$
declare
  cap integer;
  used integer;
begin
  if new.kind <> 'submit' then
    return new;
  end if;
  perform pg_advisory_xact_lock(hashtextextended(new.session_id::text, 0));
  select case s.kind when 'duel' then 10 else 50 end
    into cap
    from public.sessions s
    where s.id = new.session_id;
  select count(*) into used
    from public.session_submissions
    where session_id = new.session_id and kind = 'submit';
  if used >= cap then
    raise exception 'submission limit reached'
      using errcode = 'check_violation';
  end if;
  return new;
end;
$$;

drop trigger if exists session_submission_cap on public.session_submissions;
create trigger session_submission_cap
  before insert on public.session_submissions
  for each row execute function public.enforce_session_submission_cap();
