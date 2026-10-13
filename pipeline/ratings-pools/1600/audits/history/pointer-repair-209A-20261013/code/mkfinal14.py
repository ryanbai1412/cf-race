import json, hashlib, sys, shutil
from pathlib import Path
ME = Path(__file__).resolve().parent; WT = Path('/home/ubuntu/audit14/wt'); AUD = WT / 'pipeline/ratings-pools/1600/audits'
X = Path('/home/ubuntu/audit14/x/1600')
sys.path.insert(0, str(WT / 'pipeline'))
from pool_contract import digest, publication_gate
REL = 'pipeline/ratings-pools/1600/audits/history/pointer-repair-209A-20261013'; BD = WT / REL
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
INTERIM = '037b97756f0a45d2a20eb61326e7f3277f751adfe546db9793335563dd893178'
if BD.exists(): shutil.rmtree(BD)
(BD / 'code').mkdir(parents=True)
for f in ['harness.py', 'harness_witness.py', 'launcher14.py', 'witness14.py', 'judge14.py', 'mktuples14.py', 'mkfinal14.py', 'proofs_a.json', 'proofs_b.json', 'parquet-verified-130943124.json']: shutil.copy(ME / f, BD / 'code' / f)
for d in ['replay', 'replay-lf', 'witness']: shutil.copytree(ME / d, BD / d)
for f in ['replay-summary.json', 'proof-tuples.json']: shutil.copy(ME / f, BD / f)
code = {f'code/{p.name}': sha(p) for p in sorted((BD / 'code').iterdir())}
T = json.load(open(ME / 'proof-tuples.json')); summ = json.load(open(ME / 'replay-summary.json'))
FLAGS = ("Pinned python@sha256:5887f265d8d44d8b4734d3658b21d668edf5aaf92e4945bc0c984afbfab105d3, --pull=never, --network=none, --read-only, --user=65534:65534, --cap-drop=ALL, no-new-privileges, "
         "pids<=32, 1 CPU, 2560m memory/swap, tmpfs /w 128m and /tmp 16m, inputs and harness mounted read-only, RLIMIT_CPU/AS at problem limits, RLIMIT_FSIZE 16MiB, launched from env -i (PATH only) without credentials; "
         "g++ -O2 -std=c++17 -DONLINE_JUDGE; python3 for Python sources.")
out = {'base': '7c9dbe885dd8b9ede48cf2c509cd3af55d25adde', 'bundle': REL, 'codeSha256': code, 'signed': {}}
for pid in ['209A']:
    hist = list((AUD / 'history' / pid).glob('*.json')); assert len(hist) == 1
    a = json.loads(hist[0].read_bytes()); old = digest(a); assert hist[0].stem == old
    ev = json.load(open(WT / f'pipeline/ratings-pools/1600/evidence/{pid}.json')); assert ev == json.load(open(X / f'evidence/{pid}.json'))
    a['evidenceHash'] = digest(ev); a['baseCommit'] = out['base']; a['archiveSha256'] = INTERIM
    a['review']['sandbox'] = (f"Re-signed 2026-10-13 after evidence pointer repair (supersedes revoked auditHash {old}). Fresh full replay of all 10 sources on every package test and sample, plus LF-only replay of the 5 incorrect, "
        f"with own harness myharness_tok.py sha256 {code['code/harness.py']} ({REL}/code/harness.py), launched by {REL}/code/launcher14.py sha256 {code['code/launcher14.py']}, judged by {REL}/code/judge14.py sha256 {code['code/judge14.py']}; "
        f"witnesses by {REL}/code/witness14.py sha256 {code['code/witness14.py']} mounting harness_witness.py sha256 {code['code/harness_witness.py']}; not worker pool_harness. " + FLAGS)
    a['review']['pointerRepair'] = {'supersededAudit': {'auditHash': old, 'fileSha256': sha(hist[0]), 'path': str(hist[0].relative_to(WT)), 'status': 'revoked in correction-20261013 (format-only pointer 30579897, wrong-problem 37271596)'},
        'bytes': f"209A pointer-repair archive sha256 {INTERIM} (11012712 bytes) verified; all 1121 manifest/provenance members match; replayed directly from it. Package (incl. all 204 tests), statement and statement-source bytes identical to the previously signed 209A bytes; evidence, semantic, coverage, source-policy and package files identical to worker commit 7c9dbe8 (evidence digest {a['evidenceHash']}). semantic recipeHash changed only because more_recipes.py changed in 910B/845B lines; its 209A recipe text is identical. New source 130943124 verified byte-identical to pinned open-r1 shard train-00022 (sha256 f02c2771...) row (WRONG_ANSWER, passedTestCount 3).",
        'change': 'Source 37271596 (wrong-problem) excluded by hash-bound source policy and replaced by authentic 130943124; 30579897 failedTest rebound 0001->0004 with algorithmicCounterexampleBinding equal to my independent witness; other 8 submissions unchanged.'}
    a['review']['freshReplay'] = summ[pid]
    sub = {str(x['submissionId']): x for x in ev['submissions']}
    a['review']['submissions'] = [dict(id=sid, expected=sub[sid]['expected'], **{k: v for k, v in d.items() if k in ('compiled', 'evidenceFailedTest', 'evidenceVerdict', 'maxCpu', 'myFirstFailed', 'myVerdict', 'perTestEvidenceMatch', 'samplesOK', 'numericallyWrongTests', 'formatOrDebugOnlyWA', 'lfFirstFailed', 'lfNumericallyWrongTests')}) for sid, d in summ[pid].items()]
    a['review']['submissionProvenance'] = 'All 10 current sources byte-identical (sha256) to rows in pinned open-r1/codeforces-submissions shards (shard sha256 verified independently; 130943124 from train-00022 f02c2771..., WRONG_ANSWER, passedTestCount 3); 37271596 excluded by hash-bound source policy as wrong-problem.'
    ks = sorted(k for k in T if k.startswith(pid + '/')); assert len(ks) == 5 and all(T[k]['qualifies'] for k in ks)
    a['review']['incorrectProofs'] = {k.split('/')[1]: T[k] for k in ks}
    a['review']['incorrectAreAlgorithmic'] = ("Each of the 5 incorrect sources was read in full; review.incorrectProofs gives the implemented algorithm, faulty source lines with text, and a legal LF witness on the current evidence failedTest "
        "with exit 0, no timeout, equal token count and a numerically wrong answer, plus source/input/expected/actual/proof sha256. Format/debug-only, CRLF, TLE-only and wrong-problem failures are not counted.")
    p = AUD / f'{pid}.json'; p.write_text(json.dumps(a, indent=2, sort_keys=True, ensure_ascii=False) + '\n')
    out['signed'][pid] = {'oldAuditHash': old, 'newAuditHash': digest(json.load(open(p))), 'fileSha256': sha(p), 'evidenceHash': a['evidenceHash'], 'packageHash': a['packageHash']}
json.dump(out, open(BD / 'report.json', 'w'), indent=1, sort_keys=True)
print(json.dumps(out['signed'], indent=1))
