import json, hashlib, sys, shutil
from pathlib import Path
ME = Path(__file__).resolve().parent; WT = Path('/home/ubuntu/audit15/wt'); AUD = WT / 'pipeline/ratings-pools/1600/audits'
X = Path('/home/ubuntu/audit15/x/1600')
sys.path.insert(0, str(WT / 'pipeline'))
from pool_contract import digest, publication_gate
REL = 'pipeline/ratings-pools/1600/audits/history/next6-704A-20261013'; BD = WT / REL
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
INTERIM = 'c23b7888cddcd86285f888e0e2cf2266aa7e4584ac4ba972e214a2583d403a4e'
if BD.exists(): shutil.rmtree(BD)
(BD / 'code').mkdir(parents=True)
for f in ['harness.py', 'harness_witness.py', 'launcher15.py', 'witness15.py', 'judge15.py', 'mktuples15.py', 'mkfinal15.py', 'proofs_a.json', 'parquet-check.json', 'NOTES.md']: shutil.copy(ME / f, BD / 'code' / f)
for d in ['replay', 'replay-lf', 'witness']: shutil.copytree(ME / d, BD / d)
for f in ['replay-summary.json', 'proof-tuples.json']: shutil.copy(ME / f, BD / f)
code = {f'code/{p.name}': sha(p) for p in sorted((BD / 'code').iterdir())}
T = json.load(open(ME / 'proof-tuples.json')); summ = json.load(open(ME / 'replay-summary.json'))
FLAGS = ("Pinned python@sha256:5887f265d8d44d8b4734d3658b21d668edf5aaf92e4945bc0c984afbfab105d3, --pull=never, --network=none, --read-only, --user=65534:65534, --cap-drop=ALL, no-new-privileges, "
         "pids<=32, 1 CPU, 2560m memory/swap, tmpfs /w 128m and /tmp 16m, inputs and harness mounted read-only, RLIMIT_CPU/AS at problem limits, RLIMIT_FSIZE 16MiB, launched from env -i (PATH only) without credentials; "
         "g++ -O2 -std=c++17 -DONLINE_JUDGE; python3 for Python sources.")
out = {'base': '8fcd0068e9d0d1d6d3551fcbe5c9358b6ded472b', 'bundle': REL, 'codeSha256': code, 'signed': {}}
for pid in ['704A']:
    hist = list((AUD / 'history' / pid).glob('*.json')); assert len(hist) == 1
    a = json.loads(hist[0].read_bytes()); old = digest(a); assert hist[0].stem == old
    ev = json.load(open(WT / f'pipeline/ratings-pools/1600/evidence/{pid}.json')); assert ev == json.load(open(X / f'evidence/{pid}.json'))
    a['evidenceHash'] = digest(ev); a['baseCommit'] = out['base']; a['archiveSha256'] = INTERIM
    a['review']['sandbox'] = (f"Re-signed 2026-10-13 after evidence pointer repair (supersedes revoked auditHash {old}). Fresh full replay of all 10 sources on every package test and sample, plus LF-only replay of the 5 incorrect, "
        f"with own harness myharness_tok.py sha256 {code['code/harness.py']} ({REL}/code/harness.py), launched by {REL}/code/launcher15.py sha256 {code['code/launcher15.py']}, judged by {REL}/code/judge15.py sha256 {code['code/judge15.py']}; "
        f"witnesses by {REL}/code/witness15.py sha256 {code['code/witness15.py']} mounting harness_witness.py sha256 {code['code/harness_witness.py']}; not worker pool_harness. " + FLAGS)
    a['review']['pointerRepair'] = {'supersededAudit': {'auditHash': old, 'fileSha256': sha(hist[0]), 'path': str(hist[0].relative_to(WT)), 'status': 'revoked in correction-20261013 (format-only pointer 20046740)'},
        'bytes': f"next6 archive sha256 {INTERIM} (68143474 bytes, 3303 members) verified; replayed directly from it; 704A evidence identical to worker 8fcd006 (digest {a['evidenceHash']}); all 10 sources byte-identical to pinned open-r1 shard train-00027 (sha256 a043ccb4...).",
        'change': '20046740 (format-only list output) replaced by authentic 20796252 (CF WRONG_ANSWER, passedTestCount 2); other 9 submissions unchanged.',
        'cpuBoundary': '20796252: 3 tests (0006-0028 range) exceed the 2.0 s CPU limit in my sandbox (~2.2 s; evidence ~1.2 s WA) with output sha256 identical to evidence; all after the first failure 0003, so verdict, first failure and witness are unaffected.'}
    a['review']['freshReplay'] = summ[pid]
    sub = {str(x['submissionId']): x for x in ev['submissions']}
    a['review']['submissions'] = [dict(id=sid, expected=sub[sid]['expected'], **{k: v for k, v in d.items() if k in ('compiled', 'evidenceFailedTest', 'evidenceVerdict', 'maxCpu', 'myFirstFailed', 'myVerdict', 'perTestEvidenceMatch', 'samplesOK', 'numericallyWrongTests', 'formatOrDebugOnlyWA', 'lfFirstFailed', 'lfNumericallyWrongTests')}) for sid, d in summ[pid].items()]
    a['review']['submissionProvenance'] = 'All 10 current sources byte-identical (sha256) to rows in pinned open-r1/codeforces-submissions shards (shard sha256 verified independently; 20796252 from train-00027 a043ccb4..., WRONG_ANSWER, passedTestCount 2); 20046740 excluded (format-only).'
    ks = sorted(k for k in T if k.startswith(pid + '/')); assert len(ks) == 5 and all(T[k]['qualifies'] for k in ks)
    a['review']['incorrectProofs'] = {k.split('/')[1]: T[k] for k in ks}
    a['incorrectAnalysis'] = {k.split('/')[1]: {'kind': 'wrong-answer', 'test': T[k]['witness']['test'], 'proofSha256': T[k]['proofSha256'], 'faultyLines': T[k]['faultyLines'],
        'reason': T[k]['fault'] + f" (LF witness {T[k]['witness']['test']}: expected sha {T[k]['witness']['expectedOutputSha256'][:16]}, actual sha {T[k]['witness']['actualOutputSha256'][:16]}, exit 0, no timeout)"} for k in ks}
    for c in ('deterministicGeneration', 'independentOracle', 'generatedBasis', 'algorithmicallyWrong', 'inputConstraints'): assert a.get('checks', {}).get(c) is True, c
    a['review']['incorrectAreAlgorithmic'] = ("Each of the 5 incorrect sources was read in full; review.incorrectProofs gives the implemented algorithm, faulty source lines with text, and a legal LF witness on the current evidence failedTest "
        "with exit 0, no timeout, equal token count and a numerically wrong answer, plus source/input/expected/actual/proof sha256. Format/debug-only, CRLF, TLE-only and wrong-problem failures are not counted.")
    p = AUD / f'{pid}.json'; p.write_text(json.dumps(a, indent=2, sort_keys=True, ensure_ascii=False) + '\n')
    out['signed'][pid] = {'oldAuditHash': old, 'newAuditHash': digest(json.load(open(p))), 'fileSha256': sha(p), 'evidenceHash': a['evidenceHash'], 'packageHash': a['packageHash']}
json.dump(out, open(BD / 'report.json', 'w'), indent=1, sort_keys=True)
print(json.dumps(out['signed'], indent=1))
