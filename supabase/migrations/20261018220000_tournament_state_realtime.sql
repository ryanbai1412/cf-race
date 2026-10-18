-- Tournament tabs subscribe to private Realtime topics so that only the
-- server (service role, which bypasses RLS) can broadcast state on them.
-- No insert policy: clients can listen but never send.
drop policy if exists "tournament state topics are listen-only" on realtime.messages;
create policy "tournament state topics are listen-only"
  on realtime.messages
  for select
  to anon, authenticated
  using (
    realtime.messages.extension = 'broadcast'
    and realtime.topic() like 'tournament-state-%'
  );
