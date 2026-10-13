import json,sys
for k in sys.argv[1:]:
    e=json.load(open(f'/home/ubuntu/Documents/cf-pools/1400/evidence/{k}.json'))
    out=[]
    for it in e['excludedSubmissions']:
        if it.get('expected')=='OK':
            r=it.get('result') or {}
            if r.get('verdict') not in (None,'OK'):
                out.append(f"{it.get('submissionId') or r.get('submissionId')} {r.get('verdict')}@{r.get('failedTest')}")
    print(k, 'acceptedContradiction=',e['acceptedContradiction'], 'acc',sum(1 for s in e['submissions'] if s.get('expected','OK')=='OK' and s['verdict']=='OK'), '|', '; '.join(out[:6]))
