-- Periodic abandonment sweep via pg_cron (PRD 11 §5.1): sessions with no
-- events for 15 minutes flip to abandoned even when nobody reads them.
-- The lazy flip in application reads stays as a backstop.
create extension if not exists pg_cron;

create or replace function public.sweep_stale_sessions()
returns integer language sql as $$
  with flipped as (
    update public.sessions
    set outcome = 'abandoned'
    where outcome is null
      and last_event_at < now() - interval '15 minutes'
    returning 1
  )
  select count(*)::integer from flipped;
$$;

select cron.schedule(
  'sweep-stale-sessions',
  '* * * * *',
  $$select public.sweep_stale_sessions()$$
)
where not exists (
  select 1 from cron.job where jobname = 'sweep-stale-sessions'
);
