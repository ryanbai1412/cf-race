"""Exact-output recipes, strict domains, and small independent search checks."""
from collections import deque, Counter
from functools import lru_cache
import itertools
import math
import random

IDS = ('346A','372A','373B','495B','597A','626C','645C','678C','704A','712C','741A','913C','992B','440B','605A','593B')
SEMANTICS = {
    '346A': 'Distinct positive set, n2..100, values<=10^9. Difference closure is all positive multiples of gcd through max; parity of missing elements gives Alice/Bob. Exhaustive small minimax checked.',
    '372A': 'n1..500000, sizes1..100000. Disjoint kangaroo pairing with size ratio>=2; greedily pair sorted lower half with upper half. Small unrestricted matching independently checked.',
    '373B': 'Budget/start1..10^16, per-digit price1..10^9. Group consecutive integers by decimal digit length; stop at first unaffordable integer. Linear small-budget simulation checked.',
    '495B': 'a,b0..10^9. Equal values give infinity; a<b gives0; otherwise count divisors of a-b strictly above b. Independent direct modular enumeration checked.',
    '597A': 'k1..10^18; -10^18<=a<=b<=10^18. Exact floor division counts negative/zero/positive multiples. Direct interval enumeration checked.',
    '626C': 'n,m0..10^6, positive total. Distinct towers, heights multiples of2 or3; binary-search Hall capacity including union overlap. Exhaustive small slot assignments checked.',
    '645C': '1<=k<n<=100000, binary room string with at least k+1 zeros. Each optimal group uses consecutive free rooms; test free-room centers nearest its midpoint. Exhaustive room subsets checked.',
    '678C': 'n,a,b,p,q1..10^9. Exact integer inclusion-exclusion with lcm overlap and larger reward on shared tiles. Direct tile enumeration checked.',
    '704A': 'n,q1..300000, events1/2 use app1..n and type3 refers to existing notification prefix. Per-app clearing and monotone global prefix reproduce unique count after every event; independent full-list simulation checked.',
    '712C': '3<=y<x<=100000. Reverse triangle transformation greedily grows shortest side to min(x,other-sides-minus1). Small all-legal-triangle BFS checked.',
    '741A': 'n1..100, crush values1..n. f^(2t)=identity requires permutation; lcm of cycle lengths divided by gcd(length,2) is unique minimum. Direct function powers checked.',
    '913C': 'n1..30,L1..10^9,costs1..10^9. Normalize each power-of-two cost against two smaller bottles, then consider exact fills and overbuy at every bit. Independent unbounded-knapsack checked.',
    '992B': '1<=l<=r<=10^9,1<=x<=y<=10^9. Enumerate coprime factor pairs of y/x, scale by x, enforce range; ordered pairs counted. Direct gcd/lcm enumeration checked.',
    '440B': 'n1..50000, nonnegative match counts<=10^9, total divisible by n. Sum absolute prefix imbalances equals minimum adjacent transfers. Independent small-state transfer BFS checked.',
    '605A': 'Permutation1..n,n1..100000. Keep longest value-consecutive subsequence whose positions increase, move all remaining values to endpoints. Full small-permutation BFS checked.',
    '593B': 'n2..100000; strip bounds and distinct slope/intercept pairs within +/-10^6. Integer endpoint ordering reversal detects intersection strictly inside strip; endpoint-only ties excluded. Direct pair-product test checked.',
}


def parse(pid,text):
    v=text.split()
    if pid=='645C':
        n,k=map(int,v[:2]);s=v[2]
        if len(v)!=3 or not 1<=k<n<=100000 or len(s)!=n or set(s)-set('01') or s.count('0')<k+1: raise ValueError('hotel domain/arity')
        return k,s
    a=list(map(int,v))
    if pid in ('346A','372A','741A','440B','605A'):
        n=a[0];values=a[1:]
        lo,hi={'346A':(2,100),'372A':(1,500000),'741A':(1,100),'440B':(1,50000),'605A':(1,100000)}[pid]
        if len(values)!=n or not lo<=n<=hi: raise ValueError('array length/arity')
        low,high=(0,10**9) if pid=='440B' else (1,n) if pid in ('741A','605A') else (1,100000) if pid=='372A' else (1,10**9)
        if not all(low<=x<=high for x in values): raise ValueError('array values')
        if pid in ('346A','605A') and len(set(values))!=n: raise ValueError('distinctness/permutation')
        if pid=='440B' and sum(values)%n: raise ValueError('indivisible total')
        return values
    if pid=='704A':
        n,q=a[:2];events=list(zip(a[2::2],a[3::2]));generated=0
        if not 1<=n<=300000 or not 1<=q<=300000 or len(a)!=2+2*q: raise ValueError('notification arity/size')
        for t,x in events:
            if t not in (1,2,3) or not 1<=x<=(generated if t==3 else n): raise ValueError('invalid app/prefix/type')
            generated+=t==1
        return n,events
    if pid=='913C':
        n,L=a[:2]
        if not 1<=n<=30 or not 1<=L<=10**9 or len(a)!=n+2 or not all(1<=x<=10**9 for x in a[2:]): raise ValueError('lemonade domain/arity')
        return L,a[2:]
    if pid=='593B':
        n,x1,x2=a[:3];lines=list(zip(a[3::2],a[4::2]))
        if not 2<=n<=100000 or not -10**6<=x1<x2<=10**6 or len(a)!=3+2*n or len(set(lines))!=n or not all(abs(x)<=10**6 for x in a[3:]): raise ValueError('line domain/distinctness/arity')
        return x1,x2,lines
    count={'373B':3,'495B':2,'597A':3,'626C':2,'678C':5,'712C':2,'992B':4}[pid]
    if len(a)!=count: raise ValueError('scalar arity')
    if pid=='373B': valid=1<=a[0]<=10**16 and 1<=a[1]<=10**16 and 1<=a[2]<=10**9
    elif pid=='495B': valid=all(0<=x<=10**9 for x in a)
    elif pid=='597A': valid=1<=a[0]<=10**18 and -10**18<=a[1]<=a[2]<=10**18
    elif pid=='626C': valid=all(0<=x<=10**6 for x in a) and sum(a)>0
    elif pid=='678C': valid=all(1<=x<=10**9 for x in a)
    elif pid=='712C': valid=3<=a[1]<a[0]<=100000
    else: valid=1<=a[0]<=a[1]<=10**9 and 1<=a[2]<=a[3]<=10**9
    if not valid: raise ValueError('scalar range')
    return a


def answer(pid,data):
    if pid=='346A': return ['Alice' if (max(data)//math.gcd(*data)-len(data))%2 else 'Bob']
    if pid=='372A':
        a=sorted(data);i,j=0,(len(a)+1)//2
        while i<len(a)//2 and j<len(a):
            if 2*a[i]<=a[j]: i+=1
            j+=1
        return [len(a)-i]
    if pid=='373B':
        w,m,k=data;digits=w//k;result=0
        while digits>=len(str(m)):
            width=len(str(m));take=min(10**width-m,digits//width)
            result+=take;digits-=take*width;m+=take
        return [result]
    if pid=='495B':
        a,b=data
        if a==b: return ['infinity']
        if a<b: return [0]
        d=a-b;total=0
        for i in range(1,math.isqrt(d)+1):
            if d%i==0: total+=int(i>b)+int(d//i>b and i!=d//i)
        return [total]
    if pid=='597A':
        k,a,b=data;return [b//k-(a-1)//k]
    if pid=='626C':
        n,m=data;lo,hi=0,3*(n+m)
        while lo<hi:
            mid=(lo+hi)//2
            if mid//2>=n and mid//3>=m and mid//2+mid//3-mid//6>=n+m: hi=mid
            else: lo=mid+1
        return [lo]
    if pid=='645C':
        k,s=data;p=[i for i,x in enumerate(s) if x=='0'];j=0;best=len(s)
        for i in range(len(p)-k):
            j=max(j,i)
            while j+1<=i+k and p[j]+p[j+1]<=p[i]+p[i+k]: j+=1
            best=min(best,max(p[j]-p[i],p[i+k]-p[j]))
            if j+1<=i+k: best=min(best,max(p[j+1]-p[i],p[i+k]-p[j+1]))
        return [best]
    if pid=='678C':
        n,a,b,p,q=data;return [n//a*p+n//b*q-n//math.lcm(a,b)*min(p,q)]
    if pid=='704A':
        n,events=data;apps=[[] for _ in range(n)];unread=[];prefix=total=0;out=[]
        for t,x in events:
            if t==1: apps[x-1].append(len(unread));unread.append(True);total+=1
            elif t==2:
                for i in apps[x-1]: total-=unread[i];unread[i]=False
                apps[x-1].clear()
            else:
                while prefix<x: total-=unread[prefix];unread[prefix]=False;prefix+=1
            out.append(total)
        return out
    if pid=='712C':
        x,y=data;sides=[y]*3;count=0
        while min(sides)<x:
            sides.sort();sides[0]=min(x,sides[1]+sides[2]-1);count+=1
        return [count]
    if pid=='741A':
        if len(set(data))!=len(data): return [-1]
        seen=set();result=1
        for i in range(len(data)):
            if i in seen: continue
            count=0
            while i not in seen: seen.add(i);i=data[i]-1;count+=1
            result=math.lcm(result,count//math.gcd(count,2))
        return [result]
    if pid=='913C':
        L,c=data;c=c[:]
        while len(c)<32: c.append(2*c[-1])
        for i in range(1,32): c[i]=min(c[i],2*c[i-1])
        paid=0;best=10**30
        for i in reversed(range(32)):
            amount,L=divmod(L,1<<i);paid+=amount*c[i];best=min(best,paid+(c[i] if L else 0))
        return [best]
    if pid=='992B':
        l,r,x,y=data
        if y%x: return [0]
        d=y//x;result=0
        for i in range(1,math.isqrt(d)+1):
            if d%i==0 and math.gcd(i,d//i)==1 and l<=x*i<=r and l<=x*(d//i)<=r: result+=1 if i*i==d else 2
        return [result]
    if pid=='440B':
        average=sum(data)//len(data);prefix=total=0
        for x in data[:-1]: prefix+=x-average;total+=abs(prefix)
        return [total]
    if pid=='605A':
        pos=[0]*len(data)
        for i,x in enumerate(data): pos[x-1]=i
        best=run=1
        for a,b in zip(pos,pos[1:]): run=run+1 if a<b else 1;best=max(best,run)
        return [len(data)-best]
    x1,x2,lines=data;ordered=sorted((k*x1+b,k*x2+b) for k,b in lines)
    return ['Yes' if any(a[1]>b[1] for a,b in zip(ordered,ordered[1:])) else 'No']


def brute_checks():
    counts=Counter();rng=random.Random(160031)
    def check(pid,data,expect):
        assert answer(pid,data)==[expect],(pid,data,answer(pid,data),expect)
        counts[pid]+=1
    @lru_cache(None)
    def winning(values):
        moves={abs(x-y) for x,y in itertools.combinations(values,2)}-set(values)
        return any(not winning(tuple(sorted((*values,x)))) for x in moves)
    for n in range(2,6):
        for values in itertools.combinations(range(1,7),n): check('346A',values,'Alice' if winning(values) else 'Bob')
    @lru_cache(None)
    def pairing(a):
        if len(a)<2: return 0
        return max([pairing(a[1:])]+[1+pairing(a[1:j]+a[j+1:]) for j in range(1,len(a)) if 2*min(a[0],a[j])<=max(a[0],a[j])])
    for _ in range(100):
        a=tuple(rng.randint(1,20) for _ in range(rng.randint(1,8)));check('372A',a,len(a)-pairing(a))
        w,m,k=rng.randint(1,200),rng.randint(1,200),rng.randint(1,5);budget=w;count=0
        while budget>=len(str(m+count))*k: budget-=len(str(m+count))*k;count+=1
        check('373B',(w,m,k),count)
    for a in range(40):
        for b in range(40): check('495B',(a,b),'infinity' if a==b else sum(a%x==b for x in range(1,a+2)))
    for k in range(1,12):
        for a in range(-12,12):
            for b in range(a,13): check('597A',(k,a,b),sum(x%k==0 for x in range(a,b+1)))
    for n,m in itertools.product(range(5),repeat=2):
        if not n+m: continue
        expected=next(t for t in range(1,30) if any(len(set(range(3,t+1,3))-set(taken))>=m for taken in itertools.combinations(range(2,t+1,2),n)))
        check('626C',(n,m),expected)
    for _ in range(100):
        n=rng.randint(2,10);s=''.join(rng.choice('01') for _ in range(n));p=[i for i,x in enumerate(s) if x=='0']
        if len(p)>1:
            k=rng.randint(1,len(p)-1);expect=min(min(max(abs(c-x) for x in group) for c in group) for group in itertools.combinations(p,k+1));check('645C',(k,s),expect)
        v=[rng.randint(1,40) for _ in range(5)];n,a,b,p,q=v;check('678C',v,sum(max(p if i%a==0 else 0,q if i%b==0 else 0) for i in range(1,n+1)))
        events=[];notifications=[];expected=[]
        for __ in range(30):
            t=rng.randint(1,3) if notifications else rng.randint(1,2);x=rng.randint(1,len(notifications) if t==3 else 4);events.append((t,x))
            if t==1: notifications.append([x,True])
            elif t==2:
                for row in notifications:
                    if row[0]==x: row[1]=False
            else:
                for row in notifications[:x]: row[1]=False
            expected.append(sum(row[1] for row in notifications))
        assert answer('704A',(4,events))==expected;counts['704A']+=1
        L=rng.randint(1,25);cost=[rng.randint(1,20) for __ in range(rng.randint(1,4))];limit=L+(1<<(len(cost)-1));dp=[0]+[10**9]*limit
        for volume in range(1,limit+1): dp[volume]=min(dp[volume-(1<<i)]+c for i,c in enumerate(cost) if 1<<i<=volume)
        check('913C',(L,cost),min(dp[L:]))
        l,r=sorted([rng.randint(1,20),rng.randint(1,20)]);x,y=sorted([rng.randint(1,20),rng.randint(1,20)]);check('992B',(l,r,x,y),sum(math.gcd(a,b)==x and math.lcm(a,b)==y for a in range(l,r+1) for b in range(l,r+1)))
        lines=list(set((rng.randint(-4,4),rng.randint(-4,4)) for __ in range(8)));x1,x2=sorted(rng.sample(range(-5,6),2));check('593B',(x1,x2,lines),'Yes' if any(((k-j)*x1+b-c)*((k-j)*x2+b-c)<0 for (k,b),(j,c) in itertools.combinations(lines,2)) else 'No')
    for y in range(3,7):
        for x in range(y+1,10):
            queue=deque([((y,y,y),0)]);seen={(y,y,y)};expected=None
            while queue:
                state,d=queue.popleft()
                if state==(x,x,x): expected=d;break
                for i in range(3):
                    for v in range(y,x+1):
                        nxt=list(state);nxt[i]=v;nxt=tuple(sorted(nxt))
                        if nxt[0]+nxt[1]>nxt[2] and nxt not in seen: seen.add(nxt);queue.append((nxt,d+1))
            check('712C',(x,y),expected)
    for n in range(1,5):
        for data in itertools.product(range(1,n+1),repeat=n):
            expected=-1
            for t in range(1,13):
                current=list(range(n))
                for _ in range(2*t): current=[data[i]-1 for i in current]
                if current==list(range(n)): expected=t;break
            check('741A',data,expected)
    for total in (3,6):
        target=(total//3,)*3;queue=deque([(target,0)]);seen={target}
        while queue:
            state,d=queue.popleft();check('440B',state,d)
            for i,j in ((0,1),(1,0),(1,2),(2,1)):
                if state[i]:
                    nxt=list(state);nxt[i]-=1;nxt[j]+=1;nxt=tuple(nxt)
                    if nxt not in seen: seen.add(nxt);queue.append((nxt,d+1))
    for n in range(1,6):
        target=tuple(range(1,n+1));queue=deque([(target,0)]);seen={target}
        while queue:
            state,d=queue.popleft();check('605A',state,d)
            for i in (0,n-1):
                x=state[i];rest=state[:i]+state[i+1:]
                for j in range(n):
                    nxt=rest[:j]+(x,)+rest[j:]
                    if nxt not in seen: seen.add(nxt);queue.append((nxt,d+1))
    return dict(counts)


def extras(pid):
    rng=random.Random(160000+int(pid[:-1]));cases=[]
    def add(text,reason,category='adversarial'):
        data=parse(pid,text);cases.append({'input':text,'output':'\n'.join(map(str,answer(pid,data)))+'\n','reason':reason,'category':category})
    def array(a): return str(len(a))+'\n'+' '.join(map(str,a))+'\n'
    def scalar(a): return ' '.join(map(str,a))+'\n'
    if pid in ('346A','372A','741A','440B','605A'):
        fixed={'346A':[[1,2],[2,4],[6,10,14],list(range(10**9-99,10**9+1))],
               '372A':[[1],[1,1],[1,2],[1]*250000+[100000]*250000],
               '741A':[[1],[1,1],[2,1],list(range(2,101))+[1]],
               '440B':[[0],[0,2],[3,0,0],[10**9]*25000+[0]*25000],
               '605A':[[1],[2,1],[2,3,1],list(reversed(range(1,100001)))]}[pid]
        for a in fixed: add(array(a),'minimum, exact/no move, overlap/order edge','maxSize' if len(a)>=100 else 'boundary')
        for _ in range(150):
            n=rng.randint(2 if pid=='346A' else 1,100)
            if pid=='346A': a=rng.sample(range(1,10000),n)
            elif pid=='372A': a=[rng.randint(1,100000) for __ in range(n)]
            elif pid=='741A':
                a=list(range(1,n+1));rng.shuffle(a)
                if rng.randrange(4)==0: a=[rng.randint(1,n) for __ in range(n)]
            elif pid=='440B':
                a=[rng.randint(0,100000) for __ in range(n)];a[-1]+=(-sum(a))%n
            else: a=list(range(1,n+1));rng.shuffle(a)
            add(array(a),'fixed-seed disjoint matching/closure/transport/permutation distributions')
    elif pid=='704A':
        add('1 5\n1 1\n3 1\n2 1\n1 1\n3 1\n','re-reading prefixes, clearing then re-adding','boundary')
        add('300000 300000\n'+('1 300000\n'*150000)+('3 150000\n'*150000),'maximum dimensions, prefix re-read storm','maxSize')
        for _ in range(150):
            n=rng.randint(1,30);events=[];generated=0
            for __ in range(100):
                t=rng.randint(1,3) if generated else rng.randint(1,2);x=rng.randint(1,generated if t==3 else n);events.append((t,x));generated+=t==1
            add(f'{n} 100\n'+''.join(f'{t} {x}\n' for t,x in events),'fixed-seed app clearing and overlapping historical prefixes')
    elif pid=='645C':
        add('2 1\n00\n','minimum free group','boundary');add('100000 99999\n'+'0'*100000+'\n','all rooms free, maximal group','maxSize')
        for _ in range(150):
            n=rng.randint(3,300);s=''.join(rng.choice('001') for __ in range(n));k=rng.randint(1,max(1,s.count('0')-1))
            if s.count('0')>=2: add(f'{n} {k}\n{s}\n','fixed-seed occupied gaps and midpoint choices')
    elif pid=='913C':
        add('1 1\n1\n','single unit bottle','boundary');add('30 1000000000\n'+' '.join(['1000000000']*30)+'\n','max volumes/costs, cheap overbuy relative to unit fill','maxSize')
        for _ in range(150):
            n=rng.randint(1,30);L=rng.randint(1,10**9);c=[rng.randint(1,10**9) for __ in range(n)];add(f'{n} {L}\n'+' '.join(map(str,c))+'\n','fixed-seed unnormalized prices, exact fills vs overbuy')
    elif pid=='593B':
        def lines(x1,x2,a): return f'{len(a)}\n{x1} {x2}\n'+''.join(f'{k} {b}\n' for k,b in a)
        for a in [[(0,0),(1,0)],[(0,0),(1,-1)],[(0,0),(1,-2)],[(1,1),(1,2)]]: add(lines(0,2,a),'intersection at endpoints/interior, parallel lines','boundary')
        add(lines(-10**6,10**6,[(i-50000,i) for i in range(100000)]),'maximum distinct lines and endpoint products','maxSize')
        for _ in range(150):
            a=list(set((rng.randint(-1000,1000),rng.randint(-1000,1000)) for __ in range(30)));x1,x2=sorted(rng.sample(range(-1000,1001),2));add(lines(x1,x2,a),'fixed-seed strict crossings and order ties')
    else:
        fixed={'373B':[(1,1,1),(1,10,2),(10**16,10**16,10**9)],'495B':[(0,0),(0,1),(1,0),(10**9,0)],
               '597A':[(1,0,0),(2,-3,3),(10**18,-10**18,10**18)],'626C':[(0,1),(1,0),(1,1),(10**6,10**6)],
               '678C':[(1,1,1,1,1),(10**9,1,1,10**9,10**9),(10**9,999999999,1000000000,1,10**9)],
               '712C':[(4,3),(100000,3),(100000,99999)],'992B':[(1,1,1,1),(1,10**9,1,10**9),(10**9,10**9,10**9,10**9)]}[pid]
        for i,a in enumerate(fixed): add(scalar(a),'minimum, impossible/equal/divisibility, numeric-limit boundary','maxSize' if i==len(fixed)-1 else 'boundary')
        for _ in range(150):
            if pid=='373B': a=(rng.randint(1,10**16),rng.randint(1,10**16),rng.randint(1,10**9))
            elif pid=='495B': a=(rng.randint(0,10**9),rng.randint(0,10**9))
            elif pid=='597A': a=(rng.randint(1,10**18),*sorted([rng.randint(-10**18,10**18) for __ in range(2)]))
            elif pid=='626C': a=(rng.randint(0,10**6),rng.randint(1,10**6))
            elif pid=='678C': a=[rng.randint(1,10**9) for __ in range(5)]
            elif pid=='712C': x=rng.randint(4,100000);a=(x,rng.randint(3,x-1))
            elif rng.randrange(2):
                x=rng.randint(1,1000);i,j=rng.randint(1,100),rng.randint(1,100);a=(1,100000,x,x*i*j)
            else: a=(*sorted([rng.randint(1,10**9) for __ in range(2)]),*sorted([rng.randint(1,10**9) for __ in range(2)]))
            add(scalar(a),'fixed-seed arithmetic thresholds and64-bit extremes')
    return cases


def review(pid,tests,samples):
    failures=[]
    for name,pair in [*tests,*samples]:
        try:
            if pair['output'].split()!=list(map(str,answer(pid,parse(pid,pair['input'])))): raise ValueError('oracle output disagreement')
        except (ValueError,IndexError,KeyError,AssertionError) as exc: failures.append({'test':name,'reason':str(exc)})
    return failures
