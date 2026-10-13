import json, sys
from pathlib import Path
ME = Path(__file__).resolve().parent
res = {'pairs': 0, 'tests': 0, 'shaEqual': 0, 'rcEqual': 0, 'timeoutEqual': 0, 'compiledEqual': 0, 'differences': []}
for sub in ('', '-lf'):
    for p in sorted((ME / f'replay{sub}').glob('*.json')):
        a = json.load(open(p)); b = json.load(open(ME / f'replay-c582{sub}' / p.name))
        res['pairs'] += 1; res['compiledEqual'] += a['compiled'] == b['compiled']
        ta = {t['name']: t for t in a['tests']}; tb = {t['name']: t for t in b['tests']}
        assert ta.keys() == tb.keys()
        for n in ta:
            x, y = ta[n], tb[n]; res['tests'] += 1
            for k, c in (('sha', 'shaEqual'), ('rc', 'rcEqual'), ('timeout', 'timeoutEqual')):
                if x[k] == y[k]: res[c] += 1
            if (x['sha'], x['rc'], x['timeout']) != (y['sha'], y['rc'], y['timeout']):
                res['differences'].append({'record': p.name, 'lf': bool(sub), 'test': n, 'tok': [x['rc'], x['timeout'], x['cpu'], x['sha'][:16]], 'c582': [y['rc'], y['timeout'], y['cpu'], y['sha'][:16]]})
json.dump(res, open(ME / 'harness-equivalence.json', 'w'), indent=1)
print({k: v for k, v in res.items() if k != 'differences'}, len(res['differences']))
for d in res['differences'][:20]: print(d)
