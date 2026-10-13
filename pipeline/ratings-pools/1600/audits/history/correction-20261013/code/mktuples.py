import json, base64, hashlib, sys
from pathlib import Path
ME = Path(__file__).resolve().parent
sys.path.insert(0, '/home/ubuntu/audit11/wt/pipeline')
from pool_contract import digest
src = open(ME / 'wfull_analyze.py').read().split('out = {}')[0]
ns = {'__file__': str(ME / 'wfull_analyze.py')}; exec(src, ns); classify = ns['classify']
import witness as W
P = {**json.load(open(ME / 'proofs_a.json')), **json.load(open(ME / 'proofs_b.json'))}
FULL = json.load(open(ME / 'witness-full-analysis.json'))
GAP = {
 '209A/30579897': 'evidence failedTest 0001 is format-only (prints 6.0 for expected 6); first legal LF math-wrong normal-exit test is 0004 (2 -> 4.0, expected 3)',
 '235A/6367509': 'evidence failedTest 0005 is format-only (prints 60.0 for expected 60); first legal LF math-wrong normal-exit test is 0032 (924 -> 783770988, expected 783776526)',
 '704A/20046740': 'evidence failedTest 0001 is format-only (Python list [1, 2, 3, 2] with correct numbers); first legal LF test with wrong numbers is 0003 (85 values, value #26 is 8, expected 9) but every output of this source is list-formatted, so replacing the source is cleaner',
 '888D/58168625': 'evidence failedTest 0002 is format-only (prints 7.0 for expected 7); first legal LF math-wrong normal-exit test is 0004 (5 4 -> 56.0, expected 76)',
 '55B/5592269': 'evidence failedTest 0003 prints intermediate values (2 3 4 ++), not an answer; first legal LF math-wrong normal-exit test is 0087 (1 1000 0 2 / + * + -> 1002, expected 1); 0091 and 0222 are the only other math-wrong tests',
}
EXCLUDE = {'209A/37271596': 'wrong-problem source: reads n as a character string and counts adjacent pairs; does not implement 209A; needs replacement'}
CAVEAT = {'209A/68858672': 'correct recurrence without the required modulo 1e9+7: printed integer is the unreduced count, not the requested residue (counted as a genuine output defect; flagged)',
          '209A/119337156': 'same missing-modulo defect as 68858672 (flagged)',
          '910B/33503406': 'also reads c[6] out of bounds (UB); outputs identical at -O0, -O2 and repeated -O2, and the in-bounds first-fit alone yields 3 bars on 0012',
          '845B/29655296': 'source 84% similar to 29655583 (same template, different final formula); different first failures and wrong-test sets',
          '845B/29655583': 'see 29655296 similarity caveat'}
SUBS = {(f'{j[0]}/{j[1]}'): j for j in W.jobs()}
T = {}
for key, j in sorted(SUBS.items()):
    pid, sid, base, sub, ft = j
    s = sub['source'].replace('\r\n', '\n').replace('\r', '\n').split('\n')
    r = json.load(open(ME / 'witness' / f'{pid}-{sid}.json')); t = r['tests'][0]; o = base64.b64decode(t['outB64'])
    exp = (Path(base) / f'packages/{pid}/tests/{ft}.out').read_bytes(); inp = (Path(base) / f'packages/{pid}/tests/{ft}.in').read_bytes()
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
