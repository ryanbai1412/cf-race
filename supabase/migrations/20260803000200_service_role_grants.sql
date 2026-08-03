-- The project was created with "automatically expose new tables" off, so new
-- tables get no grants. The app talks to PostgREST as service_role only.
grant usage on schema public to service_role;
grant all privileges on all tables in schema public to service_role;
grant all privileges on all sequences in schema public to service_role;
alter default privileges in schema public grant all on tables to service_role;
alter default privileges in schema public grant all on sequences to service_role;
