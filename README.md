# Code vs Racing (cf-race)

Head-to-head competitive programming races for live events: two contestants solve the
same Codeforces problem side by side while racing a replay of tourist solving it.

## Quickstart

```bash
./scripts/setup.sh   # checks prerequisites, creates .env.local, installs deps
pnpm dev             # web app on http://localhost:3000
```

`scripts/setup.sh` (or `make setup`) verifies Node 20+, pnpm (enables it via
corepack if missing), copies `.env.example` to `.env.local`, and tells you which
env vars are still empty.

### Env vars (`.env.local`)

| Var | Where to get it |
|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase Dashboard → Settings → API |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase Dashboard → Settings → API |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase Dashboard → Settings → API (server-side only) |
| `NEXT_PUBLIC_LIVEKIT_URL` | LiveKit project `wss://` URL |
| `LIVEKIT_API_KEY` / `LIVEKIT_API_SECRET` | LiveKit project settings |
| `JUDGE_URL` | `http://localhost:8080` (local judge) or `https://cf-race-judge.fly.dev` |
| `JUDGE_TOKEN` | `dev` for a local judge; shared secret in production |

## Common tasks

Everything is available both as `pnpm` scripts and `make` targets:

| Command | What it does |
|---|---|
| `make setup` | prerequisites + `.env.local` + install |
| `pnpm dev` / `make dev` | web app on :3000 |
| `pnpm lint` / `pnpm typecheck` / `pnpm build` | checks (`make check` runs all three) |
| `pnpm seed` / `make seed` | upload `problems/` packages to Supabase Storage + upsert `problems` table |
| `pnpm seed:tourist <id> <log.json>` | upload a tourist replay log + set `tourist_time_ms` |
| `make judge-dev` | local judge on :8080, no sandbox (dev only) |
| `make judge-docker` | local judge in Docker with the real isolate sandbox |
| `make judge-test` | judge unit + integration tests |
| `make judge-deploy` | deploy judge to Fly.io |
| `make smoke` / `pnpm smoke` | end-to-end API smoke test (`BASE_URL=...`) |

## Local judge

The judge (`judge/`) normally runs code inside [isolate](https://github.com/ioi/isolate),
which needs Linux cgroups. For local dev there are two options:

1. **No Docker** — `make judge-dev` runs the judge with `JUDGE_SANDBOX=none`
   (plain subprocesses, no isolation — dev only) and `PROBLEMS_DIR=../problems`,
   so all repo problem packages are available immediately.
2. **Docker** — `make judge-docker` builds the production image (isolate included)
   and runs it privileged via `docker-compose.yml`, mounting `./problems` into
   the container. Inside containers without cgroup v1 the entrypoint automatically
   falls back to `JUDGE_SANDBOX=isolate-nocg` (rlimit-based, no cgroups).

Then point the web app at it in `.env.local`:

```
JUDGE_URL=http://localhost:8080
JUDGE_TOKEN=dev
```

See `judge/README.md` for the full env var reference and `docs/JUDGE_API.md`
for the HTTP/WS contract and problem package format.

## Seeding problems

Problem packages live in `problems/<id>/` (`meta.json`, `statement.html`,
`samples/`, `tests/` — format in `docs/JUDGE_API.md`). To make them available to
the deployed app and judge:

```bash
pnpm seed                  # everything under problems/ (incl. problems/dev/*)
pnpm seed --only 2024A     # one package
pnpm seed --dry-run        # list what would be uploaded
```

This uploads each package to the `problems` Supabase Storage bucket (the judge
syncs from it on boot — re-deploy or restart the judge to pick up new problems)
and upserts the `problems` table rows the web app reads.

Tourist replay logs (see `TouristLog` in `src/lib/tourist.ts`):

```bash
pnpm seed:tourist 2024A path/to/2024A-log.json
```

## Smoke test

`scripts/smoke.sh` exercises the whole flow over the public API:
create event → check-in → start race → submit (expects `AC`) → finish race.

```bash
pnpm seed --only dev/aplusb          # once: the problem must exist in Supabase
BASE_URL=http://localhost:3000 make smoke
BASE_URL=https://<your-app>.vercel.app make smoke
PROBLEM_ID=2024A SOURCE_FILE=sol.py make smoke   # custom problem/solution
```

## Deploy

- **Web app**: Vercel, deploys on push to `main`. Set the same env vars as
  `.env.example` in the Vercel project (with the production `JUDGE_URL`/`JUDGE_TOKEN`).
- **Judge**: Fly.io app `cf-race-judge` (org `cf-racing-129`) — `make judge-deploy`.
  Secrets (`JUDGE_TOKEN`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`) via
  `fly secrets set`; see `judge/README.md`.
- **Database**: migrations in `supabase/migrations/`, applied via Supabase.

## Architecture

- `src/` — Next.js app (App Router): contestant **stations**, spectator
  **monitors**, admin, and the `/api` routes (Supabase Postgres + Realtime,
  LiveKit for AV). Deployed on Vercel.
- `judge/` — sandboxed code-execution service (Node + isolate) on Fly.io.
  Contract: `docs/JUDGE_API.md`.
- `pipeline/` — Codeforces problem scraping / test generation (Python), writes
  `problems/` packages.
- `problems/` — problem packages; `problems/dev/*` are tiny dev problems baked
  into the judge image.
- `scripts/` — devex scripts (`setup.sh`, `seed.ts`, `upload-tourist.ts`, `smoke.sh`).
- `docs/` — [PRD](docs/PRD.md), [architecture](docs/ARCHITECTURE.md),
  [judge/problem contract](docs/JUDGE_API.md), flow PRDs in `docs/flows/`.

## Checks

```bash
pnpm lint && pnpm typecheck && pnpm build   # or: make check
```
