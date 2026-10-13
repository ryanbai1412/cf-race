import json, base64, re, hashlib
from pathlib import Path
from fractions import Fraction
ME = Path(__file__).resolve().parent
def num(t):
    try: return Fraction(t)
    except Exception: return None
res = {}
for p in sorted((ME / 'witness').glob('*.json')):
    r = json.load(open(p)); t = r['tests'][0]; out = base64.b64decode(t['outB64'])
    assert hashlib.sha256(out).hexdigest() == t['sha']
    B = Path(r['archiveBase']); pid, sid = r['key'].split('/')
    exp = (B / f"packages/{pid}/tests/{r['test']}.out").read_bytes(); inp = (B / f"packages/{pid}/tests/{r['test']}.in").read_bytes()
    E = exp.split(); A = out.split()
    tokEq = E == A
    numEq = len(E) == len(A) and all(a == e or (num(a.decode()) is not None and num(a.decode()) == num(e.decode())) for a, e in zip(A, E))
    tailEq = len(A) > len(E) and (A[-len(E):] == E or all(num(a.decode()) == num(e.decode()) for a, e in zip(A[-len(E):], E)))
    diff = next((k for k, (a, e) in enumerate(zip(A, E)) if a != e and not (num(a.decode()) is not None and num(a.decode()) == num(e.decode()))), None)
    NA = re.findall(rb'-?\d+(?:\.\d+)?', out)
    numsOnlyEq = len(NA) == len(E) and all(num(a.decode()) == num(e.decode()) for a, e in zip(NA, E) if num(e.decode()) is not None) and all(num(e.decode()) is not None for e in E)
    normal = t['rc'] == 0 and not t['timeout']
    cls = ('NOT-NORMAL-EXIT' if not normal else 'AC?!' if tokEq else 'FORMAT-ONLY' if numEq or numsOnlyEq else 'DEBUG-TAIL-CORRECT' if tailEq else 'MATH-WRONG')
    res[r['key']] = {'class': cls, 'test': r['test'], 'rc': t['rc'], 'timeout': t['timeout'], 'cpu': t['cpu'], 'sourceSha256': r['sourceSha256'],
        'packageInputSha256': r['packageInputSha256'], 'lfInputSha256': r['lfInputSha256'], 'packageInputHadCRLF': r['packageInputHadCRLF'],
        'expectedOutputSha256': r['expectedOutputSha256'], 'actualOutputSha256': t['sha'], 'actualOutputBytes': t['outBytes'],
        'expectedTokens': len(E), 'actualTokens': len(A), 'firstDifferingToken': diff, 'numbersOnlyEqualExpected': numsOnlyEq,
        'input': inp.decode()[:300], 'expected': exp.decode()[:300], 'actual': out.decode(errors='replace')[:300],
        'atDiff': None if diff is None else {'expected': E[diff].decode(), 'actual': A[diff].decode()}}
json.dump(res, open(ME / 'witness-analysis.json', 'w'), indent=1, sort_keys=True)
for k, v in res.items():
    print(k, v['test'], v['class'], 'rc', v['rc'], 'to', v['timeout'], 'tok', v['actualTokens'], '/', v['expectedTokens'], 'diff@', v['firstDifferingToken'], v['atDiff'], repr(v['actual'][:60]))
