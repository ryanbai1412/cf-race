import json, re, hashlib, sys
from pathlib import Path
ME = Path(__file__).resolve().parent
BOUND = {'209A': 14}
def nums(s): return re.findall(r'-?\d+(?:\.\d+)?|infinity', s)
def judge(X, pid, s, r, names):
    mine = {t['name'][:-3]: t for t in r['tests'] if not t['name'].startswith('s')}
    samp = [t for t in r['tests'] if t['name'].startswith('s')]
    ev = {x['test']: x for x in s['runs']}
    first = None; rb = []; numwrong = 0; fmtonly = 0; ex = None; hm = 0; vs = {}
    for n in names:
        t = mine[n]; exp = (X / f'packages/{pid}/tests/{n}.out').read_text().split()
        v = 'TLE' if t['timeout'] else 'RE' if t['rc'] != 0 else 'AC' if t['tokSha'] == hashlib.sha256(' '.join(exp).encode()).hexdigest() else 'WA'
        vs[v] = vs.get(v, 0) + 1
        if ev[n]['outputHash'] == t['sha'] and ev[n]['verdict'] == v: hm += 1
        elif first is not None and v in ('TLE', 'RE') and ev[n]['verdict'] in ('TLE', 'RE'): rb.append({'test': n, 'evidence': ev[n]['verdict'], 'mine': v, 'rc': t['rc'], 'cpu': t['cpu']})
        if v != 'AC':
            first = first or n
            if v == 'WA':
                o = t['out'].split()
                if t['outBytes'] >= 200 and len(exp) > 1:
                    numwrong += 1; ex = ex or f'{n}: long output, token hash differs'; continue
                try: ok = len(o) == len(exp) and all(a == b or (b != 'infinity' and float(a) == int(b)) for a, b in zip(o, exp))
                except Exception: ok = False
                tail = nums(t['out'])[-len(exp):] if len(exp) else []
                dbg = tail == exp or (len(tail) == len(exp) and all(a == b or (b != 'infinity' and re.fullmatch(r'-?\d+(\.\d+)?', a) and float(a) == int(b)) for a, b in zip(tail, exp)))
                if ok or dbg: fmtonly += 1
                else:
                    numwrong += 1; ex = ex or f"{n}: {' '.join((X / f'packages/{pid}/tests/{n}.in').read_text().split())[:60]} -> {' '.join(o)[:50]}, expected {' '.join(exp)[:50]}"
    myv = 'AC' if first is None else ('TLE' if mine[first]['timeout'] else 'RE' if mine[first]['rc'] else 'WA')
    d = {'myVerdict': myv, 'myFirstFailed': first, 'evidenceVerdict': s['verdict'], 'evidenceFailedTest': s['failedTest'], 'perTestEvidenceMatch': f'{hm}/{len(names)}', 'resourceBoundaryOnly': rb,
         'verdictCounts': vs, 'maxCpu': max(t['cpu'] for t in mine.values()), 'samplesOK': all(t['rc'] == 0 and not t['timeout'] for t in samp), 'compiled': r['compiled']}
    if s['expected'] != 'OK': d.update({'numericallyWrongTests': numwrong, 'formatOrDebugOnlyWA': fmtonly, 'counterexample': ex})
    return d
def hm_ok(d, names):
    h = int(d['perTestEvidenceMatch'].split('/')[0])
    return h + len(d['resourceBoundaryOnly']) == len(names)
out = {}; bad = []
for pid, n in BOUND.items():
    X = Path(f'/home/ubuntu/audit{n}/x/1600'); e = json.load(open(X / f'evidence/{pid}.json'))
    names = [p['name'] for p in json.load(open(X / f'packages/{pid}/provenance.json'))['tests']['pairs']]
    out[pid] = {}
    for s in e['submissions']:
        sid = str(s['submissionId']); r = json.load(open(ME / 'replay' / f'{pid}-{sid}.json'))
        assert r['harnessSha256'] == hashlib.sha256((ME / 'harness.py').read_bytes()).hexdigest() and r['sourceSha256'] == s['sourceHash'] and r['compiled']
        d = judge(X, pid, s, r, names)
        good = hm_ok(d, names) and d['myVerdict'] == s['verdict'] and d['myFirstFailed'] == s.get('algorithmicCounterexampleBinding', {}).get('previousFailedTest', s['failedTest']) and (s['expected'] == 'OK' or d['numericallyWrongTests'] > 0) and d['samplesOK']
        if s['expected'] != 'OK':
            l = judge(X, pid, s, json.load(open(ME / 'replay-lf' / f'{pid}-{sid}.json')), names)
            d['lfFirstFailed'] = l['myFirstFailed']; d['lfNumericallyWrongTests'] = l['numericallyWrongTests']
            good = good and l['myFirstFailed'] == s.get('algorithmicCounterexampleBinding', {}).get('previousFailedTest', s['failedTest']) and l['numericallyWrongTests'] > 0
        out[pid][sid] = d
        if not good: bad.append((pid, sid, d))
        print(pid, sid, s['expected'], d['myVerdict'], d['myFirstFailed'], d['perTestEvidenceMatch'], d.get('numericallyWrongTests'), d.get('lfFirstFailed'), 'OK' if good else 'PROBLEM')
json.dump(out, open(ME / 'replay-summary.json', 'w'), indent=1, sort_keys=True)
print('PROBLEMS', bad)
