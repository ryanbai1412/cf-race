-- Admin panel: DB-granted admins (on top of the hard-coded email allowlist
-- in src/lib/admin.ts). Read/written only through the service role.

create table if not exists public.app_admins (
  user_id uuid primary key references auth.users(id) on delete cascade,
  granted_by uuid references auth.users(id) on delete set null,
  granted_at timestamptz not null default now()
);

alter table public.app_admins enable row level security;
grant select, insert, update, delete on public.app_admins to service_role;
