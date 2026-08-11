-- Warm-up readiness for booth stations: set when the player clicks "I'm
-- ready", cleared on un-ready and when a race starts.
alter table public.contestants
  add column if not exists ready_at timestamptz;
