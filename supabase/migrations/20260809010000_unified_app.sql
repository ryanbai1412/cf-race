-- Unified app shell: share tokens, session inactivity timeout, event ownership.

-- 1) Private-by-default replays with explicit share tokens.
create table if not exists public.session_shares (
  token text primary key default replace(gen_random_uuid()::text, '-', ''),
  session_id uuid not null references public.sessions(id) on delete cascade,
  created_by uuid references auth.users(id) on delete set null,
  created_at timestamptz not null default now(),
  revoked_at timestamptz
);
create index if not exists session_shares_session_idx on public.session_shares (session_id);

create table if not exists public.match_shares (
  token text primary key default replace(gen_random_uuid()::text, '-', ''),
  match_id uuid not null references public.duel_matches(id) on delete cascade,
  created_by uuid references auth.users(id) on delete set null,
  created_at timestamptz not null default now(),
  revoked_at timestamptz
);
create index if not exists match_shares_match_idx on public.match_shares (match_id);

-- 2) 15-minute inactivity timeout -> abandoned sessions.
alter table public.sessions
  add column if not exists last_event_at timestamptz not null default now();

create or replace function public.bump_session_last_event()
returns trigger language plpgsql as $$
begin
  update public.sessions set last_event_at = now() where id = new.session_id;
  return new;
end $$;

drop trigger if exists session_events_bump_last_event on public.session_events;
create trigger session_events_bump_last_event
  after insert on public.session_events
  for each row execute function public.bump_session_last_event();

-- Backfill last_event_at from existing events.
update public.sessions s
set last_event_at = e.max_at
from (select session_id, greatest(max(created_at)) as max_at from public.session_events group by session_id) e
where e.session_id = s.id;

-- 3) Event ownership for /events listing (null = legacy secret-link-only event).
alter table public.events
  add column if not exists created_by uuid references auth.users(id) on delete set null;
