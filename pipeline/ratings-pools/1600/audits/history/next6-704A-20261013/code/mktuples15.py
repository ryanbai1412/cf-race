import json, base64, hashlib, sys
from pathlib import Path
ME = Path(__file__).resolve().parent
sys.path.insert(0, '/home/ubuntu/audit11/wt/pipeline')
from pool_contract import digest
src = open(ME / 'wfull_analyze.py').read().split('out = {}')[0]
ns = {'__file__': str(ME / 'wfull_analyze.py')}; exec(src, ns); classify = ns['classify']
import witness15 as W
P = {**json.load(open(ME / 'proofs_a.json')), **json.load(open(ME / 'proofs_b.json'))}
FULL = json.load(open(ME / 'witness-full-analysis.json'))
GAP = {}
EXCLUDE = {}
CAVEAT = {}
SUBS = {(f'{j[0]}/{j[1]}'): j for j in W.jobs()}
T = {}
for key, j in sorted(SUBS.items()):
    pid, sid, base, sub, ft = j
    s = sub['source'].replace('\r\n', '\n').replace('\r', '\n').split('\n')
    r = json.load(open(ME / 'witness' / f'{pid}-{sid}.json')); t = r['tests'][0]; o = base64.b64decode(t['outB64'])
    exp = (Path(base) / f'packages/{pid}/tests/{ft}.out').read_bytes(); inp = (Path(base) / f'packages/{pid}/tests/{ft}.in').read_bytes()
    if key not in P: continue
    cls = classify(o, exp, t); p = P[key]
    tup = {'submission': key, 'language': sub['programmingLanguage'], 'sourceSha256': r['sourceSha256'], 'sourceLines': len(s),
           'implementedAlgorithm': p['algorithm'], 'faultyLines': p['faultyLines'], 'faultyLineText': {str(n): s[n - 1] for n in p['faultyLines']}, 'fault': p['fault'],
           'witness': {'test': ft, 'isEvidenceFailedTest': True, 'packageInputSha256': r['packageInputSha256'], 'lfInputSha256': r['lfInputSha256'], 'packageInputHadCRLF': r['packageInputHadCRLF'],
                       'input': inp.replace(b'\r\n', b'\n').decode()[:300], 'expected': exp.decode().strip()[:300], 'actual': o.decode(errors='replace').strip()[:300],
                       'expectedOutputSha256': r['expectedOutputSha256'], 'actualOutputSha256': t['sha'], 'actualOutputBytes': t['outBytes'], 'exitCode': t['rc'], 'timedOut': t['timeout'], 'cpuSeconds': t['cpu'],
                       'classification': cls, 'record': f'witness/{pid}-{sid}.json', 'harnessSha256': r['harnessSha256']}}
    ok = cls == 'MATH-WRONG' and t['rc'] == 0 and not t['timeout'] and key not in EXCLUDE
    tup['qualifies'] = ok
    if key in GAP:
        tup['pointerGap'] = GAP[key]; fm = FULL[key]['firstMathWrong']
        tup['recommendedWitness'] = {k: fm[k] for k in ('test', 'input', 'expected', 'actual', 'rc', 'timeout', 'cpu', 'packageInputSha256', 'lfInputSha256', 'expectedOutputSha256', 'actualOutputSha256')}
        tup['recommendedWitness']['record'] = f'witness-full/{pid}-{sid}.json'
    b = next(x for x in json.load(open(Path(base) / f'evidence/{pid}.json'))['submissions'] if str(x['submissionId']) == sid).get('algorithmicCounterexampleBinding')
    if b: tup['pointerRepair'] = {'previousFailedTest': b['previousFailedTest'], 'note': 'evidence failedTest rebound by worker to this witness; earlier failure ' + b['previousFailedTest'] + ' was format/debug-only', 'bindingMatchesWitness': b['lfInputSha256'] == tup['witness']['lfInputSha256'] and b['expectedOutputSha256'] == tup['witness']['expectedOutputSha256'] and b['actualOutputSha256'] == tup['witness']['actualOutputSha256'] and b.get('sourceSha256', b.get('sourceHash')) == tup['sourceSha256'] and (b.get('normalExit') is True or b.get('exitCode') == 0)}
    if key in EXCLUDE: tup['excluded'] = EXCLUDE[key]
    if key in CAVEAT: tup['caveat'] = CAVEAT[key]
    tup['proofSha256'] = digest(tup)
    T[key] = tup
json.dump(T, open(ME / 'proof-tuples.json', 'w'), indent=1, sort_keys=True, ensure_ascii=False)
from collections import defaultdict
by = defaultdict(list)
for k, v in T.items(): by[k.split('/')[0]].append(v['qualifies'])
print({k: f'{sum(v)}/{len(v)}' for k, v in by.items()})
for k, v in T.items():
    if not v['qualifies']: print('NOT', k, v['witness']['classification'], v.get('excluded', '')[:40])
