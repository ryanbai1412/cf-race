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
