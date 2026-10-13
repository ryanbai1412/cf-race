import json, hashlib, sys, shutil
from pathlib import Path
ME = Path(__file__).resolve().parent; WT = Path('/home/ubuntu/audit13/wt'); AUD = WT / 'pipeline/ratings-pools/1600/audits'
X = Path('/home/ubuntu/audit13/x/1600')
sys.path.insert(0, str(WT / 'pipeline'))
from pool_contract import digest, publication_gate
REL = 'pipeline/ratings-pools/1600/audits/history/pointer-repair-20261013'; BD = WT / REL
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
INTERIM = 'ed0a85e8768f390805830fb341d2470de8e186e01c72d87f719d17f28c138298'
if BD.exists(): shutil.rmtree(BD)
(BD / 'code').mkdir(parents=True)
for f in ['harness.py', 'harness_witness.py', 'launcher13.py', 'witness13.py', 'judge13.py', 'mktuples13.py', 'mkfinal13.py', 'proofs_a.json', 'proofs_b.json']: shutil.copy(ME / f, BD / 'code' / f)
for d in ['replay', 'replay-lf', 'witness']: shutil.copytree(ME / d, BD / d)
for f in ['replay-summary.json', 'proof-tuples.json']: shutil.copy(ME / f, BD / f)
code = {f'code/{p.name}': sha(p) for p in sorted((BD / 'code').iterdir())}
T = json.load(open(ME / 'proof-tuples.json')); summ = json.load(open(ME / 'replay-summary.json'))
FLAGS = ("Pinned python@sha256:5887f265d8d44d8b4734d3658b21d668edf5aaf92e4945bc0c984afbfab105d3, --pull=never, --network=none, --read-only, --user=65534:65534, --cap-drop=ALL, no-new-privileges, "
         "pids<=32, 1 CPU, 2560m memory/swap, tmpfs /w 128m and /tmp 16m, inputs and harness mounted read-only, RLIMIT_CPU/AS at problem limits, RLIMIT_FSIZE 16MiB, launched from env -i (PATH only) without credentials; "
         "g++ -O2 -std=c++17 -DONLINE_JUDGE; python3 for Python sources.")
out = {'base': '75e70a8bc07249a2ba0a1771b749f21ae9270ad0', 'bundle': REL, 'codeSha256': code, 'signed': {}}
for pid in ['55B', '235A', '888D']:
    hist = list((AUD / 'history' / pid).glob('*.json')); assert len(hist) == 1
    a = json.loads(hist[0].read_bytes()); old = digest(a); assert hist[0].stem == old
    ev = json.load(open(WT / f'pipeline/ratings-pools/1600/evidence/{pid}.json')); assert ev == json.load(open(X / f'evidence/{pid}.json'))
    a['evidenceHash'] = digest(ev); a['baseCommit'] = out['base']; a['archiveSha256'] = INTERIM
    a['review']['sandbox'] = (f"Re-signed 2026-10-13 after evidence pointer repair (supersedes revoked auditHash {old}). Fresh full replay of all 10 sources on every package test and sample, plus LF-only replay of the 5 incorrect, "
        f"with own harness myharness_tok.py sha256 {code['code/harness.py']} ({REL}/code/harness.py), launched by {REL}/code/launcher13.py sha256 {code['code/launcher13.py']}, judged by {REL}/code/judge13.py sha256 {code['code/judge13.py']}; "
        f"witnesses by {REL}/code/witness13.py sha256 {code['code/witness13.py']} mounting harness_witness.py sha256 {code['code/harness_witness.py']}; not worker pool_harness. " + FLAGS)
    a['review']['pointerRepair'] = {'supersededAudit': {'auditHash': old, 'fileSha256': sha(hist[0]), 'path': str(hist[0].relative_to(WT)), 'status': 'revoked in correction-20261013 (format/debug-only evidence pointer)'},
        'bytes': f"pointer-repair-v2 archive sha256 {INTERIM} (10367758 bytes) verified; all 1745 manifest/provenance members match. For this ID the archive's packages (incl. tests), state, evidence, semantic, coverage, source-policy and statement-source bytes are identical to the replayed bytes (tests from interim22 9c314bfc..., evidence from worker commit 75e70a8, digest {a['evidenceHash']}).",
        'change': 'Only failedTest and a new algorithmicCounterexampleBinding changed for one incorrect submission; the binding hashes equal my independent witness (bindingMatchesWitness true).'}
    a['review']['freshReplay'] = summ[pid]
    ks = sorted(k for k in T if k.startswith(pid + '/')); assert len(ks) == 5 and all(T[k]['qualifies'] for k in ks)
    a['review']['incorrectProofs'] = {k.split('/')[1]: T[k] for k in ks}
    a['review']['incorrectAreAlgorithmic'] = ("Each of the 5 incorrect sources was read in full; review.incorrectProofs gives the implemented algorithm, faulty source lines with text, and a legal LF witness on the current evidence failedTest "
        "with exit 0, no timeout, equal token count and a numerically wrong answer, plus source/input/expected/actual/proof sha256. Format/debug-only, CRLF, TLE-only and wrong-problem failures are not counted.")
    p = AUD / f'{pid}.json'; p.write_text(json.dumps(a, indent=2, sort_keys=True, ensure_ascii=False) + '\n')
    g = publication_gate(X / 'packages' / pid, evidence_root=X.parent, require_approval=False) if (X / 'audits').exists() else None
    out['signed'][pid] = {'oldAuditHash': old, 'newAuditHash': digest(json.load(open(p))), 'fileSha256': sha(p), 'evidenceHash': a['evidenceHash'], 'packageHash': a['packageHash']}
json.dump(out, open(BD / 'report.json', 'w'), indent=1, sort_keys=True)
print(json.dumps(out['signed'], indent=1))
