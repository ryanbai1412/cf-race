import json, base64, re, hashlib, sys
from pathlib import Path
from fractions import Fraction
ME = Path(__file__).resolve().parent
def num(t):
    try: return Fraction(t)
    except Exception: return None
def classify(out, exp, t):
    E = exp.split(); A = out.split()
    if t['timeout'] or t['rc'] != 0: return 'NOT-NORMAL-EXIT'
    if A == E: return 'AC'
    if len(A) == len(E) and all(a == e or (num(a.decode()) is not None and num(a.decode()) == num(e.decode())) for a, e in zip(A, E)): return 'FORMAT-ONLY'
    NA = re.findall(rb'-?\d+(?:\.\d+)?', out)
    if len(NA) == len(E) and all(num(e.decode()) is not None and num(a.decode()) == num(e.decode()) for a, e in zip(NA, E)): return 'FORMAT-ONLY'
    if len(A) != len(E): return 'TOKEN-COUNT-MISMATCH'
    return 'MATH-WRONG'
out = {}
for p in sorted((ME / 'witness-full').glob('*.json')):
    r = json.load(open(p)); B = Path(r['archiveBase']); pid, sid = r['key'].split('/')
    rows = []
    for t in r['tests']:
        o = base64.b64decode(t['outB64']); assert hashlib.sha256(o).hexdigest() == t['sha']
        n = t['name']; exp = (B / f'packages/{pid}/tests/{n}.out').read_bytes(); raw = (B / f'packages/{pid}/tests/{n}.in').read_bytes()
        c = classify(o, exp, t)
        rows.append({'test': n, 'class': c, 'rc': t['rc'], 'timeout': t['timeout'], 'cpu': t['cpu'], 'input': raw.replace(b'\r\n', b'\n').decode()[:200],
                     'expected': exp.decode().strip()[:100], 'actual': o.decode(errors='replace').strip()[:100],
                     'packageInputSha256': hashlib.sha256(raw).hexdigest(), 'lfInputSha256': hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest(),
                     'expectedOutputSha256': hashlib.sha256(exp).hexdigest(), 'actualOutputSha256': t['sha']})
    from collections import Counter
    mw = [x for x in rows if x['class'] == 'MATH-WRONG']
    out[r['key']] = {'counts': dict(Counter(x['class'] for x in rows)), 'firstMathWrong': mw[0] if mw else None, 'mathWrongTests': [x['test'] for x in mw],
                     'firstNonAC': next((x for x in rows if x['class'] != 'AC'), None), 'rows': {x['test']: x for x in rows}}
    print(r['key'], out[r['key']]['counts'], 'firstNonAC', out[r['key']]['firstNonAC']['test'], out[r['key']]['firstNonAC']['class'], '| firstMathWrong', json.dumps({k: v for k, v in (mw[0] if mw else {}).items() if k in ('test', 'input', 'expected', 'actual', 'rc', 'timeout')}))
json.dump(out, open(ME / 'witness-full-analysis.json', 'w'), indent=1, sort_keys=True)
k = '55B/5592269'
for t in ['0003', '0087', '0091', '0222']:
    print(k, json.dumps(out[k]['rows'][t]))
