# Problem pipeline

Offline pipeline that builds problem packages (see `docs/JUDGE_API.md`,
"Problem package format") for Code Voices Racing.

Set `CF_PROXY_AUTH_TOKEN` in the environment before running scripts that fetch
HTML through `cf-p.vercel.app`. Do not commit this credential.

## Scripts
- `select_problems.py` — pick random rated-800 problems from the last ~3 years
  (official CF API), skipping constructive-tagged problems.
- `scrape.py <id>...` — scrape statement + samples via the proxy
  (https://cf-p.vercel.app mirrors codeforces.com paths); writes
  `problems/<id>/statement.html`, `samples/`, and a `meta.json` skeleton.
- `gen_tests.py <id>...` — generate `problems/<id>/tests/` from
  `pipeline/problems/<id>/gen.py` (inputs) + `ref.py`/`ref.cpp` (outputs).
  Samples are included as the first tests.
- `validate.py <id>...` — fetch ~5 AC and ~5 WA/TLE public submissions
  (API for metadata, proxy for source), run them locally against the
  generated tests, and confirm expected verdicts.
- `upload_supabase.py <id>...` — upload packages to the Supabase Storage
  bucket `problems` (uses SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY).
- `checker.py` — CF-style token checker used by validation.

## Per-problem assets (`pipeline/problems/<id>/`)
- `gen.py` — writes `NN.in` files into the directory given as argv[1]
  (random + edge + max-size tests).
- `ref.py` / `ref.cpp` — reference solution used to produce `.out` files.

Validation results: `validation-report.md`.
