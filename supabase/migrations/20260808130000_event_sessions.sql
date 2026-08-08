-- Event races join the universal sessions tables: every race participant gets
-- a sessions row (kind='event'), replay/submission data moves to
-- session_events / session_submissions, and the race_* replay tables become a
-- frozen archive (backfilled below, no new writes).

alter table public.race_participants
  add column if not exists session_id uuid;

-- One session per participant of a started race. The id is minted on the
-- participant first so the sessions insert below can reference it.
update public.race_participants rp
set session_id = gen_random_uuid()
from public.races r
where r.id = rp.race_id
  and rp.session_id is null
  and r.started_at is not null;

insert into public.sessions (id, kind, problem_id, started_at, timer_sec,
  solve_ms, outcome, recording_path, recording_offset_ms)
select rp.session_id, 'event', r.problem_id, r.started_at, r.timer_sec,
  case when rp.first_ac_at is not null then
    greatest(0, (extract(epoch from (rp.first_ac_at - r.started_at)) * 1000)::int)
  end,
  case
    when rp.first_ac_at is not null then 'solved'
    when r.state = 'finished' then 'timeout'
  end,
  rr.path, rr.offset_ms
from public.race_participants rp
join public.races r on r.id = rp.race_id
left join public.race_recordings rr
  on rr.race_id = rp.race_id and rr.station_role = rp.station_role
where rp.session_id is not null
on conflict (id) do nothing;

alter table public.race_participants
  drop constraint if exists race_participants_session_id_fkey;
alter table public.race_participants
  add constraint race_participants_session_id_fkey
  foreign key (session_id) references public.sessions(id);

-- Editor snapshots/deltas/runs/tabs/scrolls recorded per station.
insert into public.session_events (session_id, t_ms, code, lang, kind, payload)
select rp.session_id, e.t_ms, e.code, e.lang, coalesce(e.kind, 'snapshot'),
  e.payload
from public.race_editor_events e
join public.race_participants rp
  on rp.race_id = e.race_id and rp.station_role = e.station_role
where rp.session_id is not null
  and not exists (
    select 1 from public.session_events x
    where x.session_id = rp.session_id
  )
order by e.race_id, e.station_role, e.t_ms, e.id;

-- Official submissions, ids preserved.
insert into public.session_submissions (id, session_id, kind, lang, source,
  verdict, details, submitted_at, judged_at)
select s.id, rp.session_id, 'submit', s.lang, s.source, s.verdict,
  coalesce(s.details, '{}'::jsonb), s.submitted_at, s.judged_at
from public.submissions s
join public.race_participants rp
  on rp.race_id = s.race_id and rp.contestant_id = s.contestant_id
where rp.session_id is not null
on conflict (id) do nothing;

-- Derive submit/verdict playback events for backfilled submissions so
-- session_events alone can drive a replay (mirrors the solo backfill).
with subs as (
  select sub.id, rp.session_id, sub.lang, sub.verdict, sub.submitted_at,
    sub.judged_at, r.started_at
  from public.submissions sub
  join public.race_participants rp
    on rp.race_id = sub.race_id and rp.contestant_id = sub.contestant_id
  join public.races r on r.id = sub.race_id
  where rp.session_id is not null
),
marks as (
  select session_id,
    greatest(0, (extract(epoch from (submitted_at - started_at)) * 1000)::int)
      as t_ms,
    lang, 'submit' as kind,
    jsonb_build_object('submissionId', id) as payload
  from subs
  union all
  select session_id,
    greatest(0, (extract(epoch from (coalesce(judged_at, submitted_at)
      - started_at)) * 1000)::int) as t_ms,
    lang, 'verdict' as kind,
    jsonb_build_object('submissionId', id, 'verdict', verdict) as payload
  from subs
  where verdict is not null and verdict <> 'PENDING'
)
insert into public.session_events (session_id, t_ms, code, lang, kind, payload)
select m.session_id, m.t_ms, '', m.lang, m.kind, m.payload
from marks m
where not exists (
  select 1 from public.session_events x
  where x.session_id = m.session_id and x.kind in ('submit', 'verdict')
);

-- The leaderboard reads first-AC times straight from race data; define the
-- view in-repo so it survives table changes.
drop view if exists public.leaderboard;
create view public.leaderboard as
select rp.race_id, r.problem_id, rp.contestant_id, c.name, c.country,
  greatest(0,
    (extract(epoch from (rp.first_ac_at - r.started_at)) * 1000)::int
  ) as solve_ms
from public.race_participants rp
join public.races r on r.id = rp.race_id
join public.contestants c on c.id = rp.contestant_id
where rp.first_ac_at is not null
  and rp.dq = false
  and r.started_at is not null;
