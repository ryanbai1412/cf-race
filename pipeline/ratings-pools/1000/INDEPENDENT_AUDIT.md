# Source-semantics review hold

**The historical 66/103 executable gate count is not a complete source-reviewed validation count. All 66 approvals are held; the current fully source-certified count is 0.**

The classifier used 108 generic content-mismatch approvals and 202 scalar-oracle comparisons across the 330 selected wrong references in those 66 packages. The available report does not establish a concrete, source-specific defect review for those 310 references. Valid, normally terminating package-bound counterexamples remain useful evidence, but numerical/decision mismatch is not by itself proof that formatting/debug/unimplemented-algorithm artifacts were excluded through source review.

This does not assert that the 310 programs are algorithmically correct. It identifies an unsubstantiated certification claim. Twenty other references have more specific reason fields; this follow-up did not reapprove them. Every previously approved package has at least one unconfirmed reference.

The complete queue contains exact public source bytes, source URLs and SHA256s, unchanged package/evidence bindings, and the previously executed counterexample inputs and expected/actual outputs. Source review can use this evidence without rerunning unchanged packages. Before restoring a signoff, identify the exact incorrect branch/expression and establish that its package-bound witness proves an actual algorithmic defect, not only token mismatch, numeric formatting, prompts/debug output, or an unimplemented entrypoint.

The original immutable archive (SHA256 `8afca15780dd4d53ee27a07b9e78e5ccc92989810b0f9194bf9b41df13b65194`) and package/evidence bytes are unchanged. Its historical audit assertions must not authorize release without closing this hold. Current individual audit records now set `approved: false`; no third-party code was executed in this clarification.

No production publication, remote database/storage writes, or PR occurred. The 37 originally excluded packages still require the builder correction queue; this independent source-review gap is additional.

## Exact affected-package queue

| Problem | Generic content fallback | Scalar comparison |
|---|---:|---:|
| 1008B | 5 | 0 |
| 106B | 0 | 5 |
| 108A | 4 | 0 |
| 122A | 4 | 0 |
| 124A | 0 | 5 |
| 127B | 0 | 5 |
| 131A | 5 | 0 |
| 137B | 0 | 5 |
| 139A | 0 | 5 |
| 143A | 1 | 0 |
| 17A | 5 | 0 |
| 195A | 0 | 4 |
| 1A | 0 | 5 |
| 237A | 0 | 5 |
| 272A | 0 | 4 |
| 352A | 0 | 5 |
| 359A | 0 | 5 |
| 368A | 0 | 5 |
| 371A | 0 | 5 |
| 379A | 0 | 5 |
| 37A | 5 | 0 |
| 385A | 0 | 5 |
| 435A | 0 | 5 |
| 441A | 5 | 0 |
| 450A | 0 | 5 |
| 452A | 4 | 0 |
| 462A | 5 | 0 |
| 476A | 0 | 5 |
| 479A | 0 | 4 |
| 500A | 4 | 0 |
| 515A | 5 | 0 |
| 577A | 0 | 5 |
| 579A | 0 | 5 |
| 58A | 4 | 0 |
| 604A | 0 | 5 |
| 608A | 0 | 5 |
| 610A | 0 | 5 |
| 616B | 0 | 5 |
| 626A | 0 | 5 |
| 637A | 0 | 5 |
| 659A | 0 | 5 |
| 670B | 0 | 1 |
| 69A | 4 | 0 |
| 724A | 5 | 0 |
| 727A | 5 | 0 |
| 733A | 0 | 5 |
| 757A | 0 | 5 |
| 75A | 5 | 0 |
| 761A | 5 | 0 |
| 779A | 0 | 5 |
| 798A | 4 | 0 |
| 847M | 0 | 5 |
| 849A | 5 | 0 |
| 859B | 0 | 5 |
| 862A | 0 | 4 |
| 864B | 0 | 5 |
| 886A | 5 | 0 |
| 887A | 5 | 0 |
| 888B | 0 | 5 |
| 893B | 0 | 5 |
| 909A | 5 | 0 |
| 90A | 0 | 5 |
| 920A | 4 | 1 |
| 967B | 0 | 4 |
| 979A | 0 | 5 |
| 991A | 0 | 5 |

## Historical report (superseded; not release approval)

# Independent rating-1000 audit

**66 of 103 distinct audit-ready packages verified** (47 complete-official; 19 qualified-generated).
Target 100: deficit 34. Builder duplicate 691A is excluded; any separate foundation 691A is not counted here.

Every source was rerun against its complete suite and samples in the pinned offline, read-only, non-root, CPU/memory/time-bounded Docker sandbox. Independent oracle and bounds checks covered all supplied pairs and samples; deterministic generated cases were reproduced and checked against an independent accepted oracle. LF-normalized replay distinguishes arithmetic/logic mistakes from CRLF sensitivity, debug output, presentation-only differences, crashes, and timeouts. Two public accepted programs per package also passed independent edge/random stress cases. Only normal-termination algorithmic wrong answers on *included package tests* count; generated packages additionally require the builder-selected failure itself to be algorithmically wrong.

Five input archives were verified byte-for-byte (46,919 members), with 84 pinned source files and 179,935 oracle self-checks. Exact archive SHA256s, package/evidence/source/test hashes, per-source outcomes, sample checks, reasons for exclusion, and independently executed proof hashes are in `independent-audit.json`. Raw fresh execution and LF replay records are in the accompanying evidence archive.

No publication, PR, migration, merge, or production data change occurred. Excluded packages are **not** authorized for release, and the separate foundation 691A result must be counted only against its own unchanged audited bytes.

Generated evidence failure pointers were corrected only where the *unchanged existing package suite* and fresh full-suite executions prove a normally terminating algorithmic wrong answer. No run result, program, test pair, official completeness claim, or package byte was rewritten. The old and new evidence bindings and each replaced pointer are retained in the JSON report. All signoffs were checked with the current executable evidence gate after these metadata corrections.

## Excluded packages

| Problem | Qualification | Accepted / algorithmic wrong | Principal reason |
|---|---|---:|---|
| 102B | generated | 5 / 2 | 87771531: no sandboxed normal-termination mathematical WA: duplicate output on single-digit inputs; otherwise correct or nonterminating; 88917224: builder selected first failing test is formatting/CRLF/timeout-only or unproven; 89870572: builder selected first failing test is formatting/CRLF/timeout-only or unproven |
| 109A | official | 5 / 4 | 10773619: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 19, 'TLE': 4} |
| 118A | official | 5 / 4 | 220806005: no sandboxed normal-termination mathematical WA: correct lowercase consonant sequence; only uses a middle-dot instead of a period separator |
| 118B | official | 5 / 4 | 230853348: no sandboxed normal-termination mathematical WA: answer differs only by token separators |
| 122B | official | 5 / 3 | 223271341: no sandboxed normal-termination mathematical WA: answer appears intact alongside additional output; not an algorithmic witness; 223275244: no matched package test witnessing mathematical WA |
| 13A | official | 5 / 4 | 11584293: no sandboxed normal-termination mathematical WA: digit sums and reduced fraction are correct; only integer terms printed as floats |
| 165A | generated | 5 / 4 | 80718221: no sandboxed normal-termination mathematical WA: input-list echo, no supercentral-point algorithm implemented |
| 182B | generated | 5 / 3 | 9808431: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 21, 'TLE': 2}; 53205612: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 21, 'TLE': 2} |
| 259A | official | 5 / 4 | 16068483: no sandboxed normal-termination mathematical WA: answer appears intact alongside additional output; not an algorithmic witness |
| 265B | generated | 5 / 4 | 78493868: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 21, 'TLE': 2} |
| 268B | official | 5 / 4 | 187089689: no sandboxed normal-termination mathematical WA: function is never called; no executed contest algorithm |
| 284B | generated | 5 / 3 | 4339453: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 21, 'TLE': 2}; 4339460: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 21, 'TLE': 2} |
| 29A | generated | 5 / 4 | 18516909: no sandboxed normal-termination mathematical WA: correct mutual-hit algorithm plus debug indices |
| 336A | official | 5 / 3 | 4270268: no sandboxed normal-termination mathematical WA: function is never called; no executed contest algorithm; 4278763: no sandboxed normal-termination mathematical WA: answer appears intact alongside additional output; not an algorithmic witness |
| 389A | official | 5 / 4 | 8863977: no sandboxed normal-termination mathematical WA: unrelated three-string anagram program, no 389A algorithm |
| 400A | generated | 5 / 4 | 14343389: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 13} |
| 404A | generated | 5 / 2 | 78384372: builder selected first failing test is formatting/CRLF/timeout-only or unproven; 79248071: no matched package test witnessing mathematical WA; 79990057: builder selected first failing test is formatting/CRLF/timeout-only or unproven |
| 447B | generated | 5 / 2 | 7108743: builder selected first failing test is formatting/CRLF/timeout-only or unproven; 23179500: no sandboxed normal-termination mathematical WA: correct weighted answer plus debug partial answer; 30734165: builder selected first failing test is formatting/CRLF/timeout-only or unproven |
| 465B | generated | 5 / 4 | 7717088: no sandboxed normal-termination mathematical WA: correct LF answer plus debug input list |
| 535A | official | 5 / 4 | 10819886: no sandboxed normal-termination mathematical WA: normally terminating word answers are correct except for capitalization and prompt text; other branches crash |
| 560A | generated | 5 / 4 | 12199300: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 17, 'TLE': 6} |
| 583A | generated | 5 / 4 | 13428129: no sandboxed normal-termination mathematical WA: correct repair-day indices serialized as a Python list |
| 620B | official | 5 / 3 | 15475698: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 21, 'TLE': 2}; 15477398: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 21, 'TLE': 2} |
| 622A | official | 5 / 0 | 15962221: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 16, 'TLE': 6}; 15972436: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 14, 'TLE': 8}; 15986351: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 16, 'TLE': 6}; 15986832: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 13, 'TLE': 9}; 16009656: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 16, 'TLE': 6} |
| 628A | official | 5 / 4 | 16427513: no sandboxed normal-termination mathematical WA: answer appears intact alongside additional output; not an algorithmic witness |
| 641A | generated | 5 / 4 | 17779903: no sandboxed normal-termination mathematical WA: correct solver never called; entrypoint/debug defect |
| 660B | official | 5 / 4 | 17601981: no sandboxed normal-termination mathematical WA: seating algorithm produces the correct sequence followed by a debug array |
| 680B | official | 5 / 4 | 72605069: no sandboxed normal-termination mathematical WA: function is never called; no executed contest algorithm |
| 725A | generated | 5 / 1 | 21676570: builder selected first failing test is formatting/CRLF/timeout-only or unproven; 21692605: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 25}; 21693802: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 24, 'TLE': 1}; 21694953: builder selected first failing test is formatting/CRLF/timeout-only or unproven |
| 742A | official | 5 / 3 | 144840450: no sandboxed normal-termination mathematical WA: answer appears intact alongside additional output; not an algorithmic witness; non-numeric output needs source-level review; 145922390: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 12, 'TLE': 10} |
| 74A | generated | 5 / 4 | 9445467: no sandboxed normal-termination mathematical WA: unrelated distinct-digit routine, no contest-score algorithm implemented |
| 766B | generated | 5 / 4 | 129802595: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 21, 'TLE': 2} |
| 777A | official | 5 / 2 | 24981880: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 12, 'TLE': 11}; 24983950: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 12, 'TLE': 11}; 24986037: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 12, 'TLE': 11} |
| 804A | official | 5 / 3 | 26866061: no sandboxed normal-termination mathematical WA: numeric values equal; only numeric output representation differs; 27128899: no sandboxed normal-termination mathematical WA: numeric values equal; only numeric output representation differs |
| 831A | official | 5 / 4 | 134630421: no matched package test witnessing mathematical WA |
| 886B | generated | 5 / 1 | 32274795: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 22, 'TLE': 1}; 32285291: no matched package test witnessing mathematical WA; 32287643: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 22, 'TLE': 1}; 32303392: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 12} |
| 990A | official | 5 / 3 | 39106454: no sandboxed normal-termination mathematical WA: non-numeric output needs source-level review; 39106599: no sandboxed normal-termination mathematical WA; LF replay verdicts {'AC': 16, 'TLE': 7} |

## Approved problem IDs

1008B, 106B, 108A, 122A, 124A, 127B, 131A, 137B, 139A, 143A, 17A, 195A, 1A, 237A, 272A, 352A, 359A, 368A, 371A, 379A, 37A, 385A, 435A, 441A, 450A, 452A, 462A, 476A, 479A, 500A, 515A, 577A, 579A, 58A, 604A, 608A, 610A, 616B, 626A, 637A, 659A, 670B, 69A, 724A, 727A, 733A, 757A, 75A, 761A, 779A, 798A, 847M, 849A, 859B, 862A, 864B, 886A, 887A, 888B, 893B, 909A, 90A, 920A, 967B, 979A, 991A

## Additional inspected quarantines outside the audit-ready set

14B, 230A, 299A, 43A, 499A, 499B, 56A, 699A, 978C, 981B: independent semantic checks rejected malformed/out-of-bounds upstream pairs. These were never counted among the 103 audit-ready packages or approved results. Their exact first-failure records and evidence hashes are retained in the JSON report.

## Boundaries

A builder execution-passed flag is not an audit signoff. The generated suites retain incomplete official pairs as supplementary; no missing official pair was fabricated or silently made complete. Format-only, runtime/compile, unsupported-language and timeout-only failures were not counted as algorithmic kills. All remaining exclusions require replacement wrong references, additional validated package cases, or fresh correct evidence and a separate audit before release.
