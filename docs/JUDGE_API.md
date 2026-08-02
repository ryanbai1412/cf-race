# Judge Service Contract (v1)

The judge is a standalone HTTP+WS service (Fly.io machine, Node or Go, sandboxed with `isolate`).
The web app talks to it server-side using a shared bearer token (`JUDGE_TOKEN`).

## Languages
- `cpp` — GNU G++ (C++20). Debug mode: `-O1 -g -fsanitize=address,undefined`; Submit mode: `-O2`.
- `py` — Python 3 (CPython).

## Endpoints

### POST /run
Run source against sample tests and/or custom input. Fast path; debug mode by default.
```jsonc
{
  "runId": "uuid",            // client-generated
  "lang": "cpp" | "py",
  "source": "...",
  "problemId": "1927A",        // omit for sandbox/custom-only runs
  "tests": [                    // optional override; default = problem's samples
    {"name": "sample1", "input": "...", "expected": "..."},
    {"name": "custom1", "input": "...", "expected": null}   // null = no checking, just show output
  ],
  "timeLimitMs": 2000,
  "memoryLimitMb": 256
}
```
Response (also streamed over WS as tests finish):
```jsonc
{
  "runId": "uuid",
  "compile": {"ok": true, "stderr": ""},
  "results": [
    {"name": "sample1", "verdict": "AC"|"WA"|"RE"|"TLE"|"ML"|"SKIP",
     "timeMs": 12, "stdout": "...", "stderr": "...",
     "checkerNote": "token 3 differs: expected 4, got 5"}
  ]
}
```
- stdout/stderr each capped (e.g. 64KB) with truncation flags.
- If the problem is flagged `specialJudge`, results include `"checkerUnreliable": true`.

### POST /submit
Full judging against all generated tests. `-O2` for C++. Short-circuits on first failing test.
Request: `{submissionId, lang, source, problemId}`.
Response/WS stream: `{submissionId, verdict, failedTest, passedCount, totalCount, timeMsMax}`.
Final verdicts: `AC | WA | TLE | RE | ML | CE`.

### GET /healthz
`{ok: true, queue: n}`.

### WS /ws?token=...
Server pushes `run_update`, `submit_update` events (same payloads as above, incremental).

## Checker (CF-style, built into judge)
- Token-based comparison (split on whitespace); trailing whitespace/newlines ignored.
- Case-insensitive for YES/NO tokens.
- Optional float mode per problem (`floatEps` in meta): compare numeric tokens with abs/rel eps.

## Problem package format
Stored in Supabase Storage bucket `problems/` and synced to the judge VM at
`/data/problems/<problemId>/`:
```
<problemId>/                 # e.g. 1927A
  meta.json
  statement.html             # sanitized statement (used by web app, not judge)
  samples/                   # sampleK.in / sampleK.out
    1.in  1.out  2.in  2.out ...
  tests/                     # full generated tests, 01.in/01.out ... NN.in/NN.out
    01.in 01.out ...
```
`meta.json`:
```jsonc
{
  "id": "1927A",
  "name": "Make it White",
  "rating": 800,
  "timeLimitMs": 2000,
  "memoryLimitMb": 256,
  "multiTest": true,
  "specialJudge": false,      // true => sample checker warning + custom checker required
  "floatEps": null,           // e.g. 1e-6
  "raceTimerSec": 180,        // per-problem race cap
  "touristTimeMs": 41000      // tourist's solve time (null until recorded)
}
```

## Auth
All HTTP requests: `Authorization: Bearer $JUDGE_TOKEN`. WS: `?token=`.
Judge has no user concept; the web app is the only client.
