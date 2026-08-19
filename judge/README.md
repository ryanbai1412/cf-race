# Judge service

HTTP+WS code-execution judge for Code Voices Racing. Implements the contract in
[`docs/JUDGE_API.md`](../docs/JUDGE_API.md): `POST /run`, `POST /submit`,
`GET /healthz`, `WS /ws?token=...`, bearer-token auth via `JUDGE_TOKEN`.

- Languages: `cpp` (g++ C++20; debug `-O1 -g -fsanitize=address,undefined`, submit `-O2`) and `py` (CPython 3).
- Sandboxing: [ioi/isolate](https://github.com/ioi/isolate) v1.10.1 (cgroup v1 required for the default mode), no network, time/memory limits.
- Compile cache keyed by sha256(lang, flags, source); concurrent identical compiles are deduplicated.
- Worker pool sized to CPU count (`JUDGE_WORKERS` to override); sample tests run in parallel, submissions run sequentially with CF-style short-circuit.
- CF-style checker: token compare, trailing whitespace ignored, case-insensitive YES/NO, optional `floatEps` (abs/rel).

## Env vars

| Var | Default | Notes |
|---|---|---|
| `JUDGE_TOKEN` | — | required; shared bearer token |
| `PORT` | 8080 | |
| `PROBLEMS_DIR` | `/data/problems` | problem packages per contract |
| `CACHE_DIR` | `/tmp/judge-cache` | compile cache |
| `JUDGE_SANDBOX` | `isolate` | `isolate` requires the cgroup v1 memory controller; `isolate-nocg` and `none` are unsafe modes and require `ALLOW_UNSAFE_SANDBOX=1` |
| `ALLOW_UNSAFE_SANDBOX` | — | Must be `1` to explicitly enable `isolate-nocg` or `none`; never use those modes for untrusted code |
| `JUDGE_WORKERS` | CPU count | max concurrent sandbox runs |
| `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` | — | if set, problems synced from Storage bucket `problems` on boot |

## Local dev

```bash
cd judge
pnpm install
JUDGE_TOKEN=dev JUDGE_SANDBOX=none ALLOW_UNSAFE_SANDBOX=1 PROBLEMS_DIR=../problems pnpm run dev
pnpm test   # unit + integration tests against problems/dev/*
```

`JUDGE_SANDBOX=none` runs code as plain subprocesses (no isolation) — dev only.
`JUDGE_SANDBOX=isolate-nocg` uses isolate without cgroups and is also unsafe; both
modes refuse to start unless `ALLOW_UNSAFE_SANDBOX=1` is set explicitly.

Example:

```bash
curl -s localhost:8080/run -H "authorization: Bearer dev" -H 'content-type: application/json' \
  -d '{"runId":"1","lang":"py","source":"t=int(input())\nfor _ in range(t): a,b=map(int,input().split()); print(a+b)","problemId":"dev/aplusb"}'
```

## Problem sync

`pnpm run sync-problems` downloads the whole `problems` Supabase Storage bucket to
`$PROBLEMS_DIR`. The entrypoint runs it automatically on boot when Supabase creds
are present. Dev problems (`problems/dev/*` in the repo) are baked into the Docker
image so the judge works without a sync.

## Docker

Build from the repo root (the image needs the workspace pnpm lockfile and
`problems/dev/`):

```bash
docker build -f judge/Dockerfile -t cf-race-judge .
docker run --privileged -p 8080:8080 -e JUDGE_TOKEN=dev cf-race-judge
```

`--privileged` (or equivalent cgroup delegation) is needed for isolate.

## Deploy (Fly.io)

App `cf-race-judge`, org `cf-racing-129`, region `ams`, `performance-4x`.

```bash
fly secrets set JUDGE_TOKEN=... SUPABASE_URL=... SUPABASE_SERVICE_ROLE_KEY=... -a cf-race-judge
fly deploy -a cf-race-judge -c judge/fly.toml   # or: make judge-deploy
curl https://cf-race-judge.fly.dev/healthz
```
