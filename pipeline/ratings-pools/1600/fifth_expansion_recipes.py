"""Exact tree, permutation, path, fare, and alternating-sum suites."""
from bisect import bisect_left
from collections import deque
import itertools
import random


IDS = ('34D', '500B', '606B', '659E', '689B', '756B', '788A')
SEMANTICS = {
    '34D': 'n2..50000, distinct old/new roots1..n; supplied parent pointers form a tree. Rerooting gives a unique parent for every nonroot node; small trees independently checked using all-pairs distances.',
    '500B': 'n1..300, permutation1..n, symmetric binary adjacency with zero diagonal. Sort values within each connected swap component. Exhaustive reachable permutation states check the unique lexicographic minimum.',
    '606B': 'grid1..500 in each dimension, valid start, nonempty LRUD word length<=100000. First visits give each mine location its explosion time, while unvisited locations explode after the final command. Literal per-mine executions independently verify all counts.',
    '659E': 'n2..100000,m1..100000,simple undirected graph. Minimum zero-indegree vertices equals the number of acyclic connected components, including isolated nodes. Exhaustive edge orientations independently check the count.',
    '689B': 'n1..200000, sorted shortcuts i<=ai<=n. Neighbor moves cost1 and shortcuts are directed. BFS returns all shortest distances; complete weighted-graph Floyd-Warshall independently checks small domains.',
    '756B': 'n1..100000, strictly increasing distinct integer times0..1000000000. Tickets20/single,50/90minutes,120/1440minutes cover inclusive t..t+duration-1. Minimum prefix costs give incremental charges; exhaustive ticket-cover masks check each prefix.',
    '788A': 'n2..100000, signed values-1000000000..1000000000. Maximum alternating sum of adjacent absolute differences, always starting positive, checked against literal enumeration of every interval.',
}


def parse(pid, text):
    tokens = text.split()
    if not tokens:
        raise ValueError('empty input')
    if pid == '606B':
        if len(tokens) != 5:
            raise ValueError('robot arity')
        x,y,u,v = map(int,tokens[:4]); word = tokens[4]
        if not (1<=x<=500 and 1<=y<=500 and 1<=u<=x and 1<=v<=y and 1<=len(word)<=100000 and set(word)<=set('LRUD')):
            raise ValueError('robot constraints')
        return x,y,u,v,word
    n = int(tokens[0])
    if pid == '500B':
        if not 1<=n<=300 or len(tokens)!=1+2*n:
            raise ValueError('permutation arity')
        values = list(map(int,tokens[1:n+1])); matrix = tokens[n+1:]
        if sorted(values)!=list(range(1,n+1)) or any(len(row)!=n or not set(row)<=set('01') for row in matrix):
            raise ValueError('permutation/matrix constraints')
        if any(matrix[i][i]!='0' or any(matrix[i][j]!=matrix[j][i] for j in range(n)) for i in range(n)):
            raise ValueError('matrix symmetry/diagonal')
        return values,matrix
    a = list(map(int,tokens))
    if pid in ('689B','756B','788A'):
        upper = 200000 if pid=='689B' else 100000
        if not (2 if pid=='788A' else 1)<=n<=upper or len(a)!=n+1:
            raise ValueError('array arity/range')
        values = a[1:]
        if pid=='689B' and (any(not i<=v<=n for i,v in enumerate(values,1)) or values!=sorted(values)):
            raise ValueError('shortcut constraints')
        if pid=='756B' and (not all(0<=v<=1000000000 for v in values) or any(x>=y for x,y in zip(values,values[1:]))):
            raise ValueError('travel time constraints')
        if pid=='788A' and not all(-1000000000<=v<=1000000000 for v in values):
            raise ValueError('signed array constraints')
        return values
    if pid=='659E':
        if len(a)<2:
            raise ValueError('graph header')
        m=a[1]; edges=list(zip(a[2::2],a[3::2]))
        if not (2<=n<=100000 and 1<=m<=100000 and len(a)==2+2*m):
            raise ValueError('graph arity/range')
        if not all(1<=u<=n and 1<=v<=n and u!=v for u,v in edges) or len({tuple(sorted(e)) for e in edges})!=m:
            raise ValueError('graph loops/duplicates')
        return n,edges
    if len(a)!=n+2 or not 2<=n<=50000:
        raise ValueError('tree arity/range')
    old,new=a[1:3]
    if not (1<=old<=n and 1<=new<=n and old!=new):
        raise ValueError('root constraints')
    edges=[(i,p) for i,p in zip((j for j in range(1,n+1) if j!=old),a[3:])]
    if not all(1<=p<=n and i!=p for i,p in edges):
        raise ValueError('parent range/self-loop')
    parent=list(range(n+1))
    def find(u):
        while parent[u]!=u:
            parent[u]=parent[parent[u]];u=parent[u]
        return u
    for u,v in edges:
        x,y=find(u),find(v)
        if x==y:
            raise ValueError('parent graph cycle')
        parent[x]=y
    return n,new,edges


def answer(pid, data):
    if pid=='500B':
        values,matrix=data;n=len(values);seen=set();result=list(values)
        for start in range(n):
            if start in seen:
                continue
            component=[start];seen.add(start)
            for u in component:
                for v,c in enumerate(matrix[u]):
                    if c=='1' and v not in seen:
                        seen.add(v);component.append(v)
            for i,v in zip(sorted(component),sorted(values[i] for i in component)):
                result[i]=v
        return result
    if pid=='606B':
        x,y,u,v,word=data;seen={(u,v)};result=[1]
        for c in word:
            u=max(1,min(x,u+(c=='D')-(c=='U')))
            v=max(1,min(y,v+(c=='R')-(c=='L')))
            result.append(int((u,v) not in seen));seen.add((u,v))
        result[-1]+=x*y-len(seen)
        return result
    if pid=='659E':
        n,edges=data;adj=[[] for _ in range(n)]
        for u,v in edges:
            adj[u-1].append(v-1);adj[v-1].append(u-1)
        seen=set();trees=0
        for start in range(n):
            if start in seen:
                continue
            component=[start];seen.add(start);degree_sum=0
            for u in component:
                degree_sum+=len(adj[u])
                for v in adj[u]:
                    if v not in seen:
                        seen.add(v);component.append(v)
            trees+=degree_sum==2*(len(component)-1)
        return [trees]
    if pid=='689B':
        n=len(data);distance=[-1]*n;distance[0]=0;queue=deque([0])
        while queue:
            u=queue.popleft()
            for v in (u-1,u+1,data[u]-1):
                if 0<=v<n and distance[v]<0:
                    distance[v]=distance[u]+1;queue.append(v)
        return distance
    if pid=='756B':
        costs=[0]
        for i,t in enumerate(data):
            costs.append(min(costs[-1]+20,costs[bisect_left(data,t-89,0,i+1)]+50,costs[bisect_left(data,t-1439,0,i+1)]+120))
        return [y-x for x,y in zip(costs,costs[1:])]
    if pid=='788A':
        positive=negative=best=0
        for i,(x,y) in enumerate(zip(data,data[1:])):
            d=abs(x-y)*(1 if i%2==0 else -1)
            positive=max(0,positive+d);negative=max(0,negative-d)
            best=max(best,positive,negative)
        return [best]
    n,new,edges=data;adj=[[] for _ in range(n+1)]
    for u,v in edges:
        adj[u].append(v);adj[v].append(u)
    parent=[0]*(n+1);parent[new]=-1;queue=[new]
    for u in queue:
        for v in adj[u]:
            if not parent[v]:
                parent[v]=u;queue.append(v)
    return [parent[i] for i in range(1,n+1) if i!=new]


def brute(pid, data):
    if pid=='500B':
        values,matrix=data;initial=tuple(values);seen={initial};queue=deque([initial])
        edges=[(i,j) for i in range(len(values)) for j in range(i) if matrix[i][j]=='1']
        while queue:
            state=queue.popleft()
            for i,j in edges:
                successor=list(state);successor[i],successor[j]=successor[j],successor[i];successor=tuple(successor)
                if successor not in seen:
                    seen.add(successor);queue.append(successor)
        return list(min(seen))
    if pid=='606B':
        x,y,u,v,word=data;result=[0]*(len(word)+1)
        delta={'L':(0,-1),'R':(0,1),'U':(-1,0),'D':(1,0)}
        for mine in itertools.product(range(1,x+1),range(1,y+1)):
            p,q=u,v;time=0
            while (p,q)!=mine and time<len(word):
                dx,dy=delta[word[time]];np,nq=p+dx,q+dy
                if 1<=np<=x and 1<=nq<=y:
                    p,q=np,nq
                time+=1
            result[time]+=1
        return result
    if pid=='659E':
        n,edges=data;best=n
        for mask in range(1<<len(edges)):
            incoming=[0]*n
            for i,(u,v) in enumerate(edges):
                incoming[(u if mask>>i&1 else v)-1]+=1
            best=min(best,incoming.count(0))
        return [best]
    if pid=='689B':
        n=len(data);dist=[[abs(i-j) for j in range(n)] for i in range(n)]
        for i,v in enumerate(data):
            dist[i][v-1]=min(dist[i][v-1],1)
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    dist[i][j]=min(dist[i][j],dist[i][k]+dist[k][j])
        return dist[0]
    if pid=='756B':
        totals=[0]
        for n in range(1,len(data)+1):
            times=data[:n];tickets=[]
            for i,t in enumerate(times):
                tickets.append((1<<i,20))
                for duration,price in ((90,50),(1440,120)):
                    tickets.append((sum(1<<j for j,s in enumerate(times) if t<=s<t+duration),price))
            costs=[10**9]*(1<<n);costs[0]=0
            for mask in range(1<<n):
                for cover,price in tickets:
                    costs[mask|cover]=min(costs[mask|cover],costs[mask]+price)
            totals.append(costs[-1])
        return [y-x for x,y in zip(totals,totals[1:])]
    if pid=='788A':
        return [max(sum(abs(data[i]-data[i+1])*(-1)**(i-l) for i in range(l,r)) for l in range(len(data)-1) for r in range(l+1,len(data)))]
    n,new,edges=data;dist=[[n]*n for _ in range(n)]
    for i in range(n):dist[i][i]=0
    for u,v in edges:dist[u-1][v-1]=dist[v-1][u-1]=1
    for k in range(n):
        for i in range(n):
            for j in range(n):dist[i][j]=min(dist[i][j],dist[i][k]+dist[k][j])
    return [next(v if u==i else u for u,v in edges if i in (u,v) and dist[(v if u==i else u)-1][new-1]==dist[i-1][new-1]-1) for i in range(1,n+1) if i!=new]


def extras(pid):
    rng=random.Random(16008000+IDS.index(pid));cases=[];seen=set()
    def add(text,reason,category='adversarial'):
        if text in seen:return
        seen.add(text);out=answer(pid,parse(pid,text));cases.append({'input':text,'output':' '.join(map(str,out))+'\n','reason':reason,'category':category})
    def array(values,reason,category='adversarial'):
        add(str(len(values))+'\n'+'\n'.join(map(str,values))+'\n',reason,category)
    def graph(n,edges,reason,category='adversarial'):
        add(f'{n} {len(edges)}\n'+''.join(f'{u} {v}\n' for u,v in edges),reason,category)
    def permutation(values,edges,reason,category='adversarial'):
        n=len(values);matrix=[['0']*n for _ in range(n)]
        for u,v in edges:matrix[u-1][v-1]=matrix[v-1][u-1]='1'
        add(f'{n}\n'+' '.join(map(str,values))+'\n'+'\n'.join(''.join(row) for row in matrix)+'\n',reason,category)
    def tree(n,old,new,edges,reason,category='adversarial'):
        parents=answer('34D',(n,old,edges))
        add(f'{n} {old} {new}\n'+' '.join(map(str,parents))+'\n',reason,category)
    if pid=='34D':
        tree(2,1,2,[(1,2)],'minimum reroot','boundary')
        for old,new in ((1,50000),(50000,1),(25000,25001)):
            tree(50000,old,new,[(i,i+1) for i in range(1,50000)],'maximum-depth reroot','maxSize')
        tree(50000,1,50000,[(1,i) for i in range(2,50001)],'maximum-degree reroot','maxSize')
        for _ in range(150):
            n=rng.randint(3,80);old,new=rng.sample(range(1,n+1),2)
            tree(n,old,new,[(i,rng.randint(1,i-1)) for i in range(2,n+1)],'fixed-seed distinct roots and branches')
    elif pid=='500B':
        permutation([1],[],'singleton permutation','boundary')
        permutation([3,2,1],[(1,2),(2,3)],'transitive swaps required','boundary')
        for edges in ([],[(i,i+1) for i in range(1,300)],list(itertools.combinations(range(1,301),2)),[(i,i+2) for i in range(1,299)]):
            permutation(list(range(300,0,-1)),edges,'maximum300-node disconnected/path/dense/parity graph','maxSize')
        for _ in range(150):
            n=rng.randint(3,30);values=list(range(1,n+1));rng.shuffle(values)
            permutation(values,[e for e in itertools.combinations(range(1,n+1),2) if rng.randrange(4)==0],'fixed-seed swap components')
    elif pid=='606B':
        for s in ('L','R','U','D','LR','URDL'):
            add('1 1 1 1\n'+s+'\n','singleton grid blocked moves','boundary')
        for s in ('R'*100000,'LRUD'*25000,('R'*499+'D'+'L'*499+'D')*100):
            add('500 500 1 1\n'+s+'\n','maximum grid and command length/first-visit vs final explosion','maxSize')
        for _ in range(150):
            x,y=rng.randint(1,30),rng.randint(1,30);u,v=rng.randint(1,x),rng.randint(1,y)
            add(f'{x} {y} {u} {v}\n'+''.join(rng.choice('LRUD') for _ in range(rng.randint(1,150)))+'\n','fixed-seed boundaries/revisits/unvisited mines')
    elif pid=='659E':
        graph(2,[(1,2)],'minimum tree','boundary');graph(4,[(1,2),(2,3),(3,1)],'cyclic component plus isolated node','boundary')
        graph(100000,[(1,2)],'maximum isolated cities','maxSize')
        graph(100000,[(i,i+1) for i in range(1,100000)],'maximum-depth tree','maxSize')
        graph(100000,[(i,i+1) for i in range(1,100000)]+[(100000,1)],'maximum n/m single cycle','maxSize')
        for _ in range(150):
            n=rng.randint(3,35);possible=list(itertools.combinations(range(1,n+1),2));rng.shuffle(possible)
            graph(n,possible[:rng.randint(1,len(possible))],'fixed-seed trees/cycles/disconnected components')
    elif pid=='689B':
        for values in ([1],[1,2],[2,2],[4,4,4,4]):array(values,'minimum/self/direct shortcuts','boundary')
        for values in (list(range(1,200001)),[200000]*200000,[min(200000,((i-1)//100+1)*100) for i in range(1,200001)]):
            array(values,'maximum200000 directed shortcuts','maxSize')
        for _ in range(150):
            n=rng.randint(3,100);values=[]
            for i in range(1,n+1):values.append(max(values[-1] if values else 1,rng.randint(i,n)))
            array(values,'fixed-seed monotone shortcuts with backwards neighbor travel')
    elif pid=='756B':
        for values in ([0],[1000000000],[0,1,89,90,91],[0,1439,1440],[0,10,20,30,40,50,60]):
            array(values,'minimum/time bounds/exact ticket expiry/prefix fare transition','boundary')
        for values in (list(range(100000)),[i*10000 for i in range(100000)],list(range(999900001,1000000001))):
            array(values,'maximum100000 distinct times/dense vs separated tickets','maxSize')
        for _ in range(150):
            n=rng.randint(3,100);array(sorted(rng.sample(range(20000),n)),'fixed-seed fare transitions')
    else:
        for values in ([0,0],[-1000000000,1000000000],[0,1,0],[2,0,3,0,9],[7,7,7]):
            array(values,'minimum/equal/signed bound/alternation start parity','boundary')
        for values in ([-1000000000,1000000000]*50000,[0]*100000,[i*(1 if i%2 else -1) for i in range(100000)]):
            array(values,'maximum100000 terms and64-bit total','maxSize')
        for _ in range(150):array([rng.randint(-1000000000,1000000000) for _ in range(rng.randint(3,100))],'fixed-seed signed alternating arrays')
    return cases


def brute_checks():
    counts={pid:0 for pid in IDS};rng=random.Random(16009000)
    def check(pid,data):
        assert answer(pid,data)==brute(pid,data),(pid,data,answer(pid,data),brute(pid,data))
        counts[pid]+=1
    for n in range(2,7):
        for _ in range(40):
            edges=[(i,rng.randint(1,i-1)) for i in range(2,n+1)]
            for root in range(1,n+1):check('34D',(n,root,edges))
    for n in range(1,5):
        edges=list(itertools.combinations(range(1,n+1),2))
        for mask in range(1<<len(edges)):
            matrix=[['0']*n for _ in range(n)]
            for i,(u,v) in enumerate(edges):
                if mask>>i&1:matrix[u-1][v-1]=matrix[v-1][u-1]='1'
            for values in itertools.permutations(range(1,n+1)):check('500B',(values,[''.join(row) for row in matrix]))
    for _ in range(1000):
        x,y=rng.randint(1,4),rng.randint(1,4);check('606B',(x,y,rng.randint(1,x),rng.randint(1,y),''.join(rng.choice('LRUD') for _ in range(rng.randint(1,20)))))
    for n in range(2,6):
        edges=list(itertools.combinations(range(1,n+1),2))
        for mask in range(1,1<<len(edges)):check('659E',(n,[e for i,e in enumerate(edges) if mask>>i&1]))
    for n in range(1,7):
        for values in itertools.product(*(range(i,n+1) for i in range(1,n+1))):
            if list(values)==sorted(values):check('689B',values)
    for n in range(1,7):
        for values in itertools.combinations(range(12),n):check('756B',values)
    for _ in range(100):check('756B',sorted(rng.sample(range(5000),rng.randint(1,7))))
    for n in range(2,8):
        for values in itertools.product((-2,0,2),repeat=n):check('788A',values)
    return counts


def review(pid, tests, samples):
    failures=[]
    for name,pair in tests+samples:
        try:
            expected=list(map(str,answer(pid,parse(pid,pair['input']))))
            if expected!=pair['output'].split():failures.append({'test':name,'reason':'independent oracle disagreement','expected':expected[:15],'actual':pair['output'].split()[:15]})
        except (ValueError,IndexError) as exc:failures.append({'test':name,'reason':str(exc)})
    return failures
