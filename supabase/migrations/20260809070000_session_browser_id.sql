-- Durable record of which browser created an anonymous session, so sign-in
-- can claim runs even if the cfr_anon_sessions cookie was lost/truncated
-- (the cookie remains the client-side hint; this is the server-side truth).
alter table public.sessions add column if not exists browser_id uuid;

create index if not exists sessions_anon_browser
  on public.sessions (browser_id)
  where user_id is null and browser_id is not null;
