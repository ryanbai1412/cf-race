import hashlib, json, itertools, collections, random, heapq
from pathlib import Path

ROOT=Path(__file__).parent
IDS=['23B','34D','500B']
def sha(raw): return hashlib.sha256(raw).hexdigest()
def parse(pid, raw):
    lines=raw.decode().splitlines()
    if pid=='23B':
        t=int(lines[0]); a=[int(x) for x in lines[1:]]
        assert len(a)==t and 1<=t<=100000 and all(1<=n<=100000 for n in a)
        return a
    if pid=='34D':
        n,old,new=map(int,lines[0].split()); p=list(map(int,lines[1].split()))
        assert len(lines)==2 and 2<=n<=50000 and 1<=old<=n and 1<=new<=n and old!=new and len(p)==n-1
        par=[None]*(n+1);par[old]=0
        for v,k in zip([x for x in range(1,n+1) if x!=old],p):
            assert 1<=k<=n and v!=k;par[v]=k
        done={old}
        for v in range(1,n+1):
            seen=set();cur=v
            while cur not in done:
                assert cur not in seen; seen.add(cur);cur=par[cur]
            done.update(seen)
        return n,old,new,par
    n=int(lines[0]);p=list(map(int,lines[1].split()));a=lines[2:]
    assert 1<=n<=300 and sorted(p)==list(range(1,n+1)) and len(a)==n and all(len(x)==n and set(x)<=set('01') for x in a)
    assert all(a[i][i]=='0' for i in range(n)) and all(a[i][j]==a[j][i] for i in range(n) for j in range(i))
    return n,p,a

def answer(pid,raw):
    data=parse(pid,raw)
    if pid=='23B':
        out=[max(n-2,0) for n in data]
        proof={'method':'At most n-2 survive: n cannot survive because every initial degree has a departure round. If n-1 survived they must all initially have degree n-1 to avoid rounds through n-2; the sole departing vertex is then adjacent to every survivor and cannot leave before round n-1 either. For n>=3 take an (n-2)-clique joined to two mutually nonadjacent leaves: leaves depart at degree n-2, leaving the clique at already-passed degree n-3. n=1,2 leave nobody.','partySizes':data}
        return ('\n'.join(map(str,out))+'\n').encode(),proof
    if pid=='34D':
        n,old,new,par=data; original=par.copy();path=[];prev=0;cur=new
        while cur:
            nxt=par[cur];path.append(cur);par[cur]=prev;prev=cur;cur=nxt
        out=[par[v] for v in range(1,n+1) if v!=new]
        return (' '.join(map(str,out))+'\n').encode(),{'method':'Unique tree paths determine parents. Only edges on the old-root/new-root path reverse; all other parent edges remain unchanged. Follow original parent links from the new root and reverse them, saving the old next link before overwrite.','oldRoot':old,'newRoot':new,'reversedPath':path,'originalParents':original[1:]}
    n,p,a=data;parent=list(range(n))
    def find(x):
        while parent[x]!=x: parent[x]=parent[parent[x]];x=parent[x]
        return x
    for i in range(n):
        for j in range(i):
            if a[i][j]=='1': parent[find(i)]=find(j)
    groups=collections.defaultdict(list)
    for i in range(n):groups[find(i)].append(i)
    out=p.copy();details=[]
    for indices in groups.values():
        values=sorted(p[i] for i in indices)
        for i,v in zip(indices,values):out[i]=v
        details.append({'indices1Based':[i+1 for i in indices],'sortedValues':values})
    return (' '.join(map(str,out))+'\n').encode(),{'method':'Edge transpositions generate every permutation within a connected component (a path moves any chosen value between its endpoints); no value can cross components. Assign component values ascending to its ascending positions to get the unique lexicographic minimum. Components independently computed by union-find.','components':details}

def rawtree(n,edges,old,new):
    adj=[[] for _ in range(n)];par=[0]*n;q=[old];seen={old}
    for u,v in edges:adj[u].append(v);adj[v].append(u)
    for u in q:
        for v in adj[u]:
            if v not in seen:seen.add(v);par[v]=u+1;q.append(v)
    return (f'{n} {old+1} {new+1}\n'+' '.join(str(par[v]) for v in range(n) if v!=old)+'\n').encode(),adj

def rawperm(n,p,edges):
    a=[['0']*n for _ in range(n)]
    for u,v in edges:a[u][v]=a[v][u]='1'
    return (str(n)+'\n'+' '.join(map(str,p))+'\n'+'\n'.join(''.join(x) for x in a)+'\n').encode()

def crosschecks():
    counts=collections.Counter()
    for n in range(1,7):
        edges=list(itertools.combinations(range(n),2));best=0
        for mask in range(1<<len(edges)):
            adj=[set() for _ in range(n)]
            for k,(u,v) in enumerate(edges):
                if mask>>k&1:adj[u].add(v);adj[v].add(u)
            remaining=set(range(n))
            for degree in range(n):remaining-=set(v for v in remaining if len(adj[v]&remaining)==degree)
            best=max(best,len(remaining));counts['23B_graphs']+=1
        assert int(answer('23B',f'1\n{n}\n'.encode())[0])==best
    for n in range(2,6):
        for seq in itertools.product(range(n),repeat=n-2):
            deg=[1]*n
            for v in seq:deg[v]+=1
            edges=[]
            for v in seq:
                u=next(i for i in range(n) if deg[i]==1);edges.append((u,v));deg[u]-=1;deg[v]-=1
            u,v=[i for i in range(n) if deg[i]==1];edges.append((u,v))
            for old in range(n):
                for new in range(n):
                    if old==new:continue
                    raw,adj=rawtree(n,edges,old,new);d=[n]*n;d[new]=0;q=[new]
                    for u in q:
                        for v in adj[u]:
                            if d[v]==n:d[v]=d[u]+1;q.append(v)
                    want=[next(v+1 for v in adj[u] if d[v]==d[u]-1) for u in range(n) if u!=new]
                    assert list(map(int,answer('34D',raw)[0].split()))==want;counts['34D_root_pairs']+=1
    for n in range(1,5):
        edges=list(itertools.combinations(range(n),2))
        for mask in range(1<<len(edges)):
            chosen=[edge for k,edge in enumerate(edges) if mask>>k&1]
            for p in itertools.permutations(range(1,n+1)):
                seen={p};q=[p]
                for state in q:
                    for u,v in chosen:
                        t=list(state);t[u],t[v]=t[v],t[u];t=tuple(t)
                        if t not in seen:seen.add(t);q.append(t)
                assert tuple(map(int,answer('500B',rawperm(n,p,chosen))[0].split()))==min(seen)
                counts['500B_graph_permutations']+=1;counts['500B_reachable_states']+=len(seen)
    return dict(counts)

if __name__=='__main__':
    result={};failures=[]
    for pid in IDS:
        p=ROOT/'1600/packages'/pid;records={}
        for section in ['tests','samples']:
            out=[]
            for f in sorted((p/section).glob('*.in')):
                raw=f.read_bytes();expected,proof=answer(pid,raw);stored=f.with_suffix('.out').read_bytes()
                match=expected.split()==stored.split()
                if not match:failures.append([pid,section,f.stem])
                literal_ok=True
                if pid=='23B':a=parse(pid,raw);literal_ok=len(a)<=105 and max(a)<=105
                out.append({'test':f.stem,'inputHash':sha(raw),'storedOutputHash':sha(stored),'independentOutputHash':sha(expected),'expected':expected.decode(),'proofHash':sha(json.dumps(proof,sort_keys=True,separators=(',',':')).encode()),'outputMatches':match,'literalStatementBoundsLegal':literal_ok,'legalLF':b'\r' not in raw and raw.endswith(b'\n')})
            records[section]=out
        result[pid]=records
        print(pid,len(records['tests']),len(records['samples']),'mismatches',len(failures),'literal violations',sum(not x['literalStatementBoundsLegal'] for x in records['tests']),flush=True)
    brute=crosschecks();assert not failures
    (ROOT/'oracle-verification.json').write_text(json.dumps({'sourceHash':sha(Path(__file__).read_bytes()),'results':result,'crossChecks':brute,'failures':failures},indent=2)+'\n')
    print('Brute checks',brute,flush=True)
