import json, hashlib, sys, shutil, os
from pathlib import Path
ME = Path(__file__).resolve().parent; M11 = Path('/home/ubuntu/audit11/me')
WT = Path('/home/ubuntu/audit11/wt'); AUD = WT / 'pipeline/ratings-pools/1600/audits'
sys.path.insert(0, str(WT / 'pipeline'))
from pool_contract import digest
REL = 'pipeline/ratings-pools/1600/audits/history/correction-20261013'; BD = WT / REL
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
SIGN11 = ['495B', '597A', '86A', '741A', '373B', '665A', '678B', '559A', '910B']
SIGN7 = ['11B', '322B', '40B', '845B']
REVOKE = ['209A', '704A', '235A', '55B', '888D']
ARCH12 = Path('/home/ubuntu/audit12/x/1600/audits')
# bundle
if BD.exists(): shutil.rmtree(BD)
(BD / 'code').mkdir(parents=True)
for f in ['harness.py', 'harness_c582.py', 'launcher.py', 'launcher_c582.py', 'judge.py', 'compare.py']: shutil.copy(M11 / f, BD / 'code' / f)
for f in ['harness_witness.py', 'witness.py', 'witness_full.py', 'wanalyze.py', 'wfull_analyze.py', 'mktuples.py', 'mkfinal.py', 'proofs_a.json', 'proofs_b.json']: shutil.copy(ME / f, BD / 'code' / f)
for d in ['replay', 'replay-lf', 'replay-c582', 'replay-c582-lf']: shutil.copytree(M11 / d, BD / d)
for d in ['witness', 'witness-full']: shutil.copytree(ME / d, BD / d)
for f in ['replay-summary.json', 'harness-equivalence.json']: shutil.copy(M11 / f, BD / f)
for f in ['witness-full-analysis.json', 'proof-tuples.json', 'witness-strict-class.json']: shutil.copy(ME / f, BD / f)
shutil.copy(M11 / 'original-runs/original-runs.tar.gz', BD / 'original-runs.tar.gz')
code = {f'code/{p.name}': sha(p) for p in sorted((BD / 'code').iterdir())}
T = json.load(open(ME / 'proof-tuples.json')); summ = json.load(open(M11 / 'replay-summary.json')); eq = json.load(open(M11 / 'harness-equivalence.json'))
H = {'tok': '1dd7efd4776d4d8f0eb30512e4182274d33b1bd28c0a2abbffa41c137685d4a9', 'c582': 'c582ff42561c5181591b7fef36aa3ac550cffbcb09dd45135e7ea9a522983d0d', 'witness': sha(ME / 'harness_witness.py')}
assert code['code/harness.py'] == H['tok'] and code['code/harness_c582.py'] == H['c582']
SANDBOX_FLAGS = ("Pinned python@sha256:5887f265d8d44d8b4734d3658b21d668edf5aaf92e4945bc0c984afbfab105d3, --pull=never, --network=none, --read-only, --user=65534:65534, --cap-drop=ALL, "
    "no-new-privileges, pids<=32, 1 CPU, 2560m memory/swap, tmpfs /w 128m and /tmp 16m, inputs and harness mounted read-only, RLIMIT_CPU/AS at problem limits, RLIMIT_FSIZE 16MiB, "
    "launched from env -i (PATH only) without credentials; g++ -O2 -std=c++17 -DONLINE_JUDGE; python3 for Python sources.")
WIT = (f"Proof witnesses: each incorrect source re-run on its evidence failedTest with CRLF->LF normalized input by {REL}/code/witness.py (sha256 {code['code/witness.py']}) mounting "
       f"{REL}/code/harness_witness.py (sha256 {H['witness']}; identical to myharness_tok.py except it also returns the full output base64), classified by "
       f"{REL}/code/mktuples.py (sha256 {code['code/mktuples.py']}): qualifies only if exit code 0, no timeout, same token count as expected and at least one token numerically different (format/debug-only/CRLF/TLE/wrong-problem excluded).")
sys.path.insert(0, str(M11)); import importlib.util
spec = importlib.util.spec_from_file_location('mk', M11 / 'mkcorrect.py')
src = open(M11 / 'mkcorrect.py').read(); ORIG = {}
exec(src.split('summ = json.load')[0].replace("__file__", repr(str(M11 / 'mkcorrect.py'))), g := {}); ORIG = g['ORIG']
def proofs(pid):
    ks = sorted(k for k in T if k.startswith(pid + '/'))
    assert len(ks) == 5 and all(T[k]['qualifies'] for k in ks), pid
    return {k.split('/')[1]: T[k] for k in ks}
out = {'base': '3e2cdd3f1770c770adb17221878548006b827c7c', 'bundle': REL, 'codeSha256': code, 'signed': {}, 'revoked': {}}
def preserve(pid, srcbytes):
    old = digest(json.loads(srcbytes)); hp = AUD / 'history' / pid / f'{old}.json'
    hp.parent.mkdir(parents=True, exist_ok=True)
    if hp.exists(): assert hp.read_bytes() == srcbytes
    else: hp.write_bytes(srcbytes)
    return old, hp
for pid in SIGN11 + SIGN7:
    p = AUD / f'{pid}.json'
    srcb = p.read_bytes() if p.exists() else (ARCH12 / f'{pid}.json').read_bytes()
    a = json.loads(srcb); old, hp = preserve(pid, srcb)
    if pid in SIGN11:
        a['review']['sandbox'] = (f"Corrected 2026-10-13 (supersedes auditHash {old}). Fresh full replay of all 10 sources on every package test and sample, plus LF-only-input replay of the 5 incorrect, "
            f"with own harness myharness_tok.py sha256 {H['tok']} ({REL}/code/harness.py), launched by {REL}/code/launcher.py sha256 {code['code/launcher.py']}, judged by {REL}/code/judge.py sha256 {code['code/judge.py']} "
            "(full-output token sha256 vs expected; WA counted only when numerically wrong); not worker pool_harness. " + SANDBOX_FLAGS + ' ' + WIT)
        rb = {sid: d['resourceBoundaryOnly'] for sid, d in summ[pid].items() if d['resourceBoundaryOnly']}
        eqd = [d for d in eq['differences'] if d['record'].startswith(pid + '-')]
        a['review']['harnessCorrection'] = {
            'supersededAudit': {'auditHash': old, 'fileSha256': sha(hp), 'path': str(hp.relative_to(WT))},
            'originalError': "Superseded review.sandbox stated 'Own harness (sha256 c582ff42...983d0d)' for all replays.",
            'originalActualRuns': ORIG[pid].replace('harness-correction-20261013', 'correction-20261013') + f' All original runners/checkers/records: {REL}/original-runs.tar.gz (sha256 {sha(BD / "original-runs.tar.gz")}).',
            'harnessDifference': "myharness.py (c582ff42) vs myharness_tok.py (1dd7efd4) differ only on line 32, the per-test result append: tok adds 'tokSha' (sha256 of whitespace-joined output tokens) and 'outBytes', computed after the process exited from the same captured bytes. Compile command, rlimits, execution, timeout, rc, cpu and raw output 'sha' code are byte-identical. myharness_tail.py likewise only adds 'tail' and 'outBytes'; myharness_O0.py differs by -O0 (behavioral) and was supplementary only.",
            'verifiedEquivalence': (f"All 11 originally-attested IDs (normal + LF-only) were replayed with both myharness_tok.py and unchanged myharness.py c582ff42 ({REL}/code/launcher_c582.py): over {eq['pairs']} replay pairs / {eq['tests']} test executions raw output sha256 equal {eq['shaEqual']}/{eq['tests']}, "
                f"rc equal {eq['rcEqual']}/{eq['tests']}, timeout flag equal {eq['timeoutEqual']}/{eq['tests']}; the only differences are CPU-limit boundary flips on tests already past the first failure, outputs identical"
                + (f" (this ID: {json.dumps(eqd)})" if eqd else " (none for this ID)") + f". Judgment is equivalent ({REL}/harness-equivalence.json)."),
            'freshReplayResult': ("All 10 sources: verdict and first failed test equal evidence and every per-test raw output sha256 equals evidence"
                + (f" except resource-limit-only TLE/RE differences after the first failure {json.dumps(rb)}" if rb else '')
                + f"; all 5 incorrect are numerically wrong on their recorded first failing test and fail there identically with LF-only inputs; samples run cleanly. Records {REL}/replay*/{pid}-*.json, summary {REL}/replay-summary.json."),
        }
        a['review']['freshReplay'] = summ[pid]
    else:
        a['review']['proofCorrection'] = {'supersededAudit': {'auditHash': old, 'fileSha256': sha(hp), 'path': str(hp.relative_to(WT))},
            'reason': 'Re-signed 2026-10-13 to add per-reference source-level proof tuples; replay sandbox statement unchanged (original runs used the stated harness).', 'witnessHarness': WIT}
    a['review']['incorrectProofs'] = proofs(pid)
    a['review']['incorrectAreAlgorithmic'] = ('Each of the 5 incorrect sources was read in full; review.incorrectProofs gives, per source, the implemented algorithm, faulty source line numbers with their text, and a legal LF '
        'witness on the evidence failedTest with normal exit, expected vs actual and source/input/expected/actual/proof sha256. ' + WIT)
    p.write_text(json.dumps(a, indent=2, sort_keys=True, ensure_ascii=False) + '\n')
    out['signed'][pid] = {'oldAuditHash': old, 'newAuditHash': digest(json.load(open(p))), 'fileSha256': sha(p), 'history': str(hp.relative_to(WT))}
RECO = {'209A': ['209A/30579897', '209A/37271596'], '704A': ['704A/20046740'], '235A': ['235A/6367509'], '55B': ['55B/5592269'], '888D': ['888D/58168625']}
for pid in REVOKE:
    p = AUD / f'{pid}.json'; srcb = p.read_bytes(); old, hp = preserve(pid, srcb); p.unlink()
    out['revoked'][pid] = {'auditHash': old, 'history': str(hp.relative_to(WT)), 'gaps': {k: {x: T[k][x] for x in ('pointerGap', 'excluded', 'recommendedWitness', 'faultyLines', 'faultyLineText', 'fault', 'proofSha256') if x in T[k]} for k in RECO[pid]},
                           'qualifyingIncorrect': f"{sum(T[k]['qualifies'] for k in T if k.startswith(pid + '/'))}/5"}
json.dump(out, open(BD / 'report.json', 'w'), indent=1, sort_keys=True, ensure_ascii=False)
print(json.dumps({k: (v if k != 'codeSha256' else len(v)) for k, v in out.items() if k != 'revoked'}, indent=1)); print({k: v['qualifyingIncorrect'] for k, v in out['revoked'].items()})
