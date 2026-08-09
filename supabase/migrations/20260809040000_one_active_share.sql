-- At most one active (unrevoked) share token per session/match: mint uses
-- check-then-insert, so concurrent mints could otherwise create two live
-- tokens and break the single-row reads in /api/shares.
create unique index if not exists session_shares_one_active
  on public.session_shares (session_id)
  where revoked_at is null;

create unique index if not exists match_shares_one_active
  on public.match_shares (match_id)
  where revoked_at is null;
