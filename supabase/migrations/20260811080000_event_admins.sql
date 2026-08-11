-- Per-event admins: extra users (beyond `events.created_by`) who may open the
-- event admin console while logged in. Read/written only through the service
-- role, like the other event tables.

create table if not exists public.event_admins (
  event_id uuid not null references public.events(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  created_at timestamptz not null default now(),
  primary key (event_id, user_id)
);
create index if not exists event_admins_user_idx on public.event_admins (user_id);

alter table public.event_admins enable row level security;
grant select, insert, update, delete on public.event_admins to service_role;
