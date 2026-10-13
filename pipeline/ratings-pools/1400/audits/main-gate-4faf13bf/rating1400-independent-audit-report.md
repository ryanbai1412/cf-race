# Rating 1400: independent audit report

Reviewer: `devin-independent-auditor-session-4faf13bf1be94c698c44ee6503b27b8c` (https://staging.itsdev.in/sessions/4faf13bf1be94c698c44ee6503b27b8c)

**Verified: 13 of 28 candidates** (125A, 197B, 270B, 277A, 279A, 315A, 334B, 358A, 388A, 38C, 41B, 435B, 548B). The target is 100, so it is **not reached**. The builder supplied 28 execution-passed packages (v2 bundle), not 100; the 9 initial archives are byte-identical to v1, and the 19 new ones were audited from scratch.
Builder child audits were read for cross-checking only; none of their approvals are inherited. Disagreements are listed below.

- Builder branch `devin/1791845646-rated-1400` @ `556e9047951a6774775812684c3a5cb516789f3d`
- Bundle SHA256 `05f8c1e2b4e896b45be0eb85cc02cab9e10b0aeac0f48f59164138f274de13a7`: verified=True
- Pinned datasets: open-r1/codeforces@fbe3f6e903ee854eec2e69e9d96d0306cde59baf, open-r1/codeforces-submissions@07e7bf31f284b0e90e02dfc7ab675d5821e1c068; 38/38 shard SHA256 and byte sizes re-verified
- Sandbox: pipeline/pool_sandbox.py: pinned python@sha256:5887f265..., network none, uid 65534, read-only rootfs, cap-drop ALL, no-new-privileges, pids 64, 1 CPU, 1280m mem, no swap; no third-party code was run on the host
- Policy: Per the handoff ('Incorrect timeouts/unsupported languages cannot count as a killed algorithmic wrong solution'), this audit counts only WA kills on a concrete valid test, from sources with a genuine algorithmic defect. TLE/complexity, RE, placeholder and debug-output sources are not counted, even though pool_generation accepts kind=complexity.

## Summary

| Problem | Verdict | Tests (official/open-r1 gen/authored) | Accepted reproduced | Counted WA kills | Extra CF-WA killed | Extra CF-OK passing | Issues |
|---|---|---|---|---|---|---|---|
| 107A | **NOT_VALIDATED_HELD** | 179 (16 partial/13/150) | 5/5 | 4/5 | 15/15 | 11/14 | only 4/5 incorrect sources are counted WA algorithmic kills |
| 125A | **VALIDATED** | 172 (22/0/150) | 5/5 | 5/5 | 33/33 | 20/20 | none |
| 152C | **REJECTED** | 178 (16 partial/12/150) | 5/5 | 5/5 | 37/37 | 18/20 | accepted contradiction: CF-OK source(s) 19459348(RE@0001) fail the package; cause: CRLF bytes reach Python input(); passes on LF-normalized tests |
| 175A | **REJECTED** | 284 (134/0/150) | 5/5 | 4/5 | 36/36 | 5/18 | accepted contradiction: CF-OK source(s) 37495712(RE@0001), 124238640(RE@0001), 27107190(RE@0001), 196162162(RE@0001), 55006515(RE@0001), 35154521(RE@0001), 78795916(RE@0001), 29819107(RE@0001), 44186543(RE@0001), 46821841(RE@0001), 29784607(RE@0001), 34276976(RE@0001) fail the package; cause: CRLF bytes reach Python input(); passes on LF-normalized tests; only 4/5 incorrect sources are counted WA algorithmic kills |
| 197B | **VALIDATED** | 201 (42 partial/9/150) | 5/5 | 5/5 | 49/49 | 16/18 | none |
| 198B | **REJECTED** | 182 (23 partial/9/150) | 5/5 | 3/5 | 7/8 | 6/9 | only 3/5 incorrect sources are counted WA algorithmic kills; coverage gap: CF-WRONG_ANSWER source(s) 11382563 pass the full package |
| 226A | **NOT_VALIDATED_HELD** | 228 (78/0/150) | 5/5 | 3/5 | 4/4 | 13/15 | only 3/5 incorrect sources are counted WA algorithmic kills |
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
| 337B | **NOT_VALIDATED_HELD** | 184 (34/0/150) | 5/5 | 2/5 | 4/4 | 16/18 | only 2/5 incorrect sources are counted WA algorithmic kills |
| 358A | **VALIDATED** | 186 (28 partial/8/150) | 5/5 | 5/5 | 30/30 | 20/20 | none |
| 388A | **VALIDATED** | 186 (36/0/150) | 5/5 | 5/5 | 30/30 | 20/20 | none |
| 38C | **VALIDATED** | 185 (27 partial/8/150) | 5/5 | 5/5 | 16/16 | 18/20 | none |
| 417B | **NOT_VALIDATED_HELD** | 183 (24 partial/9/150) | 5/5 | 4/5 | 21/21 | 18/18 | only 4/5 incorrect sources are counted WA algorithmic kills |
| 41B | **VALIDATED** | 180 (15 partial/15/150) | 5/5 | 5/5 | 12/12 | 19/20 | none |
| 435B | **VALIDATED** | 196 (46/0/150) | 5/5 | 5/5 | 30/30 | 20/20 | none |
| 518B | **REJECTED** | 180 (18 partial/12/150) | 5/5 | 1/5 | 30/30 | 8/20 | accepted contradiction: CF-OK source(s) 9997130(WA@0001), 9998838(RE@0001), 43168918(WA@0001), 50663320(RE@0001), 46821685(WA@0001), 10002420(WA@0001), 9988304(WA@0001), 9994921(RE@0001), 42126459(WA@0001), 20403986(WA@0001), 10000805(WA@0001) fail the package; cause: CRLF bytes reach Python input(); passes on LF-normalized tests; only 1/5 incorrect sources are counted WA algorithmic kills |
| 548B | **VALIDATED** | 162 (10 partial/2/150) | 5/5 | 5/5 | 30/30 | 19/20 | none |

## Disagreements with builder child audits

- 152C: child 126f9ac4 approved; this audit REJECTED (accepted contradiction: CF-OK source(s) 19459348(RE@0001) fail the package; cause: CRLF bytes reach Python input(); passes on LF-normalized tests)
- 197B: child d95ca109 rejected; this audit VALIDATED (all checks passed)
- 198B: child 946996ea approved; this audit REJECTED (only 3/5 incorrect sources are counted WA algorithmic kills; coverage gap: CF-WRONG_ANSWER source(s) 11382563 pass the full package)
- 233B: child d95ca109 approved; this audit NOT_VALIDATED_HELD (only 3/5 incorrect sources are counted WA algorithmic kills)
- 248B: child 946996ea approved; this audit REJECTED (accepted contradiction: CF-OK source(s) 31873459(RE@0019), 27547806(RE@0019), 32332414(RE@0019), 4713392(RE@0019), 9705234(RE@0019), 32011925(RE@0019), 11022217(RE@0019), 14779449(RE@0019), 26181773(RE@0019), 7776787(RE@0019), 4786395(RE@0019), 17711024(RE@0019), 13496928(RE@0019) fail the package; cause: Python 3.11 sandbox int-str 4300-digit limit (harness fidelity))
- 272B: child f009e0db approved; this audit NOT_VALIDATED_HELD (only 4/5 incorrect sources are counted WA algorithmic kills)
- 279B: child 126f9ac4 approved; this audit NOT_VALIDATED_HELD (only 4/5 incorrect sources are counted WA algorithmic kills)
- 289B: child f009e0db approved; this audit NOT_VALIDATED_HELD (only 4/5 incorrect sources are counted WA algorithmic kills)
- 417B: child d95ca109 approved; this audit NOT_VALIDATED_HELD (only 4/5 incorrect sources are counted WA algorithmic kills)

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

## Per-problem detail

### 107A: NOT_VALIDATED_HELD

- packageHash `c82dbd5e3ff41403997cbf9463e9d8d56fbbae614e2aee661b2164d89e3dd997`
- evidenceHash `3c23ce12b7f746ef35979e21c945e7b15d463a4d973c62b80827edf3369317a3`
- auditHash `034133007410eb725d5322ec7605ca7e15ce57453697f93eb0f8a0914ccd2f49`
- archive SHA256 `25eb44ce7b035f092d176d6442af05367816160c76f1be9074a4e1d152084c4a`
- contract gate: None
- CRLF-input tests: 16; independent reference: tests=182, invalid=0, mismatches=0
- issues: only 4/5 incorrect sources are counted WA algorithmic kills
- CF-OK sources failing: 627433 GNU C++ CE@None, 627519 MS C++ CE@None, 627460 GNU C++ CE@None
- replacement WA candidates (executed here, need builder revalidation and re-audit): 90226422@0001, 114310642@0006, 104842606@0001, 195071546@0005, 113620524@0004, 136410791@0001, 73553259@0005, 97366270@0011

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [627445](https://codeforces.com/contest/107/submission/627445) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [627449](https://codeforces.com/contest/107/submission/627449) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [627474](https://codeforces.com/contest/107/submission/627474) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [627482](https://codeforces.com/contest/107/submission/627482) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [627502](https://codeforces.com/contest/107/submission/627502) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [5408132](https://codeforces.com/contest/107/submission/5408132) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | - | True | wrong-answer: Prints tank/tap pairs without the leading count line required by the statement. |
| [9819565](https://codeforces.com/contest/107/submission/9819565) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | - | False | : Source is the placeholder print("x"); it implements no algorithm, so its WA is not an algorithmic kill. |
| [27308114](https://codeforces.com/contest/107/submission/27308114) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0002 | - | True | wrong-answer: Merges pipes into union sets but treats a closed cycle as a chain (1->2->3->1) and prints a pair instead of 0. |
| [30302698](https://codeforces.com/contest/107/submission/30302698) | Python 3 | WRONG_ANSWER | WA | WA | 0011 | True | WA@0011 | - | True | wrong-answer: Treats every in-degree-0 house as a tank, including houses with no outgoing pipe; n=1000,p=0 prints 1000 pairs with diameter inf instead of 0. |
| [37558696](https://codeforces.com/contest/107/submission/37558696) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | - | True | wrong-answer: Leaves the count line out when answers exist (prints only the pairs). |

### 125A: VALIDATED

- packageHash `590e236e38caee6ab2bd6a116d04ab2b36bb8264505c0e7f9ec6cc1467fcc99f`
- evidenceHash `d2f827d4f7ee1623c8f1975dfb417dffca4bd7af1dd5069201aeda5579424daa`
- auditHash `d815166389593c589a72a6319b006ea6267fdfdfb7ea8fb619f4c37178a127d5`
- archive SHA256 `0cdd9980ca3b6c1c3f3cffec91d83afd2595abeed3a3bc2c7ed87a42b668fb66`
- contract gate: {'auditHash': 'd815166389593c589a72a6319b006ea6267fdfdfb7ea8fb619f4c37178a127d5', 'passed': True}
- CRLF-input tests: 22; independent reference: tests=174, invalid=0, mismatches=0
- issues: none

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [814491](https://codeforces.com/contest/125/submission/814491) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [814497](https://codeforces.com/contest/125/submission/814497) | GNU C++0x | OK | AC | AC | None | True | AC@None | - | True |  |
| [814500](https://codeforces.com/contest/125/submission/814500) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [814501](https://codeforces.com/contest/125/submission/814501) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [814503](https://codeforces.com/contest/125/submission/814503) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [22026877](https://codeforces.com/contest/125/submission/22026877) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | - | True | wrong-answer: Rounds up with ceil(n/3); n=1 gives 1 inch but the statement rounds 1 cm to 0 inches. |
| [42101202](https://codeforces.com/contest/125/submission/42101202) | Python 3 | WRONG_ANSWER | WA | WA | 0021 | True | WA@0021 | - | True | wrong-answer: Converts to feet before rounding inches; n=35 prints 0 12 instead of carrying to 1 0. |
| [42101236](https://codeforces.com/contest/125/submission/42101236) | Python 3 | WRONG_ANSWER | WA | WA | 0003 | True | WA@0003 | - | True | wrong-answer: Rounds a remainder of 18 cm or more up to a whole foot; n=24 prints 1 0 instead of 0 8. |
| [49637309](https://codeforces.com/contest/125/submission/49637309) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | - | True | wrong-answer: Prints one float (n//36 + (n%36)/3) instead of the integer pair a b. |
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

### 197B: VALIDATED

- packageHash `66cb5419b77fa845e2af4911140ac0e85196e4af7cadf4ec40043273235abe6b`
- evidenceHash `40165fdb27cdac3c23b3b35274566dc6051ca0427c91ad9e8aaa252f8ad5bb1e`
- auditHash `99da7ad0a64f7eeec85975e941ab01edebd4d28eb332f9d2929cba9fc0af0944`
- archive SHA256 `90235a1ed207e07f9e1e7278ab4a8ff4e94e4fe892798e375ad17d6aa2efd570`
- contract gate: {'auditHash': '99da7ad0a64f7eeec85975e941ab01edebd4d28eb332f9d2929cba9fc0af0944', 'passed': True}
- CRLF-input tests: 42; independent reference: tests=206, invalid=0, mismatches=0
- issues: none
- CF-OK sources failing: 1788242 MS C++ CE@None, 1788172 MS C++ CE@None

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [1787958](https://codeforces.com/contest/197/submission/1787958) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [1788088](https://codeforces.com/contest/197/submission/1788088) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [1788195](https://codeforces.com/contest/197/submission/1788195) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [1788224](https://codeforces.com/contest/197/submission/1788224) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [1788278](https://codeforces.com/contest/197/submission/1788278) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [4906508](https://codeforces.com/contest/197/submission/4906508) | Python 3 | WRONG_ANSWER | WA | WA | 0003 | True | WA@0003 | `1/1\n` | True | wrong-answer: The degree comparison has duplicated branches (n>m twice, m<n is unreachable), so n<m prints a fraction instead of 0/1. |
| [6327041](https://codeforces.com/contest/197/submission/6327041) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `2/4\n` | True | wrong-answer: Prints p0/q0 without normalizing the sign or reducing by gcd when p0%q0!=0 (2/4 instead of 1/2). |
| [8471901](https://codeforces.com/contest/197/submission/8471901) | Python 3 | WRONG_ANSWER | WA | WA | 0006 | True | WA@0006 | `0\n` | True | wrong-answer: Prints "0" instead of "0/1" when the denominator degree is larger. |
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

- packageHash `29fac43be2758dceb85be915c75372450cb67b3457f67a77d9c25c8f159a1104`
- evidenceHash `6b2a0886057a76692286cdd4b8802196e06fc840931050a13f9a135ff41c960c`
- auditHash `53a096c28d798e699dcb1f825c9a7a932d5e37347d93bfbf3b757af1370eae20`
- archive SHA256 `37c7bde5a700f8faaa06c01926bb7a1cb582c49052104fb263ca9c0e70ff0289`
- contract gate: None
- CRLF-input tests: 78; independent reference: tests=230, invalid=0, mismatches=0
- issues: only 3/5 incorrect sources are counted WA algorithmic kills
- max-size coverage: {'bound': 1000000000, 'maxSizeMetric': 1000000000, 'nAtMax': 2, 'ratio': 1.0, 'test': '0081'}
- CF-OK sources failing: 2237352 MS C++ CE@None, 2237332 MS C++ CE@None
- replacement WA candidates (executed here, need builder revalidation and re-audit): 81421605@0004, 63635601@0003, 63642927@0047, 81421455@0001

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [2237340](https://codeforces.com/contest/226/submission/2237340) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2237358](https://codeforces.com/contest/226/submission/2237358) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2237364](https://codeforces.com/contest/226/submission/2237364) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2237370](https://codeforces.com/contest/226/submission/2237370) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [2237372](https://codeforces.com/contest/226/submission/2237372) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [11998618](https://codeforces.com/contest/226/submission/11998618) | Python 3 | TIME_LIMIT_EXCEEDED | TLE | TLE | 0006 | True | - | - | False | : Computes pow(3,n) without a modulus; correct formula 3^n-1 but 3^(1e9) big-int is TLE only. complexity-only (TLE); not counted per handoff policy |
| [21696165](https://codeforces.com/contest/226/submission/21696165) | Python 3 | WRONG_ANSWER | WA | WA | 0047 | True | WA@0047 | `-1\n` | True | wrong-answer: Prints pow(3,n,m)-1 with no final mod; when m divides 3^n (test 0047: m=6561=3^8) it prints -1 instead of m-1. |
| [21696171](https://codeforces.com/contest/226/submission/21696171) | Python 3 | WRONG_ANSWER | WA | WA | 0047 | True | WA@0047 | `-1\n` | True | wrong-answer: Same missing wrap: r<0 check happens before subtracting 1, so r=0 prints -1 instead of m-1 (test 0047). |
| [51590219](https://codeforces.com/contest/226/submission/51590219) | Python 3 | TIME_LIMIT_EXCEEDED | TLE | TLE | 0006 | True | - | - | False | : Computes (3**n-1)%m with a full big integer; correct but TLE for n=1e9. complexity-only (TLE); not counted per handoff policy |
| [55486527](https://codeforces.com/contest/226/submission/55486527) | Python 3 | WRONG_ANSWER | WA | WA | 0047 | True | WA@0047 | `-1\n` | True | wrong-answer: pow(3,n,m)-1 without wrap; prints -1 when 3^n = 0 mod m (test 0047). |

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
- auditHash `a84e98afefee98abc1ff8b6e9eb51fad0a1300f8e7de119d062b96247a055748`
- archive SHA256 `690478a9f71331d4ad2cd325cc588ae1ef743675f092123aecea82b0608588fe`
- contract gate: {'auditHash': 'a84e98afefee98abc1ff8b6e9eb51fad0a1300f8e7de119d062b96247a055748', 'passed': True}
- CRLF-input tests: 32; independent reference: tests=186, invalid=0, mismatches=0
- issues: none
- max-size coverage: {'bound': 100, 'maxSizeMetric': 100, 'nAtMax': 10, 'ratio': 1.0, 'test': '0040'}

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Got on failed test | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|---|
| [3238846](https://codeforces.com/contest/279/submission/3238846) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3238857](https://codeforces.com/contest/279/submission/3238857) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3238923](https://codeforces.com/contest/279/submission/3238923) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3238926](https://codeforces.com/contest/279/submission/3238926) | GNU C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [3238943](https://codeforces.com/contest/279/submission/3238943) | MS C++ | OK | AC | AC | None | True | AC@None | - | True |  |
| [191418646](https://codeforces.com/contest/279/submission/191418646) | Python 3 | WRONG_ANSWER | WA | WA | 0020 | True | WA@0020 | `` | True | wrong-answer: Closed-form turn formula with wrong region boundaries; independently verified wrong on the failed test by spiral simulation. |
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
- auditHash `9650a52cab8ab1ce76b3c03d1c79d1df893f29f1159262d16aa0d2b3871fd82f`
- archive SHA256 `0306402995ac8aa6c697147e23d485c6f5dd0aaabb94adae86b62f12ae361495`
- contract gate: None
- CRLF-input tests: 34; independent reference: tests=186, invalid=0, mismatches=0
- issues: only 2/5 incorrect sources are counted WA algorithmic kills
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
| [199577681](https://codeforces.com/contest/337/submission/199577681) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | `0\n` | True | wrong-answer: Prints 0 instead of the required irreducible fraction 0/1 when a:b == c:d (spec violation in an explicit branch); also float ratio comparisons. |
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

