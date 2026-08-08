-- 1v1 duel mode (docs/flows/09-1v1-duel.md): rooms, matches, players,
-- and problem invalidations. Per-player run data lives in public.sessions.
create table if not exists public.duel_rooms (
  id uuid primary key default gen_random_uuid(),
  created_by uuid not null references auth.users(id),
  status text not null default 'lobby' check (status in ('lobby','racing','done')),
  total_time_sec integer,
  grace_after_ac_sec integer default 60,
  created_at timestamptz not null default now()
);

-- Lobby membership + async ready-up (max 2 players, enforced in the API).
create table if not exists public.duel_room_players (
  room_id uuid not null references public.duel_rooms(id) on delete cascade,
  user_id uuid not null references auth.users(id),
  name text not null,
  avatar_url text,
  joined_at timestamptz not null default now(),
  ready_at timestamptz,
  primary key (room_id, user_id)
);

create table if not exists public.duel_matches (
  id uuid primary key default gen_random_uuid(),
  room_id uuid not null references public.duel_rooms(id) on delete cascade,
  problem_id text not null references public.problems(id),
  started_at timestamptz not null,
  total_time_sec integer,
  grace_after_ac_sec integer,
  first_ac_at timestamptz,
  winner_user_id uuid references auth.users(id),
  finished_at timestamptz,
  created_at timestamptz not null default now()
);
create index if not exists duel_matches_room on public.duel_matches (room_id, created_at);

-- One row per player per match, fkeying into the universal sessions table.
create table if not exists public.duel_players (
  match_id uuid not null references public.duel_matches(id) on delete cascade,
  user_id uuid not null references auth.users(id),
  session_id uuid not null references public.sessions(id),
  primary key (match_id, user_id)
);
create index if not exists duel_players_user on public.duel_players (user_id);

-- Problems can be marked invalid (excluded from picks + solved-tracking);
-- an invalidation can be revoked, restoring the problem.
create table if not exists public.problem_invalidations (
  id uuid primary key default gen_random_uuid(),
  problem_id text not null references public.problems(id),
  by_user uuid references auth.users(id),
  reason text,
  created_at timestamptz not null default now(),
  revoked_at timestamptz
);
create index if not exists problem_invalidations_problem
  on public.problem_invalidations (problem_id, created_at);

alter table public.duel_rooms enable row level security;
alter table public.duel_room_players enable row level security;
alter table public.duel_matches enable row level security;
alter table public.duel_players enable row level security;
alter table public.problem_invalidations enable row level security;
