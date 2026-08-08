-- Universal sessions: one row per player-run of a problem, shared by solo,
-- duel, and (later) live-event races (docs/flows/09-1v1-duel.md).
-- session_events is the single playback stream (editor deltas/keyframes,
-- runs, tabs, scroll, submit + verdict moments); session_submissions is the
-- judge-facing record (source, verdict, details) for runs and submissions;
-- webcam recordings hang off sessions.recording_path.
create table if not exists public.sessions (
  id uuid primary key default gen_random_uuid(),
  kind text not null check (kind in ('solo','duel','event')),
  user_id uuid references auth.users(id) on delete set null,
  problem_id text not null references public.problems(id),
  lang text check (lang in ('cpp','py')),
  started_at timestamptz not null,
  timer_sec integer,
  solve_ms integer,
  outcome text check (outcome in ('solved','timeout','abandoned')),
  recording_path text,
  recording_offset_ms integer,
  created_at timestamptz not null default now()
);
create index if not exists sessions_problem on public.sessions (problem_id, created_at);
create index if not exists sessions_user on public.sessions (user_id)
  where user_id is not null;

create table if not exists public.session_events (
  id bigint generated always as identity primary key,
  session_id uuid not null references public.sessions(id) on delete cascade,
  t_ms integer not null,
  code text not null default '',
  lang text not null check (lang in ('cpp','py')),
  kind text not null default 'snapshot'
    check (kind in ('snapshot','delta','run','run_result','tab','scroll','submit','verdict')),
  payload jsonb,
  created_at timestamptz not null default now()
);
create index if not exists session_events_session_t
  on public.session_events (session_id, t_ms);

create table if not exists public.session_submissions (
  id uuid primary key default gen_random_uuid(),
  session_id uuid not null references public.sessions(id) on delete cascade,
  kind text not null default 'submit' check (kind in ('run','submit')),
  lang text not null check (lang in ('cpp','py')),
  source text not null,
  verdict text,
  details jsonb not null default '{}'::jsonb,
  submitted_at timestamptz not null default now(),
  judged_at timestamptz
);
create index if not exists session_submissions_session
  on public.session_submissions (session_id, submitted_at);

alter table public.sessions enable row level security;
alter table public.session_events enable row level security;
alter table public.session_submissions enable row level security;

-- Signed-in users can read their own session history with the anon key.
drop policy if exists "sessions_select_own" on public.sessions;
create policy "sessions_select_own" on public.sessions
  for select to authenticated
  using (auth.uid() = user_id);

-- Backfill solo runs. Ids are preserved so /solo/replay/<sessionId> URLs keep
-- working; the old solo_* tables are left in place as a frozen archive.
insert into public.sessions (id, kind, user_id, problem_id, lang, started_at,
  timer_sec, solve_ms, outcome, recording_path, recording_offset_ms, created_at)
select id, 'solo', user_id, problem_id, lang, started_at, timer_sec, solve_ms,
  outcome, recording_path, recording_offset_ms, created_at
from public.solo_sessions
on conflict (id) do nothing;

insert into public.session_events (session_id, t_ms, code, lang, kind, payload)
select e.session_id, e.t_ms, e.code, e.lang, coalesce(e.kind, 'snapshot'), e.payload
from public.solo_editor_events e
where not exists (
  select 1 from public.session_events x where x.session_id = e.session_id
)
order by e.session_id, e.t_ms, e.id;

insert into public.session_submissions (id, session_id, kind, lang, source,
  verdict, details, submitted_at, judged_at)
select id, session_id, 'submit', lang, source, verdict, details, submitted_at,
  judged_at
from public.solo_submissions
on conflict (id) do nothing;

-- Derive submit/verdict playback events for backfilled solo submissions so
-- session_events alone can drive a replay.
with subs as (
  select sub.id, sub.session_id, sub.lang, sub.verdict, sub.submitted_at,
    sub.judged_at, s.started_at
  from public.solo_submissions sub
  join public.sessions s on s.id = sub.session_id
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
  where x.session_id = m.session_id and x.kind in ('submit','verdict')
);
