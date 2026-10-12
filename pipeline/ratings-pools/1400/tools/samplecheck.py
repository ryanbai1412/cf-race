import sys,importlib,json,signal
sys.path.insert(0,'recipes'); import lib, rand_extra
for m in 'abcdef': importlib.import_module('probs_'+m)
def alarm(*a): raise TimeoutError
signal.signal(signal.SIGALRM, alarm)
for p in sys.argv[1:]:
    c=lib.REG[p]; f=getattr(c,'SMALL',None) or rand_extra.R.get(p)
    r=lib.rng(p+'-gen'); ok=set(); bad=0; err=None
    signal.alarm(60)
    try:
        for _ in range(400):
            s=f(r)
            if len(s)>20000: continue
            try: c.V(s); ok.add(s)
            except lib.Bad as e: bad+=1; err=str(e)[:60]
        signal.alarm(0)
        print(p,'distinct',len(ok),'bad',bad,err, flush=True)
    except TimeoutError: print(p,'TIMEOUT distinct',len(ok), flush=True)
