next6 (606B/659E/704A only; archive c23b7888 verified 3303 members; worker 8fcd006). Do AFTER 209A is reported.
Flags to check: 606B all 5 incorrect first-fail 0001 (all Python) -> suspect CRLF; 659E/55973493 evidence verdict TLE at 0012 -> TLE pointer does not qualify unless math-wrong witness; 704A/20796252 proof drafted in proofs_next6.json.
Tooling to reuse: ~/audit14/me/{launcher14,witness14,judge14,mktuples14,mkfinal14}.py patterns (sources from archive state/<id>/sources/<sid>.json 'code', verify vs parquet shards).
FINDINGS (witness at evidence failedTest, LF):
- 606B: 14748527/14783733/14826919/14914349 are AC on LF 0001 (CRLF artifact; CF passed 2-3); 14767740 prints extra leading '6' line (token-count mismatch, debug/extra output). 0/5 qualify -> blocked, report pointer gaps.
- 659E: 39747922@0006, 49833185@0032, 49886094@0033, 69799534@0002 MATH-WRONG normal exit; 55973493@0012 TLE (rc -24) -> not qualifying, needs math pointer or replacement.
- 704A: all 5 MATH-WRONG at 0003 (incl new 20796252). Candidate to sign if full replay matches.
- All 30 sources byte-identical to parquet shards 25/27 (parquet-check.json).
REPAIR CANDIDATES (witness-full-analysis.json, LF, rc0, no timeout):
- 606B/14748527 -> 0004 (exp ...1 1 1 1 245, act ...0 0 1 1 1 246); 14783733 -> 0004; 14826919 -> 0004; 14914349 -> 0003; 14767740 -> NONE (token-count mismatch on all 187 tests: extra leading line) => replace source.
- 659E/55973493 -> 0032 (4 3 / triangle: exp 1, act 0); first non-AC 0011 is TLE.
NEXT: finish 704A (judge15, mktuples15, mkfinal15 based on 8fcd006 worktree), report 606B/659E gaps; do not sign 606B/659E.
704A: judge 704A all OK except 20796252 perTestEvidenceMatch 175/181 (6 TLE label diffs, hashes equal; investigating). proof-tuples.json has 704A 5/5 qualifying.
704A/20796252 solo re-run: 178/181; 3 tests TLE in my sandbox (cpu ~2.2s vs 2.0 limit; evidence WA ~1.2s) with IDENTICAL output hashes, all after first failure 0003 -> CPU-boundary-only, record in audit note. All other 704A subs 181/181. Next: mkfinal15 (copy ~/audit14/me/mkfinal14.py pattern), worktree on 8fcd006, sign 704A only; report 606B/659E repair list.
