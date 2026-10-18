-- The tournament state poll's whole viewer-independent read in one call: the
-- tournament row plus its members, matches and games (each game with its
-- problem name and both sessions' outcome/solve_ms), shaped like the
-- PostgREST embedded select in src/lib/tournament.ts so either can serve it.
-- Lookup by code or by id; null when nothing matches. The result includes
-- members' token_hash, so only service_role may call it.
create or replace function public.tournament_snapshot(p_code text default null, p_id uuid default null)
returns jsonb
language sql
stable
set search_path = ''
as $$
  select to_jsonb(t) || jsonb_build_object(
    'members', coalesce((
      select jsonb_agg(to_jsonb(m))
      from public.tournament_members m
      where m.tournament_id = t.id
    ), '[]'::jsonb),
    'matches', coalesce((
      select jsonb_agg(to_jsonb(x))
      from public.tournament_matches x
      where x.tournament_id = t.id
    ), '[]'::jsonb),
    'games', coalesce((
      select jsonb_agg(to_jsonb(g) || jsonb_build_object(
        'problem', (select jsonb_build_object('name', p.name) from public.problems p where p.id = g.problem_id),
        'sa', (select jsonb_build_object('outcome', s.outcome, 'solve_ms', s.solve_ms) from public.sessions s where s.id = g.session_a),
        'sb', (select jsonb_build_object('outcome', s.outcome, 'solve_ms', s.solve_ms) from public.sessions s where s.id = g.session_b)
      ))
      from public.tournament_games g
      where g.tournament_id = t.id
    ), '[]'::jsonb)
  )
  from public.tournaments t
  where t.code = p_code or t.id = p_id
  limit 1;
$$;

revoke execute on function public.tournament_snapshot(text, uuid) from public, anon, authenticated;
grant execute on function public.tournament_snapshot(text, uuid) to service_role;
