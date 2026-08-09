-- Two players per duel room, enforced where the row is created: the app read
-- the player list and then inserted, so two simultaneous joins could both see
-- an open slot and produce a three-player room.
create or replace function public.enforce_duel_room_player_cap()
returns trigger
language plpgsql
as $$
declare
  used integer;
begin
  perform pg_advisory_xact_lock(hashtextextended(new.room_id::text, 0));
  select count(*) into used
    from public.duel_room_players
    where room_id = new.room_id;
  if used >= 2 then
    raise exception 'room full' using errcode = 'check_violation';
  end if;
  return new;
end;
$$;

drop trigger if exists duel_room_player_cap on public.duel_room_players;
create trigger duel_room_player_cap
  before insert on public.duel_room_players
  for each row execute function public.enforce_duel_room_player_cap();
