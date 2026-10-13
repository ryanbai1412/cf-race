# Rating 1400: independent audit report

Reviewer: `devin-independent-auditor-session-4faf13bf1be94c698c44ee6503b27b8c` (https://staging.itsdev.in/sessions/4faf13bf1be94c698c44ee6503b27b8c)

**Verified: 21 of 74 candidates** (270B, 277A, 279A, 315A, 334B, 358A, 388A, 38C, 41B, 435B, 441B, 489C, 507B, 548B, 550B, 604B, 710B, 757B, 803A, 911C, 940B). The target is 100, so it is **not reached**. The current whole-pool archive has 135 packages; this audit covers all 74 builder execution-passed IDs: the 39 handed to the primary first (the 28 v2 IDs, 27 byte-identical and 226A changed, plus the 11 builder-child-approved IDs) and, in v4, the 35 remaining execution-passed IDs (16 builder-child-held/rejected and 19 never audited), none of which validated. The other 61 whole-pool IDs are not execution-passed/quarantined by the builder. Builder child approvals are not inherited.
Builder child audits were read for cross-checking only; none of their approvals are inherited. Disagreements are listed below.

**Correction:** this report supersedes the 21/28 audit (commit `451e9eb1`, JSON SHA256 `d0d260c90e5e5b3dc2c3edeb728b47325177ae651c733c7ba488ab9a18f94f0c`). v4: the 35 remaining current execution-passed IDs (builder child-held/rejected and never-audited) were primary-audited on the unchanged whole-pool bytes; none validated (9 REJECTED, 26 NOT_VALIDATED_HELD), so the count stays 21. 911C extra-source exclusion wording corrected (UB-only, 1,758 inputs not exhaustive); its per-ID audit file and auditHash are unchanged. Superseded 125A audit SHA256 `38d08811b28b0104472dfbf77ecc9fad2b2b4a6b91b8763f71cadcf4b8d1ed65`, auditHash `73d11041e9fdda74ec412a1b7bbe31007ce798254ece1f789a469188f458d2e1`. Earlier: 13/28 audit `a1ac5783` (`12790623ac6e9579452775da04113cec478872a052472e68ceaafa4a441d0f60`); superseded 197B audit SHA256 `f8961310a3ff83f18f6224c188a8490f8b4d254d6aaa2311bea0697a943430c5`, auditHash `99da7ad0a64f7eeec85975e941ab01edebd4d28eb332f9d2929cba9fc0af0944`.

- Builder branch `devin/1791845646-rated-1400` @ `556e9047951a6774775812684c3a5cb516789f3d`
- Bundle SHA256 `05f8c1e2b4e896b45be0eb85cc02cab9e10b0aeac0f48f59164138f274de13a7`: verified=True
- Pinned datasets: open-r1/codeforces@fbe3f6e903ee854eec2e69e9d96d0306cde59baf, open-r1/codeforces-submissions@07e7bf31f284b0e90e02dfc7ab675d5821e1c068; 38/38 shard SHA256 and byte sizes re-verified
- Sandbox: pipeline/pool_sandbox.py: pinned python@sha256:5887f265..., network none, uid 65534, read-only rootfs, cap-drop ALL, no-new-privileges, pids 64, 1 CPU, 1280m mem, no swap; no third-party code was run on the host
- Policy: Per the handoff ('Incorrect timeouts/unsupported languages cannot count as a killed algorithmic wrong solution'), this audit counts only WA kills on a concrete valid test, from sources with a genuine algorithmic defect. TLE/complexity, RE, placeholder and debug-output sources are not counted, even though pool_generation accepts kind=complexity.

## Summary

| Problem | Verdict | Tests (official/open-r1 gen/authored) | Accepted reproduced | Counted WA kills | Extra CF-WA killed | Extra CF-OK passing | Issues |
|---|---|---|---|---|---|---|---|
| 107A | **NOT_VALIDATED_HELD** | 179 (16 partial/13/150) | 5/5 | 2/5 | 15/15 | 11/14 | only 2/5 incorrect sources are counted WA algorithmic kills |
| 125A | **NOT_VALIDATED_HELD** | 172 (22/0/150) | 5/5 | 4/5 | 33/33 | 20/20 | only 4/5 incorrect sources are counted WA algorithmic kills |
| 152C | **REJECTED** | 178 (16 partial/12/150) | 5/5 | 5/5 | 37/37 | 18/20 | accepted contradiction: CF-OK source(s) 19459348(RE@0001) fail the package; cause: CRLF bytes reach Python input(); passes on LF-normalized tests |
| 175A | **REJECTED** | 284 (134/0/150) | 5/5 | 4/5 | 36/36 | 5/18 | accepted contradiction: CF-OK source(s) 37495712(RE@0001), 124238640(RE@0001), 27107190(RE@0001), 196162162(RE@0001), 55006515(RE@0001), 35154521(RE@0001), 78795916(RE@0001), 29819107(RE@0001), 44186543(RE@0001), 46821841(RE@0001), 29784607(RE@0001), 34276976(RE@0001) fail the package; cause: CRLF bytes reach Python input(); passes on LF-normalized tests; only 4/5 incorrect sources are counted WA algorithmic kills |
| 197B | **NOT_VALIDATED_HELD** | 201 (42 partial/9/150) | 5/5 | 3/5 | 49/49 | 16/18 | only 3/5 incorrect sources are counted WA algorithmic kills |
| 198B | **REJECTED** | 182 (23 partial/9/150) | 5/5 | 3/5 | 7/8 | 6/9 | only 3/5 incorrect sources are counted WA algorithmic kills; coverage gap: CF-WRONG_ANSWER source(s) 11382563 pass the full package |
| 226A | **NOT_VALIDATED_HELD** | 228 (78/0/150) | 5/5 | 3/5 | 0/0 | 0/0 | only 3/5 incorrect sources are counted WA algorithmic kills |
| 233B | **NOT_VALIDATED_HELD** | 198 (48/0/150) | 5/5 | 3/5 | 22/22 | 12/12 | only 3/5 incorrect sources are counted WA algorithmic kills |
| 245E | **REJECTED** | 200 (41 partial/9/150) | 5/5 | 1/5 | 32/32 | 5/20 | accepted contradiction: CF-OK source(s) 29488834(WA@0002), 6912638(WA@0002), 31526728(WA@0001), 3685951(WA@0001), 17802998(WA@0002), 4891069(WA@0002), 4435266(WA@0002), 42447218(WA@0002), 49460007(WA@0001), 69404238(WA@0002), 17833202(WA@0002), 14563275(WA@0002), 10341189(WA@0002), 13907610(WA@0001) fail the package; cause: CRLF bytes reach Python input(); passes on LF-normalized tests; only 1/5 incorrect sources are counted WA algorithmic kills |
| 248B | **REJECTED** | 216 (66/0/150) | 5/5 | 5/5 | 49/49 | 7/20 | accepted contradiction: CF-OK source(s) 31873459(RE@0019), 27547806(RE@0019), 32332414(RE@0019), 4713392(RE@0019), 9705234(RE@0019), 32011925(RE@0019), 11022217(RE@0019), 14779449(RE@0019), 26181773(RE@0019), 7776787(RE@0019), 4786395(RE@0019), 17711024(RE@0019), 13496928(RE@0019) fail the package; cause: Python 3.11 sandbox int-str 4300-digit limit (harness fidelity) |
| 261A | **NOT_VALIDATED_HELD** | 180 (9 partial/21/150) | 5/5 | 3/5 | 11/11 | 20/20 | only 3/5 incorrect sources are counted WA algorithmic kills |
| 270B | **VALIDATED** | 183 (24 partial/9/150) | 5/5 | 5/5 | 0/0 | 9/9 | none |
| 272B | **NOT_VALIDATED_HELD** | 173 (11 partial/12/150) | 5/5 | 4/5 | 0/0 | 16/17 | only 4/5 incorrect sources are counted WA algorithmic kills |
| 277A | **VALIDATED** | 180 (14 partial/16/150) | 5/5 | 5/5 | 130/130 | 19/20 | none |
| 279A | **VALIDATED** | 182 (32/0/150) | 5/5 | 5/5 | 2/2 | 9/9 | none |
| 279B | **NOT_VALIDATED_HELD** | 180 (13 partial/17/150) | 5/5 | 4/5 | 30/30 | 20/20 | only 4/5 incorrect sources are counted WA algorithmic kills |
| 289B | **NOT_VALIDATED_HELD** | 180 (12 partial/18/150) | 5/5 | 4/5 | 38/38 | 19/20 | only 4/5 incorrect sources are counted WA algorithmic kills |
| 315A | **VALIDATED** | 180 (19 partial/11/150) | 5/5 | 5/5 | 30/30 | 20/20 | none |
| 334B | **VALIDATED** | 195 (45/0/150) | 5/5 | 5/5 | 30/30 | 19/20 | none |
| 337B | **NOT_VALIDATED_HELD** | 184 (34/0/150) | 5/5 | 1/5 | 4/4 | 16/18 | only 1/5 incorrect sources are counted WA algorithmic kills |
| 358A | **VALIDATED** | 186 (28 partial/8/150) | 5/5 | 5/5 | 30/30 | 20/20 | none |
| 388A | **VALIDATED** | 186 (36/0/150) | 5/5 | 5/5 | 30/30 | 20/20 | none |
| 38C | **VALIDATED** | 185 (27 partial/8/150) | 5/5 | 5/5 | 16/16 | 18/20 | none |
| 417B | **NOT_VALIDATED_HELD** | 183 (24 partial/9/150) | 5/5 | 4/5 | 21/21 | 18/18 | only 4/5 incorrect sources are counted WA algorithmic kills |
| 41B | **VALIDATED** | 180 (15 partial/15/150) | 5/5 | 5/5 | 12/12 | 19/20 | none |
| 435B | **VALIDATED** | 196 (46/0/150) | 5/5 | 5/5 | 30/30 | 20/20 | none |
| 441B | **VALIDATED** | 190 (31 partial/9/150) | 5/5 | 5/5 | 30/30 | 19/20 | none |
| 489C | **VALIDATED** | 215 (65/0/150) | 5/5 | 5/5 | 30/30 | 20/20 | none |
| 507B | **VALIDATED** | 187 (37/0/150) | 5/5 | 5/5 | 30/30 | 19/20 | none |
| 518B | **REJECTED** | 180 (18 partial/12/150) | 5/5 | 1/5 | 30/30 | 8/20 | accepted contradiction: CF-OK source(s) 9997130(WA@0001), 9998838(RE@0001), 43168918(WA@0001), 50663320(RE@0001), 46821685(WA@0001), 10002420(WA@0001), 9988304(WA@0001), 9994921(RE@0001), 42126459(WA@0001), 20403986(WA@0001), 10000805(WA@0001) fail the package; cause: CRLF bytes reach Python input(); passes on LF-normalized tests; only 1/5 incorrect sources are counted WA algorithmic kills |
| 548B | **VALIDATED** | 162 (10 partial/2/150) | 5/5 | 5/5 | 30/30 | 19/20 | none |
| 550B | **VALIDATED** | 180 (30/0/150) | 5/5 | 5/5 | 4/4 | 19/20 | none |
| 604B | **VALIDATED** | 184 (26 partial/8/150) | 5/5 | 5/5 | 30/30 | 20/20 | none |
| 710B | **VALIDATED** | 182 (23 partial/9/150) | 5/5 | 5/5 | 30/30 | 20/20 | none |
| 757B | **VALIDATED** | 238 (79 partial/9/150) | 5/5 | 5/5 | 30/30 | 20/20 | none |
| 803A | **VALIDATED** | 318 (168/0/150) | 5/5 | 5/5 | 30/30 | 20/20 | none |
| 911C | **VALIDATED** | 217 (67/0/150) | 5/5 | 5/5 | 28/30 | 20/20 | none |
| 920C | **REJECTED** | 280 (120 partial/10/150) | 5/5 | 5/5 | 30/30 | 14/20 | accepted contradiction: CF-OK source(s) 34864682(RE@0001), 34855332(RE@0001), 34849132(RE@0001), 34856737(RE@0001), 34852086(RE@0001) fail the package; cause: CRLF bytes reach Python input(); passes on LF-normalized tests |
| 940B | **VALIDATED** | 208 (58/0/150) | 5/5 | 5/5 | 30/30 | 20/20 | none |

## Disagreements with builder child audits

- 125A: child 946996ea approved; this audit NOT_VALIDATED_HELD (only 4/5 incorrect sources are counted WA algorithmic kills)
- 152C: child 126f9ac4 approved; this audit REJECTED (accepted contradiction: CF-OK source(s) 19459348(RE@0001) fail the package; cause: CRLF bytes reach Python input(); passes on LF-normalized tests)
- 198B: child 946996ea approved; this audit REJECTED (only 3/5 incorrect sources are counted WA algorithmic kills; coverage gap: CF-WRONG_ANSWER source(s) 11382563 pass the full package)
- 233B: child d95ca109 approved; this audit NOT_VALIDATED_HELD (only 3/5 incorrect sources are counted WA algorithmic kills)
- 248B: child 946996ea approved; this audit REJECTED (accepted contradiction: CF-OK source(s) 31873459(RE@0019), 27547806(RE@0019), 32332414(RE@0019), 4713392(RE@0019), 9705234(RE@0019), 32011925(RE@0019), 11022217(RE@0019), 14779449(RE@0019), 26181773(RE@0019), 7776787(RE@0019), 4786395(RE@0019), 17711024(RE@0019), 13496928(RE@0019) fail the package; cause: Python 3.11 sandbox int-str 4300-digit limit (harness fidelity))
- 272B: child f009e0db approved; this audit NOT_VALIDATED_HELD (only 4/5 incorrect sources are counted WA algorithmic kills)
- 279B: child 126f9ac4 approved; this audit NOT_VALIDATED_HELD (only 4/5 incorrect sources are counted WA algorithmic kills)
- 289B: child f009e0db approved; this audit NOT_VALIDATED_HELD (only 4/5 incorrect sources are counted WA algorithmic kills)
- 417B: child d95ca109 approved; this audit NOT_VALIDATED_HELD (only 4/5 incorrect sources are counted WA algorithmic kills)
- 920C: child b93287be approved; this audit REJECTED (accepted contradiction: CF-OK source(s) 34864682(RE@0001), 34855332(RE@0001), 34849132(RE@0001), 34856737(RE@0001), 34852086(RE@0001) fail the package; cause: CRLF bytes reach Python input(); passes on LF-normalized tests)

## What was executed

1. Re-ran all 280 builder-selected sources against every package test in the bounded sandbox. Verdicts, first failed test and every per-test output hash were compared with the builder evidence.
2. Wrote my own statement-derived validator, direct solution and brute force for each problem. Checked every package test and sample for input bounds, exact expected output and output uniqueness (all 28 problems have a unique answer, with no special checker).
3. Matched every official, open-r1 generated and sample pair byte-for-byte against the pinned open-r1/codeforces parquet rows. Matched every external source's SHA256 against the pinned codeforces-submissions rows, and checked the CF rating against the Codeforces API and the dataset.
4. Re-ran each builder generator twice and each independent oracle once in the sandbox. Checked the repeat hashes, the pairs digest, byte equality of all 150 authored pairs, and the oracle's AC/output hashes over the full suite.
5. Generated my own corner/max-size stress tests (seeded, with brute-force cross-checks) and ran all 5 accepted sources plus the builder oracle per problem.
6. Ran additional supported-language CF WRONG_ANSWER sources from the downloaded pinned shards: all of them for the initial 9 problems, and up to 30 per problem (lowest submission IDs) for the 19 new ones. A passing one is a coverage gap. Also ran up to 20 additional CF OK sources per problem. A failing one counts as an accepted contradiction, unless its source was confirmed to be genuinely wrong (CF's tests were weaker), it hits an unsupported runtime/compiler feature, or it fails only by TLE (timing fidelity). Each such case is classified in the JSON.
7. Re-ran all non-TLE selected sources on LF-normalized copies of the tests, to find kills that depend only on CRLF bytes reaching Python input().
8. Captured the actual output of every selected WA/RE source on its recorded failed test, and ran de-debugged mutants (debug print lines removed only) where a kill looked like output noise.
9. Ran `pool_contract.verify_evidence` and `publication_gate(require_approval=False)` for every package this audit approved.

## Whole-pool reconciliation (v3)

- Whole-pool archive SHA256 `0637f17856db18a669f39640d39c8d2ffbd80b9c1866d30de8ded075f06e8ab9` (37252 SHA256SUMS entries verified); builder ledger `7534943681853e0dc133351f956cefc1fab4e5405beaaf4c390815f36a2732dc`; manifest `3a0c4e48db105837a8f8864294baf7a25add10fab17f0f84b410bd202f5fa45e`.
- package/evidence hashes recomputed with pool_contract.manifest/digest, not taken from the builder ledger. 27 of the 28 reviewed IDs are byte-identical, so their verdicts stand without rerun; 226A changed and was re-audited; the 11 child-approved IDs were audited from scratch (child approvals not inherited). Sources were re-extracted from the pinned codeforces-submissions shards with SHA256 checks, because the whole-pool archive carries no source code.
- Byte-identical to reviewed v2 bytes: 27 (107A, 125A, 152C, 175A, 197B, 198B, 233B, 245E, 248B, 261A, 270B, 272B, 277A, 279A, 279B, 289B, 315A, 334B, 337B, 358A, 388A, 38C, 417B, 41B, 435B, 518B, 548B). Changed: 226A.
- For the 12 v3 IDs I repeated steps 1-9 on the whole-pool bytes: all 120 selected sources rerun (verdicts, failed tests and every per-test output hash match the builder evidence), LF reruns, generator x2 and oracle replays, pinned-parquet provenance, my own validators/references/brute forces on every test, seeded stress tests on all accepted sources and builder oracles, up to 30 extra CF-WA and 20 extra CF-OK sources per problem, and per-kill source-level witnesses (fault line plus same-field-count semantically wrong output on a valid LF test, YES/NO case-insensitive).

## v4: remaining 35 execution-passed IDs

all 350 selected sources of the 35 v4 IDs classified (GENUINE-BOUND / EXCLUDED / CRLF-ONLY / TIMING-ONLY / FAIL-FAST-NOT-REVIEWED / NOT-COUNTED); 13 IDs with up to 5 non-timing non-CRLF incorrect refs got full source review, independent validators/references/brute forces, generator/oracle replay, pinned provenance, extra CF-WA/CF-OK scans and LF reruns; every bound failedTest re-run on original and LF bytes (rectest4.json); 30 source witnesses in witness4.json. A ref counts only if its evidence-bound recorded failedTest is a semantic failure on both original and LF bytes.

Fail-fast order: malformed package or accepted-source contradiction -> REJECTED; fewer than 5 genuine algorithmic incorrect refs bound to a semantically failing recorded failedTest -> NOT_VALIDATED_HELD. Timing-only (builder TLE) and CRLF-only refs are excluded before source review; debug/prompt output, placeholders, different-problem sources, order-only output, typo-only output, %I64d/ABI output and recorded failures that disappear on LF bytes are excluded after source review. A later genuine witness never replaces the evidence-bound failedTest.

| Problem | Verdict | Genuine bound refs | Issues |
|---|---|---|---|
| 124B | **REJECTED** | 0/5 | MALFORMED: pool_contract.manifest() rejects the whole-pool package (missing or unpaired tests; no .in files) although evidence testCount=135; 5 rerun verdict/failedTest mismatches (TLE/partial-output timing variance); FAIL-FAST: 2 incorrect ref(s) are timing-only (builder TLE) and 3 have a CRLF-only recorded failedTest, so at most 0/5 could be genuine algorithmic kills; held without individual source certification |
| 19A | **REJECTED** | 0/5 | accepted contradiction: CF-OK source(s) 77276315(WA@0001), 78387799(RE@0001), 79005855(RE@0001), 82287034(WA@0002), 79771886(WA@0002), 90210078(RE@0001), 79120583(WA@0002), 5353782(RE@0001), 79043682(RE@0001), 79062878(WA@0002), 77110073(RE@0001), 7100781(RE@0001), 77880004(RE@0001) fail the package; causes: CRLF bytes reach Python input(); passes on LF-normalized tests / UNRESOLVED: still fails on LF-normalized tests (['WA', '0060']); package rejected regardless; only 0/5 incorrect sources are genuine algorithmic kills bound to a semantically failing recorded test (source-level review) |
| 284A | **NOT_VALIDATED_HELD** | 0/5 | FAIL-FAST: 3 incorrect ref(s) are timing-only (builder TLE) and 0 have a CRLF-only recorded failedTest, so at most 2/5 could be genuine algorithmic kills; held without individual source certification |
| 414B | **NOT_VALIDATED_HELD** | 0/5 | FAIL-FAST: 1 incorrect ref(s) are timing-only (builder TLE) and 0 have a CRLF-only recorded failedTest, so at most 4/5 could be genuine algorithmic kills; held without individual source certification |
| 448B | **REJECTED** | 2/5 | accepted contradiction: CF-OK source(s) 7128394(RE@0002), 116174909(RE@0001), 7130147(WA@0042) fail the package; causes: CRLF bytes reach Python input(); passes on LF-normalized tests / UNRESOLVED: still fails on LF-normalized tests (['WA', '0042']); package rejected regardless; only 2/5 incorrect sources are genuine algorithmic kills bound to a semantically failing recorded test (source-level review) |
| 475B | **REJECTED** | 0/5 | accepted contradiction: CF-OK source(s) 8086823(WA@0004), 8098654(WA@0004), 8088012(WA@0001), 8088601(WA@0004), 8089280(WA@0002), 8092429(WA@0002) fail the package; causes: CRLF bytes reach Python input(); passes on LF-normalized tests; only 0/5 incorrect sources are genuine algorithmic kills bound to a semantically failing recorded test (source-level review) |
| 485A | **NOT_VALIDATED_HELD** | 0/5 | FAIL-FAST: 1 incorrect ref(s) are timing-only (builder TLE) and 0 have a CRLF-only recorded failedTest, so at most 4/5 could be genuine algorithmic kills; held without individual source certification |
| 505B | **NOT_VALIDATED_HELD** | 0/5 | FAIL-FAST: 1 incorrect ref(s) are timing-only (builder TLE) and 0 have a CRLF-only recorded failedTest, so at most 4/5 could be genuine algorithmic kills; held without individual source certification |
| 515C | **NOT_VALIDATED_HELD** | 0/5 | FAIL-FAST: 1 incorrect ref(s) are timing-only (builder TLE) and 0 have a CRLF-only recorded failedTest, so at most 4/5 could be genuine algorithmic kills; held without individual source certification |
| 520B | **NOT_VALIDATED_HELD** | 0/5 | FAIL-FAST: 1 incorrect ref(s) are timing-only (builder TLE) and 0 have a CRLF-only recorded failedTest, so at most 4/5 could be genuine algorithmic kills; held without individual source certification |
| 525B | **NOT_VALIDATED_HELD** | 0/5 | FAIL-FAST: 0 incorrect ref(s) are timing-only (builder TLE) and 5 have a CRLF-only recorded failedTest, so at most 0/5 could be genuine algorithmic kills; held without individual source certification |
| 534B | **NOT_VALIDATED_HELD** | 0/5 | FAIL-FAST: 1 incorrect ref(s) are timing-only (builder TLE) and 0 have a CRLF-only recorded failedTest, so at most 4/5 could be genuine algorithmic kills; held without individual source certification |
| 602B | **NOT_VALIDATED_HELD** | 0/5 | FAIL-FAST: 4 incorrect ref(s) are timing-only (builder TLE) and 0 have a CRLF-only recorded failedTest, so at most 1/5 could be genuine algorithmic kills; held without individual source certification |
| 612C | **NOT_VALIDATED_HELD** | 0/5 | FAIL-FAST: 0 incorrect ref(s) are timing-only (builder TLE) and 2 have a CRLF-only recorded failedTest, so at most 3/5 could be genuine algorithmic kills; held without individual source certification |
| 614B | **REJECTED** | 4/5 | accepted contradiction: CF-OK source(s) 15351571(WA@0001) fail the package; causes: CRLF bytes reach Python input(); passes on LF-normalized tests; only 4/5 incorrect sources are genuine algorithmic kills bound to a semantically failing recorded test (source-level review) |
| 637C | **NOT_VALIDATED_HELD** | 0/5 | 1 rerun verdict/failedTest mismatches (TLE/partial-output timing variance); FAIL-FAST: 1 incorrect ref(s) are timing-only (builder TLE) and 1 have a CRLF-only recorded failedTest, so at most 3/5 could be genuine algorithmic kills; held without individual source certification |
| 652A | **NOT_VALIDATED_HELD** | 0/5 | FAIL-FAST: 2 incorrect ref(s) are timing-only (builder TLE) and 0 have a CRLF-only recorded failedTest, so at most 3/5 could be genuine algorithmic kills; held without individual source certification |
| 665B | **REJECTED** | 0/5 | accepted contradiction: CF-OK source(s) 17406330(RE@0001) fail the package; causes: CRLF bytes reach Python input(); passes on LF-normalized tests; only 0/5 incorrect sources are genuine algorithmic kills bound to a semantically failing recorded test (source-level review) |
| 697B | **NOT_VALIDATED_HELD** | 0/5 | only 0/5 incorrect sources are genuine algorithmic kills bound to a semantically failing recorded test (source-level review) |
| 698A | **NOT_VALIDATED_HELD** | 0/5 | only 0/5 incorrect sources are genuine algorithmic kills bound to a semantically failing recorded test (source-level review) |
| 748C | **REJECTED** | 0/5 | accepted contradiction: CF-OK source(s) 23292090(WA@0002), 23293129(WA@0002), 23294073(WA@0001), 23293240(WA@0001) fail the package; causes: CRLF bytes reach Python input(); passes on LF-normalized tests; only 0/5 incorrect sources are genuine algorithmic kills bound to a semantically failing recorded test (source-level review) |
| 762A | **NOT_VALIDATED_HELD** | 0/5 | 2 rerun verdict/failedTest mismatches (TLE/partial-output timing variance); FAIL-FAST: 3 incorrect ref(s) are timing-only (builder TLE) and 0 have a CRLF-only recorded failedTest, so at most 2/5 could be genuine algorithmic kills; held without individual source certification |
| 762B | **NOT_VALIDATED_HELD** | 0/5 | FAIL-FAST: 1 incorrect ref(s) are timing-only (builder TLE) and 0 have a CRLF-only recorded failedTest, so at most 4/5 could be genuine algorithmic kills; held without individual source certification |
| 77A | **NOT_VALIDATED_HELD** | 0/5 | only 0/5 incorrect sources are genuine algorithmic kills bound to a semantically failing recorded test (source-level review) |
| 799B | **NOT_VALIDATED_HELD** | 0/5 | FAIL-FAST: 2 incorrect ref(s) are timing-only (builder TLE) and 0 have a CRLF-only recorded failedTest, so at most 3/5 could be genuine algorithmic kills; held without individual source certification |
| 79B | **NOT_VALIDATED_HELD** | 0/5 | FAIL-FAST: 1 incorrect ref(s) are timing-only (builder TLE) and 0 have a CRLF-only recorded failedTest, so at most 4/5 could be genuine algorithmic kills; held without individual source certification |
| 804B | **NOT_VALIDATED_HELD** | 0/5 | FAIL-FAST: 0 incorrect ref(s) are timing-only (builder TLE) and 2 have a CRLF-only recorded failedTest, so at most 3/5 could be genuine algorithmic kills; held without individual source certification |
| 816B | **NOT_VALIDATED_HELD** | 0/5 | 1 rerun verdict/failedTest mismatches (TLE/partial-output timing variance); FAIL-FAST: 4 incorrect ref(s) are timing-only (builder TLE) and 0 have a CRLF-only recorded failedTest, so at most 1/5 could be genuine algorithmic kills; held without individual source certification |
| 888C | **NOT_VALIDATED_HELD** | 0/5 | FAIL-FAST: 2 incorrect ref(s) are timing-only (builder TLE) and 2 have a CRLF-only recorded failedTest, so at most 1/5 could be genuine algorithmic kills; held without individual source certification |
| 928B | **NOT_VALIDATED_HELD** | 0/5 | 1 rerun verdict/failedTest mismatches (TLE/partial-output timing variance); FAIL-FAST: 1 incorrect ref(s) are timing-only (builder TLE) and 0 have a CRLF-only recorded failedTest, so at most 4/5 could be genuine algorithmic kills; held without individual source certification |
| 934A | **NOT_VALIDATED_HELD** | 4/5 | only 4/5 incorrect sources are genuine algorithmic kills bound to a semantically failing recorded test (source-level review) |
| 954B | **REJECTED** | 5/5 | accepted contradiction: CF-OK source(s) 36472743(WA@0001), 36471818(WA@0001), 36472641(WA@0001) fail the package; causes: CRLF bytes reach Python input(); passes on LF-normalized tests |
| 958A1 | **REJECTED** | 3/5 | accepted contradiction: CF-OK source(s) 37315634(WA@0017), 37915567(WA@0001), 37319998(WA@0001), 37312926(WA@0001), 37320883(WA@0001), 37311989(WA@0001), 37368576(WA@0001), 37318234(WA@0001), 37393354(WA@0001) fail the package; causes: CRLF bytes reach Python input(); passes on LF-normalized tests; only 3/5 incorrect sources are genuine algorithmic kills bound to a semantically failing recorded test (source-level review) |
| 958D1 | **NOT_VALIDATED_HELD** | 0/5 | FAIL-FAST: 2 incorrect ref(s) are timing-only (builder TLE) and 0 have a CRLF-only recorded failedTest, so at most 3/5 could be genuine algorithmic kills; held without individual source certification |
| 995B | **NOT_VALIDATED_HELD** | 0/5 | only 0/5 incorrect sources are genuine algorithmic kills bound to a semantically failing recorded test (source-level review) |

Per-ref classification for the 13 fully source-reviewed v4 IDs:

| Problem | Submission | Builder | Failed test | Class | Reason |
|---|---|---|---|---|---|
| 124B | [127807117](https://codeforces.com/contest/124/submission/127807117) | WA | 0013 | CRLF-ONLY | fails on raw CRLF bytes, AC on LF-normalized tests |
| 124B | [141962151](https://codeforces.com/contest/124/submission/141962151) | TLE | 0005 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 124B | [202297322](https://codeforces.com/contest/124/submission/202297322) | WA | 0009 | CRLF-ONLY | fails on raw CRLF bytes, AC on LF-normalized tests |
| 124B | [202299681](https://codeforces.com/contest/124/submission/202299681) | WA | 0009 | CRLF-ONLY | fails on raw CRLF bytes, AC on LF-normalized tests |
| 124B | [212775202](https://codeforces.com/contest/124/submission/212775202) | TLE | 0005 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 19A | [21260552](https://codeforces.com/contest/19/submission/21260552) | WA | 0001 | EXCLUDED | BINDING: genuine missing goal-difference/goals tie-breakers, but its recorded failedTest 0001 output is the correct set in a different order (not a semantic failure on the bound test). |
| 19A | [26921613](https://codeforces.com/contest/19/submission/26921613) | WA | 0001 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 19A | [35554519](https://codeforces.com/contest/19/submission/35554519) | WA | 0001 | EXCLUDED | PRESENTATION/ORDER-ONLY: stable multi-key sort selects the correct top-n/2 set (semanticWrongTests=0 under set comparison on all LF tests) but prints it in standings order instead of lexicographic order. |
| 19A | [47872149](https://codeforces.com/contest/19/submission/47872149) | WA | 0001 | EXCLUDED | BINDING: recorded failedTest 0001 fails only on CRLF bytes (AC on LF 0001). |
| 19A | [77275072](https://codeforces.com/contest/19/submission/77275072) | WA | 0001 | EXCLUDED | BINDING: recorded failedTest 0001 fails only on CRLF bytes (AC on LF 0001). |
| 284A | [3718084](https://codeforces.com/contest/284/submission/3718084) | TLE | 0007 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 284A | [3718116](https://codeforces.com/contest/284/submission/3718116) | TLE | 0007 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 284A | [13229342](https://codeforces.com/contest/284/submission/13229342) | TLE | 0007 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 414B | [6335341](https://codeforces.com/contest/414/submission/6335341) | TLE | 0004 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 448B | [113440763](https://codeforces.com/contest/448/submission/113440763) | WA | 0001 | EXCLUDED | BINDING: recorded failedTest 0001 fails only on CRLF bytes (AC on LF 0001; first LF failure 0005). |
| 448B | [113473906](https://codeforces.com/contest/448/submission/113473906) | WA | 0006 | GENUINE-BOUND | inverted equality/count flag; z->zz yields both instead of need tree |
| 448B | [115671358](https://codeforces.com/contest/448/submission/115671358) | WA | 0001 | EXCLUDED | BINDING: recorded failedTest 0001 fails only on CRLF bytes (AC on LF 0001; first LF failure 0005). |
| 448B | [116184867](https://codeforces.com/contest/448/submission/116184867) | WA | 0029 | GENUINE-BOUND | greedy index matching (lines 23-37) re-uses earlier positions; returns array/both where need tree is required |
| 448B | [117460936](https://codeforces.com/contest/448/submission/117460936) | WA | 0001 | EXCLUDED | PRESENTATION/TYPO on bound test: recorded failedTest 0001 prints 'automation' for 'automaton' (typo-only); its separate containsAll defect is not the bound failure. |
| 475B | [8095983](https://codeforces.com/contest/475/submission/8095983) | WA | 0008 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 475B | [8100202](https://codeforces.com/contest/475/submission/8100202) | WA | 0004 | CRLF-ONLY | recorded failedTest 0004 fails only on raw CRLF bytes (it passes on LF; first LF-normalized failure WA@0008), so the evidence-bound failure is not an algorithmic witness |
| 475B | [8122708](https://codeforces.com/contest/475/submission/8122708) | WA | 0001 | EXCLUDED | DEBUG OUTPUT: prints the DFS visited list before YES/NO. |
| 475B | [8545870](https://codeforces.com/contest/475/submission/8545870) | WA | 0007 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 475B | [11541454](https://codeforces.com/contest/475/submission/11541454) | WA | 0001 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 485A | [8562250](https://codeforces.com/contest/485/submission/8562250) | TLE | 0010 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 505B | [9477246](https://codeforces.com/contest/505/submission/9477246) | TLE | 0006 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 515C | [79357103](https://codeforces.com/contest/515/submission/79357103) | TLE | 0003 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 520B | [219399057](https://codeforces.com/contest/520/submission/219399057) | TLE | 0002 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 525B | [10464395](https://codeforces.com/contest/525/submission/10464395) | WA | 0001 | CRLF-ONLY | recorded failedTest 0001 fails only on raw CRLF bytes (it passes on LF; first LF-normalized failure TLE@0008), so the evidence-bound failure is not an algorithmic witness |
| 525B | [10465094](https://codeforces.com/contest/525/submission/10465094) | WA | 0001 | CRLF-ONLY | recorded failedTest 0001 fails only on raw CRLF bytes (it passes on LF; first LF-normalized failure WA@0007), so the evidence-bound failure is not an algorithmic witness |
| 525B | [10465962](https://codeforces.com/contest/525/submission/10465962) | WA | 0001 | CRLF-ONLY | recorded failedTest 0001 fails only on raw CRLF bytes (it passes on LF; first LF-normalized failure TLE@0008), so the evidence-bound failure is not an algorithmic witness |
| 525B | [10475095](https://codeforces.com/contest/525/submission/10475095) | WA | 0001 | CRLF-ONLY | recorded failedTest 0001 fails only on raw CRLF bytes (it passes on LF; first LF-normalized failure TLE@0008), so the evidence-bound failure is not an algorithmic witness |
| 525B | [10476961](https://codeforces.com/contest/525/submission/10476961) | WA | 0001 | CRLF-ONLY | recorded failedTest 0001 fails only on raw CRLF bytes (it passes on LF; first LF-normalized failure TLE@0008), so the evidence-bound failure is not an algorithmic witness |
| 534B | [12745599](https://codeforces.com/contest/534/submission/12745599) | TLE | 0006 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 602B | [14450998](https://codeforces.com/contest/602/submission/14450998) | TLE | 0021 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 602B | [14451385](https://codeforces.com/contest/602/submission/14451385) | TLE | 0021 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 602B | [14456846](https://codeforces.com/contest/602/submission/14456846) | TLE | 0021 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 602B | [14457684](https://codeforces.com/contest/602/submission/14457684) | TLE | 0021 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 612C | [15012839](https://codeforces.com/contest/612/submission/15012839) | WA | 0001 | CRLF-ONLY | recorded failedTest 0001 fails only on raw CRLF bytes (it passes on LF; first LF-normalized failure WA@0010), so the evidence-bound failure is not an algorithmic witness |
| 612C | [15019694](https://codeforces.com/contest/612/submission/15019694) | WA | 0001 | CRLF-ONLY | recorded failedTest 0001 fails only on raw CRLF bytes (it passes on LF; first LF-normalized failure TLE@0031), so the evidence-bound failure is not an algorithmic witness |
| 614B | [15487278](https://codeforces.com/contest/614/submission/15487278) | WA | 0001 | GENUINE-BOUND | detects beautiful numbers with float math.log(number,10) |
| 614B | [15487545](https://codeforces.com/contest/614/submission/15487545) | WA | 0001 | GENUINE-BOUND | ad-hoc digit tests misclassify non-beautiful numbers; concatenates instead of multiplying |
| 614B | [15490074](https://codeforces.com/contest/614/submission/15490074) | WA | 0001 | EXCLUDED | BINDING: recorded failedTest 0001 fails only on CRLF bytes (AC on LF 0001; first LF failure 0003). |
| 614B | [15514806](https://codeforces.com/contest/614/submission/15514806) | WA | 0007 | GENUINE-BOUND | res initialised to '0' when all numbers are beautiful; input 1 -> 0 |
| 614B | [15556998](https://codeforces.com/contest/614/submission/15556998) | WA | 0032 | GENUINE-BOUND | prints the non-beautiful factor before seeing a later 0; product with 0 must be 0 |
| 637C | [16717349](https://codeforces.com/contest/637/submission/16717349) | WA | 0005 | CRLF-ONLY | recorded failedTest 0005 fails only on raw CRLF bytes (it passes on LF; first LF-normalized failure WA@0007), so the evidence-bound failure is not an algorithmic witness |
| 637C | [16751521](https://codeforces.com/contest/637/submission/16751521) | TLE | 0044 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 652A | [16922655](https://codeforces.com/contest/652/submission/16922655) | TLE | 0010 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 652A | [16923727](https://codeforces.com/contest/652/submission/16923727) | TLE | 0010 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 665B | [17403780](https://codeforces.com/contest/665/submission/17403780) | WA | 0004 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 665B | [17417468](https://codeforces.com/contest/665/submission/17417468) | WA | 0001 | EXCLUDED | PROMPT/DEBUG OUTPUT: input('input n m k:\n') writes a prompt to stdout. |
| 665B | [18257545](https://codeforces.com/contest/665/submission/18257545) | WA | 0004 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 665B | [19072910](https://codeforces.com/contest/665/submission/19072910) | WA | 0001 | EXCLUDED | PLACEHOLDER: never prints an answer. |
| 665B | [36753860](https://codeforces.com/contest/665/submission/36753860) | WA | 0002 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 697B | [19157880](https://codeforces.com/contest/697/submission/19157880) | WA | 0001 | EXCLUDED | DEBUG OUTPUT: prints the untrimmed 250-digit Decimal before trimming a local copy. |
| 697B | [19157943](https://codeforces.com/contest/697/submission/19157943) | WA | 0007 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 697B | [19158047](https://codeforces.com/contest/697/submission/19158047) | WA | 0008 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 697B | [19162045](https://codeforces.com/contest/697/submission/19162045) | WA | 0007 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 697B | [19162172](https://codeforces.com/contest/697/submission/19162172) | WA | 0029 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 698A | [27188602](https://codeforces.com/contest/698/submission/27188602) | WA | 0006 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 698A | [27277927](https://codeforces.com/contest/698/submission/27277927) | WA | 0001 | CRLF-ONLY | recorded failedTest 0001 fails only on raw CRLF bytes (it passes on LF; first LF-normalized failure WA@0005), so the evidence-bound failure is not an algorithmic witness |
| 698A | [27688879](https://codeforces.com/contest/698/submission/27688879) | WA | 0006 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 698A | [27718163](https://codeforces.com/contest/698/submission/27718163) | WA | 0004 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 698A | [27977411](https://codeforces.com/contest/698/submission/27977411) | WA | 0001 | EXCLUDED | DEBUG OUTPUT: print(dp) / print(t) before the answer. |
| 748C | [23306553](https://codeforces.com/contest/748/submission/23306553) | WA | 0001 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 748C | [23314648](https://codeforces.com/contest/748/submission/23314648) | WA | 0001 | EXCLUDED | DEBUG OUTPUT: print(protokol) and print(t_pr) before the answer. |
| 748C | [23341823](https://codeforces.com/contest/748/submission/23341823) | WA | 0002 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 748C | [23383827](https://codeforces.com/contest/748/submission/23383827) | WA | 0003 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 748C | [23384735](https://codeforces.com/contest/748/submission/23384735) | WA | 0005 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 762A | [25833456](https://codeforces.com/contest/762/submission/25833456) | TLE | 0008 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 762A | [26076803](https://codeforces.com/contest/762/submission/26076803) | TLE | 0005 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 762A | [26077548](https://codeforces.com/contest/762/submission/26077548) | TLE | 0005 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 762B | [26983984](https://codeforces.com/contest/762/submission/26983984) | TLE | 0034 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 77A | [20485616](https://codeforces.com/contest/77/submission/20485616) | WA | 0003 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 77A | [25020964](https://codeforces.com/contest/77/submission/25020964) | WA | 0001 | EXCLUDED | DIFFERENT PROBLEM: solves 71A Way Too Long Words. |
| 77A | [35555409](https://codeforces.com/contest/77/submission/35555409) | WA | 0004 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 77A | [51039006](https://codeforces.com/contest/77/submission/51039006) | WA | 0003 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 77A | [51864740](https://codeforces.com/contest/77/submission/51864740) | WA | 0003 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 799B | [97699746](https://codeforces.com/contest/799/submission/97699746) | TLE | 0006 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 799B | [110268195](https://codeforces.com/contest/799/submission/110268195) | TLE | 0006 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 79B | [30040253](https://codeforces.com/contest/79/submission/30040253) | TLE | 0004 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 804B | [26864937](https://codeforces.com/contest/804/submission/26864937) | WA | 0001 | CRLF-ONLY | fails on raw CRLF bytes, AC on LF-normalized tests |
| 804B | [26866996](https://codeforces.com/contest/804/submission/26866996) | WA | 0001 | CRLF-ONLY | recorded failedTest 0001 fails only on raw CRLF bytes (it passes on LF; first LF-normalized failure WA@0002), so the evidence-bound failure is not an algorithmic witness |
| 816B | [28617946](https://codeforces.com/contest/816/submission/28617946) | TLE | 0005 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 816B | [28618127](https://codeforces.com/contest/816/submission/28618127) | TLE | 0005 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 816B | [28693044](https://codeforces.com/contest/816/submission/28693044) | TLE | 0005 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 816B | [29293156](https://codeforces.com/contest/816/submission/29293156) | TLE | 0009 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 888C | [32485264](https://codeforces.com/contest/888/submission/32485264) | WA | 0001 | CRLF-ONLY | recorded failedTest 0001 fails only on raw CRLF bytes (it passes on LF; first LF-normalized failure WA@0004), so the evidence-bound failure is not an algorithmic witness |
| 888C | [32485756](https://codeforces.com/contest/888/submission/32485756) | WA | 0002 | CRLF-ONLY | fails on raw CRLF bytes, AC on LF-normalized tests |
| 888C | [32515760](https://codeforces.com/contest/888/submission/32515760) | TLE | 0001 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 888C | [32516054](https://codeforces.com/contest/888/submission/32516054) | TLE | 0035 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 928B | [35669821](https://codeforces.com/contest/928/submission/35669821) | TLE | 0046 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 934A | [35230199](https://codeforces.com/contest/934/submission/35230199) | WA | 0005 | GENUINE-BOUND | answers b[m]*a[n-1] only; ignores negative/mixed-sign products |
| 934A | [35230336](https://codeforces.com/contest/934/submission/35230336) | WA | 0017 | GENUINE-BOUND | max(v2[m]*v1[n-1], v2[1]*v1[1]) omits mixed-sign products |
| 934A | [35230446](https://codeforces.com/contest/934/submission/35230446) | WA | 0010 | GENUINE-BOUND | reads b with a loop to n instead of m |
| 934A | [35230520](https://codeforces.com/contest/934/submission/35230520) | WA | 0010 | GENUINE-BOUND | sort(b+1,b+n+1) sorts the wrong range of b |
| 934A | [35230534](https://codeforces.com/contest/934/submission/35230534) | WA | 0005 | EXCLUDED | ENVIRONMENT/UB on bound test: its algorithm returns the correct 127184126241438168 on recorded failedTest 0005; output -105874984 arises only because glibc parses %I64d as I-flag + width 64 + %d and reads a long long vararg as int (low 32 bits, undefined behaviour). 25 tests are env-only; its genuin |
| 954B | [36470387](https://codeforces.com/contest/954/submission/36470387) | WA | 0003 | GENUINE-BOUND | loop breaks at i*2>=n, missing the exact-doubling prefix |
| 954B | [36470719](https://codeforces.com/contest/954/submission/36470719) | WA | 0003 | GENUINE-BOUND | condition i*2<s.size() excludes the exact-doubling prefix |
| 954B | [36470820](https://codeforces.com/contest/954/submission/36470820) | WA | 0003 | GENUINE-BOUND | loop i<n excludes i=n, missing the exact-doubling prefix |
| 954B | [36471000](https://codeforces.com/contest/954/submission/36471000) | WA | 0002 | GENUINE-BOUND | answer n-i-1 is off and the match loop bound j<i*2 is wrong; aa -> 1 instead of 2 |
| 954B | [36471047](https://codeforces.com/contest/954/submission/36471047) | WA | 0003 | GENUINE-BOUND | ans=n/2-1 constant whenever any doubled prefix exists, independent of its length |
| 958A1 | [37313668](https://codeforces.com/contest/958/submission/37313668) | WA | 0011 | GENUINE-BOUND | applies each of rotate/flipV/flipH at most once, so 180/270-degree rotations are never tried |
| 958A1 | [37313799](https://codeforces.com/contest/958/submission/37313799) | WA | 0017 | EXCLUDED | BINDING: recorded failedTest 0017 fails only on CRLF bytes (AC on LF 0017; first LF failure 0019). |
| 958A1 | [38302451](https://codeforces.com/contest/958/submission/38302451) | WA | 0001 | GENUINE-BOUND | checks only three rotations, not identity or reflections |
| 958A1 | [40109855](https://codeforces.com/contest/958/submission/40109855) | WA | 0007 | GENUINE-BOUND | checks only the first n cells (range(n) instead of n*n) |
| 958A1 | [40800069](https://codeforces.com/contest/958/submission/40800069) | WA | 0001 | EXCLUDED | BINDING: recorded failedTest 0001 fails only on CRLF bytes (AC on LF 0001; first LF failure 0010). |
| 958D1 | [37312018](https://codeforces.com/contest/958/submission/37312018) | TLE | 0004 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 958D1 | [37312384](https://codeforces.com/contest/958/submission/37312384) | TLE | 0004 | TIMING-ONLY | builder verdict TLE; timing is not an algorithmic kill |
| 995B | [39656541](https://codeforces.com/contest/995/submission/39656541) | WA | 0002 | EXCLUDED | DIFFERENT PROBLEM: implements 996B World Cup logic. |
| 995B | [39677202](https://codeforces.com/contest/995/submission/39677202) | WA | 0004 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 995B | [39692592](https://codeforces.com/contest/995/submission/39692592) | WA | 0001 | EXCLUDED | DIFFERENT PROBLEM: implements 977D Divide by three, multiply by two. |
| 995B | [45305994](https://codeforces.com/contest/995/submission/45305994) | WA | 0004 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |
| 995B | [55227287](https://codeforces.com/contest/995/submission/55227287) | WA | 0006 | NOT-COUNTED | package already fails another fail-fast rule; not individually certified |

Each v4 audit has approved=false; verify_evidence and publication_gate(require_approval=False) reject all 35 (recorded per ID as contractGate in the JSON). 911C note: EXCLUDED EXTRA SOURCE, UB-ONLY (uninitialised read), not counted as a wrong kill and not one of the five qualifying incorrect references. CF-WRONG_ANSWER on Codeforces; its implemented algorithm is correct, and its only identified defect is reading an uninitialised new bool[] array (undefined behaviour). Under the bounded ONLINE_JUDGE harness it passes all package tests and all 1,758 auditor-enumerated inputs (inputs SHA256 fae3c6f07943bf1a91d0740dd0d8e7242d5c3629471d9124ea071631ee2baf10, ub911.json). That enumeration is NOT the full legal input domain and is not a proof that no valid test can expose the UB; it only shows no tested input does under this harness. The five qualifying incorrect references of 911C are the separate selected sources with source-level witnesses.

## Per-problem detail (39 earlier IDs)

### 107A: NOT_VALIDATED_HELD

- packageHash `c82dbd5e3ff41403997cbf9463e9d8d56fbbae614e2aee661b2164d89e3dd997`
- evidenceHash `3c23ce12b7f746ef35979e21c945e7b15d463a4d973c62b80827edf3369317a3`
- auditHash `8ebf16a3ee4e3b0d04cacbefcbfbf0f74531021577fef9236a37cb377d79287e`
- archive SHA256 `25eb44ce7b035f092d176d6442af05367816160c76f1be9074a4e1d152084c4a`
- contract gate: None
- CRLF-input tests: 16; independent reference: tests=182, invalid=0, mismatches=0
- issues: only 2/5 incorrect sources are counted WA algorithmic kills
- CF-OK sources failing: 627433 GNU C++ CE@None, 627519 MS C++ CE@None, 627460 GNU C++ CE@None
- replacement WA candidates (executed here, need builder revalidation and re-audit): 90226422@0001, 114310642@0006, 104842606@0001, 195071546@0005, 113620524@0004, 136410791@0001, 73553259@0005, 97366270@0011

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [627445](https://codeforces.com/contest/107/submission/627445) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [627449](https://codeforces.com/contest/107/submission/627449) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [627474](https://codeforces.com/contest/107/submission/627474) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [627482](https://codeforces.com/contest/107/submission/627482) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [627502](https://codeforces.com/contest/107/submission/627502) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [5408132](https://codeforces.com/contest/107/submission/5408132) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | - | False | : Presentation-only: the tank/tap pairs are correct but the leading count line is missing. Not counted, by the same rule applied to 197B. |
| [9819565](https://codeforces.com/contest/107/submission/9819565) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | - | False | : Source is the placeholder print("x"); it implements no algorithm, so its WA is not an algorithmic kill. |
| [27308114](https://codeforces.com/contest/107/submission/27308114) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0002 | - | True | wrong-answer: Merges pipes into union sets but treats a closed cycle as a chain (1->2->3->1) and prints a pair instead of 0. |
| [30302698](https://codeforces.com/contest/107/submission/30302698) | Python 3 | WRONG_ANSWER | WA | WA | 0011 | True | WA@0011 | - | True | wrong-answer: Treats every in-degree-0 house as a tank, including houses with no outgoing pipe; n=1000,p=0 prints 1000 pairs with diameter inf instead of 0. |
| [37558696](https://codeforces.com/contest/107/submission/37558696) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | - | False | : Presentation-only: the tank/tap pairs are correct but the leading count line is missing. Not counted, by the same rule applied to 197B. |

### 125A: NOT_VALIDATED_HELD

- packageHash `590e236e38caee6ab2bd6a116d04ab2b36bb8264505c0e7f9ec6cc1467fcc99f`
- evidenceHash `d2f827d4f7ee1623c8f1975dfb417dffca4bd7af1dd5069201aeda5579424daa`
- auditHash `da376cc4c721df71f793164459c40a868a3ee67f2b7b132b8e3855161b527a8c`
- archive SHA256 `0cdd9980ca3b6c1c3f3cffec91d83afd2595abeed3a3bc2c7ed87a42b668fb66`
- contract gate: None
- CRLF-input tests: 22; independent reference: tests=174, invalid=0, mismatches=0
- issues: only 4/5 incorrect sources are counted WA algorithmic kills
- semantic check (LF, numeric fraction comparison): 42101202: 7 token-WA, 0 numerically wrong
- replacement WA candidates (executed here, need builder revalidation and re-audit): 210509999@0021, 219225771@0021, 67135490@0021, 149945129@0021, 147008686@0001, 149945330@0021, 64165010@0021, 144606347@0021

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 22026877 | L1: `n=(int(input())+2)//3` | 0004 | `1\n` | `0 0` | `0 1\n` | `a79122992d53d358` |
| 42101202 | L7: `print(n//36, (n%36)//3+add)` | 0021 | `35\n` | `1 0` | `0 12\n` | `c84f1f0f270a4c12` |
| 42101236 | L5: `if n%36 >= 18:` | 0003 | `24\n` | `0 8` | `1 0\n` | `f4a8ae8e74ddfb89` |
| 49637309 | L2: `print(n//36+(n%36)/3)` | 0002 | `5\n` | `0 2` | `1.6666666666666667\n` | `effa2bb251dd23fe` |
| 49637385 | L3: `print(str(n//36)+' '+str(ceil((n%36)/3)))` | 0004 | `1\n` | `0 0` | `0 1\n` | `a79122992d53d358` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [814491](https://codeforces.com/contest/125/submission/814491) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [814497](https://codeforces.com/contest/125/submission/814497) | GNU C++0x | OK | AC | AC | None | True | AC@None | - | True |  |
| [814500](https://codeforces.com/contest/125/submission/814500) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [814501](https://codeforces.com/contest/125/submission/814501) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [814503](https://codeforces.com/contest/125/submission/814503) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [22026877](https://codeforces.com/contest/125/submission/22026877) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | - | True | wrong-answer: Rounds up with ceil(n/3); n=1 gives 1 inch but the statement rounds 1 cm to 0 inches. |
| [42101202](https://codeforces.com/contest/125/submission/42101202) | Python 3 | WRONG_ANSWER | WA | WA | 0021 | True | WA@0021 | - | False | : Presentation-only: the rounded total is always right ((n%36)//3 plus a round-up when (n%36)%3==2 equals (n+1)//3 - 12*(n//36)), but when n%36==35 it prints "a 12" without carrying into feet. All 7 WA tests are that case with the same total inches (sem125.json; outputs reproduced from the recorded LF-run hashes, no new execution). Non-canonical form of the same quantity, excluded like 197B 6327041. |
| [42101236](https://codeforces.com/contest/125/submission/42101236) | Python 3 | WRONG_ANSWER | WA | WA | 0003 | True | WA@0003 | - | True | wrong-answer: Rounds a remainder of 18 cm or more up to a whole foot; n=24 prints 1 0 instead of 0 8. |
| [49637309](https://codeforces.com/contest/125/submission/49637309) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | - | True | wrong-answer: Source print(n//36+(n%36)/3) adds the leftover inches straight onto the feet count, mixing units, and never rounds. Witness on the recorded failedTest 0001: n=42 (reference answer 1 2) prints 3.0. On test 0073, n=9 (reference answer 0 3), it prints the same bytes 3.0 (identical outputHash 66e4c000f2000eb1...). Two different correct answers give the same output, so no output format could encode the correct answer; the defect is numeric, not presentation. Also wrong on test 0002: n=5 should round to 0 2, but it prints 1.6666666666666667. |
| [49637385](https://codeforces.com/contest/125/submission/49637385) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | - | True | wrong-answer: Rounds inches with ceil; n=1 prints 0 1 instead of 0 0. |

### 152C: REJECTED

- packageHash `f7bfc82a3b02fe278b6a1da326f74a49196e2fb86391198691a5c87c91fa17df`
- evidenceHash `7d0e6b0a7719a634842723cc43bc15396d4b59a778b592001256880fe953da8b`
- auditHash `7d8f485d9f77b16f27cef88b9c21831957eb02eb4e016b861414a36d607b8401`
- archive SHA256 `48f95e3c42f94c2f413dbd80f4cb31f46e0cda2d6ed4cf46be8950f407f02151`
- contract gate: None
- CRLF-input tests: 16; independent reference: tests=180, invalid=0, mismatches=0
- issues: accepted contradiction: CF-OK source(s) 19459348(RE@0001) fail the package; cause: CRLF bytes reach Python input(); passes on LF-normalized tests
- CF-OK sources failing: 19459348 Python 3 RE@0001, 1206562 GNU C++ CE@None

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [1206062](https://codeforces.com/contest/152/submission/1206062) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [1206180](https://codeforces.com/contest/152/submission/1206180) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [1206181](https://codeforces.com/contest/152/submission/1206181) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [1206348](https://codeforces.com/contest/152/submission/1206348) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [1206349](https://codeforces.com/contest/152/submission/1206349) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [4839442](https://codeforces.com/contest/152/submission/4839442) | Python 3 | WRONG_ANSWER | WA | WA | 0007 | True | WA@0007 | - | True | wrong-answer: Multiplies the distinct-letter counts per column without taking mod 1e9+7. |
| [15021289](https://codeforces.com/contest/152/submission/15021289) | Python 3 | WRONG_ANSWER | WA | WA | 0008 | True | WA@0008 | - | True | wrong-answer: Takes the modulo with a float (res % (1e9+7)), which loses precision on large products. |
| [21213094](https://codeforces.com/contest/152/submission/21213094) | Python 3 | WRONG_ANSWER | WA | WA | 0007 | True | WA@0007 | - | True | wrong-answer: Leaves out the modulo 1e9+7, so it prints the full product. |
| [32826732](https://codeforces.com/contest/152/submission/32826732) | Python 3 | WRONG_ANSWER | WA | WA | 0007 | True | WA@0007 | - | True | wrong-answer: Leaves out the modulo 1e9+7, so it prints the full product. |
| [54790763](https://codeforces.com/contest/152/submission/54790763) | Python 3 | WRONG_ANSWER | WA | WA | 0007 | True | WA@0007 | - | True | wrong-answer: Leaves out the modulo 1e9+7, so it prints the full product. |

### 175A: REJECTED

- packageHash `28d2c08bcb9e2568bba4e7285326f0456cc3e836390e373a9254eec4dc5591ba`
- evidenceHash `41028bedd579711fbb29e9a3ac0fba5721bc2157c868e28a2170f9aa2ae3fb32`
- auditHash `2070f8ec44b409dd8e2696ceb995ed06e2c55e2146b61226cfd28053ce736024`
- archive SHA256 `1be352ad504672216b52686b1024d0891045f2bddf7524bd2317d37c7465af7c`
- contract gate: None
- CRLF-input tests: 134; independent reference: tests=287, invalid=0, mismatches=0
- issues: accepted contradiction: CF-OK source(s) 37495712(RE@0001), 124238640(RE@0001), 27107190(RE@0001), 196162162(RE@0001), 55006515(RE@0001), 35154521(RE@0001), 78795916(RE@0001), 29819107(RE@0001), 44186543(RE@0001), 46821841(RE@0001), 29784607(RE@0001), 34276976(RE@0001) fail the package; cause: CRLF bytes reach Python input(); passes on LF-normalized tests; only 4/5 incorrect sources are counted WA algorithmic kills
- CF-OK sources failing: 37495712 Python 3 RE@0001, 124238640 Python 3 RE@0001, 27107190 Python 3 RE@0001, 196162162 Python 3 RE@0001, 55006515 Python 3 RE@0001, 35154521 Python 3 RE@0001, 78795916 Python 3 RE@0001, 29819107 Python 3 RE@0001, 1532004 GNU C++ CE@None, 44186543 Python 3 RE@0001, 46821841 Python 3 RE@0001, 29784607 Python 3 RE@0001, 34276976 Python 3 RE@0001
- replacement WA candidates (executed here, need builder revalidation and re-audit): 215368025@0004

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [1531984](https://codeforces.com/contest/175/submission/1531984) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [1531986](https://codeforces.com/contest/175/submission/1531986) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [1531990](https://codeforces.com/contest/175/submission/1531990) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [1531991](https://codeforces.com/contest/175/submission/1531991) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [1531992](https://codeforces.com/contest/175/submission/1531992) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [14702816](https://codeforces.com/contest/175/submission/14702816) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | - | True | wrong-answer: Limits split lengths with the wrong window (min(5,n-1)); misses 1000000+1000000+1000000. |
| [14702891](https://codeforces.com/contest/175/submission/14702891) | Python 3 | WRONG_ANSWER | WA | WA | 0016 | True | WA@0016 | - | True | wrong-answer: Uses break instead of continue on leading-zero and >1e6 parts, so it skips valid later splits. |
| [15770608](https://codeforces.com/contest/175/submission/15770608) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | - | False | : A debug print(g) echoes the input before the answer, so the WA on 0001 is a formatting artifact, not an algorithmic defect. |
| [42333877](https://codeforces.com/contest/175/submission/42333877) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | - | True | wrong-answer: Splits the integer from the right and never rejects leading zeros or parts that are empty after integer conversion. |
| [193699107](https://codeforces.com/contest/175/submission/193699107) | Python 3 | WRONG_ANSWER | WA | WA | 0003 | True | WA@0003 | - | True | wrong-answer: Accepts parts with leading zeros through int() and only special-cases a "000" prefix; 0009 prints 9 instead of -1. |

### 197B: NOT_VALIDATED_HELD

- packageHash `66cb5419b77fa845e2af4911140ac0e85196e4af7cadf4ec40043273235abe6b`
- evidenceHash `40165fdb27cdac3c23b3b35274566dc6051ca0427c91ad9e8aaa252f8ad5bb1e`
- auditHash `55ac5972f42a956f223d9c49b2303892f6172a87eb9f7ccecdac15130be64f98`
- archive SHA256 `90235a1ed207e07f9e1e7278ab4a8ff4e94e4fe892798e375ad17d6aa2efd570`
- contract gate: None
- CRLF-input tests: 42; independent reference: tests=206, invalid=0, mismatches=0
- issues: only 3/5 incorrect sources are counted WA algorithmic kills
- CF-OK sources failing: 1788242 MS C++ CE@None, 1788172 MS C++ CE@None
- semantic check (LF, numeric fraction comparison): 4906508: 72 token-WA, 72 numerically wrong; 6327041: 16 token-WA, 0 numerically wrong; 8471901: 51 token-WA, 0 numerically wrong; 8471960: 135 token-WA, 49 numerically wrong; 11940891: 27 token-WA, 23 numerically wrong
- replacement WA candidates (executed here, need builder revalidation and re-audit): 165490894@0008, 21696304@0008, 103987333@0008, 98057127@0008, 93077666@0008, 59668523@0008, 55689536@0008, 42844074@0008, 144003147@0008, 75117786@0008

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [1787958](https://codeforces.com/contest/197/submission/1787958) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [1788088](https://codeforces.com/contest/197/submission/1788088) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [1788195](https://codeforces.com/contest/197/submission/1788195) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [1788224](https://codeforces.com/contest/197/submission/1788224) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [1788278](https://codeforces.com/contest/197/submission/1788278) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [4906508](https://codeforces.com/contest/197/submission/4906508) | Python 3 | WRONG_ANSWER | WA | WA | 0003 | True | WA@0003 | `1/1\n` | True | wrong-answer: The degree comparison has duplicated branches (n>m twice, m<n is unreachable), so n<m prints a fraction instead of 0/1. |
| [6327041](https://codeforces.com/contest/197/submission/6327041) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `2/4\n` | False | : Presentation-only: prints an unreduced fraction (2/4 instead of 1/2). On all 201 package tests with LF line endings, every one of its 16 WA outputs is numerically equal to the expected value (sem197.json), so no algorithmic defect is witnessed. Revoked from the earlier 13/28 signoff. |
| [8471901](https://codeforces.com/contest/197/submission/8471901) | Python 3 | WRONG_ANSWER | WA | WA | 0006 | True | WA@0006 | `0\n` | False | : Presentation-only: prints the integer 0 instead of the fraction 0/1 when deg P < deg Q. On all 201 package tests with LF line endings, every one of its 51 WA outputs is numerically equal to the expected value (sem197.json); its degree, sign and Infinity handling is never wrong on a package test. Revoked from the earlier 13/28 signoff. |
| [8471960](https://codeforces.com/contest/197/submission/8471960) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0002 | `Infinity\n` | True | wrong-answer: Ignores the leading-coefficient signs when the limit is infinite, so it prints Infinity instead of -Infinity. |
| [11940891](https://codeforces.com/contest/197/submission/11940891) | Python 3 | WRONG_ANSWER | WA | WA | 0005 | True | WA@0005 | `-9/-5\n` | True | wrong-answer: Adds a "-" prefix from b*c<0 but keeps the signed values, so 9/-5 prints -9/-5 instead of -9/5. |

### 198B: REJECTED

- packageHash `190e31375bb375853b42fdbdff92c64914f27c6f77542177ad05cae69c387ca5`
- evidenceHash `df6b45c558d12824a4be77e2a452c118415ea2ffa857c9dafd8d24502519b48d`
- auditHash `641edaac6db1cd8dd3483c3d52dcad7837b466f0d11f31a094c11ba55a535a71`
- archive SHA256 `e0f23fded119cfcf6de58b318bb6d640ce6572a98fb7bd4c50520eb2b3680499`
- contract gate: None
- CRLF-input tests: 23; independent reference: tests=184, invalid=0, mismatches=0
- issues: only 3/5 incorrect sources are counted WA algorithmic kills; coverage gap: CF-WRONG_ANSWER source(s) 11382563 pass the full package
- counterexample for CF-WA 11382563: `'7 2\n---X-X-\n----X-X\n'` expected `NO`, sandbox ['WA', 'WA', 'WA']
- CF-OK sources failing: 1814812 GNU C++ CE@None, 1814734 GNU C++ CE@None, 1814896 GNU C++0x CE@None
- replacement WA candidates (executed here, need builder revalidation and re-audit): 213484089@0002, 206146753@0001, 127412935@0004, 168339946@0004, 163660509@0002, 206143090@0001, 222828876@0001

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [1814636](https://codeforces.com/contest/198/submission/1814636) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [1814717](https://codeforces.com/contest/198/submission/1814717) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [1814790](https://codeforces.com/contest/198/submission/1814790) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [1814858](https://codeforces.com/contest/198/submission/1814858) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [1814977](https://codeforces.com/contest/198/submission/1814977) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [9741783](https://codeforces.com/contest/198/submission/9741783) | Python 3 | WRONG_ANSWER | WA | WA | 0012 | True | WA@0012 | - | True | wrong-answer: Its DFS caps consecutive downs/ups at k+1 and prunes valid climbs; 5 2/-----/XXXXX prints NO. |
| [9742416](https://codeforces.com/contest/198/submission/9742416) | Python 3 | TIME_LIMIT_EXCEEDED | TLE | TLE | 0023 | True | - | - | False | complexity: BFS/DFS has no visited set and blows up exponentially (TLE; an individual rerun ran out of memory at 8.3s); not counted, see policy. |
| [23110434](https://codeforces.com/contest/198/submission/23110434) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0002 | - | True | wrong-answer: Its visited marks ignore water level/time, so it accepts unsafe paths. |
| [31871384](https://codeforces.com/contest/198/submission/31871384) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | - | True | wrong-answer: Hard-codes a jump of +3 instead of k. |
| [31959794](https://codeforces.com/contest/198/submission/31959794) | Python 3 | TIME_LIMIT_EXCEEDED | TLE | TLE | 0023 | True | - | - | False | complexity: Aliased visited rows ([[0]*n]*2) and recursive DFS (TLE on 0023, RE on 0024); not counted, see policy. |

### 226A: NOT_VALIDATED_HELD

- packageHash `393ee1f27b113d737328f2c91ae5578579bb372fc7dd7a90bf3d93da6668cef5`
- evidenceHash `a94ba4a06c59407251fd255506d2367e95d23e5ef6b87e3616ba9be66ae08178`
- auditHash `13ed690f260facde8c0f77c9a4fa550697ddf8a3d0c163d60c888e8b9af42412`
- archive SHA256 `n/a (whole-pool archive 0637f17856db18a669f39640d39c8d2ffbd80b9c1866d30de8ded075f06e8ab9; no per-ID archive)`
- contract gate: None
- CRLF-input tests: 78; independent reference: tests=230, invalid=0, mismatches=0
- issues: only 3/5 incorrect sources are counted WA algorithmic kills
- max-size coverage: {'bound': 1000000000, 'maxSizeMetric': 1000000000, 'nAtMax': 2, 'ratio': 1.0, 'test': '0081'}

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 11998618 |  | None | `` | `` | `` | `` |
| 21696165 | L3: `print(r-1)` | 0067 | `1 1\n` | `0` | `-1\n` | `ee3aa64bb94a5084` |
| 21696171 | L5: `print(r-1)` | 0067 | `1 1\n` | `0` | `-1\n` | `ee3aa64bb94a5084` |
| 51590219 |  | None | `` | `` | `` | `` |
| 55486527 | L1: `n,m=map(int,input().split());print(pow(3,n,m)-1)` | 0067 | `1 1\n` | `0` | `-1\n` | `ee3aa64bb94a5084` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [2237340](https://codeforces.com/contest/226/submission/2237340) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2237358](https://codeforces.com/contest/226/submission/2237358) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2237364](https://codeforces.com/contest/226/submission/2237364) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2237370](https://codeforces.com/contest/226/submission/2237370) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2237372](https://codeforces.com/contest/226/submission/2237372) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [11998618](https://codeforces.com/contest/226/submission/11998618) | Python 3 | TIME_LIMIT_EXCEEDED | TLE | TLE | 0006 | True | - | - | False | : Computes pow(3,n) without a modulus; correct formula 3^n-1 but 3^(1e9) big-int is TLE only. complexity-only (TLE); not counted per handoff policy |
| [21696165](https://codeforces.com/contest/226/submission/21696165) | Python 3 | WRONG_ANSWER | WA | WA | 0047 | True | WA@0047 | - | True | wrong-answer: Prints pow(3,n,m)-1 with no final mod; when m divides 3^n (test 0047: m=6561=3^8) it prints -1 instead of m-1. Witness (valid LF package test 0067): input '1 1\n', reference '0', source prints '-1'; wrong on 49 tests after case-insensitive YES/NO and numeric normalisation. |
| [21696171](https://codeforces.com/contest/226/submission/21696171) | Python 3 | WRONG_ANSWER | WA | WA | 0047 | True | WA@0047 | - | True | wrong-answer: Same missing wrap: r<0 check happens before subtracting 1, so r=0 prints -1 instead of m-1 (test 0047). Witness (valid LF package test 0067): input '1 1\n', reference '0', source prints '-1'; wrong on 49 tests after case-insensitive YES/NO and numeric normalisation. |
| [51590219](https://codeforces.com/contest/226/submission/51590219) | Python 3 | TIME_LIMIT_EXCEEDED | TLE | TLE | 0006 | True | - | - | False | : Computes (3**n-1)%m with a full big integer; correct but TLE for n=1e9. complexity-only (TLE); not counted per handoff policy |
| [55486527](https://codeforces.com/contest/226/submission/55486527) | Python 3 | WRONG_ANSWER | WA | WA | 0047 | True | WA@0047 | - | True | wrong-answer: pow(3,n,m)-1 without wrap; prints -1 when 3^n = 0 mod m (test 0047). Witness (valid LF package test 0067): input '1 1\n', reference '0', source prints '-1'; wrong on 49 tests after case-insensitive YES/NO and numeric normalisation. |

### 233B: NOT_VALIDATED_HELD

- packageHash `f396281e73a4bd3a07aa1a7728aa0414d7b03a2b1bee8e9f99570ec0e30ecf71`
- evidenceHash `ec24691b263c4615a545d812809f62dc8cb097d3adaaf3694505330079fa4d58`
- auditHash `851eb5229adf02631076923e50a0f81baa820b8bdf61929b8fc710afe199c285`
- archive SHA256 `17576b354a37c4b0f331f53e779334fff1907d4b9b1f4a53c5e2c43c0da7b2f7`
- contract gate: None
- CRLF-input tests: 48; independent reference: tests=201, invalid=0, mismatches=0
- issues: only 3/5 incorrect sources are counted WA algorithmic kills
- replacement WA candidates (executed here, need builder revalidation and re-audit): 135611678@0006, 211052544@0005, 135960142@0002, 149890923@0046, 161628529@0006, 173405148@0001, 141023743@0046, 229779194@0006

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [2340528](https://codeforces.com/contest/233/submission/2340528) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2340550](https://codeforces.com/contest/233/submission/2340550) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2340612](https://codeforces.com/contest/233/submission/2340612) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2340671](https://codeforces.com/contest/233/submission/2340671) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2340678](https://codeforces.com/contest/233/submission/2340678) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [126957423](https://codeforces.com/contest/233/submission/126957423) | Python 3 | WRONG_ANSWER | WA | WA | 0003 | True | WA@0003 | - | True | wrong-answer: Uses a float sqrt discriminant test and never checks the digit sum of the root; n=4 prints 2 instead of -1. |
| [126959060](https://codeforces.com/contest/233/submission/126959060) | Python 3 | WRONG_ANSWER | WA | WA | 0005 | True | WA@0005 | - | True | wrong-answer: Searches x only up to 9*18 instead of the digit-sum values s; misses x=1e8. |
| [127232883](https://codeforces.com/contest/233/submission/127232883) | Python 3 | TIME_LIMIT_EXCEEDED | TLE | TLE | 0005 | True | - | - | False | complexity: Linear scan over x up to sqrt(n)=1e9 (TLE, about 20s CPU under a 20x cap); not counted, see policy. |
| [127737961](https://codeforces.com/contest/233/submission/127737961) | Python 3 | WRONG_ANSWER | WA | WA | 0046 | True | WA@0046 | - | True | wrong-answer: The float-sqrt integrality test in the quadratic solver accepts a non-root near 1e18 (expected -1). |
| [128560902](https://codeforces.com/contest/233/submission/128560902) | Python 3 | TIME_LIMIT_EXCEEDED | TLE | TLE | 0005 | True | - | - | False | complexity: Linear scan up to sqrt(n) (TLE, about 20s CPU under a 20x cap); not counted, see policy. |

### 245E: REJECTED

- packageHash `bcf8733144e378d6bd95723401411694d51015708550107be87a0cf705268aec`
- evidenceHash `7652f2c23be661636dbe30025a85a4dd2757143818640957db3630471e2c4f92`
- auditHash `caa443952654b398577b730367c035fc00b825db7a6d25e17968d9f478b982de`
- archive SHA256 `bccb805a54a9def52da5a0a79502839bc3de7f47627bffa7a505961c69d173d6`
- contract gate: None
- CRLF-input tests: 41; independent reference: tests=202, invalid=0, mismatches=0
- issues: accepted contradiction: CF-OK source(s) 29488834(WA@0002), 6912638(WA@0002), 31526728(WA@0001), 3685951(WA@0001), 17802998(WA@0002), 4891069(WA@0002), 4435266(WA@0002), 42447218(WA@0002), 49460007(WA@0001), 69404238(WA@0002), 17833202(WA@0002), 14563275(WA@0002), 10341189(WA@0002), 13907610(WA@0001) fail the package; cause: CRLF bytes reach Python input(); passes on LF-normalized tests; only 1/5 incorrect sources are counted WA algorithmic kills
- CF-OK sources failing: 29488834 Python 3 WA@0002, 6912638 Python 3 WA@0002, 31526728 Python 3 WA@0001, 3685951 Python 3 WA@0001, 17802998 Python 3 WA@0002, 4891069 Python 3 WA@0002, 4435266 Python 3 WA@0002, 42447218 Python 3 WA@0002, 49460007 Python 3 WA@0001, 69404238 Python 3 WA@0002, 17833202 Python 3 WA@0002, 14563275 Python 3 WA@0002, 10341189 Python 3 WA@0002, 2594454 MS C++ CE@None, 13907610 Python 3 WA@0001
- replacement WA candidates (executed here, need builder revalidation and re-audit): 40550029@0001, 108505479@0001, 108506983@0034, 95054988@0001, 108067609@0001, 108214912@0007, 80087760@0034, 108565361@0001

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [2591847](https://codeforces.com/contest/245/submission/2591847) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2592014](https://codeforces.com/contest/245/submission/2592014) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2592122](https://codeforces.com/contest/245/submission/2592122) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2593339](https://codeforces.com/contest/245/submission/2593339) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2594437](https://codeforces.com/contest/245/submission/2594437) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3685391](https://codeforces.com/contest/245/submission/3685391) | Python 3 | WRONG_ANSWER | WA | WA | 0007 | True | WA@0007 | - | True | wrong-answer: Prints |final balance| instead of the max prefix minus the min prefix. |
| [3771557](https://codeforces.com/contest/245/submission/3771557) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0015 | - | False | : Recorded kill is a CRLF artifact: with the test inputs normalized to LF the source gives WA (failed 0015), not WA on 0002; a stray '\r' from input() is scored as data. Original analysis: Prints the max |prefix|, which ignores that people can leave and re-enter (+- patterns). |
| [4890821](https://codeforces.com/contest/245/submission/4890821) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0015 | - | False | : Recorded kill is a CRLF artifact: with the test inputs normalized to LF the source gives WA (failed 0015), not WA on 0002; a stray '\r' from input() is scored as data. Original analysis: Prints the max |prefix| instead of max prefix - min prefix (with 0 included). |
| [9260456](https://codeforces.com/contest/245/submission/9260456) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0007 | - | False | : Recorded kill is a CRLF artifact: with the test inputs normalized to LF the source gives WA (failed 0007), not WA on 0001; a stray '\r' from input() is scored as data. Original analysis: Prints |final balance|. |
| [14563248](https://codeforces.com/contest/245/submission/14563248) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0015 | - | False | : Recorded kill is a CRLF artifact: with the test inputs normalized to LF the source gives WA (failed 0015), not WA on 0002; a stray '\r' from input() is scored as data. Original analysis: Prints the max |prefix|. |

### 248B: REJECTED

- packageHash `90a7bc594438a76b0abbbc45aee0114b49db72cc9506310f5f1f5975751db2e3`
- evidenceHash `728d089f00c9ef1999fee7edbbd431476513162370a1e595ecdb41040fd87c49`
- auditHash `70f7dddf4c1ad3317570074a0614b7c62cea64bd5628e2e0d455a7f681ccefd5`
- archive SHA256 `80e2f8f831e3f74fe4ff53bca88fde027e6ae996e21a1a7bb988b24727be7052`
- contract gate: None
- CRLF-input tests: 66; independent reference: tests=218, invalid=0, mismatches=0
- issues: accepted contradiction: CF-OK source(s) 31873459(RE@0019), 27547806(RE@0019), 32332414(RE@0019), 4713392(RE@0019), 9705234(RE@0019), 32011925(RE@0019), 11022217(RE@0019), 14779449(RE@0019), 26181773(RE@0019), 7776787(RE@0019), 4786395(RE@0019), 17711024(RE@0019), 13496928(RE@0019) fail the package; cause: Python 3.11 sandbox int-str 4300-digit limit (harness fidelity)
- CF-OK sources failing: 31873459 Python 3 RE@0019, 27547806 Python 3 RE@0019, 32332414 Python 3 RE@0019, 4713392 Python 3 RE@0019, 9705234 Python 3 RE@0019, 32011925 Python 3 RE@0019, 11022217 Python 3 RE@0019, 14779449 Python 3 RE@0019, 26181773 Python 3 RE@0019, 7776787 Python 3 RE@0019, 4786395 Python 3 RE@0019, 17711024 Python 3 RE@0019, 13496928 Python 3 RE@0019

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [2642739](https://codeforces.com/contest/248/submission/2642739) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2643057](https://codeforces.com/contest/248/submission/2643057) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2643149](https://codeforces.com/contest/248/submission/2643149) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2643164](https://codeforces.com/contest/248/submission/2643164) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2643191](https://codeforces.com/contest/248/submission/2643191) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [4307483](https://codeforces.com/contest/248/submission/4307483) | Python 3 | WRONG_ANSWER | WA | WA | 0009 | True | WA@0009 | - | True | wrong-answer: Computes the ceil of a float division 10**(n-1)/210, which loses precision for n=120. |
| [4786571](https://codeforces.com/contest/248/submission/4786571) | Python 3 | WRONG_ANSWER | WA | WA | 0011 | True | WA@0011 | - | True | wrong-answer: After the decrement, the n>2 guard rejects n=3 (prints -1 instead of 210). |
| [7554568](https://codeforces.com/contest/248/submission/7554568) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0002 | - | True | wrong-answer: Prints 210 followed by zeros, which is not the minimum (n=5 gives 21000, but 10080 is smaller). |
| [8474692](https://codeforces.com/contest/248/submission/8474692) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0002 | - | True | wrong-answer: The residue derivation for 10**n mod 210 is wrong, so the n=5 output is not 10080. |
| [9741229](https://codeforces.com/contest/248/submission/9741229) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0002 | - | True | wrong-answer: Prints 210 followed by zeros, which is not minimal. |

### 261A: NOT_VALIDATED_HELD

- packageHash `cc5d9e2297411bbf5af2077d7953dd0a545e17f6a3e1f071f98de493db4e3d51`
- evidenceHash `c6690cebd5c23d561a0ff2234376a1b88a25b68b85c46055ed81f067ec769142`
- auditHash `4333a51c5d16e9a9345bb55051d610102403815027cee43c8e7379d07d59f997`
- archive SHA256 `d50a7f70e8dbbe3d2518fba879aca8b283db7d91e849d739416d06fc77369ef6`
- contract gate: None
- CRLF-input tests: 9; independent reference: tests=183, invalid=0, mismatches=0
- issues: only 3/5 incorrect sources are counted WA algorithmic kills
- max-size coverage: {'bound': 200000, 'maxSizeMetric': 200000, 'nAtMax': 10, 'ratio': 1.0, 'test': '0032'}
- replacement WA candidates (executed here, need builder revalidation and re-audit): 55392754@0002, 34458637@0001, 160215420@0004, 56447570@0004, 76666652@0001, 71994116@0001, 137523902@0001, 127903476@0004

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [2911982](https://codeforces.com/contest/261/submission/2911982) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2912028](https://codeforces.com/contest/261/submission/2912028) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2912094](https://codeforces.com/contest/261/submission/2912094) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2912104](https://codeforces.com/contest/261/submission/2912104) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2912112](https://codeforces.com/contest/261/submission/2912112) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [4390055](https://codeforces.com/contest/261/submission/4390055) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | `[100, 100, 50, 50]\n200\n` | False | : Correct greedy plus a debug print(item_values); with only that line removed it passes all package tests (mutants.json), so the WA is not an algorithmic kill. |
| [21916773](https://codeforces.com/contest/261/submission/21916773) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `46114\n` | True | wrong-answer: Bubble-sort/greedy hybrid that decrements n while advancing start by 2, so it takes the wrong items as free after the first basket. |
| [21918207](https://codeforces.com/contest/261/submission/21918207) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `40199\n` | True | wrong-answer: sorted() results discarded (lists never sorted) and string prices summed in input order; wrong totals on unsorted input. |
| [24459839](https://codeforces.com/contest/261/submission/24459839) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | `1\r\n` | False | : Code for a different problem (capitalizes the first input line); not an attempt at 261A. |
| [30185746](https://codeforces.com/contest/261/submission/30185746) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `35629\n` | True | wrong-answer: Ascending-sort loop steps by 2*c and adds a[i+j] from the wrong end, then adds n%c cheapest items; miscounts paid items. |

### 270B: VALIDATED

- packageHash `26a7f9198b8cafd602541980c061e91d9e9eab85d3d72fb7fc90cc75375221e2`
- evidenceHash `47f572853ec1a3d2b5fc66f02192c0856de7a381154a6c380e45e0650532cae1`
- auditHash `236064036291109c4b73eb721657d426ffcb811f1957b06e5b3663606096fde5`
- archive SHA256 `03e5a02a6fec8c8c1247a9b7a62d452243ede52202c6239035ae145ec0cf8f4b`
- contract gate: {'auditHash': '236064036291109c4b73eb721657d426ffcb811f1957b06e5b3663606096fde5', 'passed': True}
- CRLF-input tests: 24; independent reference: tests=186, invalid=0, mismatches=0
- issues: none
- max-size coverage: {'bound': 100000, 'maxSizeMetric': 100000, 'nAtMax': 3, 'ratio': 1.0, 'test': '0037'}

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 153510996 | L4: `answer = threads.index(1)` | 0011 | `3\n1 3 2\n` | `2` | `0\n` | `9a271f2a916b0b6e` |
| 211206820 | L10: `if ans==0: ans+=1` | 0005 | `1\n1\n` | `0` | `1\n` | `4355a46b19d348dc` |
| 225897139 | L3: `print(a.index(1))` | 0011 | `3\n1 3 2\n` | `2` | `0\n` | `9a271f2a916b0b6e` |
| 225897527 | L6: `k+=1` | 0011 | `3\n1 3 2\n` | `2` | `1\n` | `4355a46b19d348dc` |
| 225898375 | L5: `while (a[i]-a[i-1])==1:` | 0008 | `3\n2 1 3\n` | `1` | `2\n` | `53c234e5e8472b6a` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [3045836](https://codeforces.com/contest/270/submission/3045836) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3045871](https://codeforces.com/contest/270/submission/3045871) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3046098](https://codeforces.com/contest/270/submission/3046098) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3046518](https://codeforces.com/contest/270/submission/3046518) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3046606](https://codeforces.com/contest/270/submission/3046606) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [153510996](https://codeforces.com/contest/270/submission/153510996) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `0\n` | True | wrong-answer: Prints the index of thread 1 in the new list; ignores later inversions (answer is last descent position). |
| [211206820](https://codeforces.com/contest/270/submission/211206820) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0002 | `1\n` | True | wrong-answer: Counts positions whose value is not a running suffix minimum and forces ans>=1; wrong when the list is already sorted (prints 1, expected 0). |
| [225897139](https://codeforces.com/contest/270/submission/225897139) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `0\n` | True | wrong-answer: Prints a.index(1); same flawed idea as 153510996 (distinct source). |
| [225897527](https://codeforces.com/contest/270/submission/225897527) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `1\n` | True | wrong-answer: Counts the number of descents instead of the position of the last descent. |
| [225898375](https://codeforces.com/contest/270/submission/225898375) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | `3\n` | True | wrong-answer: Counts the trailing run of consecutive +1 steps only; misses increasing-but-not-consecutive suffixes. |

### 272B: NOT_VALIDATED_HELD

- packageHash `fcf14c09bf67e238c207c87ba3755b471f31532ccb4e1a0398e5ebc9249993db`
- evidenceHash `581d2476be98725af3eafce8a1daa9c22639a32cae10a045f88e30db1dcbc9fd`
- auditHash `05439d3964483c9a713eeee11fbe888df81de1914b12834e31b5bd0f3b15b605`
- archive SHA256 `f8e9223a4d786b35ab8fa661c67a23113e11b61c2289d2c7055bae068d3a7df6`
- contract gate: None
- CRLF-input tests: 11; independent reference: tests=175, invalid=0, mismatches=0
- issues: only 4/5 incorrect sources are counted WA algorithmic kills
- max-size coverage: {'bound': 100000, 'maxSizeMetric': 100000, 'nAtMax': 14, 'ratio': 1.0, 'test': '0026'}
- CF-OK sources failing: 3112679 GNU C++ WA@0025

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [3112383](https://codeforces.com/contest/272/submission/3112383) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3112385](https://codeforces.com/contest/272/submission/3112385) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3112484](https://codeforces.com/contest/272/submission/3112484) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3112573](https://codeforces.com/contest/272/submission/3112573) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3112615](https://codeforces.com/contest/272/submission/3112615) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [47719996](https://codeforces.com/contest/272/submission/47719996) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `0\n` | True | wrong-answer: Sums bits[i] only for i<n; when n is smaller than a popcount value (e.g. n=2, popcount 5) pairs are dropped. |
| [54885453](https://codeforces.com/contest/272/submission/54885453) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | `2\n` | True | wrong-answer: Counts adjacent equal values after sorting (s+=1) instead of C(k,2) per group. |
| [54885605](https://codeforces.com/contest/272/submission/54885605) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `0\n` | True | wrong-answer: norm() is not popcount: it strips factors of 2 then collapses (a-1)%4==0 chains, so different popcounts collide and equal ones split. |
| [75475383](https://codeforces.com/contest/272/submission/75475383) | Python 3 | TIME_LIMIT_EXCEEDED | TLE | TLE | 0012 | True | - | - | False | : Correct f(x) but O(n^2) pair loop; TLE at n=1e5 only. complexity-only (TLE); not counted per handoff policy |
| [129896253](https://codeforces.com/contest/272/submission/129896253) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `1\n` | True | wrong-answer: answer = val*(val-1)//2 overwrites instead of accumulating over groups. |

### 277A: VALIDATED

- packageHash `5e56b7be4eafa7211ad99cf76cbcc44762abfea231daadc3a4ebb5361a771674`
- evidenceHash `f0c396fba02a5477d9db5d48aae4433e9bc453e08cd5cca4f28dc8d524311dc9`
- auditHash `ba071f9bd974077b60aaf661487a823a97b52fdaae2bf3aa06d1200f4f3efacc`
- archive SHA256 `2f4f13f816d03ed43fb9b9f5cfb6b6d052aef084f0c3b3050770c87e1bf94346`
- contract gate: {'auditHash': 'ba071f9bd974077b60aaf661487a823a97b52fdaae2bf3aa06d1200f4f3efacc', 'passed': True}
- CRLF-input tests: 14; independent reference: tests=183, invalid=0, mismatches=0
- issues: none
- max-size coverage: {'bound': 10000, 'maxSizeMetric': 10000, 'nAtMax': 3, 'ratio': 1.0, 'test': '0035'}
- CF-OK sources failing: 10617845 Python 3 WA@0034

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 9220573 | L41: `print(num-1)` | 0004 | `2 2\n0\n0\n` | `2` | `1\n` | `4355a46b19d348dc` |
| 9357260 | L22: `print(sum(i == root(i) for i in range(n)) - any(lang))` | 0004 | `2 2\n0\n0\n` | `2` | `1\n` | `4355a46b19d348dc` |
| 10617748 | L28: `print(n-1)` | 0004 | `2 2\n0\n0\n` | `2` | `1\n` | `4355a46b19d348dc` |
| 11352639 | L10: `break` | 0004 | `2 2\n0\n0\n` | `2` | `1\n` | `4355a46b19d348dc` |
| 11352706 | L16: `print(len(v) - 1)` | 0004 | `2 2\n0\n0\n` | `2` | `1\n` | `4355a46b19d348dc` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [3208310](https://codeforces.com/contest/277/submission/3208310) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3208319](https://codeforces.com/contest/277/submission/3208319) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3208326](https://codeforces.com/contest/277/submission/3208326) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3208341](https://codeforces.com/contest/277/submission/3208341) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3208399](https://codeforces.com/contest/277/submission/3208399) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [9220573](https://codeforces.com/contest/277/submission/9220573) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `1\n` | True | wrong-answer: Prints components-1 even when nobody knows any language (expected n). |
| [9357260](https://codeforces.com/contest/277/submission/9357260) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `1\n` | True | wrong-answer: Subtracts any(lang), which is always True for non-empty lists, so the all-zero case prints n-1 instead of n; union direction also skips merged roots. |
| [10617748](https://codeforces.com/contest/277/submission/10617748) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `1\n` | True | wrong-answer: Two fixed passes of pairwise merging are not transitive closure; chains needing more merges stay split. |
| [11352639](https://codeforces.com/contest/277/submission/11352639) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0002 | `3\n` | True | wrong-answer: Merges each employee into the first overlapping group only, never joining groups bridged by a later employee. |
| [11352706](https://codeforces.com/contest/277/submission/11352706) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `1\n` | True | wrong-answer: Merges overlapping groups but uses a stale index after v.remove and mis-handles the all-empty case. |

### 279A: VALIDATED

- packageHash `1c495b3b7a7e2b36735d2a75e45c0fde255e731a659f6635952611d746e43ada`
- evidenceHash `93729677e068a2f92392e6c85b61a74e0c8b68617dbcd0b119710d636298fe08`
- auditHash `f0a81422fa404524642fcae22c349a88a87d54df3f24dbfe7ab914e76a62bc2d`
- archive SHA256 `690478a9f71331d4ad2cd325cc588ae1ef743675f092123aecea82b0608588fe`
- contract gate: {'auditHash': 'f0a81422fa404524642fcae22c349a88a87d54df3f24dbfe7ab914e76a62bc2d', 'passed': True}
- CRLF-input tests: 32; independent reference: tests=186, invalid=0, mismatches=0
- issues: none
- max-size coverage: {'bound': 100, 'maxSizeMetric': 100, 'nAtMax': 10, 'ratio': 1.0, 'test': '0040'}

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 191418646 | L40: `if y in range(-1*x,abs(x)):` | 0067 | `-2 0\n` | `7` | `` | `e3b0c44298fc1c14` |
| 193191838 | L39: `if self.quad == 3:` | 0014 | `3 -5\n` | `20` | `11\n` | `25d4f2a86deb5e25` |
| 200117074 | L9: `elif x<0 and y>=4 and y<=-1-x:` | 0013 | `-1 0\n` | `3` | `0\n` | `9a271f2a916b0b6e` |
| 206358102 | L21: `print(4*(abs(y))+1)` | 0143 | `3 0\n` | `9` | `8\n` | `aa67a169b0bba217` |
| 211700308 | L10: `if x<=-y+1:` | 0004 | `-1 -1\n` | `3` | `4\n` | `7de1555df0c27003` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [3238846](https://codeforces.com/contest/279/submission/3238846) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3238857](https://codeforces.com/contest/279/submission/3238857) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3238923](https://codeforces.com/contest/279/submission/3238923) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3238926](https://codeforces.com/contest/279/submission/3238926) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3238943](https://codeforces.com/contest/279/submission/3238943) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [191418646](https://codeforces.com/contest/279/submission/191418646) | Python 3 | WRONG_ANSWER | WA | WA | 0020 | True | WA@0020 | `` | True | wrong-answer: Region conditions leave cases uncovered (e.g. x<=-2 with y=0: range(-x,|x|) is empty), so it prints no answer on 29 valid tests (first 0020: -97 0, expected 387). Missing a case is a logic defect, not presentation. |
| [193191838](https://codeforces.com/contest/279/submission/193191838) | Python 3 | WRONG_ANSWER | WA | WA | 0007 | True | WA@0007 | `27\n` | True | wrong-answer: Closed-form turn formula with wrong region boundaries; independently verified wrong on the failed test by spiral simulation. |
| [200117074](https://codeforces.com/contest/279/submission/200117074) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `0\n` | True | wrong-answer: Closed-form turn formula with wrong region boundaries; independently verified wrong on the failed test by spiral simulation. |
| [206358102](https://codeforces.com/contest/279/submission/206358102) | Python 3 | WRONG_ANSWER | WA | WA | 0008 | True | WA@0008 | `401\n` | True | wrong-answer: Closed-form turn formula with wrong region boundaries; independently verified wrong on the failed test by spiral simulation. |
| [211700308](https://codeforces.com/contest/279/submission/211700308) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `4\n` | True | wrong-answer: Closed-form turn formula with wrong region boundaries; independently verified wrong on the failed test by spiral simulation. |

### 279B: NOT_VALIDATED_HELD

- packageHash `8dc1534513a5e4ce6abf4e50734ea4eee92558a98c0c42c48d187101e8f2fa6c`
- evidenceHash `9882a21c686ddd966f320bb28614cd208adacd1913de34d077fd771aa0213ee2`
- auditHash `30a396dca38dbd45857f681c4bf183cdba56f9b08986740887203e9d515691e0`
- archive SHA256 `33c659e708c66b4a370ed64746aa7782a41c09749df5057f32a0649e3aa1d227`
- contract gate: None
- CRLF-input tests: 13; independent reference: tests=182, invalid=0, mismatches=0
- issues: only 4/5 incorrect sources are counted WA algorithmic kills
- max-size coverage: {'bound': 100000, 'maxSizeMetric': 100000, 'nAtMax': 19, 'ratio': 1.0, 'test': '0034'}
- replacement WA candidates (executed here, need builder revalidation and re-audit): 186141560@0006, 189751797@0006, 188817449@0012, 183995196@0005, 189514759@0005, 186864655@0002, 186274956@0004, 188816191@0010

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [3238812](https://codeforces.com/contest/279/submission/3238812) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3238829](https://codeforces.com/contest/279/submission/3238829) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3238868](https://codeforces.com/contest/279/submission/3238868) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3238887](https://codeforces.com/contest/279/submission/3238887) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3238889](https://codeforces.com/contest/279/submission/3238889) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [183040305](https://codeforces.com/contest/279/submission/183040305) | Python 3 | WRONG_ANSWER | WA | WA | 0005 | True | WA@0005 | `1\n` | True | wrong-answer: Sorts book times (books must be consecutive from i) and counts while t>0 strictly. |
| [183292864](https://codeforces.com/contest/279/submission/183292864) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | `[3, 1, 2, 1]\n3\n` | False | : Recorded failure on 0001 is a debug print(arr); the de-debugged program still fails 0004 (sorted greedy), but the recorded kill is output noise, so not counted. |
| [183293018](https://codeforces.com/contest/279/submission/183293018) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | `4\n` | True | wrong-answer: Sorts the books (reorders a consecutive-window problem) and prints i+1 after overshooting t. |
| [183369494](https://codeforces.com/contest/279/submission/183369494) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `0\n` | True | wrong-answer: Compares against n instead of t and sorts the books. |
| [183621632](https://codeforces.com/contest/279/submission/183621632) | Python 3 | WRONG_ANSWER | WA | WA | 0005 | True | WA@0005 | `1\n` | True | wrong-answer: Sorts and requires t-i>0 strictly; wrong for exact fits and non-consecutive selection. |

### 289B: NOT_VALIDATED_HELD

- packageHash `9d887a9713d895c4f13d600cbd95d518645d7f8a1afb84b6bb7a951299df73ff`
- evidenceHash `1772a873273638f16d176ac26de3b0a57281c7b07d23b812f5fcb4c488345491`
- auditHash `9830e66e68bd9558ab0631249ae77f9e91a95a815bf5e1dfdcfc77ed790b395c`
- archive SHA256 `fc2462137d26929c0133c4018a2391d27a6d4bb5bf6f31ad075113a18cb437fc`
- contract gate: None
- CRLF-input tests: 12; independent reference: tests=182, invalid=0, mismatches=0
- issues: only 4/5 incorrect sources are counted WA algorithmic kills
- max-size coverage: {'bound': 10000, 'maxSizeMetric': 10000, 'nAtMax': 14, 'ratio': 1.0, 'test': '0034'}
- CF-OK sources failing: 44989655 Python 3 WA@0040
- replacement WA candidates (executed here, need builder revalidation and re-audit): 53282611@0003, 35848097@0001, 70822527@0004, 142617909@0003, 68364449@0001, 35972680@0006, 62171498@0010, 73312585@0003

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [3453821](https://codeforces.com/contest/289/submission/3453821) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3454105](https://codeforces.com/contest/289/submission/3454105) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3454417](https://codeforces.com/contest/289/submission/3454417) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3454493](https://codeforces.com/contest/289/submission/3454493) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3454665](https://codeforces.com/contest/289/submission/3454665) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3746791](https://codeforces.com/contest/289/submission/3746791) | Python 3 | TIME_LIMIT_EXCEEDED | TLE | TLE | 0016 | True | - | - | False | : Correct residue check and exhaustive target scan, but O(nm*10^4) is TLE only. complexity-only (TLE); not counted per handoff policy |
| [4039763](https://codeforces.com/contest/289/submission/4039763) | Python 3 | WRONG_ANSWER | WA | WA | 0003 | True | WA@0003 | `160\n` | True | wrong-answer: Targets the value nearest to the mean, not the median; float division and int() truncation. |
| [4803409](https://codeforces.com/contest/289/submission/4803409) | Python 3 | WRONG_ANSWER | WA | WA | 0003 | True | WA@0003 | `160\n` | True | wrong-answer: Targets the rounded mean of a//d instead of the median. |
| [7253300](https://codeforces.com/contest/289/submission/7253300) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0002 | `0\n` | True | wrong-answer: Feasibility check compares a[0][0]%d with the maximum residue only, so mixed residues below the max pass as feasible. |
| [18764386](https://codeforces.com/contest/289/submission/18764386) | Python 3 | WRONG_ANSWER | WA | WA | 0003 | True | WA@0003 | `108\n` | True | wrong-answer: Targets the element closest to the mean, not the median. |

### 315A: VALIDATED

- packageHash `eeee817832ae8d051f09ddc3c9c80fe0ee09f7cfe09f169bcba849394a1bed35`
- evidenceHash `3063abd76fe36e68e1e8fc819346a89db8482530bbc1f37a999e98d1b9f12e03`
- auditHash `42958ff9221c23461accbd67a5ad812a4a15b49ecb90bf4a48c76b311efe664c`
- archive SHA256 `ae170b374f5a95ae2e2b8a8589360f2faf051b06b6b443c0b0a9a5fc1d4b8f48`
- contract gate: {'auditHash': '42958ff9221c23461accbd67a5ad812a4a15b49ecb90bf4a48c76b311efe664c', 'passed': True}
- CRLF-input tests: 19; independent reference: tests=182, invalid=0, mismatches=0
- issues: none
- max-size coverage: {'bound': 100, 'maxSizeMetric': 100, 'nAtMax': 14, 'ratio': 1.0, 'test': '0065'}

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 3832878 | L12: `if lst[i] != p[i] or kol[lst[i]] > 1:` | 0019 | `3\n1 2\n1 2\n1 1\n` | `1` | `0\n` | `9a271f2a916b0b6e` |
| 3852053 | L9: `if a[b-1] == 0:` | 0016 | `2\n1 1\n1 1\n` | `0` | `1\n` | `4355a46b19d348dc` |
| 3878628 | L9: `k+=1` | 0156 | `3\n2 1\n2 2\n1 2\n` | `0` | `-1\n` | `ee3aa64bb94a5084` |
| 4204402 | L6: `if i != j and a[i][1] == a[j][0]: t.add(i)` | 0019 | `3\n1 2\n1 2\n1 1\n` | `1` | `2\n` | `53c234e5e8472b6a` |
| 4403875 | L7: `if int(q[1]) not in a :` | 0056 | `1\n4 8\n` | `1` | `0\n` | `9a271f2a916b0b6e` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [3831707](https://codeforces.com/contest/315/submission/3831707) | GNU C++0x | OK | AC | AC | None | True | AC@None | - | True |  |
| [3831709](https://codeforces.com/contest/315/submission/3831709) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3831716](https://codeforces.com/contest/315/submission/3831716) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3831727](https://codeforces.com/contest/315/submission/3831727) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3831728](https://codeforces.com/contest/315/submission/3831728) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3832878](https://codeforces.com/contest/315/submission/3832878) | Python 3 | WRONG_ANSWER | WA | WA | 0018 | True | WA@0018 | `2\n` | True | wrong-answer: Marks brands openable when a!=b or a brand repeats, conflating opener brand with bottle brand. |
| [3852053](https://codeforces.com/contest/315/submission/3852053) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0002 | `4\n` | True | wrong-answer: Counts distinct a values instead of bottles that cannot be opened. |
| [3878628](https://codeforces.com/contest/315/submission/3878628) | Python 3 | WRONG_ANSWER | WA | WA | 0005 | True | WA@0005 | `0\n` | True | wrong-answer: Counts (i,j) pairs, so a bottle openable by two others is subtracted twice. |
| [4204402](https://codeforces.com/contest/315/submission/4204402) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `3\n` | True | wrong-answer: Checks a[i][1]==a[j][0] (whether i opens someone) instead of whether someone opens i. |
| [4403875](https://codeforces.com/contest/315/submission/4403875) | Python 3 | WRONG_ANSWER | WA | WA | 0003 | True | WA@0003 | `0\n` | True | wrong-answer: Counts distinct b values with a!=b; ignores self-opening rules and duplicates. |

### 334B: VALIDATED

- packageHash `eb03ab6beb6dde89862b84744c27661eb94bbda6ee6c8b9f306f7b5491d913a8`
- evidenceHash `af1cfaf9cbbbe1b5984d6122afd08ce8c06e8cf0528a131e1546bf9a9aea3839`
- auditHash `f255bf7e1c32ccd31b56edba01e6f99dcbbd621285214cefbecc043d87f20920`
- archive SHA256 `875da63cd3674b5461d3068de596c247c42548b535fe4d91e04215e5a63c9e41`
- contract gate: {'auditHash': 'f255bf7e1c32ccd31b56edba01e6f99dcbbd621285214cefbecc043d87f20920', 'passed': True}
- CRLF-input tests: 45; independent reference: tests=198, invalid=0, mismatches=0
- issues: none
- max-size coverage: {'bound': 1000000, 'maxSizeMetric': 1000000, 'nAtMax': 7, 'ratio': 1.0, 'test': '0050'}
- CF-OK sources failing: 4176193 GNU C++ WA@0048

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 4177010 | L22: `if len(X) == 3 and len(Y) == 3 and X[0][1] == 3 and X[1][1] == 2 and X` | 0007 | `0 0\n2 1\n1 0\n0 2\n2 2\n1 0\n2 1\n0 2\n` | `ugly` | `respectable\n` | `17ea5b65144ac177` |
| 4177576 | L14: `if (sorted(cols)[1], sorted(rows)[1]) in points:` | 0007 | `0 0\n2 1\n1 0\n0 2\n2 2\n1 0\n2 1\n0 2\n` | `ugly` | `respectable\n` | `17ea5b65144ac177` |
| 4180814 | L20: `if [vertex[0] + i, vertex[1]] not in points:` | 0040 | `0 0\n0 1\n0 2\n1 0\n1 2\n3 0\n3 1\n3 2\n` | `respectable` | `ugly\n` | `c814470f06d13e98` |
| 4187940 | L12: `if temp[0][1]==3 and temp[1][1] == 2 and temp[2][1] ==3:` | 0007 | `0 0\n2 1\n1 0\n0 2\n2 2\n1 0\n2 1\n0 2\n` | `ugly` | `respectable\n` | `17ea5b65144ac177` |
| 4189069 | L23: `if q[2]-q[1]==q[1]-q[0] and w[2]-w[1]==w[1]-w[0]:` | 0007 | `0 0\n2 1\n1 0\n0 2\n2 2\n1 0\n2 1\n0 2\n` | `ugly` | `respectable\n` | `17ea5b65144ac177` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [4175438](https://codeforces.com/contest/334/submission/4175438) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [4175718](https://codeforces.com/contest/334/submission/4175718) | GNU C++0x | OK | AC | AC | None | True | AC@None | - | True |  |
| [4175931](https://codeforces.com/contest/334/submission/4175931) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [4175932](https://codeforces.com/contest/334/submission/4175932) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [4175942](https://codeforces.com/contest/334/submission/4175942) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [4177010](https://codeforces.com/contest/334/submission/4177010) | Python 3 | WRONG_ANSWER | WA | WA | 0007 | True | WA@0007 | `respectable\n` | True | wrong-answer: Checks only 3-2-3 count patterns per axis; accepts a set with a duplicate point and the centre present. |
| [4177576](https://codeforces.com/contest/334/submission/4177576) | Python 3 | WRONG_ANSWER | WA | WA | 0007 | True | WA@0007 | `respectable\n` | True | wrong-answer: Checks the centre is absent but not that the 8 points are distinct (duplicates accepted). |
| [4180814](https://codeforces.com/contest/334/submission/4180814) | Python 3 | WRONG_ANSWER | WA | WA | 0025 | True | WA@0025 | `ugly\n` | True | wrong-answer: Assumes unit spacing from the min vertex; rejects respectable sets with gaps >1. |
| [4187940](https://codeforces.com/contest/334/submission/4187940) | Python 3 | WRONG_ANSWER | WA | WA | 0007 | True | WA@0007 | `respectable\n` | True | wrong-answer: Only checks 3-2-3 count patterns; duplicates and wrong combos pass. |
| [4189069](https://codeforces.com/contest/334/submission/4189069) | Python 3 | WRONG_ANSWER | WA | WA | 0007 | True | WA@0007 | `respectable\n` | True | wrong-answer: Requires equal spacing x3-x2==x2-x1, which is not part of the definition. |

### 337B: NOT_VALIDATED_HELD

- packageHash `2a4288d0daad6a9cf96ecae1dc78c6d7ade183638b5616250de085e4ebb0eafc`
- evidenceHash `75a9d63a58f4f3ff0757d1b820e5c0b94fd31479d413bdd937e19047325810c9`
- auditHash `220e2047d94990b29a5d1c7fa80457369709af5b33664aa56c0c92f8aa036641`
- archive SHA256 `0306402995ac8aa6c697147e23d485c6f5dd0aaabb94adae86b62f12ae361495`
- contract gate: None
- CRLF-input tests: 34; independent reference: tests=186, invalid=0, mismatches=0
- issues: only 1/5 incorrect sources are counted WA algorithmic kills
- max-size coverage: {'bound': 1000, 'maxSizeMetric': 1000, 'nAtMax': 8, 'ratio': 1.0, 'test': '0038'}
- CF-OK sources failing: 4289261 Python 3 RE@0001, 4289534 Python 3 RE@0001
- replacement WA candidates (executed here, need builder revalidation and re-audit): 206284682@0001, 228128852@0004, 206144360@0001, 206151818@0001

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [4288545](https://codeforces.com/contest/337/submission/4288545) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [4288707](https://codeforces.com/contest/337/submission/4288707) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [4288745](https://codeforces.com/contest/337/submission/4288745) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [4288786](https://codeforces.com/contest/337/submission/4288786) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [4288898](https://codeforces.com/contest/337/submission/4288898) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [199577681](https://codeforces.com/contest/337/submission/199577681) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `0\n` | False | : Presentation-only: prints 0 instead of 0/1 when a:b == c:d. All 10 of its WA outputs on LF tests are numerically equal to the expected value (semall.json), so it is not counted (same rule as 197B). |
| [202536774](https://codeforces.com/contest/337/submission/202536774) | Python 3 | WRONG_ANSWER | WA | WA | 0003 | True | WA@0003 | `1/-1\n` | True | wrong-answer: Ad-hoc formula 1/round(1/z) with shifted a,b; prints e.g. 1/-1. |
| [206033978](https://codeforces.com/contest/337/submission/206033978) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | `` | False | : Only defines a function; never reads input or prints, so no algorithm runs. |
| [206034249](https://codeforces.com/contest/337/submission/206034249) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | `Enter multiple values: 0.33333333333333337\n` | False | : Writes an input() prompt to stdout and prints a float; not a genuine attempt at the required p/q output. |
| [206036582](https://codeforces.com/contest/337/submission/206036582) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | `Enter multiple values: 0.3333333333333333\n` | False | : Writes an input() prompt to stdout and hard-codes the two sample answers. |

### 358A: VALIDATED

- packageHash `fa8eb3ff9445896b5c0258ad893fa978d37114960967ba021366bd5bf1dace33`
- evidenceHash `4e405405889ffdae19308517cf605db2706185caeb80c395ef58e4ae98631649`
- auditHash `795ece947097ced40ae584c5a2f0fb251f2feeb50afa90b34c009b67238f68af`
- archive SHA256 `eb78c2230a885a1f544f43d0fbd9a748c642b6b2d4b1b0aedab36507ccfc7338`
- contract gate: {'auditHash': '795ece947097ced40ae584c5a2f0fb251f2feeb50afa90b34c009b67238f68af', 'passed': True}
- CRLF-input tests: 28; independent reference: tests=188, invalid=0, mismatches=0
- issues: none
- max-size coverage: {'bound': 1000, 'maxSizeMetric': 1000, 'nAtMax': 3, 'ratio': 1.0, 'test': '0041'}

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 4881213 | L15: `Max, Last = Last, Nums[i]` | 0021 | `3\n1 0 3\n` | `no` | `yes\n` | `5040625b1fb6fa4a` |
| 4882668 | L6: `if intersection > 1 and intersection not in [points[i][1] - points[i][` | 0013 | `4\n3 1 4 2\n` | `yes` | `no\n` | `564739ea8fa5926d` |
| 4884281 | L9: `if min(a[i], a[i+1]) < min(a[j], a[j+1]) < max(a[i], a[i+1]) < max(a[j` | 0015 | `5\n1 9 8 7 0\n` | `yes` | `no\n` | `564739ea8fa5926d` |
| 4885597 | L10: `mx[1]=last` | 0021 | `3\n1 0 3\n` | `no` | `yes\n` | `5040625b1fb6fa4a` |
| 4900050 | L10: `if M <= Max and m >= Min:` | 0054 | `2\n-5 5\n` | `no` | `yes\n` | `5040625b1fb6fa4a` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [4880789](https://codeforces.com/contest/358/submission/4880789) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [4880790](https://codeforces.com/contest/358/submission/4880790) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [4880797](https://codeforces.com/contest/358/submission/4880797) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [4880805](https://codeforces.com/contest/358/submission/4880805) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [4880831](https://codeforces.com/contest/358/submission/4880831) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [4881213](https://codeforces.com/contest/358/submission/4881213) | Python 3 | WRONG_ANSWER | WA | WA | 0009 | True | WA@0009 | `yes\n` | True | wrong-answer: Tracks a single min/max window; misses intersections that need full interval nesting history. |
| [4882668](https://codeforces.com/contest/358/submission/4882668) | Python 3 | WRONG_ANSWER | WA | WA | 0008 | True | WA@0008 | `no\n` | True | wrong-answer: Overlap-length heuristic (intersection>1) mis-classifies touching/nested arcs. |
| [4884281](https://codeforces.com/contest/358/submission/4884281) | Python 3 | WRONG_ANSWER | WA | WA | 0011 | True | WA@0011 | `no\n` | True | wrong-answer: Prints no for n<=3 correctly but checks only one interleaving orientation. |
| [4885597](https://codeforces.com/contest/358/submission/4885597) | Python 3 | WRONG_ANSWER | WA | WA | 0009 | True | WA@0009 | `yes\n` | True | wrong-answer: Single shrinking window; nesting order not tracked. |
| [4900050](https://codeforces.com/contest/358/submission/4900050) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `yes\n` | True | wrong-answer: Requires each new arc to be nested in the previous one; outer non-crossing arcs are flagged yes. |

### 388A: VALIDATED

- packageHash `6f3ab24ba997e1c6053512a076d3e29b84127a2766d6ac3329377c6ea315253b`
- evidenceHash `c113d73853f193416137830b43e44af44c11a3243dee86c3eb4c3bb240790d4a`
- auditHash `ac7a3f6309174f83820a39ec6652048a562586e18b53e35ea34f9b5a7edc7d3a`
- archive SHA256 `6b60f90f3499586f2da21a31aa97620b91b9ed9d0dfa759240e3f66b535c432d`
- contract gate: {'auditHash': 'ac7a3f6309174f83820a39ec6652048a562586e18b53e35ea34f9b5a7edc7d3a', 'passed': True}
- CRLF-input tests: 36; independent reference: tests=190, invalid=0, mismatches=0
- issues: none
- max-size coverage: {'bound': 100, 'maxSizeMetric': 100, 'nAtMax': 18, 'ratio': 1.0, 'test': '0093'}

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 5888189 | L12: `if not u[j] and a[j]<prev:` | 0055 | `3\n2 3 2\n` | `1` | `2\n` | `53c234e5e8472b6a` |
| 5898411 | L22: `ml=a[j]+1` | 0183 | `5\n0 0 2 2 2\n` | `2` | `3\n` | `1121cfccd5913f0a` |
| 9089117 | L12: `print(max(m,b))` | 0055 | `3\n2 3 2\n` | `1` | `2\n` | `53c234e5e8472b6a` |
| 9126570 | L16: `if(i > k[t]):` | 0055 | `3\n2 3 2\n` | `1` | `2\n` | `53c234e5e8472b6a` |
| 9245036 | L8: `ans=max(ans,b[i]-i);` | 0055 | `3\n2 3 2\n` | `1` | `2\n` | `53c234e5e8472b6a` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [5874693](https://codeforces.com/contest/388/submission/5874693) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [5874709](https://codeforces.com/contest/388/submission/5874709) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [5874711](https://codeforces.com/contest/388/submission/5874711) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [5874729](https://codeforces.com/contest/388/submission/5874729) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [5874734](https://codeforces.com/contest/388/submission/5874734) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [5888189](https://codeforces.com/contest/388/submission/5888189) | Python 3 | WRONG_ANSWER | WA | WA | 0010 | True | WA@0010 | `6\n` | True | wrong-answer: Builds piles by strictly decreasing strength, ignoring that strength counts boxes above (equal strengths can stack). |
| [5898411](https://codeforces.com/contest/388/submission/5898411) | Python 3 | WRONG_ANSWER | WA | WA | 0021 | True | WA@0021 | `1\n` | True | wrong-answer: Pile-height bookkeeping (ml=a[j]+1) resets mid-pile; miscounts piles. |
| [9089117](https://codeforces.com/contest/388/submission/9089117) | Python 3 | WRONG_ANSWER | WA | WA | 0010 | True | WA@0010 | `6\n` | True | wrong-answer: Answers the maximum multiplicity of a strength value. |
| [9126570](https://codeforces.com/contest/388/submission/9126570) | Python 3 | WRONG_ANSWER | WA | WA | 0010 | True | WA@0010 | `6\n` | True | wrong-answer: Stacks only strictly larger strengths; equal-strength boxes force new piles. |
| [9245036](https://codeforces.com/contest/388/submission/9245036) | Python 3 | WRONG_ANSWER | WA | WA | 0010 | True | WA@0010 | `6\n` | True | wrong-answer: max(count[i]+i-i) style formula with b initialised to range(101); not the pile bound. |

### 38C: VALIDATED

- packageHash `524af8c89488613b07661bf1ab1bded891e341e22345da8fa185cc95f959c050`
- evidenceHash `ec1f8add6c5eddbb5b0777ef31dd076d02809274e4a2cbd605957f933380843f`
- auditHash `cd61e55426ba91dc4afa62588cb08f90ef5a637665ea8bce7dc79dd40fb6a225`
- archive SHA256 `d9f909610f16cdb2e9ab6e9b3167becda13814351b71395debd84c2ba1c85404`
- contract gate: {'auditHash': 'cd61e55426ba91dc4afa62588cb08f90ef5a637665ea8bce7dc79dd40fb6a225', 'passed': True}
- CRLF-input tests: 27; independent reference: tests=188, invalid=0, mismatches=0
- issues: none
- max-size coverage: {'bound': 100, 'maxSizeMetric': 100, 'nAtMax': 6, 'ratio': 1.0, 'test': '0167'}
- CF-OK sources failing: 170899 MS C++ CE@None, 51313344 Python 3 WA@0037

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 19534179 | L8: `s+=l[j]-l[j]%k` | 0004 | `2 2\n3 3\n` | `6` | `4\n` | `7de1555df0c27003` |
| 27553787 | L8: `count+=x//l` | 0004 | `2 2\n3 3\n` | `6` | `4\n` | `7de1555df0c27003` |
| 27553944 | L22: `print(len(b)*min(b))` | 0073 | `1 40\n96\n` | `96` | `4\n` | `7de1555df0c27003` |
| 27554069 | L19: `max=min(b)` | 0075 | `2 11\n68 60\n` | `121` | `120\n` | `97b912eb4a61df5f` |
| 36872890 | L6: `for i in range(l, max(a)):` | 0037 | `1 1\n1\n` | `1` | `0` | `5feceb66ffc86f38` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [170839](https://codeforces.com/contest/38/submission/170839) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [170874](https://codeforces.com/contest/38/submission/170874) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [170920](https://codeforces.com/contest/38/submission/170920) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [170943](https://codeforces.com/contest/38/submission/170943) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [170977](https://codeforces.com/contest/38/submission/170977) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [19534179](https://codeforces.com/contest/38/submission/19534179) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `4\n` | True | wrong-answer: Uses only piece length k=l (and suffix sums), never other lengths d>l. |
| [27553787](https://codeforces.com/contest/38/submission/27553787) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `4\n` | True | wrong-answer: Only tries length l. |
| [27553944](https://codeforces.com/contest/38/submission/27553944) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0002 | `10\n` | True | wrong-answer: Splits stripes by l heuristically and multiplies by the minimum piece. |
| [27554069](https://codeforces.com/contest/38/submission/27554069) | Python 3 | WRONG_ANSWER | WA | WA | 0010 | True | WA@0010 | `112\n` | True | wrong-answer: Uses min(b) as the piece length only. |
| [36872890](https://codeforces.com/contest/38/submission/36872890) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `4` | True | wrong-answer: Loops d in range(l, max(a)), excluding d=max(a) (e.g. single stripe of length 100). |

### 417B: NOT_VALIDATED_HELD

- packageHash `4e681c07761fd36a946b7aa8c0f2ef9b73eceeeb90bd121c6e8f7a41fcfa976f`
- evidenceHash `bf4fe451daf80ff5a1095b3ccb23d3d346d3c1bcd646492a460184de238b4b40`
- auditHash `a2e24af6b65f3ae87145f57882dde6605f656ba1af913934fea27ccfb7335178`
- archive SHA256 `4908288d8d5e319193d82d7abfe92053fa23006233341a0ea5992746545dc9e3`
- contract gate: None
- CRLF-input tests: 24; independent reference: tests=186, invalid=0, mismatches=0
- issues: only 4/5 incorrect sources are counted WA algorithmic kills
- max-size coverage: {'bound': 100000, 'maxSizeMetric': 100000, 'nAtMax': 11, 'ratio': 1.0, 'test': '0037'}
- replacement WA candidates (executed here, need builder revalidation and re-audit): 92913852@0005, 6392225@0004, 92912976@0004, 6393946@0004, 6418602@0003, 6387492@0003, 26304568@0003, 65696748@0011

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [6385736](https://codeforces.com/contest/417/submission/6385736) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [6386063](https://codeforces.com/contest/417/submission/6386063) | GNU C++0x | OK | AC | AC | None | True | AC@None | - | True |  |
| [6386069](https://codeforces.com/contest/417/submission/6386069) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [6386176](https://codeforces.com/contest/417/submission/6386176) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [6386264](https://codeforces.com/contest/417/submission/6386264) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [6388077](https://codeforces.com/contest/417/submission/6388077) | Python 3 | WRONG_ANSWER | WA | WA | 0012 | True | WA@0012 | `NO\n` | True | wrong-answer: Overwrites mem[k]=x with the latest x, losing the maximum; later valid x are rejected. |
| [6391028](https://codeforces.com/contest/417/submission/6391028) | Python 3 | TIME_LIMIT_EXCEEDED | TLE | TLE | 0026 | True | - | - | False | : Correct backward search but O(n^2); TLE only. complexity-only (TLE); not counted per handoff policy |
| [6391324](https://codeforces.com/contest/417/submission/6391324) | Python 3 | WRONG_ANSWER | WA | WA | 0010 | True | WA@0010 | `YES\n` | True | wrong-answer: Uses == instead of = when marking, and requires x <= len-1 in the wrong order. |
| [6396554](https://codeforces.com/contest/417/submission/6396554) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `YES\n` | True | wrong-answer: Requires participant ids to be non-decreasing per x; unrelated condition. |
| [6397137](https://codeforces.com/contest/417/submission/6397137) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0002 | `NO\nYES\n` | True | wrong-answer: Requires x == previous+1 exactly (repeats are valid) and prints YES after printing NO. |

### 41B: VALIDATED

- packageHash `70c9c03b3b3bd4f70bf40e765379edbb45ac2ac55bf9bb9d82d03f92cd42a514`
- evidenceHash `18d76462526d0d16bb31736ddd87a3f8ad4493a5e0def6d4925a616d73fa664e`
- auditHash `83859bbaabf8cd19c030659af477221a4570e7343d46a6a6e7e395d5e1265253`
- archive SHA256 `ff66ac7f1192818751187e0344e7515a64ff15982f74e3546dbd7cd362dc0dc9`
- contract gate: {'auditHash': '83859bbaabf8cd19c030659af477221a4570e7343d46a6a6e7e395d5e1265253', 'passed': True}
- CRLF-input tests: 15; independent reference: tests=183, invalid=0, mismatches=0
- issues: none
- max-size coverage: {'bound': 2000, 'maxSizeMetric': 2000, 'nAtMax': 3, 'ratio': 1.0, 'test': '0034'}
- CF-OK sources failing: 186320 MS C++ CE@None

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 5056958 | L14: `if a - b > best_score:` | 0071 | `5 5\n3 12 2 8 1\n` | `17` | `14\n` | `9a92adbc0cee38ef` |
| 9382036 | L11: `if(vmin > an[i] - an[j]):` | 0071 | `5 5\n3 12 2 8 1\n` | `17` | `14\n` | `9a92adbc0cee38ef` |
| 25366403 | L6: `for j in range(0,n-1,1):` | 0001 | `2 4\n3 7\n` | `8` | `4\n` | `7de1555df0c27003` |
| 27681704 | L11: `print((b//list1[l.index(max(l))])*(max(l))+b)` | 0071 | `5 5\n3 12 2 8 1\n` | `17` | `14\n` | `9a92adbc0cee38ef` |
| 61597190 | L8: `if a[j]/a[i] > m:` | 0071 | `5 5\n3 12 2 8 1\n` | `17` | `14\n` | `9a92adbc0cee38ef` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [186180](https://codeforces.com/contest/41/submission/186180) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [186215](https://codeforces.com/contest/41/submission/186215) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [186229](https://codeforces.com/contest/41/submission/186229) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [186260](https://codeforces.com/contest/41/submission/186260) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [186380](https://codeforces.com/contest/41/submission/186380) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [5056958](https://codeforces.com/contest/41/submission/5056958) | Python 3 | WRONG_ANSWER | WA | WA | 0020 | True | WA@0020 | `1556\n` | True | wrong-answer: Maximises the price difference a-b instead of the final money (b//buy)*sell + b%buy. |
| [9382036](https://codeforces.com/contest/41/submission/9382036) | Python 3 | WRONG_ANSWER | WA | WA | 0020 | True | WA@0020 | `1172\n` | True | wrong-answer: Picks the pair with the most negative a[i]-a[j], not the best final amount. |
| [25366403](https://codeforces.com/contest/41/submission/25366403) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | `4\n` | True | wrong-answer: Both loops stop at n-1 and allow j<i (selling before buying). |
| [27681704](https://codeforces.com/contest/41/submission/27681704) | Python 3 | WRONG_ANSWER | WA | WA | 0020 | True | WA@0020 | `1172\n` | True | wrong-answer: Adds (b//price)*gain but the buy price index comes from l.index on gains, mixing indices. |
| [61597190](https://codeforces.com/contest/41/submission/61597190) | Python 3 | WRONG_ANSWER | WA | WA | 0020 | True | WA@0020 | `1172\n` | True | wrong-answer: Maximises the sell/buy ratio, which ignores integer division leftovers. |

### 435B: VALIDATED

- packageHash `04e08683a5f31880b482266aca6879e2ee66bd398236601a8a7ac0cfac743f87`
- evidenceHash `708e7bc306a8ad1fdea9f4fa497e8fff977c58cd38895beb698471c8b37cd879`
- auditHash `6a0a3f308b8e5b714b75a307f3ebca1ed9f2d7187400851881beb4a60055dd4e`
- archive SHA256 `9c65b632e29be6f0f8ba8aac7cfaa21a9e782021455558d090cef523d432beb4`
- contract gate: {'auditHash': '6a0a3f308b8e5b714b75a307f3ebca1ed9f2d7187400851881beb4a60055dd4e', 'passed': True}
- CRLF-input tests: 46; independent reference: tests=200, invalid=0, mismatches=0
- issues: none
- max-size coverage: {'bound': 19100, 'maxSizeMetric': 19100, 'nAtMax': 1, 'ratio': 1.0, 'test': '0049'}

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 6752853 | L14: `if diff > max_diff:` | 0005 | `1234 3\n` | `4123` | `3214\n` | `03c68912fb8a8ad8` |
| 6755856 | L9: `if j - i: continue` | 0096 | `39 1\n` | `93` | `39\n` | `eedb85ab90d324a5` |
| 6756206 | L8: `while (j > 0) and (s[j] > s[j - 1]) and (k > 0):` | 0005 | `1234 3\n` | `4123` | `3214\n` | `03c68912fb8a8ad8` |
| 6794843 | L17: `if b[l]==max(b):` | 0009 | `9022 2\n` | `9220` | `9202\n` | `4aa4c187186bf2a2` |
| 6816804 | L7: `if a[i-1] < a[i]:` | 0150 | `446 1\n` | `464` | `644\n` | `0a2a5ea75282bf45` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [6742610](https://codeforces.com/contest/435/submission/6742610) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [6742784](https://codeforces.com/contest/435/submission/6742784) | GNU C++0x | OK | AC | AC | None | True | AC@None | - | True |  |
| [6742941](https://codeforces.com/contest/435/submission/6742941) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [6743125](https://codeforces.com/contest/435/submission/6743125) | GNU C++0x | OK | AC | AC | None | True | AC@None | - | True |  |
| [6743172](https://codeforces.com/contest/435/submission/6743172) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [6752853](https://codeforces.com/contest/435/submission/6752853) | Python 3 | WRONG_ANSWER | WA | WA | 0005 | True | WA@0005 | `3214\n` | True | wrong-answer: Greedy single best adjacent swap each step; not optimal over k swaps. |
| [6755856](https://codeforces.com/contest/435/submission/6755856) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | `1990\n` | True | wrong-answer: Skips any non-adjacent larger digit (if j-i: continue) and never decrements k correctly. |
| [6756206](https://codeforces.com/contest/435/submission/6756206) | Python 3 | WRONG_ANSWER | WA | WA | 0005 | True | WA@0005 | `3214\n` | True | wrong-answer: Insertion-sort bubbling consumes swaps left-to-right without looking ahead for the best digit within k. |
| [6794843](https://codeforces.com/contest/435/submission/6794843) | Python 3 | WRONG_ANSWER | WA | WA | 0009 | True | WA@0009 | `9202\n` | True | wrong-answer: Window includes positions past k after k shrinks; ties choose the last max (should be first). |
| [6816804](https://codeforces.com/contest/435/submission/6816804) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `9970000008001234\n` | True | wrong-answer: Bubble with moving j pointer; spends swaps on early positions sub-optimally. |

### 441B: VALIDATED

- packageHash `5c0e678a5d14c8e10f6450d5c5bc03889b7c11836934ba1848bb6c5dc34e1d78`
- evidenceHash `4a9858750121e5883b536f10a94abbb1d1bed806de8a5e7631d892169a92773f`
- auditHash `5ff1441f364ba7b9c8e08e781149467c8e3d3b1b5b6682eff6771cc6d87d4919`
- archive SHA256 `n/a (whole-pool archive 0637f17856db18a669f39640d39c8d2ffbd80b9c1866d30de8ded075f06e8ab9; no per-ID archive)`
- contract gate: {'auditHash': '5ff1441f364ba7b9c8e08e781149467c8e3d3b1b5b6682eff6771cc6d87d4919', 'emptyApprovalRejected': True, 'passed': True}
- CRLF-input tests: 31; independent reference: tests=192, invalid=0, mismatches=0
- issues: none
- max-size coverage: {'bound': 3000, 'maxSizeMetric': 3000, 'nAtMax': 11, 'ratio': 1.0, 'test': '0044'}
- CF-OK sources failing: 6839985 MS C++ CE@None

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 6845814 | L8: `for i in range(1,3001):` | 0019 | `1 1\n3000 2\n` | `2` | `1\n` | `4355a46b19d348dc` |
| 6850840 | L15: `days.append(day)` | 0086 | `1 1\n1 3\n` | `2` | `3\n` | `1121cfccd5913f0a` |
| 6852929 | L5: `li[i] += (int(input().split()[1]))` | 0054 | `1 5\n5 2\n` | `2` | `-4\n` | `8fbfec21acf8f743` |
| 6855572 | L4: `b_last = 0` | 0015 | `2 3\n1 6\n3 6\n` | `12` | `9\n` | `2e6d31a5983a9125` |
| 6857892 | L13: `for i in range(3001):` | 0019 | `1 1\n3000 2\n` | `2` | `1\n` | `4355a46b19d348dc` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [6839393](https://codeforces.com/contest/441/submission/6839393) | GNU C++0x | OK | AC | AC | None | True | AC@None | - | True |  |
| [6839461](https://codeforces.com/contest/441/submission/6839461) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [6839464](https://codeforces.com/contest/441/submission/6839464) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [6839585](https://codeforces.com/contest/441/submission/6839585) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [6839709](https://codeforces.com/contest/441/submission/6839709) | GNU C++0x | OK | AC | AC | None | True | AC@None | - | True |  |
| [6845814](https://codeforces.com/contest/441/submission/6845814) | Python 3 | WRONG_ANSWER | WA | WA | 0008 | True | WA@0008 | - | True | wrong-answer: Day loop for i in range(1,3001) never visits day 3001, so fruit ripening on day 3000 can only be picked on day 3000; on a one-tree day-3000 case with b>v it loses the day-3001 harvest. Witness (valid LF package test 0019): input '1 1\n3000 2\n', reference '2', source prints '1'; wrong on 25 tests after case-insensitive YES/NO and numeric normalisation. |
| [6850840](https://codeforces.com/contest/441/submission/6850840) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0002 | - | True | wrong-answer: days.append(day) inside the tree loop re-adds every ripening day after the de-duplicated day list was built, so the same day is processed again with a fresh daily limit v and the total exceeds the true capacity. debug() is a no-op (its print is commented out), so the wrong total is not debug output. Witness (valid LF package test 0086): input '1 1\n1 3\n', reference '2', source prints '3'; wrong on 82 tests after case-insensitive YES/NO and numeric normalisation. |
| [6852929](https://codeforces.com/contest/441/submission/6852929) | Python 3 | WRONG_ANSWER | WA | WA | 0003 | True | WA@0003 | - | True | wrong-answer: li[i] += b indexes fruit by input row i instead of ripening day a, and adds the unclamped negative leftover li[i-1]-limit; the result ignores the ripening days entirely. Witness (valid LF package test 0054): input '1 5\n5 2\n', reference '2', source prints '-4'; wrong on 129 tests after case-insensitive YES/NO and numeric normalisation. |
| [6855572](https://codeforces.com/contest/441/submission/6855572) | Python 3 | WRONG_ANSWER | WA | WA | 0006 | True | WA@0006 | - | True | wrong-answer: b_last is reset to 0 before the current day fruit is processed, and when yesterday leftovers fill the whole daily capacity the current fruit is never carried to tomorrow; leftover fruit is lost. Witness (valid LF package test 0015): input '2 3\n1 6\n3 6\n', reference '12', source prints '9'; wrong on 76 tests after case-insensitive YES/NO and numeric normalisation. |
| [6857892](https://codeforces.com/contest/441/submission/6857892) | Python 3 | TIME_LIMIT_EXCEEDED | WA | WA | 0008 | True | WA@0008 | - | True | wrong-answer: for i in range(3001) covers days 0..3000 only and never harvests day 3001, so fruit ripening on day 3000 loses its second day. Codeforces judged it TLE, but in the sandbox it gives a WA on a valid test within the time limit, so the kill is a wrong value, not a timeout. Witness (valid LF package test 0019): input '1 1\n3000 2\n', reference '2', source prints '1'; wrong on 25 tests after case-insensitive YES/NO and numeric normalisation. |

### 489C: VALIDATED

- packageHash `1c63ecd0807a7bae721a97e16ba5cf2ee7c5b7665047f2afcef105c2dc480276`
- evidenceHash `df95890f2b0e23f24fa1115451ba96c0ff77bcab710e304b42cd31383ef91e85`
- auditHash `260c9b7c4155e273ccb1355ba9cc4a35f43824e3e7b90d45af4cd4f494bd14da`
- archive SHA256 `n/a (whole-pool archive 0637f17856db18a669f39640d39c8d2ffbd80b9c1866d30de8ded075f06e8ab9; no per-ID archive)`
- contract gate: {'auditHash': '260c9b7c4155e273ccb1355ba9cc4a35f43824e3e7b90d45af4cd4f494bd14da', 'emptyApprovalRejected': True, 'passed': True}
- CRLF-input tests: 65; independent reference: tests=217, invalid=0, mismatches=0
- issues: none
- max-size coverage: {'bound': 100, 'maxSizeMetric': 100, 'nAtMax': 27, 'ratio': 1.0, 'test': '0208'}

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 192580474 | L10: `number += f'{s}'`; L3: `if m > s:` | 0003 | `2 1\n` | `10 10` | `-1 -1\n` | `6a21cc779f3d8182` |
| 192671817 | L3: `if sum_N < start:` | 0008 | `1 0\n` | `0 0` | `-1 -1\n` | `6a21cc779f3d8182` |
| 192780155 | L9: `if(diff >= 0 and reqLen - 1 <= diff):` | 0003 | `2 1\n` | `10 10` | `-1 -1\n` | `6a21cc779f3d8182` |
| 192783888 | L24: `if(diff >= 0 and reqLen1 - 1 <= diff):` | 0008 | `1 0\n` | `0 0` | `-1 -1\n` | `6a21cc779f3d8182` |
| 192867818 | L24: `if s== 0 or s > m*9:` | 0008 | `1 0\n` | `0 0` | `-1 -1\n` | `6a21cc779f3d8182` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [8720301](https://codeforces.com/contest/489/submission/8720301) | GNU C++0x | OK | AC | AC | None | True | AC@None | - | True |  |
| [8720530](https://codeforces.com/contest/489/submission/8720530) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [8720584](https://codeforces.com/contest/489/submission/8720584) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [8720716](https://codeforces.com/contest/489/submission/8720716) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [8721064](https://codeforces.com/contest/489/submission/8721064) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [192580474](https://codeforces.com/contest/489/submission/192580474) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | - | True | wrong-answer: Treats the remaining digit sum as one digit, appending str(s) and decrementing it, so the number has the wrong length and digit sum. It also prints -1 -1 whenever m > s, although e.g. m=3, s=1 has answer 100 100. Witness (valid LF package test 0003): input '2 1\n', reference '10 10', source prints '-1 -1'; wrong on 209 tests after case-insensitive YES/NO and numeric normalisation. |
| [192671817](https://codeforces.com/contest/489/submission/192671817) | Python 3 | WRONG_ANSWER | WA | WA | 0008 | True | WA@0008 | - | True | wrong-answer: Both searches start at digit 1 and reject sum_N < start, so the valid m=1, s=0 number 0 is reported as -1 -1. Witness (valid LF package test 0008): input '1 0\n', reference '0 0', source prints '-1 -1'; wrong on 2 tests after case-insensitive YES/NO and numeric normalisation. |
| [192780155](https://codeforces.com/contest/489/submission/192780155) | Python 3 | WRONG_ANSWER | WA | WA | 0003 | True | WA@0003 | - | True | wrong-answer: The greedy condition reqLen-1 <= remaining sum reserves at least 1 for every remaining digit, which forbids zero digits. Cases like m=2, s=1 (answer 10 10) are reported impossible, and minima with internal zeros come out wrong. Witness (valid LF package test 0003): input '2 1\n', reference '10 10', source prints '-1 -1'; wrong on 171 tests after case-insensitive YES/NO and numeric normalisation. |
| [192783888](https://codeforces.com/contest/489/submission/192783888) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | - | True | wrong-answer: The minimum is built with the same at-least-one-per-remaining-digit reservation and then reversed, which forces nonzero internal digits. Its maxNum[0]=="0" rejection also reports m=1, s=0 (answer 0 0) as -1 -1. Witness (valid LF package test 0008): input '1 0\n', reference '0 0', source prints '-1 -1'; wrong on 160 tests after case-insensitive YES/NO and numeric normalisation. |
| [192867818](https://codeforces.com/contest/489/submission/192867818) | Python 3 | WRONG_ANSWER | WA | WA | 0008 | True | WA@0008 | - | True | wrong-answer: if s==0 or s>m*9 prints -1 -1 even for m=1, s=0, whose answer is 0 0. Witness (valid LF package test 0008): input '1 0\n', reference '0 0', source prints '-1 -1'; wrong on 2 tests after case-insensitive YES/NO and numeric normalisation. |

### 507B: VALIDATED

- packageHash `efb7c9449fa79bacb42a058270441286a2ab31d5e1cb28e7ddd563e74f5da1e7`
- evidenceHash `ffc7f515641f70be1d76b805403c575a98cabf66e01efab0ae53f0fafd2dfbbf`
- auditHash `50ffe684a8a57de4b04d3b58d31e10f9add80b9939b792f3136dd4fa2c0f9395`
- archive SHA256 `n/a (whole-pool archive 0637f17856db18a669f39640d39c8d2ffbd80b9c1866d30de8ded075f06e8ab9; no per-ID archive)`
- contract gate: {'auditHash': '50ffe684a8a57de4b04d3b58d31e10f9add80b9939b792f3136dd4fa2c0f9395', 'emptyApprovalRejected': True, 'passed': True}
- CRLF-input tests: 37; independent reference: tests=190, invalid=0, mismatches=0
- issues: none
- max-size coverage: {'bound': 100000, 'maxSizeMetric': 100000, 'nAtMax': 10, 'ratio': 1.0, 'test': '0044'}
- CF-OK sources failing: 9521663 Python 3 WA@0093

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 48066369 | L12: `if (int(res) == 0):` | 0013 | `5 6 3 7 2\n` | `1` | `0\n` | `9a271f2a916b0b6e` |
| 48676896 | L3: `print(max(0,int(math.sqrt((a-x)*(a-x)+(b-y)*(b-y))//r)-1))` | 0013 | `5 6 3 7 2\n` | `1` | `0\n` | `9a271f2a916b0b6e` |
| 48677159 | L3: `print(int(math.sqrt((a-x)*(a-x)+(b-y)*(b-y))/(2*r)))` | 0002 | `1 1 1 4 4\n` | `3` | `2\n` | `53c234e5e8472b6a` |
| 49981713 | L4: `return math.ceil(st/2*r)` | 0001 | `2 0 0 0 4\n` | `1` | `4\n` | `7de1555df0c27003` |
| 50595154 | L4: `d = (dx**2 + dy**2)*0.5` | 0070 | `8 8 5 9 1\n` | `1` | `4\n` | `7de1555df0c27003` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [9515711](https://codeforces.com/contest/507/submission/9515711) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [9515762](https://codeforces.com/contest/507/submission/9515762) | GNU C++0x | OK | AC | AC | None | True | AC@None | - | True |  |
| [9515865](https://codeforces.com/contest/507/submission/9515865) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [9515996](https://codeforces.com/contest/507/submission/9515996) | GNU C++0x | OK | AC | AC | None | True | AC@None | - | True |  |
| [9516026](https://codeforces.com/contest/507/submission/9516026) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [48066369](https://codeforces.com/contest/507/submission/48066369) | Python 3 | WRONG_ANSWER | WA | WA | 0006 | True | WA@0006 | - | True | wrong-answer: When the distance is positive but less than the diameter, int(res)==0 forces the answer to 0, although one step is needed. Witness (valid LF package test 0013): input '5 6 3 7 2\n', reference '1', source prints '0'; wrong on 79 tests after case-insensitive YES/NO and numeric normalisation. |
| [48676896](https://codeforces.com/contest/507/submission/48676896) | Python 3 | WRONG_ANSWER | WA | WA | 0005 | True | WA@0005 | - | True | wrong-answer: Uses floor(dist/r)-1 instead of ceil(dist/(2r)), which is wrong whenever dist/(2r) is not just below an integer. Witness (valid LF package test 0013): input '5 6 3 7 2\n', reference '1', source prints '0'; wrong on 155 tests after case-insensitive YES/NO and numeric normalisation. |
| [48677159](https://codeforces.com/contest/507/submission/48677159) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0002 | - | True | wrong-answer: Truncates dist/(2r) with int() instead of taking the ceiling, so it undercounts by 1 whenever the distance is not an exact multiple of the diameter. Witness (valid LF package test 0002): input '1 1 1 4 4\n', reference '3', source prints '2'; wrong on 177 tests after case-insensitive YES/NO and numeric normalisation. |
| [49981713](https://codeforces.com/contest/507/submission/49981713) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | - | True | wrong-answer: Precedence error: math.ceil(st/2*r) computes (st/2)*r instead of st/(2r). Witness (valid LF package test 0001): input '2 0 0 0 4\n', reference '1', source prints '4'; wrong on 166 tests after case-insensitive YES/NO and numeric normalisation. |
| [50595154](https://codeforces.com/contest/507/submission/50595154) | Python 3 | WRONG_ANSWER | WA | WA | 0005 | True | WA@0005 | - | True | wrong-answer: Replaces the distance by half the squared distance and uses per-axis quotient/remainder formulas, which is not Euclidean distance; the step counts are wrong. Witness (valid LF package test 0070): input '8 8 5 9 1\n', reference '1', source prints '4'; wrong on 163 tests after case-insensitive YES/NO and numeric normalisation. |

### 518B: REJECTED

- packageHash `d9f94d535596a1604ade2cc4bfb08ba91f4f38949e072ef55fbd77d8d7d560c8`
- evidenceHash `f983744a020f17e577c8a20702c1ddd4b89b49b7f8124973e90ff19a9a54c3f5`
- auditHash `5c5fa0e9cd679db9aaa255877da67ce88d7cc6019fb410a04e633c29f630fa5d`
- archive SHA256 `119a1ef735f375496a39f0711256e318858abcdf857966979ca82fa467cce095`
- contract gate: None
- CRLF-input tests: 18; independent reference: tests=183, invalid=0, mismatches=0
- issues: accepted contradiction: CF-OK source(s) 9997130(WA@0001), 9998838(RE@0001), 43168918(WA@0001), 50663320(RE@0001), 46821685(WA@0001), 10002420(WA@0001), 9988304(WA@0001), 9994921(RE@0001), 42126459(WA@0001), 20403986(WA@0001), 10000805(WA@0001) fail the package; cause: CRLF bytes reach Python input(); passes on LF-normalized tests; only 1/5 incorrect sources are counted WA algorithmic kills
- max-size coverage: {'bound': 400000, 'maxSizeMetric': 400000, 'nAtMax': 1, 'ratio': 1.0, 'test': '0034'}
- CF-OK sources failing: 9997130 Python 3 WA@0001, 9998838 Python 3 RE@0001, 43168918 Python 3 WA@0001, 50663320 Python 3 RE@0001, 46821685 Python 3 WA@0001, 10002420 Python 3 WA@0001, 9984464 GNU C++0x CE@None, 9988304 Python 3 WA@0001, 9994921 Python 3 RE@0001, 42126459 Python 3 WA@0001, 20403986 Python 3 WA@0001, 10000805 Python 3 WA@0001
- replacement WA candidates (executed here, need builder revalidation and re-audit): 53585300@0001, 51416878@0001, 58910318@0001, 58684474@0001, 58839270@0001, 54827868@0001, 47820035@0009, 51346217@0001

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [9983509](https://codeforces.com/contest/518/submission/9983509) | GNU C++0x | OK | AC | AC | None | True | AC@None | - | True |  |
| [9983706](https://codeforces.com/contest/518/submission/9983706) | GNU C++0x | OK | AC | AC | None | True | AC@None | - | True |  |
| [9983836](https://codeforces.com/contest/518/submission/9983836) | GNU C++0x | OK | AC | AC | None | True | AC@None | - | True |  |
| [9984010](https://codeforces.com/contest/518/submission/9984010) | GNU C++0x | OK | AC | AC | None | True | AC@None | - | True |  |
| [9984220](https://codeforces.com/contest/518/submission/9984220) | GNU C++0x | OK | AC | AC | None | True | AC@None | - | True |  |
| [42384570](https://codeforces.com/contest/518/submission/42384570) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0009 | `4 0\n` | False | : Recorded kill is a CRLF artifact: with the test inputs normalized to LF the source gives WA (failed 0009), not WA on 0001; a stray '\r' from input() is scored as data. Original analysis: Greedy per s character takes a WHOOPS before all YAYs are fixed (one pass). |
| [45701865](https://codeforces.com/contest/518/submission/45701865) | Python 3 | WRONG_ANSWER | WA | WA | 0005 | True | WA@0005 | `5 3\n` | True | wrong-answer: Array maps with (yay -= ...) ordering bug: zeroes s_map[i] before subtracting from t_map[i]. |
| [45901580](https://codeforces.com/contest/518/submission/45901580) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | `A 1 1\n1\nb 1 1\n2\nC 1 1\n3\n3 0\n` | False | : Prints debug lines before the answer; the recorded 0001 failure is output noise (de-debugged it fails 0008). |
| [46031625](https://codeforces.com/contest/518/submission/46031625) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0008 | `4 0\n` | False | : Recorded kill is a CRLF artifact: with the test inputs normalized to LF the source gives WA (failed 0008), not WA on 0001; a stray '\r' from input() is scored as data. Original analysis: Iterates t and counts WHOOPS for every swapcase match without consuming s counts. |
| [46142003](https://codeforces.com/contest/518/submission/46142003) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0009 | `4 0\n` | False | : Recorded kill is a CRLF artifact: with the test inputs normalized to LF the source gives WA (failed 0009), not WA on 0001; a stray '\r' from input() is scored as data. Original analysis: min() recomputed after mutating dics[m], so dict[m] is not decremented correctly. |

### 548B: VALIDATED

- packageHash `dff0aff8a12ef1aa21a67393cc6ca8348d32f3b5e8c66d65f4772a45a9a9efbb`
- evidenceHash `3e4e7386e7087c2203892154e2ccbbdb9191b103a82329311a9551d6016839ca`
- auditHash `f1675a5a7610f3667eaf4b45da9f2f8337b81601bb07d14059228c372411beba`
- archive SHA256 `6e299ce081c3b9288858a381bf2eeb52ba070ffdf90e6998e22e439d2478df52`
- contract gate: {'auditHash': 'f1675a5a7610f3667eaf4b45da9f2f8337b81601bb07d14059228c372411beba', 'passed': True}
- CRLF-input tests: 10; independent reference: tests=163, invalid=0, mismatches=0
- issues: none
- max-size coverage: {'bound': 255000, 'maxSizeMetric': 255000, 'nAtMax': 4, 'ratio': 1.0, 'test': '0015'}
- CF-OK sources failing: 11283355 GNU C++ TLE@0014

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 11307618 | L21: `li.append(sum(g[f][:]))` | 0043 | `2 1 1\n1\n1\n1 1\n` | `1` | `0\n` | `9a271f2a916b0b6e` |
| 11309046 | L11: `m = max(m, mr)` | 0143 | `1 4 2\n0 1 1 1\n1 1\n1 3\n` | `4\n2` | `4\n1\n` | `63e50714f29bc440` |
| 11313092 | L13: `if sum(x) > max_bears:` | 0072 | `1 4 2\n1 0 1 0\n1 4\n1 3\n` | `2\n1` | `3\n2\n` | `751f43ef30ddf4d6` |
| 11314099 | L8: `mas[x] = reduce(lambda c, d: c + d, a[x])` | 0072 | `1 4 2\n1 0 1 0\n1 4\n1 3\n` | `2\n1` | `3\n2\n` | `751f43ef30ddf4d6` |
| 11320706 | L23: `if(high<sum(l[i])):` | 0072 | `1 4 2\n1 0 1 0\n1 4\n1 3\n` | `2\n1` | `3\n2\n` | `751f43ef30ddf4d6` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [11281775](https://codeforces.com/contest/548/submission/11281775) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [11282588](https://codeforces.com/contest/548/submission/11282588) | GNU C++11 | OK | AC | AC | None | True | AC@None | - | True |  |
| [11282855](https://codeforces.com/contest/548/submission/11282855) | GNU C++11 | OK | AC | AC | None | True | AC@None | - | True |  |
| [11283009](https://codeforces.com/contest/548/submission/11283009) | GNU C++11 | OK | AC | AC | None | True | AC@None | - | True |  |
| [11283080](https://codeforces.com/contest/548/submission/11283080) | GNU C++11 | OK | AC | AC | None | True | AC@None | - | True |  |
| [11307618](https://codeforces.com/contest/548/submission/11307618) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `4\n3\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n5\n5\n` | True | wrong-answer: Uses row sum (and loops f<m) instead of longest consecutive run. |
| [11309046](https://codeforces.com/contest/548/submission/11309046) | Python 3 | WRONG_ANSWER | WA | WA | 0007 | True | WA@0007 | `1\n2\n1\n2\n5\n` | True | wrong-answer: Resets the run counter on bb[j-1] but never takes the max inside the row; returns the last run. |
| [11313092](https://codeforces.com/contest/548/submission/11313092) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `4\n3\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n5\n5\n` | True | wrong-answer: Uses row sum instead of longest consecutive run of 1s. |
| [11314099](https://codeforces.com/contest/548/submission/11314099) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `4\n3\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n5\n5\n` | True | wrong-answer: Uses row sum instead of longest consecutive run of 1s. |
| [11320706](https://codeforces.com/contest/548/submission/11320706) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `4\n3\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n4\n5\n5\n` | True | wrong-answer: Uses row sum instead of longest consecutive run of 1s. |

### 550B: VALIDATED

- packageHash `9760ce21b5f264b705d482e33ed3819f60708c21e4b6568205d08de6858fa70d`
- evidenceHash `850fbcadff176be31b347c75517cc4735bddfdb407d6634ab90ee5c05d45e7a3`
- auditHash `80bfc3215cb3a4fa508593c9094ecc480a883f5ff9cc6b44ed7754486d3cdb37`
- archive SHA256 `n/a (whole-pool archive 0637f17856db18a669f39640d39c8d2ffbd80b9c1866d30de8ded075f06e8ab9; no per-ID archive)`
- contract gate: {'auditHash': '80bfc3215cb3a4fa508593c9094ecc480a883f5ff9cc6b44ed7754486d3cdb37', 'emptyApprovalRejected': True, 'passed': True}
- CRLF-input tests: 30; independent reference: tests=183, invalid=0, mismatches=0
- issues: none
- max-size coverage: {'bound': 15, 'maxSizeMetric': 15, 'nAtMax': 27, 'ratio': 1.0, 'test': '0178'}
- CF-OK sources failing: 11418158 MS C++ CE@None

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 188014416 | L3: `ans[0] += 1` | 0155 | `3 12 20 1\n5 7 4\n` | `2` | `1\n` | `4355a46b19d348dc` |
| 193158167 | L2: `if sum < l:` | 0001 | `3 5 6 1\n1 2 3\n` | `2` | `0\n` | `9a271f2a916b0b6e` |
| 197643532 | L15: `if(l <= sum(i) <= r and abs(i[-1]-i[0]) >= x):` | 0009 | `4 10 20 1\n4 6 4 6\n` | `9` | `7\n` | `10159baf262b43a9` |
| 208069928 | L19: `if (subListTotal > l and subListTotal < r) and (max(totalList[i]) - mi` | 0001 | `3 5 6 1\n1 2 3\n` | `2` | `0\n` | `9a271f2a916b0b6e` |
| 208074946 | L4: `l -= 1` | 0035 | `2 1 11 1\n1 10\n` | `1` | `0\n` | `9a271f2a916b0b6e` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [11417461](https://codeforces.com/contest/550/submission/11417461) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [11417550](https://codeforces.com/contest/550/submission/11417550) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [11417619](https://codeforces.com/contest/550/submission/11417619) | GNU C++11 | OK | AC | AC | None | True | AC@None | - | True |  |
| [11417726](https://codeforces.com/contest/550/submission/11417726) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [11417999](https://codeforces.com/contest/550/submission/11417999) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [188014416](https://codeforces.com/contest/550/submission/188014416) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | - | True | wrong-answer: After counting a valid subset it returns immediately (ans[0] += 1; return), so valid supersets of a valid subset are never explored; it undercounts. Witness (valid LF package test 0155): input '3 12 20 1\n5 7 4\n', reference '2', source prints '1'; wrong on 84 tests after case-insensitive YES/NO and numeric normalisation. |
| [193158167](https://codeforces.com/contest/550/submission/193158167) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | - | True | wrong-answer: Prunes any partial subset whose sum is below l or whose spread is below x, including the empty start state, although adding later problems can satisfy both lower bounds; it undercounts. Witness (valid LF package test 0001): input '3 5 6 1\n1 2 3\n', reference '2', source prints '0'; wrong on 126 tests after case-insensitive YES/NO and numeric normalisation. |
| [197643532](https://codeforces.com/contest/550/submission/197643532) | Python 3 | WRONG_ANSWER | WA | WA | 0006 | True | WA@0006 | - | True | wrong-answer: Uses abs(last-first) of each combination in input order as the spread, instead of max-min; with unsorted input, subsets whose extremes are interior elements are misjudged. Witness (valid LF package test 0009): input '4 10 20 1\n4 6 4 6\n', reference '9', source prints '7'; wrong on 84 tests after case-insensitive YES/NO and numeric normalisation. |
| [208069928](https://codeforces.com/contest/550/submission/208069928) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | - | True | wrong-answer: Enumerates ordered n-tuples with repetition instead of subsets, and tests l < sum < r and spread > x with strict inequalities instead of the inclusive bounds. Witness (valid LF package test 0001): input '3 5 6 1\n1 2 3\n', reference '2', source prints '0'; wrong on 44 tests after case-insensitive YES/NO and numeric normalisation. |
| [208074946](https://codeforces.com/contest/550/submission/208074946) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0002 | - | True | wrong-answer: Decrements l and r by 1, as if they were indices, so it accepts sums in [l-1, r-1] instead of [l, r]. Witness (valid LF package test 0035): input '2 1 11 1\n1 10\n', reference '1', source prints '0'; wrong on 53 tests after case-insensitive YES/NO and numeric normalisation. |

### 604B: VALIDATED

- packageHash `20d54dcbd8511ed21f66b94fea29ce775fbc35870491cfa672abc401085b0a10`
- evidenceHash `65d9bdec22c8e5471e7f22779367de67a42aa71e3c7ac086e4ba71cb141baef5`
- auditHash `7fe013e22b1d2e1ba9ce55f3aeeb9a7046329607a2508907a63a623237c272be`
- archive SHA256 `n/a (whole-pool archive 0637f17856db18a669f39640d39c8d2ffbd80b9c1866d30de8ded075f06e8ab9; no per-ID archive)`
- contract gate: {'auditHash': '7fe013e22b1d2e1ba9ce55f3aeeb9a7046329607a2508907a63a623237c272be', 'emptyApprovalRejected': True, 'passed': True}
- CRLF-input tests: 26; independent reference: tests=187, invalid=0, mismatches=0
- issues: none
- max-size coverage: {'bound': 100000, 'maxSizeMetric': 100000, 'nAtMax': 2, 'ratio': 1.0, 'test': '0038'}

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 14594310 | L19: `print(min(max(packed), max(packed2)))` | 0088 | `5 3\n1 12 14 16 18\n` | `26` | `28\n` | `9961d158a7e0e2f9` |
| 14604370 | L10: `if (i > 0) and (b[i] + b[i - 1] <= m):` | 0024 | `1 1\n1\n` | `1` | `2\n` | `53c234e5e8472b6a` |
| 14604632 | L9: `p2 = 0` | 0024 | `1 1\n1\n` | `1` | `2\n` | `53c234e5e8472b6a` |
| 14606425 | L11: `siz = max(s[i]+s[i+1], siz)` | 0026 | `4 2\n1 2 8 9\n` | `10` | `9\n` | `2e6d31a5983a9125` |
| 14610976 | L11: `if t%2==0:` | 0088 | `5 3\n1 12 14 16 18\n` | `26` | `30\n` | `f4ccd05b3271c386` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [14586562](https://codeforces.com/contest/604/submission/14586562) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [14587068](https://codeforces.com/contest/604/submission/14587068) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [14587089](https://codeforces.com/contest/604/submission/14587089) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [14587165](https://codeforces.com/contest/604/submission/14587165) | GNU C++11 | OK | AC | AC | None | True | AC@None | - | True |  |
| [14587242](https://codeforces.com/contest/604/submission/14587242) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [14594310](https://codeforces.com/contest/604/submission/14594310) | Python 3 | WRONG_ANSWER | WA | WA | 0013 | True | WA@0013 | - | True | wrong-answer: Takes the better of just two fixed pairings: consecutive smallest pairs, or largest with smallest from both ends over all bells. The optimum pairs s_i with s_{2(n-k)+1-i} among the 2(n-k) smallest bells, which is neither. Witness (valid LF package test 0088): input '5 3\n1 12 14 16 18\n', reference '26', source prints '28'; wrong on 16 tests after case-insensitive YES/NO and numeric normalisation. |
| [14604370](https://codeforces.com/contest/604/submission/14604370) | Python 3 | WRONG_ANSWER | WA | WA | 0009 | True | WA@0009 | - | True | wrong-answer: Its binary-search feasibility check pairs each bell with its adjacent smaller neighbour b[i-1] instead of with the smallest unpaired bell, so it overcounts boxes and the answer is too large. The search also keeps l=1 exclusive (while l != r-1, print r), so an answer of 1 (n=1, s=[1]) is unreachable and it prints 2. Witness (valid LF package test 0024): input '1 1\n1\n', reference '1', source prints '2'; wrong on 54 tests after case-insensitive YES/NO and numeric normalisation. |
| [14604632](https://codeforces.com/contest/604/submission/14604632) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | - | True | wrong-answer: Its two-pointer feasibility check starts with p2=0 instead of n-1, so it only ever examines b[0] and accepts every m >= max(s); pair sums are ignored (recorded test 0001: 2 1 / 2 5 prints 5, but 2+5 must share the box, so the answer is 7). The search also keeps l=1 exclusive, so an answer of 1 is unreachable and it prints 2. Witness (valid LF package test 0024): input '1 1\n1\n', reference '1', source prints '2'; wrong on 87 tests after case-insensitive YES/NO and numeric normalisation. |
| [14606425](https://codeforces.com/contest/604/submission/14606425) | Python 3 | WRONG_ANSWER | WA | WA | 0009 | True | WA@0009 | - | True | wrong-answer: Pairs adjacent smallest bells s[i]+s[i+1] instead of pairing smallest with largest among the bells that must share a box. Witness (valid LF package test 0026): input '4 2\n1 2 8 9\n', reference '10', source prints '9'; wrong on 39 tests after case-insensitive YES/NO and numeric normalisation. |
| [14610976](https://codeforces.com/contest/604/submission/14610976) | Python 3 | WRONG_ANSWER | WA | WA | 0009 | True | WA@0009 | - | True | wrong-answer: A closed-form guess that looks only at the single pair sum around index t=n-k plus the singles, ignoring the other required pairs s_i+s_{2t-1-i}. Witness (valid LF package test 0088): input '5 3\n1 12 14 16 18\n', reference '26', source prints '30'; wrong on 28 tests after case-insensitive YES/NO and numeric normalisation. |

### 710B: VALIDATED

- packageHash `885556d2abbb83ca4376dd303b81f4695034c383643c0cf11dbae934135c6d31`
- evidenceHash `10c50b3c6a6424cc69dc9b0217f2b02912d24142ffc0a77f49e54b3f19165053`
- auditHash `2daf2cccdf0952fc30886b4d44ad8e790fcf49b992a84b083e4dfb73c0e576da`
- archive SHA256 `n/a (whole-pool archive 0637f17856db18a669f39640d39c8d2ffbd80b9c1866d30de8ded075f06e8ab9; no per-ID archive)`
- contract gate: {'auditHash': '2daf2cccdf0952fc30886b4d44ad8e790fcf49b992a84b083e4dfb73c0e576da', 'emptyApprovalRejected': True, 'passed': True}
- CRLF-input tests: 23; independent reference: tests=183, invalid=0, mismatches=0
- issues: none
- max-size coverage: {'bound': 300000, 'maxSizeMetric': 300000, 'nAtMax': 3, 'ratio': 1.0, 'test': '0038'}

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 20077159 | L3: `average = sum(lst) / n` | 0115 | `4\n0 5 2 -1\n` | `0` | `2\n` | `53c234e5e8472b6a` |
| 20077452 | L7: `sorted(a,key=int)` | 0065 | `2\n0 3\n` | `0` | `1\n` | `4355a46b19d348dc` |
| 20080460 | L4: `print (a[n // 2])` | 0013 | `2\n1 2\n` | `1` | `2\n` | `53c234e5e8472b6a` |
| 20082668 | L8: `print(x[n//2+1])` | 0065 | `2\n0 3\n` | `0` | `1\n` | `4355a46b19d348dc` |
| 20082729 | L10: `print(sum(x)//len(x))` | 0065 | `2\n0 3\n` | `0` | `1\n` | `4355a46b19d348dc` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [20047586](https://codeforces.com/contest/710/submission/20047586) | GNU C++11 | OK | AC | AC | None | True | AC@None | - | True |  |
| [20047656](https://codeforces.com/contest/710/submission/20047656) | GNU C++11 | OK | AC | AC | None | True | AC@None | - | True |  |
| [20047671](https://codeforces.com/contest/710/submission/20047671) | GNU C++11 | OK | AC | AC | None | True | AC@None | - | True |  |
| [20047719](https://codeforces.com/contest/710/submission/20047719) | GNU C++11 | OK | AC | AC | None | True | AC@None | - | True |  |
| [20047741](https://codeforces.com/contest/710/submission/20047741) | GNU C++11 | OK | AC | AC | None | True | AC@None | - | True |  |
| [20077159](https://codeforces.com/contest/710/submission/20077159) | Python 3 | WRONG_ANSWER | WA | WA | 0003 | True | WA@0003 | - | True | wrong-answer: Picks the input point nearest the arithmetic mean; the sum of absolute distances is minimised at the (left) median, not near the mean. Witness (valid LF package test 0115): input '4\n0 5 2 -1\n', reference '0', source prints '2'; wrong on 29 tests after case-insensitive YES/NO and numeric normalisation. |
| [20077452](https://codeforces.com/contest/710/submission/20077452) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | - | True | wrong-answer: Ternary search on the cost function: when s1==s2 on a flat minimum it shrinks both ends, so it can skip the leftmost optimum (e.g. 0 3: every point in [0,3] costs 3, the leftmost is 0, it prints 1). Also sorted(a,key=int) discards its result, so a[0] and a[n-1] are not the min and max; on unsorted input the bounds can be empty, leaving the sentinel -1. Witness (valid LF package test 0065): input '2\n0 3\n', reference '0', source prints '1'; wrong on 99 tests after case-insensitive YES/NO and numeric normalisation. |
| [20080460](https://codeforces.com/contest/710/submission/20080460) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | - | True | wrong-answer: Prints a[n//2], the right median, for even n; the statement requires the leftmost optimal point, a[(n-1)//2]. Witness (valid LF package test 0013): input '2\n1 2\n', reference '1', source prints '2'; wrong on 82 tests after case-insensitive YES/NO and numeric normalisation. |
| [20082668](https://codeforces.com/contest/710/submission/20082668) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0002 | - | True | wrong-answer: For odd n prints x[n//2+1], one position right of the median. For even n prints the floored midpoint, which is not the leftmost optimum. Witness (valid LF package test 0065): input '2\n0 3\n', reference '0', source prints '1'; wrong on 112 tests after case-insensitive YES/NO and numeric normalisation. |
| [20082729](https://codeforces.com/contest/710/submission/20082729) | Python 3 | WRONG_ANSWER | WA | WA | 0003 | True | WA@0003 | - | True | wrong-answer: For even n prints the floored arithmetic mean sum(x)//n instead of the left median. Witness (valid LF package test 0065): input '2\n0 3\n', reference '0', source prints '1'; wrong on 67 tests after case-insensitive YES/NO and numeric normalisation. |

### 757B: VALIDATED

- packageHash `50bc9e72e8e5365f306308610c57aef8de4b721a61e5cfaa3cbc554cc27596ce`
- evidenceHash `277f55892a5d3128bc97d41042697bf6c974d73d2aa00cd2f76632b8569f19ec`
- auditHash `baa6d831c51a75d11512df049c89e2d03a7dd08fa7da45bd335ef0a552b1160a`
- archive SHA256 `n/a (whole-pool archive 0637f17856db18a669f39640d39c8d2ffbd80b9c1866d30de8ded075f06e8ab9; no per-ID archive)`
- contract gate: {'auditHash': 'baa6d831c51a75d11512df049c89e2d03a7dd08fa7da45bd335ef0a552b1160a', 'emptyApprovalRejected': True, 'passed': True}
- CRLF-input tests: 79; independent reference: tests=240, invalid=0, mismatches=0
- issues: none
- max-size coverage: {'bound': 100000, 'maxSizeMetric': 100000, 'nAtMax': 9, 'ratio': 1.0, 'test': '0093'}

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 23771618 | L5: `for num in range(2, math.floor(math.sqrt(10 ** 5 + 1)) + 1):` | 0026 | `2\n541 541\n` | `2` | `1\n` | `4355a46b19d348dc` |
| 23772167 | L24: `if p > M/2 :` | 0050 | `2\n2 2\n` | `2` | `1\n` | `4355a46b19d348dc` |
| 23772314 | L14: `if strengths[j][0] % strengths[i][0] == 0:` | 0054 | `2\n6 9\n` | `2` | `1\n` | `4355a46b19d348dc` |
| 23772496 | L35: `miniLens=[l for l in nums if nums[l] == minLen]` | 0027 | `2\n1 1\n` | `1` | `2\n` | `53c234e5e8472b6a` |
| 23772648 | L18: `divisors += [i] * a` | 0022 | `2\n3 6\n` | `2` | `1\n` | `4355a46b19d348dc` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [23739860](https://codeforces.com/contest/757/submission/23739860) | C++14 (GCC 6-32) | OK | AC | AC | None | True | AC@None | - | True |  |
| [23740025](https://codeforces.com/contest/757/submission/23740025) | GNU C++11 | OK | AC | AC | None | True | AC@None | - | True |  |
| [23740284](https://codeforces.com/contest/757/submission/23740284) | GNU C++11 | OK | AC | AC | None | True | AC@None | - | True |  |
| [23740360](https://codeforces.com/contest/757/submission/23740360) | C++14 (GCC 6-32) | OK | AC | AC | None | True | AC@None | - | True |  |
| [23740393](https://codeforces.com/contest/757/submission/23740393) | GNU C++11 | OK | AC | AC | None | True | AC@None | - | True |  |
| [23771618](https://codeforces.com/contest/757/submission/23771618) | Python 3 | WRONG_ANSWER | WA | WA | 0018 | True | WA@0018 | - | True | wrong-answer: Only tries primes up to floor(sqrt(100001)) = 316, so common prime factors above 316 (e.g. many copies of a large prime) are never counted. Witness (valid LF package test 0026): input '2\n541 541\n', reference '2', source prints '1'; wrong on 24 tests after case-insensitive YES/NO and numeric normalisation. |
| [23772167](https://codeforces.com/contest/757/submission/23772167) | Python 3 | TIME_LIMIT_EXCEEDED | WA | WA | 0018 | True | WA@0018 | - | True | wrong-answer: Stops at p > M/2, where M = max strength, so a prime equal to a strength (e.g. many copies of a large prime) is never tried. Codeforces judged it TLE; in the sandbox the first failure is a WA within the time limit. Witness (valid LF package test 0050): input '2\n2 2\n', reference '2', source prints '1'; wrong on 18 tests after case-insensitive YES/NO and numeric normalisation. |
| [23772314](https://codeforces.com/contest/757/submission/23772314) | Python 3 | WRONG_ANSWER | WA | WA | 0003 | True | WA@0003 | - | True | wrong-answer: Only tries divisors that are themselves input strengths (and marks multiples as used), so a common divisor absent from the input is never found; e.g. 4 and 6 share 2. Witness (valid LF package test 0054): input '2\n6 9\n', reference '2', source prints '1'; wrong on 91 tests after case-insensitive YES/NO and numeric normalisation. |
| [23772496](https://codeforces.com/contest/757/submission/23772496) | Python 3 | TIME_LIMIT_EXCEEDED | WA | WA | 0013 | True | WA@0013 | - | True | wrong-answer: Heuristic: keeps only values with the minimum pairwise-coprime score and tries only their factors, which can miss the optimal divisor. factors(1) returns [1], so divisor 1 is counted as a common divisor and two strength-1 Pokemon give 2 instead of 1. Codeforces judged it TLE; in the sandbox the first failure is a WA within the time limit. Witness (valid LF package test 0027): input '2\n1 1\n', reference '1', source prints '2'; wrong on 18 tests after case-insensitive YES/NO and numeric normalisation. |
| [23772648](https://codeforces.com/contest/757/submission/23772648) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | - | True | wrong-answer: Appends each strength divisors into the same list as the raw strengths and counts multiplicities there, so a raw strength equal to a divisor is double-counted. Its divisor generation also skips the strength itself unless duplicated. Witness (valid LF package test 0022): input '2\n3 6\n', reference '2', source prints '1'; wrong on 89 tests after case-insensitive YES/NO and numeric normalisation. |

### 803A: VALIDATED

- packageHash `407b219f5fc083f007e53e3412f7d6c7669c3c9402725a45f3c9304002ebc57c`
- evidenceHash `55da5cac98ad746c836ecbd37d57c4a69eda3ae0f79bcc51a809d1f410e6a39d`
- auditHash `3d2bf2b20f0e982412220ca5833a1f7a4b1efa402c0bd0f75cdd3629c6554425`
- archive SHA256 `n/a (whole-pool archive 0637f17856db18a669f39640d39c8d2ffbd80b9c1866d30de8ded075f06e8ab9; no per-ID archive)`
- contract gate: {'auditHash': '3d2bf2b20f0e982412220ca5833a1f7a4b1efa402c0bd0f75cdd3629c6554425', 'emptyApprovalRejected': True, 'passed': True}
- CRLF-input tests: 168; independent reference: tests=321, invalid=0, mismatches=0
- issues: none
- max-size coverage: {'bound': 100, 'maxSizeMetric': 100, 'nAtMax': 18, 'ratio': 1.0, 'test': '0299'}

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 26722359 | L15: `mat[i][i] = 1`; L9: `if (k - n) % 2:` | 0016 | `3 5\n` | `1 1 1\n1 0 0\n1 0 0` | `1 1 0\n1 1 0\n0 0 1\n` | `6dbdc037988273a8` |
| 26722992 | L5: `for j in range(n):`; L8: `if(k>n**2)or (n%2!=k%2 and k>n*2):` | 0085 | `3 7\n` | `1 1 1\n1 1 0\n1 0 1` | `1 1 1\n1 0 0\n1 0 0\n` | `be6d6ef073add63e` |
| 26723404 | L8: `a[j][j]=1` | 0016 | `3 5\n` | `1 1 1\n1 0 0\n1 0 0` | `1 1 0 \n1 1 0 \n0 0 1 \n` | `148a471e4be6e494` |
| 26723568 | L3: `if k > n :` | 0017 | `3 3\n` | `1 1 0\n1 0 0\n0 0 0` | `1 0 0\n0 1 0\n0 0 1\n` | `bf284252c00be268` |
| 26723666 | L15: `a[i][i]=1`; L8: `if b%2:` | 0016 | `3 5\n` | `1 1 1\n1 0 0\n1 0 0` | `1 1 0\n1 1 0\n0 0 1\n` | `6dbdc037988273a8` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [26721801](https://codeforces.com/contest/803/submission/26721801) | GNU C++11 | OK | AC | AC | None | True | AC@None | - | True |  |
| [26721819](https://codeforces.com/contest/803/submission/26721819) | GNU C++11 | OK | AC | AC | None | True | AC@None | - | True |  |
| [26721824](https://codeforces.com/contest/803/submission/26721824) | GNU C++11 | OK | AC | AC | None | True | AC@None | - | True |  |
| [26721829](https://codeforces.com/contest/803/submission/26721829) | C++14 (GCC 6-32) | OK | AC | AC | None | True | AC@None | - | True |  |
| [26721831](https://codeforces.com/contest/803/submission/26721831) | GNU C++11 | OK | AC | AC | None | True | AC@None | - | True |  |
| [26722359](https://codeforces.com/contest/803/submission/26722359) | Python 3 | WRONG_ANSWER | WA | WA | 0008 | True | WA@0008 | - | True | wrong-answer: For k > n it fills the whole diagonal first, then off-diagonal pairs. That matrix is valid and symmetric but not lexicographically maximal; the greedy must fill row by row. It also prints -1 whenever (k-n) is odd, although an answer exists. Witness (valid LF package test 0016): input '3 5\n', reference '1 1 1\n1 0 0\n1 0 0', source prints '1 1 0\n1 1 0\n0 0 1'; wrong on 106 tests after case-insensitive YES/NO and numeric normalisation. |
| [26722992](https://codeforces.com/contest/803/submission/26722992) | Python 3 | WRONG_ANSWER | WA | WA | 0006 | True | WA@0006 | - | True | wrong-answer: The row-major loop also visits cells below the diagonal that symmetry has already set and spends 2 more ones on them, so the matrix is wrong. Its -1 parity condition is also wrong. Witness (valid LF package test 0085): input '3 7\n', reference '1 1 1\n1 1 0\n1 0 1', source prints '1 1 1\n1 0 0\n1 0 0'; wrong on 79 tests after case-insensitive YES/NO and numeric normalisation. |
| [26723404](https://codeforces.com/contest/803/submission/26723404) | Python 3 | WRONG_ANSWER | WA | WA | 0008 | True | WA@0008 | - | True | wrong-answer: Places all diagonal ones first, then off-diagonal pairs; not the lexicographically maximal fill. Witness (valid LF package test 0016): input '3 5\n', reference '1 1 1\n1 0 0\n1 0 0', source prints '1 1 0 \n1 1 0 \n0 0 1'; wrong on 106 tests after case-insensitive YES/NO and numeric normalisation. |
| [26723568](https://codeforces.com/contest/803/submission/26723568) | Python 3 | WRONG_ANSWER | WA | WA | 0006 | True | WA@0006 | - | True | wrong-answer: Prints -1 whenever k > n and only ever places diagonal ones, ignoring symmetric off-diagonal pairs. Witness (valid LF package test 0017): input '3 3\n', reference '1 1 0\n1 0 0\n0 0 0', source prints '1 0 0\n0 1 0\n0 0 1'; wrong on 119 tests after case-insensitive YES/NO and numeric normalisation. |
| [26723666](https://codeforces.com/contest/803/submission/26723666) | Python 3 | WRONG_ANSWER | WA | WA | 0008 | True | WA@0008 | - | True | wrong-answer: Fills the diagonal first, and prints -1 when (k-n) is odd; not the lexicographically maximal row-by-row fill. Witness (valid LF package test 0016): input '3 5\n', reference '1 1 1\n1 0 0\n1 0 0', source prints '1 1 0\n1 1 0\n0 0 1'; wrong on 106 tests after case-insensitive YES/NO and numeric normalisation. |

### 911C: VALIDATED

- packageHash `6b2256cdf8ed4d57e438d42cd28a90157bb7d52da95682cfd74d56a5b7eb12af`
- evidenceHash `af72dcf53cfb780782b952659b4c241aad345a682546d90c840371f59cce0db9`
- auditHash `0dfb44b591d1831578fe42894c5409865c52722c14498bb9a19ba1bd54417a14`
- archive SHA256 `n/a (whole-pool archive 0637f17856db18a669f39640d39c8d2ffbd80b9c1866d30de8ded075f06e8ab9; no per-ID archive)`
- contract gate: {'auditHash': '0dfb44b591d1831578fe42894c5409865c52722c14498bb9a19ba1bd54417a14', 'emptyApprovalRejected': True, 'passed': True}
- CRLF-input tests: 67; independent reference: tests=219, invalid=0, mismatches=0
- issues: none
- max-size coverage: {'bound': 1500, 'maxSizeMetric': 1500, 'nAtMax': 5, 'ratio': 1.0, 'test': '0073'}

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 33803030 | L5: `res,res1,res2 = [i%4],[(1+i)%4],[(2+i)%4]` | 0001 | `2 2 3\n` | `YES` | `NO\n` | `cfe72034a9f298fb` |
| 33805309 | L2: `if a == 1 or a == b == 2 or a == b == c == 3:` | 0006 | `4 2 4\n` | `YES` | `NO\n` | `cfe72034a9f298fb` |
| 33805310 | L1: `a=[0]*10` | 0010 | `4 4 2\n` | `YES` | `NO\n` | `cfe72034a9f298fb` |
| 33808809 | L5: `elif [l[0],l[1]] == [2,2] or [l[1],l[2]] == [2,2] or l == [3,3,3]:` | 0006 | `4 2 4\n` | `YES` | `NO\n` | `cfe72034a9f298fb` |
| 33809552 | L19: `if(Min(k1,k2,k3)>=4){cout<<"NO";}` | 0006 | `4 2 4\n` | `YES` | `NO` | `23794d91c53ae875` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [33715178](https://codeforces.com/contest/911/submission/33715178) | GNU C++11 | OK | AC | AC | None | True | AC@None | - | True |  |
| [33716295](https://codeforces.com/contest/911/submission/33716295) | C++14 (GCC 6-32) | OK | AC | AC | None | True | AC@None | - | True |  |
| [33716462](https://codeforces.com/contest/911/submission/33716462) | C++14 (GCC 6-32) | OK | AC | AC | None | True | AC@None | - | True |  |
| [33716746](https://codeforces.com/contest/911/submission/33716746) | GNU C++11 | OK | AC | AC | None | True | AC@None | - | True |  |
| [33716749](https://codeforces.com/contest/911/submission/33716749) | GNU C++11 | OK | AC | AC | None | True | AC@None | - | True |  |
| [33803030](https://codeforces.com/contest/911/submission/33803030) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | - | True | wrong-answer: Simulates only the first few lit seconds of one fixed offset assignment (i=1, then break), instead of deciding coverage over all offsets; misjudges many triples. Witness (valid LF package test 0001): input '2 2 3\n', reference 'YES', source prints 'NO'; wrong on 85 tests after case-insensitive YES/NO and numeric normalisation. |
| [33805309](https://codeforces.com/contest/911/submission/33805309) | Python 3 | WRONG_ANSWER | WA | WA | 0006 | True | WA@0006 | - | True | wrong-answer: Accepts only a==1, two 2s, or three 3s; it misses the (2,4,4) case, which is YES. Witness (valid LF package test 0006): input '4 2 4\n', reference 'YES', source prints 'NO'; wrong on 5 tests after case-insensitive YES/NO and numeric normalisation. |
| [33805310](https://codeforces.com/contest/911/submission/33805310) | Python 3 | WRONG_ANSWER | WA | WA | 0010 | True | WA@0010 | - | True | wrong-answer: Fixes the offsets to 0, 1, 2 in input order and checks only seconds 0..9; it misses (2,4,4) in some orders, and any order-dependent cover. Witness (valid LF package test 0010): input '4 4 2\n', reference 'YES', source prints 'NO'; wrong on 8 tests after case-insensitive YES/NO and numeric normalisation. |
| [33808809](https://codeforces.com/contest/911/submission/33808809) | Python 3 | WRONG_ANSWER | WA | WA | 0006 | True | WA@0006 | - | True | wrong-answer: Same case list as 33805309: misses (2,4,4), which is YES. Witness (valid LF package test 0006): input '4 2 4\n', reference 'YES', source prints 'NO'; wrong on 5 tests after case-insensitive YES/NO and numeric normalisation. |
| [33809552](https://codeforces.com/contest/911/submission/33809552) | C++14 (GCC 6-32) | WRONG_ANSWER | WA | WA | 0006 | True | WA@0006 | - | True | wrong-answer: Prints NO whenever min(k) >= 4, then accepts only 1, two 2s, or three 3s; misses (2,4,4), which is YES. Witness (valid LF package test 0006): input '4 2 4\n', reference 'YES', source prints 'NO'; wrong on 5 tests after case-insensitive YES/NO and numeric normalisation. |

### 920C: REJECTED

- packageHash `0673159b02b586426ded6bdd5903978d9c904f3fc71f024e238c09479ce7e562`
- evidenceHash `0031e872dae61fcbb1e96ef6fa308cccc782a2d91dd9c9a32a753a15c2842726`
- auditHash `ce619d88c97574a5f0a814f3869709d3df06984bd78b84fbebf81cbb7eb593ab`
- archive SHA256 `n/a (whole-pool archive 0637f17856db18a669f39640d39c8d2ffbd80b9c1866d30de8ded075f06e8ab9; no per-ID archive)`
- contract gate: None
- CRLF-input tests: 120; independent reference: tests=282, invalid=0, mismatches=0
- issues: accepted contradiction: CF-OK source(s) 34864682(RE@0001), 34855332(RE@0001), 34849132(RE@0001), 34856737(RE@0001), 34852086(RE@0001) fail the package; cause: CRLF bytes reach Python input(); passes on LF-normalized tests
- max-size coverage: {'bound': 200000, 'maxSizeMetric': 200000, 'nAtMax': 14, 'ratio': 1.0, 'test': '0136'}
- CF-OK sources failing: 34864682 Python 3 RE@0001, 34855332 Python 3 RE@0001, 34849132 Python 3 RE@0001, 34855893 Python 3 TLE@0001, 34856737 Python 3 RE@0001, 34852086 Python 3 RE@0001

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 34842556 | L58: `sort(arr+i+1, arr+j+1);` | 0072 | `2\n2 1\n1\n` | `YES` | `NO` | `23794d91c53ae875` |
| 34842779 | L35: `if(s[i] == '0'){` | 0072 | `2\n2 1\n1\n` | `YES` | `NO\n` | `cfe72034a9f298fb` |
| 34843250 | L61: `sort(a+l, a+r);` | 0072 | `2\n2 1\n1\n` | `YES` | `No\n` | `31375587f8bedb1f` |
| 34843309 | L85: `if (a[i].S != i && s[i - 1] == '0') {` | 0072 | `2\n2 1\n1\n` | `YES` | `NO` | `23794d91c53ae875` |
| 34843337 | L21: `if(a[i]<=b[i])` | 0011 | `3\n3 1 2\n10\n` | `NO` | `YES` | `f9171164593756e5` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [34842624](https://codeforces.com/contest/920/submission/34842624) | C++14 (GCC 6-32) | OK | AC | AC | None | True | AC@None | - | True |  |
| [34842660](https://codeforces.com/contest/920/submission/34842660) | C++14 (GCC 6-32) | OK | AC | AC | None | True | AC@None | - | True |  |
| [34842798](https://codeforces.com/contest/920/submission/34842798) | C++14 (GCC 6-32) | OK | AC | AC | None | True | AC@None | - | True |  |
| [34842822](https://codeforces.com/contest/920/submission/34842822) | C++14 (GCC 6-32) | OK | AC | AC | None | True | AC@None | - | True |  |
| [34842954](https://codeforces.com/contest/920/submission/34842954) | C++14 (GCC 6-32) | OK | AC | AC | None | True | AC@None | - | True |  |
| [34842556](https://codeforces.com/contest/920/submission/34842556) | C++14 (GCC 6-32) | WRONG_ANSWER | WA | WA | 0072 | True | WA@0072 | - | True | wrong-answer: For a run of 1s starting at swap i it sorts arr[i+1..j], leaving out position i, which belongs to the connected block, so some sortable arrays get NO. Witness (valid LF package test 0072): input '2\n2 1\n1\n', reference 'YES', source prints 'NO'; wrong on 35 tests after case-insensitive YES/NO and numeric normalisation. |
| [34842779](https://codeforces.com/contest/920/submission/34842779) | C++14 (GCC 6-32) | WRONG_ANSWER | WA | WA | 0072 | True | WA@0072 | - | True | wrong-answer: Sorts a block only when it sees s[i]==0; the last block (no trailing 0, because s has length n-1) is never sorted, so some sortable arrays get NO. Witness (valid LF package test 0072): input '2\n2 1\n1\n', reference 'YES', source prints 'NO'; wrong on 39 tests after case-insensitive YES/NO and numeric normalisation. |
| [34843250](https://codeforces.com/contest/920/submission/34843250) | C++14 (GCC 6-32) | TIME_LIMIT_EXCEEDED | WA | WA | 0072 | True | WA@0072 | - | True | wrong-answer: In the last block only sort(a+l, a+r) runs, so the last element of the last block is excluded and some sortable arrays get No. The YES/NO checker accepts either letter case, and db() writes only to stderr. Witness (valid LF package test 0072): input '2\n2 1\n1\n', reference 'YES', source prints 'No'; wrong on 29 tests after case-insensitive YES/NO and numeric normalisation. |
| [34843309](https://codeforces.com/contest/920/submission/34843309) | C++14 (GCC 6-32) | WRONG_ANSWER | WA | WA | 0014 | True | WA@0014 | - | True | wrong-answer: After s = "0" + s it checks, for each value i not at position i, only s[i-1]. For i=1 that is the prepended sentinel "0", so any array where 1 is not first gets NO even when it is sortable. It never checks the swaps between an element's original and target positions. Witness (valid LF package test 0072): input '2\n2 1\n1\n', reference 'YES', source prints 'NO'; wrong on 41 tests after case-insensitive YES/NO and numeric normalisation. |
| [34843337](https://codeforces.com/contest/920/submission/34843337) | C++14 (GCC 6-32) | WRONG_ANSWER | WA | WA | 0003 | True | WA@0003 | - | True | wrong-answer: Requires s[i]==1 only when a[i] > sorted(a)[i]; it compares with the sorted value instead of using the prefix maximum, so an element that must cross a forbidden swap can be missed and some unsortable arrays get YES. Witness (valid LF package test 0011): input '3\n3 1 2\n10\n', reference 'NO', source prints 'YES'; wrong on 69 tests after case-insensitive YES/NO and numeric normalisation. |

### 940B: VALIDATED

- packageHash `4223c503d9e5e793bd6e090f5db88f2e3eb47f40c4e90c39eec542b2e2942c2b`
- evidenceHash `2b82bc62219da219fc7a2a2b70c17e6e8f6e49831e6396630d90f86903c0453d`
- auditHash `19137ee38918662139b777726dea30e50dd81a53fb6ea08baf1ef2d8cba90a5f`
- archive SHA256 `n/a (whole-pool archive 0637f17856db18a669f39640d39c8d2ffbd80b9c1866d30de8ded075f06e8ab9; no per-ID archive)`
- contract gate: {'auditHash': '19137ee38918662139b777726dea30e50dd81a53fb6ea08baf1ef2d8cba90a5f', 'emptyApprovalRejected': True, 'passed': True}
- CRLF-input tests: 58; independent reference: tests=211, invalid=0, mismatches=0
- issues: none
- max-size coverage: {'bound': 2000000000, 'maxSizeMetric': 2000000000, 'nAtMax': 8, 'ratio': 1.0, 'test': '0064'}

Source-level evidence for counted incorrect sources (fault line, smallest valid LF witness, auditor reference answer vs source output, sandbox output hash):

| Submission | Fault line(s) | Witness test | Input (LF) | Reference | Source output | outputHash |
|---|---|---|---|---|---|---|
| 35620420 | L161: `lli ans = (1ll<<60);` | 0044 | `2000000000\n1\n2000000000\n98\n` | `3999999998000000000` | `1152921504606846976\n` | `40e991030d2a07f8` |
| 35621925 | L30: `sol+=b;` | 0031 | `65\n2\n3\n6\n` | `36` | `39` | `0b918943df0962bc` |
| 35623068 | L27: `cnt+=b;` | 0031 | `65\n2\n3\n6\n` | `36` | `39` | `0b918943df0962bc` |
| 35623107 | L49: `ans=ans+b;` | 0031 | `65\n2\n3\n6\n` | `36` | `39\n` | `eedb85ab90d324a5` |
| 35623175 | L19: `const ll INF = 1e18;` | 0044 | `2000000000\n1\n2000000000\n98\n` | `3999999998000000000` | `1000000000000000000` | `4ae38a44d132fb60` |

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [35620738](https://codeforces.com/contest/940/submission/35620738) | C++14 (GCC 6-32) | OK | AC | AC | None | True | AC@None | - | True |  |
| [35620813](https://codeforces.com/contest/940/submission/35620813) | C++17 (GCC 7-32) | OK | AC | AC | None | True | AC@None | - | True |  |
| [35620988](https://codeforces.com/contest/940/submission/35620988) | GNU C++11 | OK | AC | AC | None | True | AC@None | - | True |  |
| [35621042](https://codeforces.com/contest/940/submission/35621042) | C++14 (GCC 6-32) | OK | AC | AC | None | True | AC@None | - | True |  |
| [35621065](https://codeforces.com/contest/940/submission/35621065) | C++14 (GCC 6-32) | OK | AC | AC | None | True | AC@None | - | True |  |
| [35620420](https://codeforces.com/contest/940/submission/35620420) | C++14 (GCC 6-32) | WRONG_ANSWER | WA | WA | 0044 | True | WA@0044 | - | True | wrong-answer: Initial best = 2^60 (about 1.15e18) is below the true k=1 cost (n-1)*A, up to about 3.999999998e18, and k=1 is not special-cased, so it prints 2^60 itself. Witness (valid LF package test 0044): input '2000000000\n1\n2000000000\n98\n', reference '3999999998000000000', source prints '1152921504606846976'; wrong on 2 tests after case-insensitive YES/NO and numeric normalisation. |
| [35621925](https://codeforces.com/contest/940/submission/35621925) | GNU C++11 | WRONG_ANSWER | WA | WA | 0010 | True | WA@0010 | - | True | wrong-answer: Always divides when x is divisible, paying B even when subtracting down to x/k ((x-x/k)*A) is cheaper. It only compares the whole greedy with pure subtraction. Witness (valid LF package test 0031): input '65\n2\n3\n6\n', reference '36', source prints '39'; wrong on 77 tests after case-insensitive YES/NO and numeric normalisation. |
| [35623068](https://codeforces.com/contest/940/submission/35623068) | C++14 (GCC 6-32) | WRONG_ANSWER | WA | WA | 0010 | True | WA@0010 | - | True | wrong-answer: Same always-divide greedy; never compares B with (x-x/k)*A at each step. Witness (valid LF package test 0031): input '65\n2\n3\n6\n', reference '36', source prints '39'; wrong on 77 tests after case-insensitive YES/NO and numeric normalisation. |
| [35623107](https://codeforces.com/contest/940/submission/35623107) | C++14 (GCC 6-32) | WRONG_ANSWER | WA | WA | 0010 | True | WA@0010 | - | True | wrong-answer: Always pays B for every division while x >= k, without the per-step min(B, (x-x/k)*A). Witness (valid LF package test 0031): input '65\n2\n3\n6\n', reference '36', source prints '39'; wrong on 77 tests after case-insensitive YES/NO and numeric normalisation. |
| [35623175](https://codeforces.com/contest/940/submission/35623175) | C++14 (GCC 6-32) | WRONG_ANSWER | WA | WA | 0044 | True | WA@0044 | - | True | wrong-answer: INF=1e18 is below the true k=1 answer (n-1)*A, up to about 3.999999998e18, and k=1 is not special-cased, so it prints 1e18. Witness (valid LF package test 0044): input '2000000000\n1\n2000000000\n98\n', reference '3999999998000000000', source prints '1000000000000000000'; wrong on 2 tests after case-insensitive YES/NO and numeric normalisation. |

