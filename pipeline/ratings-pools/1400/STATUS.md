# 1400 worker notes (lossless progress record)
Repo: /home/ubuntu/repos/cf-race, branch devin/1791845646-rated-1400 (based on foundation FETCH_HEAD 0925656).
Workspace W=~/Documents/cf-pools, cache C=~/.cache/cf-race-pool. Inventory done (403 total/305 metadataEligible/70 complete-official).
Docker image pulled. Submissions index: ~/Documents/w1400/index_subs.py (log index_subs.log) builds W/1400/submissions/<oid>/ for all 305 eligible ids with --all-submissions semantics.
Rows of 70 complete candidates: ~/Documents/w1400/rows/PID.json (extract.py).
Prepared 63 (blocked by row_gate: 1001B/C/D/G missing output_format; 1505C,290A,290D missing description).
Statement-review exclusions: 286A (multiple answers), 770D (whitespace-significant ASCII art, token checker unsound), 679A (interactive).
Recipes: ~/Documents/w1400/recipes/{lib.py,probs_a.py,probs_b.py,probs_c.py}: per-problem class with V (validator), S (oracle), G (extra tests: (category, reason, input)), optional B (brute) + SMALL(r) random small input for brute cross-check, rules string. REG dict in lib.
Written so far: probs_a (1068A..2038L 16), probs_b (219B..475B 16), probs_c (485A..675B 14).
TODO probs_d: 689A 697B 698A 762A 803A 851B 868B 8B 911C 937B 940B 954B 958A1 962C.
Then driver build.py: validate all official+examples with V, check S vs official outputs (checker.check), brute vs S on SMALL, gen extras -> extra-PID.json, run rated_pool generate --extra-tests, write coverage-PID.json bound to packageHash, then validate --all-submissions --validator <id>.
Note from 1000 worker: foundation compile lacks -DONLINE_JUDGE (freopen under #ifndef ONLINE_JUDGE -> contradictions). Do not edit shared harness; record.
SCOPE CHANGE (parent, 23:05): officialComplete NOT required if extensive generated full suite validated by 5 acc/5 incorrect + independent constraints/oracle/boundary/max/adversarial audit. Foundation worker updating shared gate on original branch -> pull updates (git fetch origin devin/1791844312-rated-pipeline). Don't edit shared gate. Keep truncated official excluded, contradictions quarantined. Document generated-vs-official basis.
Owned paths only: pipeline/ratings-pools/1400/, pipeline/problems/<ids>/, problems/<ids>/. Tests gitignored -> archive with SHA256.

## Progress 23:16
- Submission index COMPLETE (36 shards). count_subs.py -> subcounts.json; ok55.json = 123 IDs with >=5 distinct supported acc AND >=5 inc (48 complete-official).
- build.py PID [--check-only]: checks V/S vs all supplied (official+open-r1 generated+examples), brute, extras -> checks/PID.json, extra/extra-PID.json, coverage/coverage-PID.json, runs generate.
- pipeline_run.sh PID...: build + sandbox validate (--all-submissions --validator devin-1400-worker). run1.log = background run over 43 clean complete-official IDs (8B done separately: acceptedContradiction from CRLF).
- FINDING: ALL official inputs are CRLF; getline readers false-WA (8B 34328/34187/34302). Posted on shared phase note. Foundation fix needed.
- FINDING: open-r1 generated tests violate constraints -> quarantine: 108B (a>1e9), 205B (a>1e9), 24A (c=1000>100), 1009B (extra 2nd line). Gate requires all generated pairs.
- Recipes: probs_d (689A..962C) and probs_e (1009B..272B) and probs_f (277A..505B) written. lib has LR line reader, LOWER/UPPER.
- Clean check-only so far: probs_a-d 44 ids all CLEAN; probs_e CLEAN: 107A 152C 159C 180C 197B 198B 245E 261A 270B 272B. 19A still DIRTY (inspect checks/19A.json).
- Excluded at statement review (multi-answer): 286A, 379C, 402B, 711B (n=1 any x). 679A interactive, 770D whitespace art. Prepare-blocked: 1001B/C/D/G,1505C,290A,290D (missing fields), 436B, 60B (truncated test pair).
- TODO recipes: 514B 518B 525B 548B 581C 602B 604B 612C 614B 632B 637C 665B 670D1 710B 713A 719B 745B 748C 757B 762B 77A 797B 799B 79B 804B 816B 81A 838A 888C 920C 928B 929A 934A 955B 958D1 975C 987C 994B 995B (statements via stmt.py)
- 23:17: probs_f CLEAN: 277A 279B 289B 315A 358A 38C 417B 41B 437C 441B 445B 492C 505B. Quarantine (invalid open-r1 generated inputs): 413C (a=7e8+1>1e7), 479C (b=0), 493B (|a|>1e9). 19A validator still flags official sample 'a','A' -> debug.
- run1.log slow (~2-3 min/problem); 124B,125A execution-passed 5/5.
- Next: write probs_g for 514B.. list; after run1 finishes, run pipeline_run.sh for new clean IDs (incomplete-official ones: generate works now; validate status only, gate pending foundation).
- 23:20: foundation ff to 5faeff9 (generated basis: generator.py seed->JSON pairs >=100 distinct; independent oracle author != generator/validator + reviewUrl; v2 ONLINE_JUDGE harness invalidates pre-v2 evidence). Killed run1. Inventory re-run: 328 metadata-eligible, 70 complete official, 313 generated-qualification-required.
- Oracle child sessions (independent authors, statement-only), batches in oracle_batches.json (67 clean recipes ∩ ok55):
  1 fd6274073bf3479982ad49ba3b664eb9  2 8dc36606ff0a48dc9a19970337df361d  3 5f3ca81eaf764afca9e2a31be82155bc
  4 eb221b8703b14b4c938c78f6760ca7a5  5 9371ac9ab5214d04a26e21730cb5c880  6 23a990a22af6447d99b72f95f7661c6c
- Next: bundle.py -> gen/<ID>/generator.py self-contained (lib+module+runner); need RAND for 54 recipes w/o SMALL.
- 23:37: foundation ff to 3a44647. 64 oracles integrated (oracles/index.json; raw in oracles_raw/<attachment-uuid>/). Oracle exclusions: 675B (diagram), 851B/868B (case-insensitive output). 745B prepare-blocked (truncated pair).
- gen_run.py PID: prepare -> generate (gen/PID/generator.py + independent oracle) -> gcoverage -> validate. 125A execution-passed 5/5 generated basis v2 (172 tests). Batch of remaining 63: todo1.txt, xargs -P4, log gen_batch1.log, results gen_results.jsonl.
- New oracle batches 7-10 (38 new cands, prompts oracle_req/prompt7-10.txt): d20d3880f6554a359d43efb76ed8965d 93c28ce8f33c48709a44509edb3091f9 042dd6d9a09541d9b740c1b089a36a0e 47744976e27e4a408a748d0857f183ba
- 23:40: 124B quarantined by independent oracle at official test 0006 (oracle author enforces positivity of input numbers; investigate - do NOT repair). 107A,152C execution-passed generated v2.
- probs_g.py (new 1400 recipes: 514B 518B 525B 548B 581C 602B ...), probs_h.py for rest. bundle.py/gen_run.py import probs_a..h. 955B excluded (case-insensitive Yes/No). 838A deferred (max-size reference too slow for 10s generator CPU in pure Python).
- Remaining recipes to write: 604B 612C 614B 632B 637C 665B 670D1 710B 713A 719B 748C 757B 762B 77A 797B 799B 79B 804B 816B 81A 888C 920C 928B 929A 934A 958D1 975C 987C 994B 995B
- 23:48: oracle batches 7,9,10 integrated (91 oracles). Quarantined (upstream open-r1 generated input violates statement): 514B,670D1,632B,797B. 180C accepted contradiction (1608245 WA official 0001); 124B oracle rejects official 0006. 637C recipe bug n=1 fixed (would have been caught: official expected 6).
- probs_h.py has 29 recipes; check_h.log + check_h2.log.
- 23:49: batch 8 oracles (518B,602B,632B,710B,757B,799B,81A,928B,958D1,995B) sha 0dfb04b3... verified, integrated.
- 23:49: batch 8 oracles (518B,602B,632B,710B,757B,799B,81A,928B,958D1,995B) sha 0dfb04b3... verified, integrated.

## Status 23:55 UTC (execution v2, generated basis)
- execution-passed 5 AC / 5 incorrect, NOT independently audited: 125A 107A 152C 175A 197B 198B 233B 245E 248B (9). Independently validated: 0.
- incomplete, accepted contradiction on official tests (preserved, not repaired):
  159C 1316357 RE(-11) on 0001; 131C 891836 WA 0005, 892514 TLE 0001; 219B 2053200 WA 0002, 2053245/2053542 WA 0010; 180C 1608245 WA 0001 (1608242 no result).
- blocked: 124B independent oracle disagrees with official 0006.
- quarantined, upstream open-r1 generated inputs violate statement bounds: 514B 670D1 632B 797B. Truncated: 745B. Earlier: 108B 205B 24A 1009B 413C 479C 493B.
- excluded, output not unique / case-insensitive: 675B 851B 868B 955B.
- Per-package archives: `python3 pipeline/rated_pool.py archive --rating 1400 --id PID ...` (verified byte-reproducible for 125A); SHA256SUMS bundled in rating1400-execution-passed-audit.tar.gz.

## Status 2026-10-13 00:23 UTC (resume pass)
- Independently validated (different-agent audit, current publication_gate(require_approval=False) passes): 20 —
  125A 152C 198B 233B 248B 270B 272B 277A 279A 279B 289B 315A 334B 358A 388A 38C 417B 41B 435B 548B.
- Audit-rejected (kept, not counted): 107A (print("x") / missing count line), 175A (debug echo), 261A (debug print; wrong-problem source),
  197B (8471901 representation-only failure), 245E (CRLF artifacts; correct Python input() fails official tests), 337B (non-attempt sources),
  518B (CRLF artifacts + debug prints), 226A (false coverage label; recipe label fixed and test 2 8 added, re-run pending re-audit).
- CRLF artifact scan (crlf_scan.log): counted incorrect source passes its failedTest after CRLF->LF on 525B 612C 448B 614B 475B 637C 804B 698A 518B 245E -> not sent to audit.
- New accepted contradictions: 386B 5705687 WA@0045; 581C 13261919 WA@0076; 430B 6589136 WA@0020; 445B 7022262/7022264 WA@0007.
- Upstream-invalid generated inputs: 929A (x not increasing, 2 open-r1 inputs), 713A, 719B (+ earlier list).
- Source shortfall: 437C (2 incorrect), 492C (2 accepted, 0 incorrect).
- 762B/799B/816B generator JSON exceeded sandbox 8 MiB output cap; second max case shrunk (one true max case kept), rerunning.
- Shared defects reported to parent: CRLF official inputs unnormalized; first-5-by-id incorrect selection admits non-attempts.

## Status 2026-10-13 01:06 UTC
- Audit 10 (60ebaedc...) approved 226A 652A 604B; rejected 77A (25020964 solves CF 71A) and 816B (29293156 recorded TLE@0009 is a timing artifact, output correct). Imported; gate_all: 41 pass.
- Never-run 5/5 candidates resolved: 81A quarantined (9 open-r1 generated inputs length 200001 > 2e5), 987C (3 generated inputs contain s_i=0 < 1),
  994B (4 generated inputs with values > 1e9), 689A (pinned statement text puts 0 under 7 in its LaTeX array; official tests (e.g. 0023 '1468'->NO) require 0 under 8;
  independent oracle followed the text and disagrees on 14 official tests -> statement/test inconsistency quarantined, not repaired).
- 954B regenerated after label fix: fresh execution-passed, CRLF scan ok; awaiting re-audit. 799B, 838A validating.
