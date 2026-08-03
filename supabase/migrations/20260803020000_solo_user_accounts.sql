-- Tie solo practice sessions to Supabase Auth accounts (Google login).
-- Anonymous runs keep user_id null and live only in localStorage.
alter table public.solo_sessions
  add column if not exists user_id uuid references auth.users(id) on delete set null;

create index if not exists solo_sessions_user on public.solo_sessions(user_id)
  where user_id is not null;

-- Signed-in users can read their own session history with the anon key.
drop policy if exists "solo_sessions_select_own" on public.solo_sessions;
create policy "solo_sessions_select_own" on public.solo_sessions
  for select to authenticated
  using (auth.uid() = user_id);
