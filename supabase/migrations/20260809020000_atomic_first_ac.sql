-- Atomic AC stamping: the outcome stamp and first-AC/winner stamp happen in
-- one transaction, and the caller learns whether this AC was the first so
-- side effects (confetti, grace window) only fire for the real winner.

create or replace function public.record_event_ac(
  p_session_id uuid,
  p_race_id uuid,
  p_contestant_id uuid,
  p_submitted_at timestamptz,
  p_solve_ms integer,
  p_lang text
) returns boolean
language plpgsql
as $$
declare
  stamped boolean;
begin
  update public.race_participants
    set first_ac_at = p_submitted_at
    where race_id = p_race_id
      and contestant_id = p_contestant_id
      and first_ac_at is null;
  stamped := found;

  update public.sessions
    set outcome = 'solved', solve_ms = p_solve_ms, lang = p_lang
    where id = p_session_id
      and solve_ms is null;

  return stamped;
end;
$$;

create or replace function public.record_duel_ac(
  p_session_id uuid,
  p_match_id uuid,
  p_user_id uuid,
  p_submitted_at timestamptz,
  p_solve_ms integer,
  p_lang text
) returns boolean
language plpgsql
as $$
declare
  stamped boolean;
begin
  update public.sessions
    set outcome = 'solved', solve_ms = p_solve_ms, lang = p_lang
    where id = p_session_id
      and solve_ms is null;

  update public.duel_matches
    set first_ac_at = p_submitted_at,
        winner_user_id = p_user_id
    where id = p_match_id
      and first_ac_at is null;
  stamped := found;

  return stamped;
end;
$$;
