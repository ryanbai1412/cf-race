# Rating 1000 — corrected independent audit

**52 technically qualified / 103 audited; 49 rejected, 2 held; target deficit 48.**

35 complete-official-suite packages and 17 independently qualified generated-suite packages pass the current executable evidence gate. All 52 have five normally terminating, source-reviewed algorithmically wrong references and five accepted references that passed the complete included suite. This is technical validation, not publication permission or legal clearance. Publication-approved/published: **0/0**.

Scope: the original 103 distinct builder packages, excluding 691A. Corrective source review covers all five incorrect references for each of the formerly held 66 packages (330 sources). The original 37 exclusions remain excluded. The separate 20 builder-corrected packages are outside this audit and are not counted.

The five reviewer reports classified 316 references pass, 11 reject, 3 unconfirmed. Primary exact-byte reconciliation instead accepts 312 reference proofs, rejects 16, and holds 2. Only 52 packages have 5/5 qualifying wrong-source proofs; no reviewer label independently authorizes a package.

## Evidence and execution

- Reused the original fresh offline, resource-bounded Docker executions after verifying exact source, input, output, package, evidence and proof hashes. No new public-program execution or duplicate full-suite rerun during this correction.
- Read the complete problem implementations and reviewed source-specific faulty branches/expressions, exact source ranges, independent mathematical expected answers, actual-answer traces and normal-exit included witnesses. Empty-stdout-only, nonportable parsing, placeholder/unrelated programs and presentation-only failures do not qualify.
- Source review verified 283 applicable historical proof-file hashes and every one of the 330 complete source hashes. The original 1030 source attributions and package bytes remain bound to the original independent execution records.
- Package, statement, tests, generator and public-source bytes are unchanged. The only newly modified evidence is 106B: two failedTest pointers now select already-included, originally executed mathematical counterexamples; new evidence and audit hashes are bound below.
- executionVersion 2, exact ONLINE_JUDGE compiler context, network-none sandbox and original source pins are retained. Generated qualification remains distinct from complete official qualification; incomplete official pairs are supplementary, not silently relabeled complete.

## Historical records retained

The old 66-signoff archive is historical, not current approval. The immutable hold JSON and old Git commits are retained; current per-problem audits and the current aggregate supersede their approval status.

- Historical execution/proof archive SHA256: `8afca15780dd4d53ee27a07b9e78e5ccc92989810b0f9194bf9b41df13b65194`
- Historical hold commit: https://github.com/ryanbai1412/cf-race/commit/8cf9bf9c77829449de5dfd4aa853131531b17e02
- Frozen 330-reference bundle SHA256: `19ab115b63cb991ec952bd544b1aa8b95f4a6c4e2c6ac96eade69ec2811d22c5`
- Frozen source/proof supplement SHA256: `ef131f1c30bc4d3c255a47238d98e06ea6f7ce4129a3d7be69edef6b2fa7e4fb`

## Exact witness reconciliation

- 122A/211244483: LF input 444 matches included test 0045 and the CRLF-equivalent 0024; original normal-exit WA/output binding verified. Not approved on an independent mutation alone.
- 131A and 626A: source-semantic reconstruction reproduces the CR-containing original stdout hash, while independent LF executions demonstrate the same genuine defect. 626A/32525982 counts only 7 (LF: 6) rather than the mathematical 12 because of the erroneous break.
- 143A/8985121: original CRLF execution verified, not substituted with a diagnostic-copy execution.
- 577A/12926294 and 12926306: nonportable %I64d input behavior is excluded; no algorithmic kill claimed.
- 108A/9008626 and 195A/51642398 remain held: missing output/internal-state defects are not a normally emitted wrong algorithmic answer.
- 887A uses exact-hash included official counterexamples, not the mismatched-case supplemental expected output.
- Previously identified presentation-only first failures in 859B, 862A, 864B, 888B, 979A were not blessed: 859B/862A are excluded; 864B/888B/979A qualify using already bound included mathematical witnesses from the original audit.

## Current passing IDs

1008B, 106B, 122A, 124A, 127B, 131A, 137B, 139A, 143A, 237A, 272A, 352A, 359A, 368A, 379A, 37A, 385A, 435A, 441A, 450A, 462A, 476A, 479A, 500A, 515A, 579A, 58A, 604A, 608A, 610A, 616B, 626A, 637A, 659A, 69A, 724A, 733A, 757A, 75A, 761A, 779A, 847M, 849A, 864B, 886A, 887A, 888B, 893B, 909A, 920A, 979A, 991A

## All 103 outcomes

| Problem | Status | Basis | Accepted passes | Genuine wrong refs | Reason if excluded |
|---|---|---|---:|---:|---|
| 1008B | TECHNICAL PASS | generated | 5 | 5 |  |
| 102B | REJECTED | generated | 5 | 2 | 87771531: no sandboxed normal-termination mathematical WA; 88917224: builder selected first failing test is formatting/CRLF/timeout-only or unproven; 89870572: builder selected first failing test is formatting/CRLF/timeout-only or unproven; only 5 accepted, 2 algorithmically wrong sources proved |
| 106B | TECHNICAL PASS | generated | 5 | 5 |  |
| 108A | HELD | official | 5 | 4 | 9008626: reviewer-unconfirmed; empty-stdout-not-computed-wrong-answer |
| 109A | REJECTED | official | 5 | 4 | 10773619: no sandboxed normal-termination mathematical WA; only 5 accepted, 4 algorithmically wrong sources proved |
| 118A | REJECTED | official | 5 | 4 | 220806005: no sandboxed normal-termination mathematical WA; only 5 accepted, 4 algorithmically wrong sources proved |
| 118B | REJECTED | official | 5 | 4 | 230853348: no sandboxed normal-termination mathematical WA; only 5 accepted, 4 algorithmically wrong sources proved |
| 122A | TECHNICAL PASS | official | 5 | 5 |  |
| 122B | REJECTED | official | 5 | 3 | 223271341: no sandboxed normal-termination mathematical WA; 223275244: no matched package test witnessing mathematical WA; only 5 accepted, 3 algorithmically wrong sources proved |
| 124A | TECHNICAL PASS | official | 5 | 5 |  |
| 127B | TECHNICAL PASS | generated | 5 | 5 |  |
| 131A | TECHNICAL PASS | official | 5 | 5 |  |
| 137B | TECHNICAL PASS | generated | 5 | 5 |  |
| 139A | TECHNICAL PASS | official | 5 | 5 |  |
| 13A | REJECTED | official | 5 | 4 | 11584293: no sandboxed normal-termination mathematical WA; only 5 accepted, 4 algorithmically wrong sources proved |
| 143A | TECHNICAL PASS | official | 5 | 5 |  |
| 165A | REJECTED | generated | 5 | 4 | 80718221: no sandboxed normal-termination mathematical WA; only 5 accepted, 4 algorithmically wrong sources proved |
| 17A | REJECTED | official | 5 | 4 | 15442637: reviewer-reject |
| 182B | REJECTED | generated | 5 | 3 | 9808431: no sandboxed normal-termination mathematical WA; 53205612: no sandboxed normal-termination mathematical WA; only 5 accepted, 3 algorithmically wrong sources proved |
| 195A | HELD | official | 5 | 4 | 51642398: reviewer-unconfirmed; empty-stdout-not-computed-wrong-answer |
| 1A | REJECTED | official | 5 | 4 | 150705005: reviewer-reject |
| 237A | TECHNICAL PASS | generated | 5 | 5 |  |
| 259A | REJECTED | official | 5 | 4 | 16068483: no sandboxed normal-termination mathematical WA; only 5 accepted, 4 algorithmically wrong sources proved |
| 265B | REJECTED | generated | 5 | 4 | 78493868: no sandboxed normal-termination mathematical WA; only 5 accepted, 4 algorithmically wrong sources proved |
| 268B | REJECTED | official | 5 | 4 | 187089689: no sandboxed normal-termination mathematical WA; only 5 accepted, 4 algorithmically wrong sources proved |
| 272A | TECHNICAL PASS | official | 5 | 5 |  |
| 284B | REJECTED | generated | 5 | 3 | 4339453: no sandboxed normal-termination mathematical WA; 4339460: no sandboxed normal-termination mathematical WA; only 5 accepted, 3 algorithmically wrong sources proved |
| 29A | REJECTED | generated | 5 | 4 | 18516909: no sandboxed normal-termination mathematical WA; only 5 accepted, 4 algorithmically wrong sources proved |
| 336A | REJECTED | official | 5 | 3 | 4270268: no sandboxed normal-termination mathematical WA; 4278763: no sandboxed normal-termination mathematical WA; only 5 accepted, 3 algorithmically wrong sources proved |
| 352A | TECHNICAL PASS | generated | 5 | 5 |  |
| 359A | TECHNICAL PASS | generated | 5 | 5 |  |
| 368A | TECHNICAL PASS | official | 5 | 5 |  |
| 371A | REJECTED | official | 5 | 4 | 95556018: reviewer-reject; no-identical-normal-original-package-execution |
| 379A | TECHNICAL PASS | official | 5 | 5 |  |
| 37A | TECHNICAL PASS | generated | 5 | 5 |  |
| 385A | TECHNICAL PASS | official | 5 | 5 |  |
| 389A | REJECTED | official | 5 | 4 | 8863977: no sandboxed normal-termination mathematical WA; only 5 accepted, 4 algorithmically wrong sources proved |
| 400A | REJECTED | generated | 5 | 4 | 14343389: no sandboxed normal-termination mathematical WA; only 5 accepted, 4 algorithmically wrong sources proved |
| 404A | REJECTED | generated | 5 | 2 | 78384372: builder selected first failing test is formatting/CRLF/timeout-only or unproven; 79248071: no matched package test witnessing mathematical WA; 79990057: builder selected first failing test is formatting/CRLF/timeout-only or unproven; only 5 accepted, 2 algorithmically wrong sources proved |
| 435A | TECHNICAL PASS | official | 5 | 5 |  |
| 441A | TECHNICAL PASS | generated | 5 | 5 |  |
| 447B | REJECTED | generated | 5 | 2 | 7108743: builder selected first failing test is formatting/CRLF/timeout-only or unproven; 23179500: no sandboxed normal-termination mathematical WA; 30734165: builder selected first failing test is formatting/CRLF/timeout-only or unproven; only 5 accepted, 2 algorithmically wrong sources proved |
| 450A | TECHNICAL PASS | official | 5 | 5 |  |
| 452A | REJECTED | official | 5 | 4 | 7274102: empty-stdout-not-computed-wrong-answer |
| 462A | TECHNICAL PASS | generated | 5 | 5 |  |
| 465B | REJECTED | generated | 5 | 4 | 7717088: no sandboxed normal-termination mathematical WA; only 5 accepted, 4 algorithmically wrong sources proved |
| 476A | TECHNICAL PASS | official | 5 | 5 |  |
| 479A | TECHNICAL PASS | official | 5 | 5 |  |
| 500A | TECHNICAL PASS | generated | 5 | 5 |  |
| 515A | TECHNICAL PASS | official | 5 | 5 |  |
| 535A | REJECTED | official | 5 | 4 | 10819886: no sandboxed normal-termination mathematical WA; only 5 accepted, 4 algorithmically wrong sources proved |
| 560A | REJECTED | generated | 5 | 4 | 12199300: no sandboxed normal-termination mathematical WA; only 5 accepted, 4 algorithmically wrong sources proved |
| 577A | REJECTED | official | 5 | 3 | 12926294: reviewer-reject; 12926306: reviewer-reject |
| 579A | TECHNICAL PASS | official | 5 | 5 |  |
| 583A | REJECTED | generated | 5 | 4 | 13428129: no sandboxed normal-termination mathematical WA; only 5 accepted, 4 algorithmically wrong sources proved |
| 58A | TECHNICAL PASS | official | 5 | 5 |  |
| 604A | TECHNICAL PASS | official | 5 | 5 |  |
| 608A | TECHNICAL PASS | generated | 5 | 5 |  |
| 610A | TECHNICAL PASS | official | 5 | 5 |  |
| 616B | TECHNICAL PASS | generated | 5 | 5 |  |
| 620B | REJECTED | official | 5 | 3 | 15475698: no sandboxed normal-termination mathematical WA; 15477398: no sandboxed normal-termination mathematical WA; only 5 accepted, 3 algorithmically wrong sources proved |
| 622A | REJECTED | official | 5 | 0 | 15962221: no sandboxed normal-termination mathematical WA; 15972436: no sandboxed normal-termination mathematical WA; 15986351: no sandboxed normal-termination mathematical WA; 15986832: no sandboxed normal-termination mathematical WA; 16009656: no sandboxed normal-termination mathematical WA; only 5 accepted, 0 algorithmically wrong sources proved |
| 626A | TECHNICAL PASS | official | 5 | 5 |  |
| 628A | REJECTED | official | 5 | 4 | 16427513: no sandboxed normal-termination mathematical WA; only 5 accepted, 4 algorithmically wrong sources proved |
| 637A | TECHNICAL PASS | generated | 5 | 5 |  |
| 641A | REJECTED | generated | 5 | 4 | 17779903: no sandboxed normal-termination mathematical WA; only 5 accepted, 4 algorithmically wrong sources proved |
| 659A | TECHNICAL PASS | official | 5 | 5 |  |
| 660B | REJECTED | official | 5 | 4 | 17601981: no sandboxed normal-termination mathematical WA; only 5 accepted, 4 algorithmically wrong sources proved |
| 670B | REJECTED | generated | 5 | 2 | 101944491: empty-stdout-not-computed-wrong-answer; 106065081: reviewer-reject; empty-stdout-not-computed-wrong-answer; 106147986: empty-stdout-not-computed-wrong-answer |
| 680B | REJECTED | official | 5 | 4 | 72605069: no sandboxed normal-termination mathematical WA; only 5 accepted, 4 algorithmically wrong sources proved |
| 69A | TECHNICAL PASS | generated | 5 | 5 |  |
| 724A | TECHNICAL PASS | official | 5 | 5 |  |
| 725A | REJECTED | generated | 5 | 1 | 21676570: builder selected first failing test is formatting/CRLF/timeout-only or unproven; 21692605: no sandboxed normal-termination mathematical WA; 21693802: no sandboxed normal-termination mathematical WA; 21694953: builder selected first failing test is formatting/CRLF/timeout-only or unproven; only 5 accepted, 1 algorithmically wrong sources proved |
| 727A | REJECTED | official | 5 | 3 | 51732884: reviewer-reject; 51954222: reviewer-reject |
| 733A | TECHNICAL PASS | official | 5 | 5 |  |
| 742A | REJECTED | official | 5 | 3 | 144840450: no sandboxed normal-termination mathematical WA; 145922390: no sandboxed normal-termination mathematical WA; only 5 accepted, 3 algorithmically wrong sources proved |
| 74A | REJECTED | generated | 5 | 4 | 9445467: no sandboxed normal-termination mathematical WA; only 5 accepted, 4 algorithmically wrong sources proved |
| 757A | TECHNICAL PASS | generated | 5 | 5 |  |
| 75A | TECHNICAL PASS | official | 5 | 5 |  |
| 761A | TECHNICAL PASS | official | 5 | 5 |  |
| 766B | REJECTED | generated | 5 | 4 | 129802595: no sandboxed normal-termination mathematical WA; only 5 accepted, 4 algorithmically wrong sources proved |
| 777A | REJECTED | official | 5 | 2 | 24981880: no sandboxed normal-termination mathematical WA; 24983950: no sandboxed normal-termination mathematical WA; 24986037: no sandboxed normal-termination mathematical WA; only 5 accepted, 2 algorithmically wrong sources proved |
| 779A | TECHNICAL PASS | official | 5 | 5 |  |
| 798A | REJECTED | official | 5 | 4 | 135564343: empty-stdout-not-computed-wrong-answer |
| 804A | REJECTED | official | 5 | 3 | 26866061: no sandboxed normal-termination mathematical WA; 27128899: no sandboxed normal-termination mathematical WA; only 5 accepted, 3 algorithmically wrong sources proved |
| 831A | REJECTED | official | 5 | 4 | 134630421: no matched package test witnessing mathematical WA; only 5 accepted, 4 algorithmically wrong sources proved |
| 847M | TECHNICAL PASS | official | 5 | 5 |  |
| 849A | TECHNICAL PASS | official | 5 | 5 |  |
| 859B | REJECTED | official | 5 | 4 | 30446951: reviewer-reject; no-selected-semantic-witness |
| 862A | REJECTED | official | 5 | 4 | 31223464: empty-stdout-not-computed-wrong-answer |
| 864B | TECHNICAL PASS | official | 5 | 5 |  |
| 886A | TECHNICAL PASS | official | 5 | 5 |  |
| 886B | REJECTED | generated | 5 | 1 | 32274795: no sandboxed normal-termination mathematical WA; 32285291: no matched package test witnessing mathematical WA; 32287643: no sandboxed normal-termination mathematical WA; 32303392: no sandboxed normal-termination mathematical WA; only 5 accepted, 1 algorithmically wrong sources proved |
| 887A | TECHNICAL PASS | official | 5 | 5 |  |
| 888B | TECHNICAL PASS | official | 5 | 5 |  |
| 893B | TECHNICAL PASS | official | 5 | 5 |  |
| 909A | TECHNICAL PASS | official | 5 | 5 |  |
| 90A | REJECTED | official | 5 | 4 | 38985905: reviewer-reject; no-selected-semantic-witness |
| 920A | TECHNICAL PASS | generated | 5 | 5 |  |
| 967B | REJECTED | generated | 5 | 4 | 37730597: reviewer-reject; no-selected-semantic-witness |
| 979A | TECHNICAL PASS | official | 5 | 5 |  |
| 990A | REJECTED | official | 5 | 3 | 39106454: no sandboxed normal-termination mathematical WA; 39106599: no sandboxed normal-termination mathematical WA; only 5 accepted, 3 algorithmically wrong sources proved |
| 991A | TECHNICAL PASS | official | 5 | 5 |  |

## New evidence-pointer corrections

| Problem/source | Former test | Mathematical test | Current evidence hash |
|---|---|---|---|
| 106B/12777834 | 0002 | 0085 | 4435aa2c3afa10b08b22b92dc3961f8afca48fbf5060c84f4472006f391cb319 |
| 106B/20980929 | 0002 | 0032 | 4435aa2c3afa10b08b22b92dc3961f8afca48fbf5060c84f4472006f391cb319 |

## Review report hashes

| Batch | SHA256 |
|---|---|
| 1 | ca43961fef2540e778e5dfc2d517ba9ae59958c8198fecf0e801108165b0e722 |
| 2 | 37ab4aefa3b89e88955bddd18c024454d0b0b929d93e2f380e20f499ef9f0612 |
| 3 | 13a95ff57fc4d6b97aec98a2cea133fcb944543e9d5421886be5e8b7bb7631a9 |
| 4 | de8c7b37f70b0356c91c2ac393453ebcab2031858e514fd24cadd083c0a7c19e |
| 5 | b428fe8eb83846ca1692f87dfcd5d3bc7a98bf5bc8c3f856cd1173fc9dcbfb5a |

## Exact current package/evidence/audit bindings

Audit hashes below use the gate's canonical JSON digest, not the pretty-printed file SHA256. Both are included in the portable ledger.

| Problem | Package hash | Evidence hash | Audit digest |
|---|---|---|---|
| 1008B | 40b9f71bd94f1cef60f0e69cdcff757c50e45e40be6e709bda99a4f34a2e0ff3 | bc146b91d402821658959be2327989a76ae375d8e9b0e2122df0930cf4b14be8 | 1b03861d3334aef99b293aeaa014ebf179973967cd8b19c3bee22b1847674954 |
| 102B | d4f6e0763d9743eff7a69d31c279df138ba7a3f0553ad596ffb3344b503d8107 | 2da36ecb7b62e8bd887d4b681a7803933bd9895eb5b5ddeaad3edbb2f3e33737 | c707045c90af5a947ec6f08919598249b0edb6284e9d778f0d568e783d0252fd |
| 106B | f284db5df56d3868df95aaa3026c948039dfce35f52bcbedd55639fc006fe6d9 | 4435aa2c3afa10b08b22b92dc3961f8afca48fbf5060c84f4472006f391cb319 | ac0ab9f47f767f3bff71ca5316249ea684f66504165d1b5de4356a7b89319fc1 |
| 108A | f1a431592b2f7e84b49824bda7ef5b751481221d19a7e37a49164af4b5a69b32 | fc6a22018e2ecd9b8bc1c3d6067c3d18617c1f64b576bf40e0c4f395de1788ad | b03c85e9d13eae3a00f7c934a72c5280aa07ddb6b7c76df3cdb6889b28f3a9e2 |
| 109A | fbca5b1caa002abf282952c752d64f78998ec9cdd53b161339027baf2e65b2af | 4c01d6f2f46d45b9594ac4eec17db2803ec94578e7191a8faf295f3b2bdc287d | e64a4f62caeeb936c8b6230cecf00f912a4aa15be5df873516bb04eaf93883c8 |
| 118A | 60c98904834b75fcb4ee4a63b4350ea8ea0dedd2940b46406f79bad83a5e9f21 | 96707beb326b18a711efe860cd282e232b339ae364c6f1e746169294962d4130 | 4c1b7fbe20040a75fed085354b64a2f9df9de53d48604943ce5c83ae84d85e7e |
| 118B | e1ab40dc260613cc7c94c095847a3a16c786af68f8baa0d5f22c5a1507101adb | c881399192e53534e0653c3907a62a27739701aac2e9e9a92d3dc351a29c4110 | 60e40b6c5819a28d001e6d2fef87cda5ef16e2b3b2299152b384b19f9d5a02a0 |
| 122A | 87bfc290436e9548493c5a11f41eb6ff4684bdc97e9239d49857ecc5426831b5 | 17e9a9d669fb416ea49d95ce41970822b52974d19c120d29a9e00b65d88dad7d | f307eb281687e594edaf15e5c4d8185e935b67dea9e91a37d6b55f39bd80825c |
| 122B | 16bc3edca4643ec19cfa0f0bb7819e11689c44a1d6ae9f2b2564ee3c27520167 | 643b14c1b9a941f240c75e5698c7e21cfba8dff11b21dabb5fdd9ef370de4686 | 7322420c0dd2328d6937dff0b3971d19223f256611af054fa5f3005b32e3b189 |
| 124A | a9bb46f692e55e1a0a452e691f37ee00e51a0887c5015e26e7eb416316285b7c | dda70a0a73544a3937f68e9fc1310284d28754f4c601e986ccad52b286b3ec00 | 2d2a8238398dbd6bca660496dabe58d4bcc2cfec46af9d261318747747a73bc6 |
| 127B | dd4ed6a24def75a5e7f524373d5d0a0bea8b2018036acb512b13a19f7a9e6ee8 | b5ef9a5d0f0d0a250be7ad6b66e5b746ace734d24b4cd61cc7475c736db389b1 | c65edc6215e3d84e82f417bfc1036559ed08bfd8eb0acb3ec1437b9a8c1d37c2 |
| 131A | 86e1da085a3e51d84e5efd94dcf587413ceef62e33c9b7be60344fd6bf7f8bfe | 1da61bf2a6df5334517ad4207faeb7e40f54409873e265440d6187b4dfcfbd31 | 9e88746c49b874463121d1803406c26844dafd64bc87cf95f6a8f952ad7f19b5 |
| 137B | 1f29f4a3a9d8cb7e5078cbe12c286e2c19b20d39a84a2a475ec692d3da28911f | f754df59cee05180128644d0ae4ec50f77d594501f603368ebc6853cd9ce3512 | 7b26aec3ec2008ffd53859393dceab7a45fe199ee3ad1aff7edeabfae9c39441 |
| 139A | 9135bc545d4ac0f9f174eec2188b4d16165a8a47893671ffcf64aec338c05fec | 0589a9bf522d9ee11ee1c783acbfb6abfcdf7daabc40914c438f0ccf23441eaa | e90661b7ae6fe24185e633c9cb8afe0dac64b9fec764771c3c0f8b4e23939bdd |
| 13A | 60ca4616f583cb0629b7c77abc92ae62200789f6657f8cb0b6584d46b955bfec | 62eaf1c38fb6921a4f305c8d38a955282de2e8c3ff34dc5df8b040fced200314 | b9954ced2007b30e2514028ade0e62464097a932a64d035f0005d214aa9d8eaa |
| 143A | 680ae15c5e8361b4f41647aa9874c51a31340967612f4779e516127db781b4e1 | da579d3c6b97eb709f5a1621205a6708e88ca09bd2dec2474cfe48f9bda34d10 | c00df4ab2ec528f410ac9ddf91981a0f61778d2c2cb46c6c79e8ae9d33f725f9 |
| 165A | 78519d86b2c7e2353d5b01aef39cf12aee2f2457dbc0716adb5ed07e63acc928 | 3a2b59f0310f5fab7b7979c2745917fa17a38ae114268ef7e691c949a96943d8 | bf4590ba28dc4d8b90a0e37632693312566cbb6ac1395a2849a92407b42b82aa |
| 17A | 2c0981c3163fd9e02265a3c16efbdf4f28d406afc662462d068be6e9467b4c88 | ec9c0f04ae79a9893b10d447e60a57d6a62fe6e2314534d9dd96329c41d4b7f3 | 97b237df1d92b6bde5aa7bce5dccfe6596f6cb2c4e79ed2fa1f5a4af4afb2a50 |
| 182B | af1754e99f5e7aad17f2862b4324af969a78516df8f5dca9f32973705ba069a4 | 652465ba56c2c81c58c840f35e7d0e7fa76b5ba4094027f496f03b79baa29f28 | 860b11fb3c7ebb29d830d45b6bcc4d7c027154fe7d9f749210b1f0e4877fc49b |
| 195A | 12ad21a845103473afac3e223bb3c0de4ed70852e2be4d39693030e642746751 | eb2c140480846322f47a16c46a4a27b3fd1e97156ff11ef70e6bc7ede4d8a091 | 0527d66cd460f8574c966826b7fc03f77655dfbe8b20a6a1c49bde5498a9e01f |
| 1A | 1ea257e5de95e7d22c22ed6970f95cb26fd508781254c93c17da97de4d079611 | cf3f1911a153859f428c9065c79a6c41b7e38f136fc0353979892fd77fda0417 | f1fb8fbcce53b7332c95354488f44daaa687d5825d2b0f9bdb05e4f95cb4e873 |
| 237A | c5617acde74d2c94c76234e6b1dfd23611107cbd7de46ddbf1762b916c677512 | c3a4424bfc532f7c8d3a2cb79eb4401cde839bcfc49ddbf182d9a2fdefedf759 | 808744b07164ff93b419ef133dc9a4400484e77fca1e6e0b5b40249c15f3cfd9 |
| 259A | ee4db0c8e2753c5091b506b3952aeb01f1882f1552b3ae365f76e78cdde2c3fd | 8374d1edf8347ef023f98fef5dd1e50670ece8a99cfa0a3c6d96375bc915e356 | 7a0b2d9911363e6267507cd5c60fedc68bb4b790b8761d9a8fe6d64f1d4e55ea |
| 265B | a3b1b76311f69b9cc089c64a723ab7ed11e08146689424e82df9fb45f1210fb8 | ee7a4d6271bef242fcfea3683eb9e3d0e52a3b91ef02c983a43e50d4d7ae84ed | d19ffd08568ca18b23fefc76a4eac02f52d18ca842a176330316cecbf50f6286 |
| 268B | df7fdd298ce5da2e522e9dbec5a6c0c01a034f71d1d0b6381c447e6106e08619 | d0c41e752e4574c1b83c750017bbd0d49ddce98b85716859bd7958954418df80 | fc1fa1322151dfc9d7d92b6ad3def53ce17e236bf2a3af61c8c19b1e290d4e8e |
| 272A | 5de544c43f53c722b06f6b10a4431ef396312d660d126db032722154eca7fdb0 | e9ac0030be1b110d513dacee8d2c97d1f9687520f92ed0ee1f7f14d79f58eaef | 9323eb288b4f62cd820e8331112aca003d1f2b5b35501008eb46043e2120fff3 |
| 284B | bf9a5bd6a164511f70a3253dfe4502d406aaafaa076d4e2778b10307c984515e | 9ba7cd35cf28b7fbfb2e62a33b2b9ca2072e894d9776a4ce698662c8dbca7dcc | 077f86df14b8d51a5c14a75b54ddb24aaa7a489324818a02db9d8b967237d5cb |
| 29A | 3d7ea1d6e36765756774de5d7070e0926b7f325788e7082667a3fe7cd8bf8b31 | 7c2cb83292625f37a3f31227025051925e1e64acde64ae69e8fa41ecc59eae44 | bcc2284f1b442c7899c2abf252879ada8178a13ebae13d9e3e7accc4b19c85ea |
| 336A | 286f0d8ec7a77a34f1e92a17f715839e5a5dd28747aa1a4c23dc2d992396bdc3 | a6bd504523472fff4e02c2824eea0b8fe0c2493dc12f6f9b95650553c84cc1c0 | 49f32eb4a25964d48b1484bdb2863bde0824108343545e69df2c63ce7d8d7283 |
| 352A | d227439d10d7147cc06f78d79b4088b307f4c516890ecbe1fabeda062794fedf | cbb8bf3ec00c3877d9058f64d620fb62c9608e8d6d35d9150efb6775dbac9eec | e1c0c981c7e21f48389f8be81aa0644948df0d15818cd0932a1cfc8e28d83145 |
| 359A | e6b1afbf15b11c8338312ad36c52d4d2140273ed22a3c1bd6a1abe89ccd53ac8 | 0345b2785cb64f5bbeff2a17f5e1154ae4e636b1988a281b6aed82aea0be175b | 831f48fb1bd6b8463479b06892493b145bdafbed529be3f750b86d682f531792 |
| 368A | 9d8dafcd9b40563f00ed64ce1503b3eb4f3e1dcbed1d3c0c0ba1336cfccb71f7 | e1ccb53cbb03c8062e41b2d0ba341f2316808e3e65d79ee96daa6948ef318a9d | ef8a98bd4efa5d2da283cf6ff22b82bb0e379c1258f74f6f52c466796260bdcb |
| 371A | d785ab0eac33bf96ce2b92d7f16526dd1e63f482bcad2093473f6ba64233941d | dc83b3af6b703686028a2c0db2da81ab7dab14aa9b1512db4a17230fb81e12e6 | 82fbb28693ac735b7f097e1c773ee03ecf22cf0cb51d2693ee3ae08e61ff3f3a |
| 379A | 67d2173b0fc3131f80798e02618e24efc03177a80f0d1550dfdc13276cb5f3a8 | e22f95ad3d3735e701862610fa9d39d9241dda60941b8a43099e41fc4035862d | 2c2d12a3e4e0dec6ed52660be71c6c87ea29a9932f1ebbece583984bb709071b |
| 37A | 508d7b69a280220f9bf8f8bb18dfed137e4470ea4c9a6b0976d067698243537d | ee1b90bbbc376fab42543b29bafdb185370248854457812fc4d6a164957b8fd8 | 510d10ad044a07718cf1c1a36013a0c073d3a92b15f3c7c555f72442d84cef9f |
| 385A | 2ea7568593a75f6e5a4a65d10edbe119521b90c010ed982d7237c66dfc2481a5 | 7dbcadfa48a63c916ec4879a978e6e795c39f4040476ed315e62b12a2df339e5 | acd9f7feabaff6f1590abd66581db504d04dc557f1f8b1e4b4f7919fd13352f5 |
| 389A | 6c123170019c37f6ac4c997dedac2828908026aac787449f4ba53eae4ea8d555 | dcfd7f216eb9e194ab1c92259ee86a08ba57b67db8a02867997354f353e77d2e | 50a9f7ebf87e393d7d380a1e7dfddb123ddb3455720b7c7ea10789fea176c193 |
| 400A | b985ca7231f4cdb68d55f67dcf2dfc2127de3fd70f6fd671d420cb5fb6c4e613 | 63048c4214cf236344a2f837720d7329539277f1a94ffc315cdb30f917817edf | 68d70db3322c6a8d9985cb2164d7897327f8277cd738a2f9e4844485148328c3 |
| 404A | 19401735f6b770c3eea379edb0f663f48a0419c5d7db962047875d701454ace2 | 152aef05c5cb0435c294541af8463e1c254c4738260f2cfde294994a18d7c38f | 85bbf0f5bb20138fcd0462f560764f797ec139fa79c82d4f70cd0fea6c2d72b1 |
| 435A | 7f774264120b9af6fdf1814db43ac2c563cf9c242193b67b695f712efb626810 | 968e9fc014680022a3e71a134dc13a51d449b6a5c956c2c45fd4a62cc320b19e | c1bac6bef2d10017724ba71c4838a0c246f26cc34264db114a94f81e6055bfd0 |
| 441A | 67398e72be77c2c2ac85c68e07eaa6a4291d0f16cc783f493046b980deeda01b | d2bd02093d52db71ec63fb86fbd3488713e476176e5e4e20bcbb7732d6be0073 | 1486b70e5d5b47543a9798560fe4eee634d2b6706dfc3df0807e62cde0481daf |
| 447B | 3fbdc7dc3d6672328297300294d6af04a369f15d1039f8b03761a03f55a3bcf1 | 8b9c71200991c4015e2ddc48ab40e187b6dc73726a323a31a8a1be77bc412e6f | 28387fc3333e8258a3836b5fafab91172313093c74e7d112dcaf1989e7419c27 |
| 450A | 91acd3fdbe216b65b66fbdf2be817b00af1bf3bb00fe64c36326afde068ac70e | 44d39515c5a25f32be7ee77aa7dda757bc3363dbebb0364b29b966558fb22501 | 4e5da88689ef3644a1716c7dd58c1a4390dced0ae7e9572ba61f4dbef1de96ef |
| 452A | bd402fa430ba0a920ccdd15a4d1c071bf26eedadf66c566a1bab884913fd7223 | e583d661d3b2ef1552fb046acc7de4a5bea869d44e91c3fc493d4072c3b3b511 | 7f7d845d3c9da2daedfe0d37c83975b9f9db7b27241827a95082c96d35ef04b2 |
| 462A | e2e4907a156e55bb8b92f70f8ba41cfda159b2f9097f39d5178540461307c70e | 5e19b0606e34054a046948b3b7435d5dcfba415e75eea0a8649f8b1c10fe0100 | 27c937d309fc4a4b69f2e980bba56a7e9c16798c48311bb6786dfcb9384f4ec7 |
| 465B | 46c3db0d5cd79df16a7096ba49587973d53de424e1813285d9f9d2f6967e0fac | 5bb9a8477d584432725d510d1a85fde2ff2c6b195851fae16765096357ba30f4 | 415ed42589e5d7d2dcea955487f33a60e5a1f965c0b50d20198fccddb0b96c5a |
| 476A | e2d2a50b8dd1e4a550207f7c5d9fc3b136eb44a69545a2a91796276f5a3c61bb | 59dc701e8a026d9ccdb78771b1ea32cfbb834a6af373e3ad6f3fa8e1a99d3189 | 5f55594e7210cca49a0a5505c0c84b9926b02093391d1f5d467e0100b720e760 |
| 479A | fc92df438cf70c821c8b402350aa235973e232a9ba10d7758bf8833b0ddfdd01 | c480a6caf1f2e99e29b605eb72b85d07f70155fc6863a025ee6ae33713b7a2f4 | bc8bbb4ee84c72e7ec0cd63ef1ecb58bff93291f519b71378ae177b29abc9132 |
| 500A | b59cd58d7bf666a1b84086a21dbff717fcccaa42d8f3857d83fb83a103f727dd | 030941a8b2742fa80a4b1fb9ab7bc89f07de9f124d54f8bfbdf3ae085e5e30b5 | c99466fe87bd1c625d31b6c1fa471e6beb5f834ab44aa3e2fbd081212380dcb6 |
| 515A | aaf5c70868f5c4e327ec20c2f067bbac3ffb0ba49071bcc23c91efc2c9ea3f08 | 6f303b69fe331c8fa0e05e67bd3368401ef98cf1b0c113ce1a0e2aa6abdc5252 | f8dbdf129d21e6f8bcc84717143ef633f1c818e51927e3acee3c7358f0b6098e |
| 535A | 23afed7a6bf11c69ba04554b757573e7d8d410b4336f30253228007dd318f181 | 31a5bbef6ea4e6c00e95af7b78c11f851d1719717557c9ee18ef36ba16b4b4a9 | edfe732c90d80b3a951f1ed8b838d7fdcd5a85e8da232114de4baeb56df99b5b |
| 560A | c14876b5bad3c1544176112f3dfdf4a29c9344ab0d12154f165433dcfb7cffcf | b9c601b9de791641b531525dd74f7fa5bb9ebb6884290c340a34201893f309e4 | d0933db690162abbccf4a6ba5cd90e8fece6f10bd027f878c4ded34402653859 |
| 577A | 286e65c397681c278c31bb3d5caab4802d1173f41c5e6c25f161bec979f0a179 | 71dca1dbeb74bd59c7906ca3a2f762bf16b4c976e2eebb56e46b7f9092f620d5 | 5b18cc5608805a8c4a9288d92d0e2af8229e793dee4847b37064cc6aa58c7225 |
| 579A | 8c30d7420bc61cd90df44c45ac6d09f7da6e8a209a14cf6874592b1daf863aba | 716a4a08cd10bb271e5c1800cbc41211ada38596539bc7dc3cfc527a7e39d8bb | fcd3ca65de9609090bfc5a8f624ca0aae276e6398be4f570edc0be0684da9fcf |
| 583A | 532fc724c3f54558233b22a2c90bbb4b61aaeee0b1a31333d13fb2b1e4a983d6 | 3a348f057b5697678046fe875952c130927e25d6c95cdcf77b4b4b9bcdc154eb | 43dca125cb4e6ed7a28b28c6b0baec23df161904a3b52a6d5ce7c147d3176b66 |
| 58A | 237517c4292f6eb19c48fc8296cf64c3ce85b6bf132e009b991170ca798b3c46 | c933881a77f8c6a188382e837f070a3eb3b7e86bfcb72c5f6421d0a507d93ea8 | a63a525ca750d635dca5a055f471d94e97cbaf5e59cc730f8e6d425468193d19 |
| 604A | 769f20acfd28295017353da6e1ef4ad30e0d4b25ab27625d3e5bd0037ce841e2 | 9626aa55ba0901e223a30a2316f8c914f29bd3843c923c5f3f669047686d7259 | 5b4ddd2933e8a71d98075f859c842de11b624ab994646fd7b7143b73bb89a5bb |
| 608A | 22c7f4926d72bd86c7b800c0b1b9196f95367c4256a8f3e03aa68971e983486d | 701b65832e42c51d8fffc230c310ae98e071bc8271f1aad5c97994cb59ddbabd | f81003c28fc8af82998bf0af72457e538797d06fa422f5373af3065d781b3bd4 |
| 610A | 1f9bda35697a9e86d48d14154b414cf89d2dc4e02fb76c9490476cd9ffa88e73 | 6b29c72bc908f5e630cd3046c8c654d09a1870602522c10db13ad912f8c88eff | 72cdb003a2a85bc97a249ddf83c2da9ad780928849af5f8cf8306ef11c57262e |
| 616B | 6b7e99a69bf32ba191dd382dec3e2d64e1e5951d8152373f8249cf3d94443c3b | 564ea9b8a848f7e59537e75e5179679f217d7a07b41bd65ae4431376d93adf74 | 16ef140c1f78e68d16fb9a351d012d44ec8f1f9cbd314f1038cfbf6d5c347e90 |
| 620B | 3cc913e73b7d812bf63368a5f75160c9fbce970942218507d307b1474b180bf2 | a9c24bb1d64ee144a53fbe778666dfe7f3deaae60a107f8074def048ae7de98b | d19bebd90df9ed702befdf2ab5e26e8fb2e28154bd8a65b22558e933bb54027e |
| 622A | abc4cefe14dc583402fc15f5170b99be56c1f381c1ac2901daa7b319faaacb24 | e69e306ec0c2c77823bd1af9fa6ee1deb8f70369c869f3540a058839677da9d4 | 0fdb3d3f69bd2096da81f3936cb11ab625475acd32f25225ab49d1681ccf8189 |
| 626A | 26905b9171b4bce3607459400dff0477a1a8b87ce3c164e7cecc23d7a6d0c619 | 8e1b4e0803d15a75e75c7b9063dcec695642b44d54a0903939b9add23e011227 | 9a75970a50741dd52a72c63bb31de21402d76de063ab3c9065d446a7debf8884 |
| 628A | 149e1b5fe16013b057e07a84a494d8d09a3b7f3f89a9bbd710776abe582622f9 | 46462e0dccc2ec27dcdd249fd35f205900ad019bf5d15fe95e4cf9c17faea215 | d2a158506859305685205111ed91ff6b8f430fb731a92387db02c1aadf638c4e |
| 637A | 6090464f82cd21581f9b0c98ca11d633bcaf1bad291778693356354fee46f36a | ed806cd79e53ffbc1479da65e302d7ada3b4bd682a6e6511ce9ae55b1103a602 | 493d4568b4e16e7931106611f51380040fd4051655f50eace681341833014f56 |
| 641A | 6a445c772aced377d1670d6238271eeea7dc5c4d37f19b61f30026415b655802 | 516fe6a8d146b9f9809f8fb8671cbbff44dbc4ff537e515808d1beec334f768e | 499e44c10a2b64787e5c07b9330f130b4c2513b4bc650fd83bee172bcd1c251b |
| 659A | 2ef4ccd6cb2eb582d6273e8ac60bd86b057594000a224c5f7f241cc17d0f9367 | cbe248d690131ead9e939d0d567b02c1a1598b3ea3df4a4b3f84fd1d7d602ae0 | 4320b6add4d530543c7a32df9dba95d689c65a3c29d5dd4a555f3a4b2d3893ae |
| 660B | 9097d82cd198d484fcad41f982450d3120c3106d60e6f1d2e6694b6bd9d02517 | 95f68dae2163dcd63dab3027efe1cb7edd0dc69340000b48e216dd7a4d1b3e5c | a17f102acce047f5db45193c16e508296250b00347c0bb697d0ba8f93c61dc7f |
| 670B | 578f0685ba9246c36972b08ef42245b994c98bedc91467c7c26afe0e1a0bfbee | 8e644a591e53cf35acf63dc46d768eed0e28bff77528bef908d4bed0b4ad7323 | 3032347e223286a3f8f8e538e1484c0c39c990adef9f7f783b3532e757c4c92e |
| 680B | a9ea5a819daba9e029ea90a4711b1b2fc388ec2ba0d7fd049450504ff71dc9f8 | d57c707b9f3348e046f71a95678bad88c9f054f483665af8c8eb0d34b8f5a62b | b357c1322c976b52bbcf3da3d117b3401a80c3940764401c945c78ca57b063ab |
| 69A | 5140681dbcdeb337f0247885a0e625ada97779a0289f79c56e26529b9bd63460 | 26c6c801303243bf9f2112268345c1559d999234aacd3c7420fb5dc9bb4c4edb | f4c00b419ea728fa52795a741a53fd1c9a0dcfb0519045d9db3f644ce1eb11ec |
| 724A | 1b9220f0f5a62edddfaffb881823b53a2888b1b878cc670e4f474247f4507a69 | 60d87efe929dace0608e2b0027c1b5840b58360f8e062dcdb6c06fab7749927d | 88904781f5eced04d6805510a1eaa288599175813e9b63a12b78be71fe06376c |
| 725A | eee36c69a6c27b46219c07dd2a90569541dcd6c6c3b55ced1348f36a893e592b | 3e2dfafd95228a361d0972244677339acdbcc1fabb87a7360c6203d57c842b9b | caee7e3bc7a29a00998e6a79f3b96e66e2b9b42cf84f1e39f2976c387b5164ad |
| 727A | 52e597a39b8d483a790caec4da460741c2ab611eb010d92573f88d1354437a64 | 2915fdd79ba865bbcb27d017c9dfc4763231570653cd05b705734d4361014f57 | a06e242225b466609baa8decedc6644017e627e9d25dff7337afda779e0329ca |
| 733A | 839d224744502e7381b55a8a67af1543329ec3ee1538de9ddb7bbb6a5f133ca0 | 7b9b24ce37bafc03ea6d802e476fdcf163423f7ef4a05f9bcbfd439a3b977f81 | ea7786adabb3fe0a4c023e733e3c716f80002e9f71a82936c9cb752215035fd0 |
| 742A | cfffcf49ff3298dd127601c5b9b4d7c9264a8b2882954c5cabfeb1efcc16b8bf | 07fa39ec6dcf0e4a9ca977b62bf900fe05f0d92b0f91af1f940e8ce59c3ab185 | 59b4f1c898899a71c3b4977a51059cd39f20aa5a7126ec75e0ce1a9c99566139 |
| 74A | 77d2aa21611cf45738645468daa934261a4d69fe7b22b08c49148233872e9f6f | ed130f43e6647843ff95f1533736ca788ad538168f6e3f26e69e645c2d3c2708 | 2296c7d43c5f82e302b202779adf830696728254c9014e3df0e0f753cc468efb |
| 757A | 3b5deb84f980fa696f5fe88c1474c9d93b4fd9d784dec3faece320f5f386953a | bf052ebbfd5c5ebdcbd27064042aa0141789a84866b141e4002e9d8bf714e911 | c969e339d79360b119cace7cd1676cc87584b6d983e3a785084d9fe1c23a45a9 |
| 75A | 831899d95a681dabdeaa1260b9a67e79b7670ec7003b780f0028ae86495badf9 | 2bc359b81641741503f8a9ad91f7e3b9e88ce599ee3788866bf9bcf666e3fc1e | f9d912e2d14ab0e7ecbd355477ab8e56a6b01d77dc18add4a945010f4eb440a9 |
| 761A | 199d2b9c582a46ed58200a931a9bb6b5e537da4c0132f65eaaf58ef1d6ae72af | 73e31ff0a5ed0eeccb3d657259e8ef82d21d4576c123434507d1c32b01cfb701 | 8b7f7d2c56863b9f8d83806b33403bcec8f16c73835f585419d0f6b3e7335c28 |
| 766B | cb9a0fbedcb54fcca2a5c6ac093255e20819db708e2b58612523b47d2abfae3b | d4c768f9edfff7125c59495d93717d42db584e2fa309be23f352bc066a15307f | 1b7b86a1c4caaff2a60468cea3af1fecaea6a1f42c26ed4a9288fb2c828a1473 |
| 777A | ee59cda1b04ffd95595bb46cff0bf5911e2da7b91aa6137cc751fd3ddfe242d8 | ae071554db384a397e76537d8ad24ba11fde910167534bf2417c94570d9fe2fb | 61da42cb9eb75708431e9ddd85cc02c74967e1d1954ec4962c3cdb5e2a8c3524 |
| 779A | 638a10337406c872e42d93b8f94332f7b6717651c2645aa25fb3a01a1bef5344 | 359eee185dfa42bab69177b50e45aad0ac4d481551ea6cd6b43593e189d09537 | dfe2fea0355f6ed07fa0e31df440690d5428caa21fd01f8a25a6612d127ee88d |
| 798A | 9274601f27db897c8fd31ff84524a8d56143b3f1977b5fd8d5692f2c428e4077 | bf6a1aea13a087bf278534b45abb5fccfebc0d1f002fb9ab0fa0a6b7ee940387 | 94734986895b96f37a2f1e364747e3f6fcafc9a04cabe737166e6531e7622295 |
| 804A | 7d65a572104baad58fa9187f1ca4986cca2c1a2efccac797e2ad9574534dcfa2 | c8c3bfc4cce31ade56ce542264f7b29bea20e4812840a9f76a574740344ef1bd | 726853f2e9e2e6faad8a287b0002d661ff3ff73e5451641ba044e974e70cd5b3 |
| 831A | 84ce1ec9195dd9a5b50910148c8254d98541d0e1255f96908126553ad8168a98 | a234c2caad21a6052fd8b6949b6421eb5c5041ddf9958c3ba9c8e7076933f940 | 3a6d64850a2f8ac95aeec52423d47cf101e67c83f68229b80474f79d7bf82e5a |
| 847M | 3e2b956a13763cfd6b2f19478c76b598c994ef8163f26ff00508ec043f087163 | 851e5e099ce96e6dab4e0955d1b6e7d8f6688ff163c2cb02a5443774b94d2ace | 6201234bc8dec6039042a187fc9211fb5c8de263e8731c52b434390338fd6de8 |
| 849A | b7c7f2d00c95d214eae166faded576393f8dbcca9e49f81d9c2a4e78781604ce | 645d7206cc951a75f4fbd7a7dc4921d4002253ff038e67b3a5b5a79f09d9070a | a814d6a5dcaee4f1e4ab44e1dd67144c7e3cb3e620f583b49881a9f91977d925 |
| 859B | 6279d00b1b5a864d4a9d43e3fda1e23eb0c7b9f9c5feb8cc924e0d9347e88b4e | 54f4632cf3ee9abe6d583f5523b85a71e398d4e943afda8c511ac70f3127d3d3 | 994f28f537434be95d2349bec126751af1214cf79b4e0787ee1e3472a6737904 |
| 862A | ddb123a34d1792eb027784e4c7442fbf01c8901ba9004bc349582f956b70c671 | 06d513ffa09d8e6d858cdee26175b280024430c572e9c79f7c1fce3a90a6e7d6 | 6339fad36c83a0a180f54c6e16c907e9dbb2afd73a21f767bf203b31a614cfb2 |
| 864B | c43295ed01e5048b2c0c47103a987749e99e352cf359bf6d802bebb6a9d63927 | 8982ce91e61e8461f45ea16426337f3204d1f65f71ab085c12f1b16d079eeaec | 8f1b35404b6bb3bde0d4f96c845802e5a610145eac5b6f457f73f7a65a10de2e |
| 886A | 8fdfe3ac3aa4a64658c143d752fd5fad678a5a2c30c9afe8ada57d8feb84dc1d | 3e0a41bf09f8769a8df590035084baee868117f6613313ba9ae2e9adbe444e2c | 150dd51bc92d3886963bd707c9477f8a155537fd203735927a6927ff0aa8b7e6 |
| 886B | f43db6a384a91dde29d1aa14c553b835e85767d3e119908e3b403b5e58d65c46 | 9c5d1e35bf9e2dbadc057c22b72042bc9786dc2dc85bec8e5442029acd5ae412 | 3d821f5f4bcf3972c6a75cccc8ee7cddaddb83164c61add61ee809e771162060 |
| 887A | 6e6a96f28817bf503cc5650a903f39747d3fb02fae600b7ed28aa305900ffa0a | 48166fd892b54b1699a97612058baf1b3bfd39fdaf0e8c1f5755b42c9e740515 | a15fa9866df3ac7be5f57bcab84da3601be96815321aca5fedc7a5d0869002d7 |
| 888B | 4fff83e4bff47364ee2c666117b77c42b5e730f89d3921aebef833dc090b8ee7 | 667db4432e7ce636f41c89754d60c98173fbde8a2f237ddb90ff0c28184e5be6 | 764ac84c0a7e7285e31a0cf2264b9ad02f573b0b19e67ad857ec5a0424b2c16e |
| 893B | f3a3457655ccf93a72c4539b49add9073588af9ae369f511da2827aa2ebe3fee | fd8cd8c1f99626b56071f09c14ef95129286dc4349c5fee66223938100440227 | 0b1678a37a4a2166bf4f66897074f5975bff12be55d1062a27d1e8f8a6eb1983 |
| 909A | c3243abe0ade608760aa8c43fed189b2caf87084ef21365019ab5524b6c5bcb3 | a4c623b22a6af89f2d1aaa9fc68cc798af0c9df3814dc1f0ca568c4e411cee60 | f20a49bceff538262efc96e79de8ec0109809c107ee420625143f603b38902e1 |
| 90A | 60b0f5e63bb1499c8ed5291498b6254043080f678875f1baaea85c86948e2210 | 70b9da7e763c2f013e94608e99b5e734c0555ddafd2ad6cde54a19c47fd494f6 | 7dcdd2f5975cff9222c30ac5d179aedacf39501c5c9c83adffd99a38b9e0fd40 |
| 920A | c61e3f5934301943db4307bd1077add19bdc448a001a1fb144b7a9d4853073f7 | 0a437365509dc46a7980a01da96645e38e7919b08243fdb3981b41e13343b802 | cbc506fce289228b5c41c15cfbe872ef4b5b66da43f9d7e73b1745865cc8ca83 |
| 967B | 208d6eee527c0c17e6dff6ac3fd57aaec84ed83771c89753c4ce8b933ac19297 | 8909363586f35692a3cc252a71f4d4aa436a78a43b8754d83be9fc6c5e01284f | 7eabd604bcc47c8c3cfa096b43815f6157e4b524e599ae0a981f51fe97ef0d2e |
| 979A | 769f987efa3a8eab45f04416fd9c2f4f218a9ab9315b1a13650c7448ec49ab95 | ef92dd10c5aebdb1368059ba40f4d7b68aa51fdff5b4737b8fb65c4f1c201cf7 | d6725eb5f7a8c80012a1a37285cbfe3960abd628321099cd2b429977e4862a83 |
| 990A | 1a4460c0481814d6b86bdd5312b54280fa9f6cbae24da018fbea43959bf8ab8e | 90f3157a12b57d60526b6d3c4ebefdfd5216ad00c407f639ee5a2f8558bc75c2 | 3e22d31c4c837067adee3b1ea7d9ea14771eaff5f2f247cc70601c4fe6fca49a |
| 991A | e3ddceb9464f4b7751000a99051993c84a1f7aaf2a910df1a0980214cc73bc66 | 8f5a184678b0f0c4c6f6e18b1f2a3b485f7bf70382b2910a4498394421444505 | 0baeaf0dbf3afaf0bfc26f170336d0bcb22b034607ef0b4c03600e544b650a15 |

## Limits and publication

The independent foundation 691A may be added only by the parent using its exact separately audited immutable bytes and deduplicating it. It is not included in these 52.
All current technically qualified packages must still pass the parent's independent current-byte replay and a separate explicit package/evidence/audit-bound publication approval. No PR, merge, deployment, remote database/storage mutation or publication was performed.
