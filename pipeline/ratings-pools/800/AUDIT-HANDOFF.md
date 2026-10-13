# Rating 800: handoff for an independent audit

Nothing in this directory is validated. `execution-passed` means the foundation's 5 accepted / 5 WA-TLE gate passed in
the v2 sandbox. That is not validation. A package counts only after a **different agent** writes
`W/800/audits/ID.json` (schema in `pipeline/RATED_POOLS.md`, "Independent audit") and `rated_pool.py report` verifies it.

## Identities already used (the auditor must differ from all of them)

| Role | Identity |
| --- | --- |
| Recipe, generator and coverage author; `--validator` | `rated-800-worker` |
| Generated-basis oracle | public accepted Codeforces submission (`gen-qualification/ID/oracle-source.json`). It is chosen from the newest end of the accepted pool, after skipping the 25 oldest, and is never one of the five counted sources. It is **not** an audit. |

## Reproduce

```sh
tar xzf rated-800-audit-bundle.tar.gz   # verify every file against rated-800-audit-bundle.provenance.json first
# official basis
python3 pipeline/rated_pool.py prepare  --rating 800 --id ID --workspace W
python3 pipeline/ratings-pools/800/tools/recipe_check.py ID ...      # recipe validate()/solve() vs every upstream pair
python3 pipeline/rated_pool.py validate --rating 800 --id ID --workspace W --extra-tests ... --coverage ... --all-submissions
# generated basis (end-to-end driver; see gen_qualify.py)
python3 pipeline/ratings-pools/800/tools/gen_qualify.py --id ID --workspace W
```

## What the auditor must check for each package

1. Statement, constraints and the single-answer claim (`UNIQUENESS`) against `packages/ID/statement.html`. The recipe's
   `validate()` must reject every out-of-constraint input.
2. Coverage: the boundary, adversarial and maxSize cases in `extra()` really are what their labels say.
3. Generated basis: two sandbox runs of the generator are byte-identical. The oracle passes every sample, official pair
   and generated pair. It is a genuinely independent public source, not one of the five counted sources.
4. Each counted incorrect submission has a concrete algorithmic defect at its `failedTest` (WA or complexity), and goes
   into `incorrectAnalysis`. CE, RE and infrastructure failures never count.
5. Every hash: `packageHash`, `evidenceHash` (canonical digest of `evidence/ID.json`), source hashes and the bundle
   manifest.

## Quarantined (never counted)

`acceptedContradiction` packages: 49A, 112A, 411A (exact CRLF upstream bytes), 447A and 673A. In each, a public accepted
source compiles under v2 and then fails a pair. The history is kept in `state/ID/evidence-history`.
`worker/exclusions.json` lists each prepare-blocked, truncated or multiple-answer exclusion with its reason.

`generate`-stage oracle defect: 71A. The fixed public oracle overflows `char a[100]` on official test 0008, which has a 100-character word and is within constraints. See `diagnostics/71A-oracle.json`. Not retried with another oracle. It needs a next-stage independent author's oracle.

`generate`-stage oracle defect: 1657B. The fixed public oracle writes `a[n]` past the end of its VLA on official test 0002 (n=100000, within constraints). See `diagnostics/1657B-oracle.json`.

Incomplete, gate not met: 271A (4 incorrect). 1657A: 5 accepted pass, but every public TLE-labelled source passes the whole suite quickly, so only 1 incorrect is confirmed. Its gate is not lowered.
