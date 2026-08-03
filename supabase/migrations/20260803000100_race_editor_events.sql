-- Editor snapshots recorded during races, for full session replay.
create table if not exists public.race_editor_events (
  id bigint generated always as identity primary key,
  race_id uuid not null references public.races(id) on delete cascade,
  station_role text not null check (station_role in ('station1','station2')),
  t_ms integer not null,
  code text not null,
  lang text not null check (lang in ('cpp','py')),
  created_at timestamptz not null default now()
);
create index if not exists race_editor_events_race_station_t
  on public.race_editor_events (race_id, station_role, t_ms);
alter table public.race_editor_events enable row level security;
