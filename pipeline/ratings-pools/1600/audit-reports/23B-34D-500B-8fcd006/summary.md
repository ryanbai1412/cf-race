# Independent audit: 23B / 34D / 500B at 8fcd006

**Complete: 0/3 approved. No signoffs created.**

Archive SHA256: `c23b7888cddcd86285f888e0e2cf2266aa7e4584ac4ba972e214a2583d403a4e`. All 3304 members and 3303 manifest-listed files verified. Worker commit: `8fcd0068e9d0d1d6d3551fcbe5c9358b6ded472b`.

- **23B withheld:** rendered bounds are literal 105 for both t and n; 171 tests violate them. Public English HTML attests both powers as 10^5. Preserve original bytes and normalize/rebind before re-audit. Three strict current-bound LF numeric witnesses exist; two other genuine numerical defects have only out-of-current-bound included witnesses.
- **34D withheld:** 6657730 and 39433531 are missing-answer-only and need replacements. Other three sources have included LF, normal-exit wrong parent mappings. Rebind 120273696 from the synthetic-node extra-token 0007 failure to numeric witness 0125.
- **500B withheld:** all five sources have included LF, normal-exit mathematical defects. 205455566's recorded 0001 output has the correct numeric values and only wrong list presentation; rebind to 0132 and rerun. Its actual algorithmic defect is **unsorted component index set iteration**, not local-neighborhood sorting (that is 232241119).

## Independently verified

- 552 tests and 5 samples: all exact input/output hash bindings checked; expected integer tokens independently derived, zero output mismatches.
- Brutes: 33,867 friendship graphs, 2,712 tree/root pairs, 1,589 graph/permutation combinations with 24,985 reachable states.
- Thirty distinct authentic counted programs: full sandbox replay, **5,520/5,520 recorded verdict/exit/timeout/output-hash tuples match**; 50 additional sample runs. Two extra targeted runs corroborate 139380605.
- Each deterministic generator repeated twice offline; all three disjoint sixth accepted public oracles match all 557 cases and recorded tuples.
- All 15 incorrect sources read in full with explicit algorithms, faults, exact line anchors, original source bytes, witness bytes, independent expected/actual bytes and hashes, normal exits/timeouts, pointer status, and canonical content-proof hashes.
- **11/15 strict current-bound LF numeric proofs**; 13/15 under the attested intended bounds. The other two are missing-answer-only. These are source-proof counts, not a release count.
- Maximum cases independently measured and answered; see report coverage for 100000-query parties, 50000-node path/star trees, and 300-node disconnected/path/dense/parity swap graphs. Party maxima are outside the currently flattened statement bounds.

## Content-bound artifacts

- Replay ledger SHA256: `735511802cf1e69dd2fef1779466d06f543854abaa97180b051d5c69491871df`
- Source proofs SHA256: `882139857873048189f3f2cd011a6921e4ef2ec309a00fef0a40439ab48eed65`
- Report SHA256: `3b33ffb15b79ea8d25b85b4e35ee98c5776bafe2f534b2ee5f6604b4ad675f6b`

Only new report/proof paths are committed. No worker bytes, historical signoffs or earlier exclusions changed; no PR, publication or production writes.
