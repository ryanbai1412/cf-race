-- Genna reference sessions: one blessed session per problem whose replay,
-- webcam recording and solve_ms are the "race Genna" ghost/benchmark
-- (docs/flows/13-genna-problems-and-monitors.md). Written only via the
-- service role from admin-gated API routes.

create table if not exists public.genna_problems (
  problem_id text primary key references public.problems(id) on delete cascade,
  session_id uuid not null references public.sessions(id) on delete cascade,
  created_at timestamptz not null default now()
);

alter table public.genna_problems enable row level security;

-- Readable by everyone (Genna times show on public surfaces).
drop policy if exists genna_problems_read on public.genna_problems;
create policy genna_problems_read on public.genna_problems
  for select using (true);

grant select on public.genna_problems to anon, authenticated;
grant select, insert, update, delete on public.genna_problems to service_role;
