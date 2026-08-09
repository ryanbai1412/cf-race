-- Per-user 1-5 star ratings on problems.
create table if not exists public.problem_ratings (
  user_id uuid not null references auth.users(id) on delete cascade,
  problem_id text not null references public.problems(id) on delete cascade,
  stars smallint not null check (stars between 1 and 5),
  rated_at timestamptz not null default now(),
  primary key (user_id, problem_id)
);
create index if not exists problem_ratings_problem_idx on public.problem_ratings (problem_id);
