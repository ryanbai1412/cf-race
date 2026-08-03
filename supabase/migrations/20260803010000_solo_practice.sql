-- Solo practice / gauntlet mode (docs/flows/07-solo-practice.md).
-- One row per solo run; editor snapshots + submissions mirror the race tables.
create table if not exists public.solo_sessions (
  id uuid primary key default gen_random_uuid(),
  problem_id text not null references public.problems(id),
  lang text check (lang in ('cpp','py')),
  started_at timestamptz not null,
  timer_sec integer not null default 180,
  solve_ms integer,
  outcome text check (outcome in ('solved','timeout','abandoned')),
  recording_path text,
  recording_offset_ms integer,
  created_at timestamptz not null default now()
);
create index if not exists solo_sessions_problem on public.solo_sessions (problem_id, created_at);

create table if not exists public.solo_editor_events (
  id bigint generated always as identity primary key,
  session_id uuid not null references public.solo_sessions(id) on delete cascade,
  t_ms integer not null,
  code text not null,
  lang text not null check (lang in ('cpp','py')),
  created_at timestamptz not null default now()
);
create index if not exists solo_editor_events_session_t
  on public.solo_editor_events (session_id, t_ms);

create table if not exists public.solo_submissions (
  id uuid primary key default gen_random_uuid(),
  session_id uuid not null references public.solo_sessions(id) on delete cascade,
  lang text not null check (lang in ('cpp','py')),
  source text not null,
  verdict text,
  details jsonb not null default '{}'::jsonb,
  submitted_at timestamptz not null default now(),
  judged_at timestamptz
);
create index if not exists solo_submissions_session
  on public.solo_submissions (session_id, submitted_at);

alter table public.solo_sessions enable row level security;
alter table public.solo_editor_events enable row level security;
alter table public.solo_submissions enable row level security;
