-- Run-samples markers in editor event logs, and webcam recordings for event races.
alter table public.race_editor_events
  add column if not exists kind text not null default 'snapshot'
    check (kind in ('snapshot','run'));
alter table public.solo_editor_events
  add column if not exists kind text not null default 'snapshot'
    check (kind in ('snapshot','run'));

-- Webcam webm per station per race (bucket `recordings`, path race/<raceId>-<station>.webm).
create table if not exists public.race_recordings (
  race_id uuid not null references public.races(id) on delete cascade,
  station_role text not null check (station_role in ('station1','station2')),
  path text not null,
  offset_ms integer not null default 0,
  created_at timestamptz not null default now(),
  primary key (race_id, station_role)
);
alter table public.race_recordings enable row level security;
