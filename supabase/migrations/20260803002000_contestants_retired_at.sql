-- Contestants are retired when their race is finished/reset so stations
-- return to check-in for the next walk-up.
alter table public.contestants add column if not exists retired_at timestamptz;
