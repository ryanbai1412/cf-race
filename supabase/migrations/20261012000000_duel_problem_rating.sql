alter table public.duel_rooms
  add column if not exists problem_rating integer not null default 800,
  add column if not exists settings_version integer not null default 0,
  add column if not exists start_claimed_at timestamptz;

do $$
begin
  if not exists (select 1 from pg_constraint where conname = 'duel_rooms_problem_rating' and conrelid = 'public.duel_rooms'::regclass) then
    alter table public.duel_rooms add constraint duel_rooms_problem_rating
      check (problem_rating in (800, 1000, 1200, 1400, 1600));
  end if;
end $$;

-- Settings and ready-up share a row lock so a race cannot start with stale settings.
create or replace function public.duel_lobby_action(
  p_room_id uuid, p_user_id uuid, p_action text, p_patch jsonb default '{}'
) returns jsonb
language plpgsql security invoker set search_path = ''
as $$
declare
  r public.duel_rooms%rowtype;
  new_rating integer;
  new_total integer;
  new_grace integer;
  player_ids uuid[];
  both_ready boolean;
begin
  select * into r from public.duel_rooms where id = p_room_id for update;
  if not found then
    return jsonb_build_object('ok', false, 'status', 404, 'error', 'Unknown room');
  end if;
  if not exists (select 1 from public.duel_room_players where room_id = p_room_id and user_id = p_user_id) then
    return jsonb_build_object('ok', false, 'status', 403, 'error', 'Not in room');
  end if;
  if p_action = 'reset' and r.status = 'lobby' then
    return jsonb_build_object('ok', true, 'activeMatch', false);
  end if;
  if p_action in ('reset', 'recover') and r.status = 'racing' then
    if p_action = 'reset' and r.start_claimed_at is distinct from (p_patch->>'startClaimedAt')::timestamptz then
      return jsonb_build_object('ok', false, 'status', 409, 'error', 'Race attempt changed');
    end if;
    if exists (select 1 from public.duel_matches where room_id = p_room_id and finished_at is null) then
      return jsonb_build_object('ok', true, 'activeMatch', true);
    end if;
    if p_action = 'recover' and r.start_claimed_at > clock_timestamp() - interval '30 seconds' then
      return jsonb_build_object('ok', false, 'status', 409, 'error', 'Race is still starting');
    end if;
    update public.duel_room_players set ready_at = null where room_id = p_room_id;
    update public.duel_rooms set status = 'lobby', start_claimed_at = null where id = p_room_id;
    return jsonb_build_object('ok', true, 'activeMatch', false);
  end if;
  if r.status <> 'lobby' then
    return jsonb_build_object('ok', false, 'status', 409, 'error', 'Room is not in the lobby');
  end if;
  if p_action = 'settings' then
    new_rating := case when p_patch ? 'rating' then (p_patch->>'rating')::integer else r.problem_rating end;
    new_total := case when p_patch ? 'totalTimeSec' then (p_patch->>'totalTimeSec')::integer else r.total_time_sec end;
    new_grace := case when p_patch ? 'graceAfterAcSec' then (p_patch->>'graceAfterAcSec')::integer else r.grace_after_ac_sec end;
    if new_rating is null or new_rating not in (800, 1000, 1200, 1400, 1600)
      or (new_total is not null and (new_total < 1 or new_total > 86400))
      or (new_grace is not null and (new_grace < 1 or new_grace > 86400)) then
      return jsonb_build_object('ok', false, 'status', 400, 'error', 'Invalid room settings');
    end if;
    if new_rating is distinct from r.problem_rating or new_total is distinct from r.total_time_sec or new_grace is distinct from r.grace_after_ac_sec then
      update public.duel_rooms set problem_rating = new_rating, total_time_sec = new_total,
        grace_after_ac_sec = new_grace, settings_version = settings_version + 1
        where id = p_room_id returning * into r;
      update public.duel_room_players set ready_at = null where room_id = p_room_id;
    end if;
    return jsonb_build_object('ok', true);
  elsif p_action = 'ready' then
    if (p_patch->>'ready')::boolean and ((p_patch->>'settingsVersion')::integer is distinct from r.settings_version) then
      return jsonb_build_object('ok', false, 'status', 409, 'error', 'Settings changed. Review them and ready up again.');
    end if;
    update public.duel_room_players set ready_at = case when (p_patch->>'ready')::boolean then now() else null end
      where room_id = p_room_id and user_id = p_user_id;
    select array_agg(user_id order by joined_at, user_id), count(*) = 2 and bool_and(ready_at is not null)
      into player_ids, both_ready from public.duel_room_players where room_id = p_room_id;
    if both_ready then
      update public.duel_rooms set status = 'racing', start_claimed_at = clock_timestamp()
        where id = p_room_id returning * into r;
    end if;
    return jsonb_build_object('ok', true, 'claimed', coalesce(both_ready, false), 'room', to_jsonb(r), 'playerIds', player_ids);
  end if;
  return jsonb_build_object('ok', false, 'status', 400, 'error', 'Invalid lobby action');
end $$;

revoke all on function public.duel_lobby_action(uuid, uuid, text, jsonb) from public, anon, authenticated;
grant execute on function public.duel_lobby_action(uuid, uuid, text, jsonb) to service_role;

drop function if exists public.duel_start_match(uuid, uuid, uuid, text);

create or replace function public.duel_start_match(
  p_room_id uuid, p_user_a uuid, p_user_b uuid, p_problem_id text, p_claim_time timestamptz
) returns jsonb
language plpgsql security invoker set search_path = ''
as $$
declare
  r public.duel_rooms%rowtype;
  v_match_id uuid;
  v_session_id uuid;
  v_user_id uuid;
  v_start_at timestamptz;
  v_rating integer;
  v_hidden boolean;
  v_members integer;
begin
  select * into r from public.duel_rooms where id = p_room_id for update;
  if not found or r.status <> 'racing' then
    return jsonb_build_object('ok', false, 'status', 409, 'error', 'Room is not starting a race');
  end if;
  if r.start_claimed_at is distinct from p_claim_time then
    return jsonb_build_object('ok', false, 'status', 409, 'error', 'Race attempt changed. Refresh the lobby.');
  end if;
  if exists (select 1 from public.duel_matches where room_id = p_room_id and finished_at is null) then
    return jsonb_build_object('ok', true);
  end if;
  select count(*) into v_members from public.duel_room_players
    where room_id = p_room_id and user_id in (p_user_a, p_user_b) and ready_at is not null;
  if p_user_a = p_user_b or p_user_a is null or p_user_b is null or v_members <> 2 or
    (select count(*) from public.duel_room_players where room_id = p_room_id) <> 2 then
    update public.duel_room_players set ready_at = null where room_id = p_room_id;
    update public.duel_rooms set status = 'lobby', start_claimed_at = null where id = p_room_id;
    return jsonb_build_object('ok', false, 'status', 409, 'error', 'Players changed. Please ready up again.');
  end if;

  select rating, coalesce(to_jsonb(tags) ? 'hidden', false) into v_rating, v_hidden
    from public.problems where id = p_problem_id;
  if not found or v_rating is distinct from r.problem_rating or v_hidden or
    exists (select 1 from public.sessions
      where user_id in (p_user_a, p_user_b) and problem_id = p_problem_id) or
    exists (select 1 from public.problem_invalidations
      where by_user in (p_user_a, p_user_b) and problem_id = p_problem_id and revoked_at is null) then
    update public.duel_room_players set ready_at = null where room_id = p_room_id;
    update public.duel_rooms set status = 'lobby', start_claimed_at = null where id = p_room_id;
    return jsonb_build_object('ok', false, 'status', 409, 'error', 'Problem is no longer eligible. Please ready up again.');
  end if;

  v_start_at := clock_timestamp() + interval '3 seconds';
  begin
    insert into public.duel_matches (room_id, problem_id, started_at, total_time_sec, grace_after_ac_sec)
      values (p_room_id, p_problem_id, v_start_at, r.total_time_sec, r.grace_after_ac_sec)
      returning id into v_match_id;
    foreach v_user_id in array array[p_user_a, p_user_b] loop
      insert into public.sessions (kind, user_id, problem_id, started_at, timer_sec)
        values ('duel', v_user_id, p_problem_id, v_start_at, r.total_time_sec)
        returning id into v_session_id;
      insert into public.duel_players (match_id, user_id, session_id)
        values (v_match_id, v_user_id, v_session_id);
    end loop;
  exception when others then
    update public.duel_room_players set ready_at = null where room_id = p_room_id;
    update public.duel_rooms set status = 'lobby', start_claimed_at = null where id = p_room_id;
    return jsonb_build_object('ok', false, 'status', 500, 'error', 'Could not start duel. Please ready up again.');
  end;
  return jsonb_build_object('ok', true);
end $$;

revoke all on function public.duel_start_match(uuid, uuid, uuid, text, timestamptz) from public, anon, authenticated;
grant execute on function public.duel_start_match(uuid, uuid, uuid, text, timestamptz) to service_role;
