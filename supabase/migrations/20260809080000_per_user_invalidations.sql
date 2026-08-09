-- Invalidating a problem is a per-user decision ("don't give me this one
-- again"), not a global takedown: previously any signed-in user could remove a
-- problem from everyone's pool. Rows are now owned by their author, and at most
-- one active invalidation exists per (problem, user).

-- Legacy rows without an author can no longer be attributed, and they are what
-- made the feature global; drop them so nobody inherits someone else's choice.
delete from public.problem_invalidations where by_user is null;

alter table public.problem_invalidations
  alter column by_user set not null;

drop index if exists problem_invalidations_one_active;
create unique index problem_invalidations_one_active
  on public.problem_invalidations (problem_id, by_user)
  where revoked_at is null;

create index if not exists problem_invalidations_by_user
  on public.problem_invalidations (by_user)
  where revoked_at is null;
