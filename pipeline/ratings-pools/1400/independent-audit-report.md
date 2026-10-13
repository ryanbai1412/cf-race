# Rating 1400: independent audit report

Reviewer: `devin-independent-auditor-session-4faf13bf1be94c698c44ee6503b27b8c` (https://staging.itsdev.in/sessions/4faf13bf1be94c698c44ee6503b27b8c)

**Verified: 2 of 9 candidates** (125A, 197B). The target is 100, so it is **not reached**. The builder supplied only 9 execution-passed packages, not 100.

- Builder branch `devin/1791845646-rated-1400` @ `59928b06f9dcedde4dd7a2b839cc7e429ac9e7e2`
- Bundle SHA256 `ac6e542a17a5f388ca53e5f77154f80f1ed7b0f15426db3cd6d86e91452a3ab4`: verified=True
- Pinned datasets: open-r1/codeforces@fbe3f6e903ee854eec2e69e9d96d0306cde59baf, open-r1/codeforces-submissions@07e7bf31f284b0e90e02dfc7ab675d5821e1c068; 16/16 shard SHA256 and byte sizes re-verified
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
| 233B | **NOT_VALIDATED_HELD** | 198 (48/0/150) | 5/5 | 3/5 | 22/22 | 12/12 | only 3/5 incorrect sources are counted WA algorithmic kills |
| 245E | **REJECTED** | 200 (41 partial/9/150) | 5/5 | 1/5 | 32/32 | 5/20 | accepted contradiction: CF-OK source(s) 29488834(WA@0002), 6912638(WA@0002), 31526728(WA@0001), 3685951(WA@0001), 17802998(WA@0002), 4891069(WA@0002), 4435266(WA@0002), 42447218(WA@0002), 49460007(WA@0001), 69404238(WA@0002), 17833202(WA@0002), 14563275(WA@0002), 10341189(WA@0002), 13907610(WA@0001) fail the package; cause: CRLF bytes reach Python input(); passes on LF-normalized tests; only 1/5 incorrect sources are counted WA algorithmic kills |
| 248B | **REJECTED** | 216 (66/0/150) | 5/5 | 5/5 | 49/49 | 7/20 | accepted contradiction: CF-OK source(s) 31873459(RE@0019), 27547806(RE@0019), 32332414(RE@0019), 4713392(RE@0019), 9705234(RE@0019), 32011925(RE@0019), 11022217(RE@0019), 14779449(RE@0019), 26181773(RE@0019), 7776787(RE@0019), 4786395(RE@0019), 17711024(RE@0019), 13496928(RE@0019) fail the package; cause: Python 3.12 int-str 4300-digit limit (runtime fidelity) |

## What was executed

1. Re-ran all 90 builder-selected sources against every package test in the bounded sandbox. Verdicts, first failed test and every per-test output hash were compared with the builder evidence.
2. Wrote my own statement-derived validator, direct solution and brute force for each problem. Checked every package test and sample for input bounds, exact expected output and output uniqueness (all 9 problems have a unique answer, with no special checker).
3. Matched every official, open-r1 generated and sample pair byte-for-byte against the pinned open-r1/codeforces parquet rows. Matched every external source's SHA256 against the pinned codeforces-submissions rows, and checked the CF rating against the Codeforces API and the dataset.
4. Re-ran each builder generator twice and each independent oracle once in the sandbox. Checked the repeat hashes, the pairs digest, byte equality of all 150 authored pairs, and the oracle's AC/output hashes over the full suite.
5. Generated my own corner/max-size stress tests (seeded, with brute-force cross-checks) and ran all 5 accepted sources plus the builder oracle per problem.
6. Ran every additional supported-language CF WRONG_ANSWER source in the downloaded pinned shards (coverage: a passing one is a gap). Also ran up to 20 additional CF OK sources per problem (fidelity: a failing one is an accepted contradiction).
7. Re-ran all non-TLE selected sources on LF-normalized copies of the tests, to find kills that depend only on CRLF bytes reaching Python input().
8. Ran `pool_contract.verify_evidence` and `publication_gate(require_approval=False)` for every package this audit approved.

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

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|
| [627445](https://codeforces.com/contest/107/submission/627445) | MS C++ | OK | AC | AC | None | True | AC@None | True |  |
| [627449](https://codeforces.com/contest/107/submission/627449) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [627474](https://codeforces.com/contest/107/submission/627474) | MS C++ | OK | AC | AC | None | True | AC@None | True |  |
| [627482](https://codeforces.com/contest/107/submission/627482) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [627502](https://codeforces.com/contest/107/submission/627502) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [5408132](https://codeforces.com/contest/107/submission/5408132) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | True | wrong-answer: Prints tank/tap pairs without the leading count line required by the statement. |
| [9819565](https://codeforces.com/contest/107/submission/9819565) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | False | : Source is the placeholder print("x"); it implements no algorithm, so its WA is not an algorithmic kill. |
| [27308114](https://codeforces.com/contest/107/submission/27308114) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0002 | True | wrong-answer: Merges pipes into union sets but treats a closed cycle as a chain (1->2->3->1) and prints a pair instead of 0. |
| [30302698](https://codeforces.com/contest/107/submission/30302698) | Python 3 | WRONG_ANSWER | WA | WA | 0011 | True | WA@0011 | True | wrong-answer: Treats every in-degree-0 house as a tank, including houses with no outgoing pipe; n=1000,p=0 prints 1000 pairs with diameter inf instead of 0. |
| [37558696](https://codeforces.com/contest/107/submission/37558696) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | True | wrong-answer: Leaves the count line out when answers exist (prints only the pairs). |

### 125A: VALIDATED

- packageHash `590e236e38caee6ab2bd6a116d04ab2b36bb8264505c0e7f9ec6cc1467fcc99f`
- evidenceHash `d2f827d4f7ee1623c8f1975dfb417dffca4bd7af1dd5069201aeda5579424daa`
- auditHash `d815166389593c589a72a6319b006ea6267fdfdfb7ea8fb619f4c37178a127d5`
- archive SHA256 `0cdd9980ca3b6c1c3f3cffec91d83afd2595abeed3a3bc2c7ed87a42b668fb66`
- contract gate: {'auditHash': 'd815166389593c589a72a6319b006ea6267fdfdfb7ea8fb619f4c37178a127d5', 'passed': True}
- CRLF-input tests: 22; independent reference: tests=174, invalid=0, mismatches=0
- issues: none

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|
| [814491](https://codeforces.com/contest/125/submission/814491) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [814497](https://codeforces.com/contest/125/submission/814497) | GNU C++0x | OK | AC | AC | None | True | AC@None | True |  |
| [814500](https://codeforces.com/contest/125/submission/814500) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [814501](https://codeforces.com/contest/125/submission/814501) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [814503](https://codeforces.com/contest/125/submission/814503) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [22026877](https://codeforces.com/contest/125/submission/22026877) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | True | wrong-answer: Rounds up with ceil(n/3); n=1 gives 1 inch but the statement rounds 1 cm to 0 inches. |
| [42101202](https://codeforces.com/contest/125/submission/42101202) | Python 3 | WRONG_ANSWER | WA | WA | 0021 | True | WA@0021 | True | wrong-answer: Converts to feet before rounding inches; n=35 prints 0 12 instead of carrying to 1 0. |
| [42101236](https://codeforces.com/contest/125/submission/42101236) | Python 3 | WRONG_ANSWER | WA | WA | 0003 | True | WA@0003 | True | wrong-answer: Rounds a remainder of 18 cm or more up to a whole foot; n=24 prints 1 0 instead of 0 8. |
| [49637309](https://codeforces.com/contest/125/submission/49637309) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | True | wrong-answer: Prints one float (n//36 + (n%36)/3) instead of the integer pair a b. |
| [49637385](https://codeforces.com/contest/125/submission/49637385) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | True | wrong-answer: Rounds inches with ceil; n=1 prints 0 1 instead of 0 0. |

### 152C: REJECTED

- packageHash `f7bfc82a3b02fe278b6a1da326f74a49196e2fb86391198691a5c87c91fa17df`
- evidenceHash `7d0e6b0a7719a634842723cc43bc15396d4b59a778b592001256880fe953da8b`
- auditHash `7d8f485d9f77b16f27cef88b9c21831957eb02eb4e016b861414a36d607b8401`
- archive SHA256 `48f95e3c42f94c2f413dbd80f4cb31f46e0cda2d6ed4cf46be8950f407f02151`
- contract gate: None
- CRLF-input tests: 16; independent reference: tests=180, invalid=0, mismatches=0
- issues: accepted contradiction: CF-OK source(s) 19459348(RE@0001) fail the package; cause: CRLF bytes reach Python input(); passes on LF-normalized tests
- CF-OK sources failing: 19459348 Python 3 RE@0001, 1206562 GNU C++ CE@None

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|
| [1206062](https://codeforces.com/contest/152/submission/1206062) | MS C++ | OK | AC | AC | None | True | AC@None | True |  |
| [1206180](https://codeforces.com/contest/152/submission/1206180) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [1206181](https://codeforces.com/contest/152/submission/1206181) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [1206348](https://codeforces.com/contest/152/submission/1206348) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [1206349](https://codeforces.com/contest/152/submission/1206349) | MS C++ | OK | AC | AC | None | True | AC@None | True |  |
| [4839442](https://codeforces.com/contest/152/submission/4839442) | Python 3 | WRONG_ANSWER | WA | WA | 0007 | True | WA@0007 | True | wrong-answer: Multiplies the distinct-letter counts per column without taking mod 1e9+7. |
| [15021289](https://codeforces.com/contest/152/submission/15021289) | Python 3 | WRONG_ANSWER | WA | WA | 0008 | True | WA@0008 | True | wrong-answer: Takes the modulo with a float (res % (1e9+7)), which loses precision on large products. |
| [21213094](https://codeforces.com/contest/152/submission/21213094) | Python 3 | WRONG_ANSWER | WA | WA | 0007 | True | WA@0007 | True | wrong-answer: Leaves out the modulo 1e9+7, so it prints the full product. |
| [32826732](https://codeforces.com/contest/152/submission/32826732) | Python 3 | WRONG_ANSWER | WA | WA | 0007 | True | WA@0007 | True | wrong-answer: Leaves out the modulo 1e9+7, so it prints the full product. |
| [54790763](https://codeforces.com/contest/152/submission/54790763) | Python 3 | WRONG_ANSWER | WA | WA | 0007 | True | WA@0007 | True | wrong-answer: Leaves out the modulo 1e9+7, so it prints the full product. |

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

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|
| [1531984](https://codeforces.com/contest/175/submission/1531984) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [1531986](https://codeforces.com/contest/175/submission/1531986) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [1531990](https://codeforces.com/contest/175/submission/1531990) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [1531991](https://codeforces.com/contest/175/submission/1531991) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [1531992](https://codeforces.com/contest/175/submission/1531992) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [14702816](https://codeforces.com/contest/175/submission/14702816) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | True | wrong-answer: Limits split lengths with the wrong window (min(5,n-1)); misses 1000000+1000000+1000000. |
| [14702891](https://codeforces.com/contest/175/submission/14702891) | Python 3 | WRONG_ANSWER | WA | WA | 0016 | True | WA@0016 | True | wrong-answer: Uses break instead of continue on leading-zero and >1e6 parts, so it skips valid later splits. |
| [15770608](https://codeforces.com/contest/175/submission/15770608) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0001 | False | : A debug print(g) echoes the input before the answer, so the WA on 0001 is a formatting artifact, not an algorithmic defect. |
| [42333877](https://codeforces.com/contest/175/submission/42333877) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | True | wrong-answer: Splits the integer from the right and never rejects leading zeros or parts that are empty after integer conversion. |
| [193699107](https://codeforces.com/contest/175/submission/193699107) | Python 3 | WRONG_ANSWER | WA | WA | 0003 | True | WA@0003 | True | wrong-answer: Accepts parts with leading zeros through int() and only special-cases a "000" prefix; 0009 prints 9 instead of -1. |

### 197B: VALIDATED

- packageHash `66cb5419b77fa845e2af4911140ac0e85196e4af7cadf4ec40043273235abe6b`
- evidenceHash `40165fdb27cdac3c23b3b35274566dc6051ca0427c91ad9e8aaa252f8ad5bb1e`
- auditHash `99da7ad0a64f7eeec85975e941ab01edebd4d28eb332f9d2929cba9fc0af0944`
- archive SHA256 `90235a1ed207e07f9e1e7278ab4a8ff4e94e4fe892798e375ad17d6aa2efd570`
- contract gate: {'auditHash': '99da7ad0a64f7eeec85975e941ab01edebd4d28eb332f9d2929cba9fc0af0944', 'passed': True}
- CRLF-input tests: 42; independent reference: tests=206, invalid=0, mismatches=0
- issues: none
- CF-OK sources failing: 1788242 MS C++ CE@None, 1788172 MS C++ CE@None

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|
| [1787958](https://codeforces.com/contest/197/submission/1787958) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [1788088](https://codeforces.com/contest/197/submission/1788088) | MS C++ | OK | AC | AC | None | True | AC@None | True |  |
| [1788195](https://codeforces.com/contest/197/submission/1788195) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [1788224](https://codeforces.com/contest/197/submission/1788224) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [1788278](https://codeforces.com/contest/197/submission/1788278) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [4906508](https://codeforces.com/contest/197/submission/4906508) | Python 3 | WRONG_ANSWER | WA | WA | 0003 | True | WA@0003 | True | wrong-answer: The degree comparison has duplicated branches (n>m twice, m<n is unreachable), so n<m prints a fraction instead of 0/1. |
| [6327041](https://codeforces.com/contest/197/submission/6327041) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | True | wrong-answer: Prints p0/q0 without normalizing the sign or reducing by gcd when p0%q0!=0 (2/4 instead of 1/2). |
| [8471901](https://codeforces.com/contest/197/submission/8471901) | Python 3 | WRONG_ANSWER | WA | WA | 0006 | True | WA@0006 | True | wrong-answer: Prints "0" instead of "0/1" when the denominator degree is larger. |
| [8471960](https://codeforces.com/contest/197/submission/8471960) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0002 | True | wrong-answer: Ignores the leading-coefficient signs when the limit is infinite, so it prints Infinity instead of -Infinity. |
| [11940891](https://codeforces.com/contest/197/submission/11940891) | Python 3 | WRONG_ANSWER | WA | WA | 0005 | True | WA@0005 | True | wrong-answer: Adds a "-" prefix from b*c<0 but keeps the signed values, so 9/-5 prints -9/-5 instead of -9/5. |

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

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|
| [1814636](https://codeforces.com/contest/198/submission/1814636) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [1814717](https://codeforces.com/contest/198/submission/1814717) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [1814790](https://codeforces.com/contest/198/submission/1814790) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [1814858](https://codeforces.com/contest/198/submission/1814858) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [1814977](https://codeforces.com/contest/198/submission/1814977) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [9741783](https://codeforces.com/contest/198/submission/9741783) | Python 3 | WRONG_ANSWER | WA | WA | 0012 | True | WA@0012 | True | wrong-answer: Its DFS caps consecutive downs/ups at k+1 and prunes valid climbs; 5 2/-----/XXXXX prints NO. |
| [9742416](https://codeforces.com/contest/198/submission/9742416) | Python 3 | TIME_LIMIT_EXCEEDED | TLE | TLE | 0023 | True | - | False | complexity: BFS/DFS has no visited set and blows up exponentially (TLE; an individual rerun ran out of memory at 8.3s); not counted, see policy. |
| [23110434](https://codeforces.com/contest/198/submission/23110434) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0002 | True | wrong-answer: Its visited marks ignore water level/time, so it accepts unsafe paths. |
| [31871384](https://codeforces.com/contest/198/submission/31871384) | Python 3 | WRONG_ANSWER | WA | WA | 0004 | True | WA@0004 | True | wrong-answer: Hard-codes a jump of +3 instead of k. |
| [31959794](https://codeforces.com/contest/198/submission/31959794) | Python 3 | TIME_LIMIT_EXCEEDED | TLE | TLE | 0023 | True | - | False | complexity: Aliased visited rows ([[0]*n]*2) and recursive DFS (TLE on 0023, RE on 0024); not counted, see policy. |

### 233B: NOT_VALIDATED_HELD

- packageHash `f396281e73a4bd3a07aa1a7728aa0414d7b03a2b1bee8e9f99570ec0e30ecf71`
- evidenceHash `ec24691b263c4615a545d812809f62dc8cb097d3adaaf3694505330079fa4d58`
- auditHash `851eb5229adf02631076923e50a0f81baa820b8bdf61929b8fc710afe199c285`
- archive SHA256 `17576b354a37c4b0f331f53e779334fff1907d4b9b1f4a53c5e2c43c0da7b2f7`
- contract gate: None
- CRLF-input tests: 48; independent reference: tests=201, invalid=0, mismatches=0
- issues: only 3/5 incorrect sources are counted WA algorithmic kills
- replacement WA candidates (executed here, need builder revalidation and re-audit): 135611678@0006, 211052544@0005, 135960142@0002, 149890923@0046, 161628529@0006, 173405148@0001, 141023743@0046, 229779194@0006

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|
| [2340528](https://codeforces.com/contest/233/submission/2340528) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [2340550](https://codeforces.com/contest/233/submission/2340550) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [2340612](https://codeforces.com/contest/233/submission/2340612) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [2340671](https://codeforces.com/contest/233/submission/2340671) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [2340678](https://codeforces.com/contest/233/submission/2340678) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [126957423](https://codeforces.com/contest/233/submission/126957423) | Python 3 | WRONG_ANSWER | WA | WA | 0003 | True | WA@0003 | True | wrong-answer: Uses a float sqrt discriminant test and never checks the digit sum of the root; n=4 prints 2 instead of -1. |
| [126959060](https://codeforces.com/contest/233/submission/126959060) | Python 3 | WRONG_ANSWER | WA | WA | 0005 | True | WA@0005 | True | wrong-answer: Searches x only up to 9*18 instead of the digit-sum values s; misses x=1e8. |
| [127232883](https://codeforces.com/contest/233/submission/127232883) | Python 3 | TIME_LIMIT_EXCEEDED | TLE | TLE | 0005 | True | - | False | complexity: Linear scan over x up to sqrt(n)=1e9 (TLE, about 20s CPU under a 20x cap); not counted, see policy. |
| [127737961](https://codeforces.com/contest/233/submission/127737961) | Python 3 | WRONG_ANSWER | WA | WA | 0046 | True | WA@0046 | True | wrong-answer: The float-sqrt integrality test in the quadratic solver accepts a non-root near 1e18 (expected -1). |
| [128560902](https://codeforces.com/contest/233/submission/128560902) | Python 3 | TIME_LIMIT_EXCEEDED | TLE | TLE | 0005 | True | - | False | complexity: Linear scan up to sqrt(n) (TLE, about 20s CPU under a 20x cap); not counted, see policy. |

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

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|
| [2591847](https://codeforces.com/contest/245/submission/2591847) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [2592014](https://codeforces.com/contest/245/submission/2592014) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [2592122](https://codeforces.com/contest/245/submission/2592122) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [2593339](https://codeforces.com/contest/245/submission/2593339) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [2594437](https://codeforces.com/contest/245/submission/2594437) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [3685391](https://codeforces.com/contest/245/submission/3685391) | Python 3 | WRONG_ANSWER | WA | WA | 0007 | True | WA@0007 | True | wrong-answer: Prints |final balance| instead of the max prefix minus the min prefix. |
| [3771557](https://codeforces.com/contest/245/submission/3771557) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0015 | False | : Recorded kill is a CRLF artifact: with the test inputs normalized to LF the source gives WA (failed 0015), not WA on 0002; a stray '\r' from input() is scored as data. Original analysis: Prints the max |prefix|, which ignores that people can leave and re-enter (+- patterns). |
| [4890821](https://codeforces.com/contest/245/submission/4890821) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0015 | False | : Recorded kill is a CRLF artifact: with the test inputs normalized to LF the source gives WA (failed 0015), not WA on 0002; a stray '\r' from input() is scored as data. Original analysis: Prints the max |prefix| instead of max prefix - min prefix (with 0 included). |
| [9260456](https://codeforces.com/contest/245/submission/9260456) | Python 3 | WRONG_ANSWER | WA | WA | 0001 | True | WA@0007 | False | : Recorded kill is a CRLF artifact: with the test inputs normalized to LF the source gives WA (failed 0007), not WA on 0001; a stray '\r' from input() is scored as data. Original analysis: Prints |final balance|. |
| [14563248](https://codeforces.com/contest/245/submission/14563248) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0015 | False | : Recorded kill is a CRLF artifact: with the test inputs normalized to LF the source gives WA (failed 0015), not WA on 0002; a stray '\r' from input() is scored as data. Original analysis: Prints the max |prefix|. |

### 248B: REJECTED

- packageHash `90a7bc594438a76b0abbbc45aee0114b49db72cc9506310f5f1f5975751db2e3`
- evidenceHash `728d089f00c9ef1999fee7edbbd431476513162370a1e595ecdb41040fd87c49`
- auditHash `ad5735b4f83f923789ed26c0f3d77ebb40baf223b444f58ba1ce0e589fece55a`
- archive SHA256 `80e2f8f831e3f74fe4ff53bca88fde027e6ae996e21a1a7bb988b24727be7052`
- contract gate: None
- CRLF-input tests: 66; independent reference: tests=218, invalid=0, mismatches=0
- issues: accepted contradiction: CF-OK source(s) 31873459(RE@0019), 27547806(RE@0019), 32332414(RE@0019), 4713392(RE@0019), 9705234(RE@0019), 32011925(RE@0019), 11022217(RE@0019), 14779449(RE@0019), 26181773(RE@0019), 7776787(RE@0019), 4786395(RE@0019), 17711024(RE@0019), 13496928(RE@0019) fail the package; cause: Python 3.12 int-str 4300-digit limit (runtime fidelity)
- CF-OK sources failing: 31873459 Python 3 RE@0019, 27547806 Python 3 RE@0019, 32332414 Python 3 RE@0019, 4713392 Python 3 RE@0019, 9705234 Python 3 RE@0019, 32011925 Python 3 RE@0019, 11022217 Python 3 RE@0019, 14779449 Python 3 RE@0019, 26181773 Python 3 RE@0019, 7776787 Python 3 RE@0019, 4786395 Python 3 RE@0019, 17711024 Python 3 RE@0019, 13496928 Python 3 RE@0019

| Submission | Lang | Expected | Builder | Rerun | Failed test | Hashes match | LF rerun | Counted | Analysis |
|---|---|---|---|---|---|---|---|---|---|
| [2642739](https://codeforces.com/contest/248/submission/2642739) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [2643057](https://codeforces.com/contest/248/submission/2643057) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [2643149](https://codeforces.com/contest/248/submission/2643149) | GNU C++ | OK | AC | AC | None | True | AC@None | True |  |
| [2643164](https://codeforces.com/contest/248/submission/2643164) | MS C++ | OK | AC | AC | None | True | AC@None | True |  |
| [2643191](https://codeforces.com/contest/248/submission/2643191) | MS C++ | OK | AC | AC | None | True | AC@None | True |  |
| [4307483](https://codeforces.com/contest/248/submission/4307483) | Python 3 | WRONG_ANSWER | WA | WA | 0009 | True | WA@0009 | True | wrong-answer: Computes the ceil of a float division 10**(n-1)/210, which loses precision for n=120. |
| [4786571](https://codeforces.com/contest/248/submission/4786571) | Python 3 | WRONG_ANSWER | WA | WA | 0011 | True | WA@0011 | True | wrong-answer: After the decrement, the n>2 guard rejects n=3 (prints -1 instead of 210). |
| [7554568](https://codeforces.com/contest/248/submission/7554568) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0002 | True | wrong-answer: Prints 210 followed by zeros, which is not the minimum (n=5 gives 21000, but 10080 is smaller). |
| [8474692](https://codeforces.com/contest/248/submission/8474692) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0002 | True | wrong-answer: The residue derivation for 10**n mod 210 is wrong, so the n=5 output is not 10080. |
| [9741229](https://codeforces.com/contest/248/submission/9741229) | Python 3 | WRONG_ANSWER | WA | WA | 0002 | True | WA@0002 | True | wrong-answer: Prints 210 followed by zeros, which is not minimal. |

