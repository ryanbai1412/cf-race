# Rated pools: evidence, not metadata

This local-only CLI targets **100 genuinely validated packages per rating**:
800 (default), 1000, 1200, 1400, 1600. `inventory` candidates, dataset
`executable=true`, legacy packages, and successful execution without audit are
**not validated**. There is deliberately no publication command.

## Prerequisites and public sources

Python 3.10+, `requests`, `pyarrow` and Docker are required. These are the only
Python dependencies; the old `import_hf.py` additionally uses `datasets`.
No new root npm dependency is needed. Missing dependencies are blockers.
Read the pinned upstream cards before using these sources:

* [CodeForces](https://huggingface.co/datasets/open-r1/codeforces/blob/fbe3f6e903ee854eec2e69e9d96d0306cde59baf/README.md)
* [Submissions](https://huggingface.co/datasets/open-r1/codeforces-submissions/blob/07e7bf31f284b0e90e02dfc7ab675d5821e1c068/README.md)
* [HF API](https://huggingface.co/docs/hub/en/api)
* [CF API](https://codeforces.com/apiHelp)
* [Docker resource constraints](https://docs.docker.com/engine/containers/resource_constraints/)

Revisions are pinned in `pool_sources.py`. Every downloaded Parquet file must
match the upstream LFS SHA256 **and** full byte size. Failed downloads retry
four times, and partial files are never accepted. Downloads use public HF,
not a credentialed CF proxy. Statements/test metadata are ~2.75GB; selected
accepted/incorrect submissions are ~74MB/~8MB. Contest-specific generated-test
shards can be much larger. Cache is content-addressed and reusable across
workers, while worker output is separated by rating. Do not share a writable
rating workspace between workers. Inventory caches the API snapshot; only
`--refresh-api` changes it. Its hash is included in inventory and provenance.

The actual problem schema has `official_tests` (complete pairs),
`official_tests_complete`, `testset_size`, `generated_tests` (a **count**, not
the pairs), `generated_checker`, `input_mode`, `aliases`, and statement fields.
Generated pairs live in `generated_tests/test_cases_<contest:04d>.parquet`.
The inspected pinned shard uses `test_i`; the card says `test_case_i`. Both
are recognized, with unique identities and exact advertised count required.

Submission rows use `submission_id`, `source`, `contestId`, `problem_index`,
`problem_id` (`contest/index`, including alias normalization),
`programmingLanguage`, `verdict`, `testset`. The accepted subset also has
`og_source`. The card's prose `original_code` is not the actual column name.
`source` can contain upstream compatibility changes: preserve its exact hash
and attribution, and never claim these are untouched originals.

Selected incorrect submissions cover only 2,385 problems. There may not be
five suitable incorrect programs for a candidate. `--all-submissions` scans
the much larger (~5.55GB) pinned default submission dataset as a read-only
alternative; do not claim success if five remain unavailable. Unsupported
languages, non-TESTS submissions, duplicate sources, CE/RE/infrastructure
failures, and incorrect submissions that still pass are excluded explicitly.

### Verified foundation run (2026-10-12)

All default problem shards and the public selected submission subsets were
downloaded and verified at the pins above. Counts are **not validated packages**:

| API rating | Deduplicated inventory | Metadata shortlist | Complete-official shortlist | Selected supported 5/5 candidates (including incomplete) |
| --- | ---: | ---: | ---: | ---: |
| 800 | 913 | 764 | 184 | 58 |
| 1000 | 358 | 293 | 96 | 41 |
| 1200 | 408 | 317 | 70 | 60 |
| 1400 | 403 | 305 | 70 | 47 |
| 1600 | 476 | 351 | 81 | 50 |

No complete-official shortlisted candidate has supported incorrect sources
in the selected subsets. Their complete-official **and** 5/5 intersection is
zero for all five ratings. The larger default submission data was not executed
in this foundation run. Four complete-source shortlists are already below100;
These are historical fully-official-path availability counts, not limits on the
generated qualification path below. Incomplete official suites no longer exclude
an otherwise eligible candidate. CF API metadata is accessible; no CF proxy credential was used.

Real diagnostic pilot691A (API1000):30 of83 advertised official pairs,
all9 generated pairs,15 authored boundary/adversarial/max-size pairs. Every
supplied pair was checked for exact constraints and expected output with an
authored oracle. Five accepted external programs passed all54 supplied pairs;
five external incorrect programs failed concrete pairs in the pinned offline
sandbox. Three duplicate/unsupported/nonfinal sources were excluded. It is
**not validated**: independent generated-basis oracle execution/review and audit
are missing. Its old15 authored cases are not an extensive generated suite.
The53 missing official pairs prevent the official path, not the generated path.

Pilot27A (API1200) retained malformed upstream generated input unchanged;
accepted-source contradictions make it incomplete (3 accepted,0 incorrect,
12 excluded). Never repair or truncate upstream bytes silently to claim success.
Final validated counts are **0/0/0/0/0**, and publication dry-run fails closed.
The attached reproducible artifacts retain both diagnostics and exact evidence.

## Commands (one worker per R)

```sh
R=1200
W="$HOME/Documents/cf-pools"
C="$HOME/.cache/cf-race-pool"
docker pull python@sha256:5887f265d8d44d8b4734d3658b21d668edf5aaf92e4945bc0c984afbfab105d3
python3 pipeline/rated_pool.py inventory --rating "$R" --target 100 --workspace "$W" --cache "$C"
python3 pipeline/rated_pool.py prepare --rating "$R" --id 27A --workspace "$W" --cache "$C"
python3 pipeline/rated_pool.py generate --rating "$R" --id 27A --workspace "$W" --cache "$C" --extra-tests extra-27A.json
python3 pipeline/rated_pool.py validate --rating "$R" --id 27A --workspace "$W" --cache "$C" --coverage coverage-27A.json --validator worker-identity
python3 pipeline/rated_pool.py report --rating "$R" --workspace "$W"
python3 pipeline/rated_pool.py publish-dry-run --rating "$R" --id 27A --workspace "$W"
python3 pipeline/rated_pool.py archive --rating "$R" --id 27A --workspace "$W" --output "$HOME/Documents/27A-tests.tar.gz"
```

`--shards data/train-00003-of-00011.parquet` supports a quick partial pilot;
the inventory records the partial scope. Default inventory includes train
and test splits. This is ingestion/verification, not model training. Preserve
the upstream request not to train on the test split. `--rating` defaults to800
in this CLI and the backward-compatible `select_problems.py [count] [seed]`.
The selector also accepts `--rating` and `--years`; `now` can be injected for
deterministic tests. Import/scraping requires the official API rating; neither
silently invents800. API tags are stored in package metadata, not fabricated
from title or inherited from another candidate.

Outputs are unique to `W/R`: `inventory.json`, `api-problems.json`,
`packages/ID/`, `state/ID/`, `evidence/ID.json`, `audits/ID.json`, `report.json`.
Package format is the existing `meta.json`, `statement.html`, `samples/`,
`tests/NNNN.in` and `.out`, plus attribution in `provenance.json`.
**Never write the shared root tests manifest.** Each worker archives its own
tests and provenance instead. Do not force-add gitignored tests to Git.

Inventory is sorted/deduplicated by canonical source IDs and aliases. Its
metadata-eligible count is only a shortlist. `prepare` checks nonempty full
statement/input/output/examples and nontruncated official pairs; `generate`
imports **every** available official pair and **all** advertised generated
pairs. There are two qualification bases, explicitly recorded as
`provenance.qualification.basis` and `evidence.qualificationBasis`:

* **official**: requires `officialComplete=true` and exact advertised/included
  official counts. This path and existing complete-official records remain compatible.
* **generated**: incomplete official pairs are supplementary known-valid pairs,
  never claimed complete. Require deterministic extensive authored generation,
  an independently authored constraint-aware oracle/brute checked on every supplied
  pair, full5AC/5algorithmically-wrong execution and independent hash-bound audit.

`completeSourceEligible` is only the official-path shortlist, not an upper bound
on generated eligibility. Neither shortlist implies validation. Special-checker,
interactive/file-IO and samples-only packages fail closed. Numeric/float and
multiple-answer tasks need a separate audited judge-compatible checker design;
there is no automatic special-checker execution or constructive-tag shortcut.

`--extra-tests` is an authored JSON list of `{input, output}` pairs. Preserve
the deterministic generator/reference source in the worker's artifact and
document constraints. Do not execute downloaded generators on the host.
All extra outputs are checked against five external accepted programs.
Those programs serve as external references, with source code retained
in `state/ID/sources/` for reproduction. A bad reference/output is a gap,
not a reason to weaken checking.

### Generated qualification command and artifacts

```sh
python3 pipeline/rated_pool.py generate --rating "$R" --id "$PID" --workspace "$W" --cache "$C" \
  --generator-source generator.py --generator-author "worker-$R" --seed 42 \
  --oracle-source independent-oracle.py --oracle-author independent-oracle-worker \
  --oracle-review-url https://example.com/actual-independent-review
# Author coverage with the newly reported packageHash, then unchanged validate/report/archive stages.
```

The generator reads that integer from stdin and emits a JSON list of complete `{input,output}` pairs
on stdout. It runs **twice**, offline/resource-bounded; bytes must match exactly.
The oracle reads one full test on stdin and returns the expected answer on stdout;
it must check input constraints and have an independent brute/reference algorithm.
All imported pairs also pass it; contradictions quarantine generation rather than
silently dropping/fixing data. Programs must be self-contained Python3 or C++;
`--generator-language 'GNU C++17'` / `--oracle-language 'GNU C++17'` select C++.
Python3 is default. Generator CPU is10s/memory1024MB; output is bounded to8MB by
the harness. Oracle limits are the problem's time/memory limits. No host execution.

Extensive mode requires at least100 distinct authored inputs, plus independently
reviewed **authored** boundary, maximum-size and adversarial cases named in coverage.
For a genuinely smaller finite domain, use `--exhaustive-domain-size N
--exhaustive-domain 'exact legal finite input domain'`: generated distinct inputs
must equal N and the independent audit must also approve `checks.exhaustiveDomain`.
The count is a minimum diversity check, not proof of semantic completeness.
Independent audit must review all constraints, domain enumeration, oracle/brute
independence, reproducibility and coverage; metadata booleans alone never qualify.

Do not combine `--extra-tests` with generated qualification. Preserve sources and
proofs in package `qualification/{generator.py|generator.cpp,oracle.py|oracle.cpp,
generation.json,oracle.json}`. Every byte is in the package manifest and approval;
these additional files do not change existing tests/judge semantics. Generator
proof binds source/seed/repeated output hashes and the authored pair digest.
Oracle proof binds independent identity/review URL/source hash and every actual
per-test result/output hash. Oracle author differs from generator/validator, and
oracle source must not duplicate any counted external reference or generator.
An operator must verify these claimed identities via the review links.
`--extra-tests` alone is diagnostic unless a complete official suite already exists.
Never fabricate an independent oracle/audit identity to upgrade the old pilot.

### Coverage record

After generation, take the exact reported `packageHash` and write:

```json
{
  "packageHash": "<hash from generate>",
  "boundary": [{"test": "0034", "reason": "minimum n; index1 present"}],
  "adversarial": [{"test": "0038", "reason": "internal missing index"}],
  "maxSize": [{"test": "0036", "reason": "all3000 values; answer3001"}],
  "inputConstraints": "Explain why every test is valid under the complete statement.",
  "checkerSemantics": "Explain why token matching is correct and output is unique.",
  "statementComplete": "Describe statement/input/output/constraints review."
}
```

These explanations are claims for an **independent reviewer to audit**, not
machine proof of semantic completeness. Named tests must exist. The reviewer
must inspect all upstream and authored tests, constraints, maximum sizes,
references, checker semantics, statement completeness, attribution and results.

### Independent audit

Execution stores `execution-passed` only after **5 distinct accepted sources
pass every test and 5 distinct WA/TLE sources fail on a concrete valid test**.
The same source hash or submission ID cannot count twice. Result caches bind
package/source/image/harness/runner/checker hashes and permit interrupted validation
to resume without reexecuting unchanged sources. Package/API/source changes
invalidate later stages and stale audits. Missing/empty/unpaired/truncated
tests, mismatched hashes and incomplete stages fail closed.

No `audit` command auto-approves anything. A separate agent/reviewer writes
`W/R/audits/ID.json` after independent inspection:

```json
{
  "approved": true,
  "reviewer": "independent-agent-identity-different-from-validator",
  "reviewUrl": "https://.../independent-review-evidence",
  "evidenceHash": "<canonical digest of complete evidence JSON>",
  "packageHash": "<package hash>",
  "checks": {
    "sourceAttribution": true, "fullTests": true, "coverage": true,
    "fiveAcceptedFiveIncorrect": true, "noSpecialChecker": true, "hashes": true
  }
}
```

Use `pool_contract.digest(read_json(path))` for canonical hashes. Audit and
approval files are local attestations, not a cryptographic identity system.
The operator must verify the linked independent reviewer and approval were
actually authorized; do not author your own purported independent signoff.

Generated audits additionally declare `qualificationBasis: "generated"`, and
checks `deterministicGeneration`, `independentOracle`, `generatedBasis`,
`algorithmicallyWrong`, `inputConstraints` must each be true. In
`incorrectAnalysis`, include **every** counted incorrect submission ID as key:
`{"reason":"specific algorithmic defect", "kind":"wrong-answer"|"complexity",
"test":"failedTest from execution"}`. The reviewer must inspect those programs
and concrete counterexamples; CE/RE/infrastructure failures never count.
Coverage's `inputConstraints` and the oracle/brute review must explicitly address
real upstream constraint contradictions; accepted-source contradictions still block
either path. `fullTests` in a generated audit means the complete explicitly declared
generated qualification basis plus all supplied supplementary pairs, not all original
official CF tests. Independent audit/approval and publication rules are unchanged.

## Sandbox and verdicts

No downloaded code executes on the host. The pinned official Python image
contains Python3.11 and g++12.2. Compilation and execution are offline in a
nonroot, read-only-root, capability-free, no-new-privileges Docker container.
Only source/input payload and the trusted harness are mounted read-only:
no repository, Docker socket, credentials, environment files, expected
outputs, or reference programs are mounted. Network is `none`; container
CPU1, memory1280MB/no swap, PIDs64, bounded tmpfs/open files/output, compile
CPU30s/wall60s and per-test CPU/memory/wall limits are enforced. The host Docker
client gets only PATH/HOME, never inherited secret variables. The checker runs
on the host on returned output hashes, matching the existing token/YES-NO judge.
Floating checks are not enabled. Compile/runtime/infrastructure failures do
not count as a successfully killed incorrect solution. CPython and C++ are
supported; PyPy is excluded rather than pretending timing equivalence.

Docker is a resource/security boundary for public contest code, not a promise
to safely run deliberately hostile malware. Kernel/runtime must be trusted
and maintained; use a dedicated VM for this work.

## Publication is separately gated

`publish-dry-run` makes **zero remote calls** and needs complete evidence and
independent audit. Real content upload remains in the existing authorized
seed/upload tools, guarded **before bucket creation or writes**. For new
packages, set `RATED_POOL_EVIDENCE_ROOT=W` and `RATED_POOL_APPROVAL=approval.json`
only after the operator explicitly approves publication. Approval format:

```json
{
  "action": "publish", "approvedBy": "authorized-human", "approvalUrl": "https://...",
  "packages": {"27A": {"packageHash": "...", "evidenceHash": "...", "auditHash": "..."}}
}
```

Copy an audited package into `problems/ID` without changing any byte. Both
uploaders snapshot files, verify every uploaded byte against approved evidence,
and derive table content from those same immutable bytes. Unexpected files or
symlinks fail. Tags remain in package metadata: the existing table uploader
does not assume a new tags column. Hidden/active flags are omitted from upserts
so maintenance does not reset them. No schema changes are made here.

`legacy_800.json` enumerates preexisting800 IDs solely for intentional existing
package maintenance. The exemption applies only to rating800 packages without
`poolPipeline`, plus local dev fixtures. **It never increases validated counts.**
New800s and all new harder packages require the same full gate; changing an
existing ID's rating to a harder value disables the exemption. `import_hf.py`
marks new imports pipeline-managed, including full tests, but ingestion alone
cannot grant publication: use the rated workflow to generate evidence.

## Artifact reproduction

`archive` is byte-deterministic (sorted paths, normalized tar metadata, zero
gzip timestamp) and includes the full package/test pairs, source row, exact external
reference/submission source code, resume state, evidence and optional audit.
Its companion `.provenance.json` has archive SHA256, size, complete per-byte
package **and archive** manifests and dataset revisions. Deliver both through attachment URLs.
Verify `sha256sum archive.tar.gz` before extraction. A worker must attach its
deterministic extra-test generator/coverage review too. Unit tests are delivered
as a gitignored test archive rather than force-added to Git. Archive creation
does not imply validation or publication approval.
