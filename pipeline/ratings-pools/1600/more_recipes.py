"""Statement-bound deterministic suites with exact token outputs and bounded independent checks."""
from collections import Counter
from functools import lru_cache
import itertools
import math
import random

IDS = ('11B', '40B', '55B', '75C', '86A', '197A', '209A', '244B', '317A', '319A',
       '337C', '343A', '476C', '559A', '665A', '678B', '735C', '735D', '768B',
       '817C', '845B', '910B', '992C')
SEMANTICS = {
    '11B': 'Integer target [-10^9,10^9]; triangular jump sum and even reachability checked with exhaustive signed subset sums.',
    '40B': 'Board 1..5000 square sides and 1..10^9 repaint count. Count black cells by difference of concentric rectangles; explicit small-board simulation.',
    '55B': 'Four values 0..1000 and three sequential +/* operations. Exact minimization of all binary pair choices; independent full permutation/tree enumeration.',
    '75C': 'Two integers 1..10^9; 1..10000 inclusive divisor-range queries <=10^9. Sorted divisors of GCD and direct small-range brute.',
    '86A': 'Inclusive range 1..10^9. Per decimal width complement n*(10^width-1-n) concave; check endpoints and center, exhaustive small-range brute.',
    '197A': 'Table/radius 1..100; strategy-stealing central symmetry is First exactly when diameter fits both dimensions.',
    '209A': 'Length1..10^6, alternating two-color marbles: Fibonacci(n+3)-2 subsequences modulo10^9+7; enumerated subsets for small n.',
    '244B': 'Positive bound1..10^9; count numbers with at most two distinct decimal digits by enumerating digit pairs, de-duplicating; direct small scan.',
    '317A': 'Signed x,y,m within 10^18. Greedily make smaller operand nonnegative then Fibonacci-like growth or prove impossibility; independent small BFS.',
    '319A': 'Binary x length1..100 including leading zeros. Each set bit yields 2^(n+i-1) XOR permutation inversions; explicit small inversion pairs.',
    '337C': 'k2..n<=10^9,m0..n. Force minimum number of k-streaks; powers of2 modulo10^9+9; exhaustive small answer-order enumeration.',
    '343A': 'Coprime a,b1..10^18; Euclidean quotient sum counts least series/parallel resistors; small rational-state BFS.',
    '476C': 'a,b1..10^7. Enumerate quotient/remainder constraints by r and k; closed sum modulo10^9+7 checked by direct small enumeration.',
    '559A': 'Six sides1..1000, valid equiangular hexagon; triangular tiling equals bounding equilateral triangle minus three corner triangles.',
    '665A': 'Bus frequencies/travel times1..120; departure hh:mm of actual bus from05:00..23:59. Count only strict open-interval crossings.',
    '678B': '1000<=year<100000; advance calendar weekday including leap years; seek same start weekday and leap status.',
    '735C': 'Players2..10^18; minimum players to support winner depth follow Fibonacci recurrence; independent small tournament DP.',
    '735D': 'Tax via maximum proper divisor after splitting income n2..2*10^9; primality of n or n-2 determines1/2/3.',
    '768B': 'n in[0,2^50), 1<=l<=r<=final-list length, span<=10^5. Recursive-prefix popcount checked against materialized small lists.',
    '817C': 'n,s1..10^18; x-digitSum(x) monotone, lower-bound binary search; direct small scan.',
    '845B': 'Exactly six decimal digits including leading zeros. Sort possible single-digit corrections until sums match; brute all edit-cost choices.',
    '910B': 'n1..1000, a,b1..n; six intact pieces (four a, two b). Exact finite subset-partition packing into bars.',
    '992C': 'x,k0..10^18; expected wardrobe count 2^k*(2x-1)+1 except x0, modulo10^9+7; brute small outcome distribution.',
}


def parse(pid, text):
    v = text.split()
    if pid == '665A':
        if len(v) != 5 or len(v[4]) != 5 or v[4][2] != ':' or not (v[4][:2]+v[4][3:]).isdigit():
            raise ValueError('bus fields/time layout')
        a, ta, b, tb = map(int, v[:4]); hour, minute = int(v[4][:2]), int(v[4][3:]); t = hour*60+minute
        if not all(1 <= x <= 120 for x in (a,ta,b,tb)) or not 5 <= hour <= 23 or not 0 <= minute < 60 or (t-300)%a:
            raise ValueError('bus bounds/departure')
        return a,ta,b,tb,t
    if pid == '319A':
        if len(v) != 1 or not 1 <= len(v[0]) <= 100 or set(v[0])-set('01'):
            raise ValueError('binary string bounds')
        return v[0]
    if pid == '55B':
        if len(v) != 7 or not all(s in ('+','*') for s in v[4:]):
            raise ValueError('operation arity/types')
        values=list(map(int,v[:4]))
        if any(x<0 or x>1000 for x in values): raise ValueError('operands bounds')
        return values,v[4:]
    if pid == '75C':
        a=list(map(int,v))
        if len(a)<3 or not all(1<=x<=10**9 for x in a[:2]) or not 1<=a[2]<=10000 or len(a)!=3+2*a[2]:
            raise ValueError('divisor query size/arity')
        q=list(zip(a[3::2],a[4::2]))
        if any(not 1<=l<=r<=10**9 for l,r in q): raise ValueError('divisor query bounds')
        return a[0],a[1],q
    a=list(map(int,v))
    ranges = {'11B': (1,-10**9,10**9),'40B':(3,1,10**9),'86A':(2,1,10**9),
              '197A':(3,1,100),'209A':(1,1,10**6),'244B':(1,1,10**9),
              '317A':(3,-10**18,10**18),'337C':(3,0,10**9),'343A':(2,1,10**18),
              '476C':(2,1,10**7),'559A':(6,1,1000),'678B':(1,1000,99999),
              '735C':(1,2,10**18),'735D':(1,2,2*10**9),'768B':(3,0,2**50-1),
              '817C':(2,1,10**18),'845B':(1,0,999999),'910B':(3,1,1000),
              '992C':(2,0,10**18)}
    count,low,high=ranges[pid]
    if len(a)!=count or any(not low<=x<=high for x in a): raise ValueError('scalar arity/ranges')
    if pid=='40B' and (a[0]>5000 or a[1]>5000): raise ValueError('board size')
    if pid=='86A' and a[0]>a[1]: raise ValueError('range order')
    if pid=='337C' and (not 2<=a[2]<=a[0] or a[1]>a[0]): raise ValueError('quiz dimensions')
    if pid=='343A' and math.gcd(*a)!=1: raise ValueError('reduced fraction')
    if pid=='559A' and (a[0]-a[2]-a[3]+a[5] or a[1]+a[2]-a[4]-a[5]):
        raise ValueError('hexagon does not close')
    if pid=='768B' and (not 1<=a[1]<=a[2]<=(1<<max(1,a[0].bit_length()))-1 or a[2]-a[1]>100000):
        raise ValueError('final list range')
    if pid=='910B':
        if len(text.strip().splitlines())!=3 or any(len(line.split())!=1 for line in text.strip().splitlines()):
            raise ValueError('bar input requires three individual integer lines')
        if a[1]>a[0] or a[2]>a[0]: raise ValueError('bar pieces longer than bar')
    if pid=='845B' and (len(v)!=1 or len(v[0])!=6 or not v[0].isdigit()): raise ValueError('ticket layout')
    return v[0] if pid=='845B' else tuple(a)


def prime(n):
    if n<2:return False
    for d in range(2,math.isqrt(n)+1):
        if n%d==0:return False
    return True


def fib(n):
    if n==0:return (0,1)
    a,b=fib(n//2); c=a*(2*b-a)%1000000007;d=(a*a+b*b)%1000000007
    return (d,(c+d)%1000000007) if n%2 else (c,d)


def prefix(n, length):
    if length<=0:return 0
    if n<=1:return n
    size=(1<<n.bit_length())-1
    if length>=size:return n
    left=(size-1)//2;half=n//2
    if length<=left:return prefix(half,length)
    return half+(n%2)+prefix(half,length-left-1)


def answer(pid, value):
    if pid=='11B':
        x=abs(value[0]);step=0;s=0
        while s<x or (s-x)%2:step+=1;s+=step
        return [step]
    if pid=='40B':
        n,m,x=value;h=n-2*(x-1);w=m-2*(x-1)
        black=lambda h,w:(h*w+1)//2 if h>0 and w>0 else 0
        return [black(h,w)-black(h-2,w-2)]
    if pid=='55B':
        values,ops=value
        @lru_cache(None)
        def rec(values,step):
            if step==3:return values[0]
            op=ops[step]
            return min(rec(tuple(sorted((values[i]+values[j] if op=='+' else values[i]*values[j],
                                         *(x for z,x in enumerate(values) if z not in (i,j))))),step+1)
                       for i in range(len(values)) for j in range(i+1,len(values)))
        return [rec(tuple(sorted(values)),0)]
    if pid=='75C':
        a,b,queries=value;g=math.gcd(a,b);divisors=sorted({d for i in range(1,math.isqrt(g)+1) if g%i==0 for d in (i,g//i)})
        import bisect
        return [divisors[p] if (p:=bisect.bisect_right(divisors,r)-1)>=0 and divisors[p]>=l else -1 for l,r in queries]
    if pid=='86A':
        l,r=value;best=0
        for digits in range(1,11):
            lo=max(l,10**(digits-1) if digits>1 else 1);hi=min(r,10**digits-1)
            if lo>hi:continue
            total=10**digits-1
            for n in {lo,hi,min(hi,max(lo,total//2)),min(hi,max(lo,total//2+1))}:
                best=max(best,n*(total-n))
        return [best]
    if pid=='197A':
        a,b,r=value;return ['First' if a>=2*r and b>=2*r else 'Second']
    if pid=='209A':return [(fib(value[0]+3)[0]-2)%1000000007]
    if pid=='244B':
        bound=value[0]; found=set()
        for x in range(10):
            for y in range(x,10):
                for width in range(1,11):
                    for mask in range(1<<width):
                        s=''.join(str(y if mask>>j&1 else x) for j in range(width))
                        if s[0]!='0' and int(s)<=bound:found.add(int(s))
        return [len(found)]
    if pid=='317A':
        x,y,m=value
        if max(x,y)>=m:return [0]
        if max(x,y)<=0:return [-1]
        a,b=sorted((x,y));steps=0
        if a<0:
            blocks=(-a+b-1)//b;a+=blocks*b;steps+=blocks
            if a>=m:return [steps]
        while max(a,b)<m:
            a,b=sorted((a+b,b));steps+=1
        return [steps]
    if pid=='319A':
        s=value;n=len(s)
        return [sum(1<<(n+i-1) for i,c in enumerate(reversed(s)) if c=='1')%1000000007]
    if pid=='337C':
        n,m,k=value;safe=(n//k)*(k-1)+n%k
        if m<=safe:return [m]
        forced=m-safe;return [((pow(2,forced+1,1000000009)-2)*k+m-forced*k)%1000000009]
    if pid=='343A':
        a,b=value;answer=0
        while b:answer+=a//b;a,b=b,a%b
        return [answer]
    if pid=='476C':
        a,b=value;return [(b*(b-1)//2*(b*a*(a+1)//2+a))%1000000007]
    if pid=='559A':
        a,b,c,d,e,f=value;return [(a+b+c)**2-a*a-c*c-e*e]
    if pid=='665A':
        a,ta,b,tb,t=value
        return [sum(t<departure+tb and departure<t+ta for departure in range(300,1440,b))]
    if pid=='678B':
        y=value[0];leap=lambda x:x%400==0 or x%4==0 and x%100!=0
        same=leap(y);weekday=0
        for next_year in range(y+1,y+401):
            weekday=(weekday+365+leap(next_year-1))%7
            if weekday==0 and leap(next_year)==same:return [next_year]
        raise ValueError('calendar recurrence failed')
    if pid=='735C':
        n=value[0];prev,curr=1,2;count=1
        while prev+curr<=n:prev,curr=curr,prev+curr;count+=1
        return [count]
    if pid=='735D':
        n=value[0];return [1 if prime(n) else 2 if n%2==0 or prime(n-2) else 3]
    if pid=='768B':
        n,l,r=value;return [prefix(n,r)-prefix(n,l-1)]
    if pid=='817C':
        n,s=value;lo,hi=1,n+1
        while lo<hi:
            mid=(lo+hi)//2
            if mid-sum(map(int,str(mid)))>=s:hi=mid
            else:lo=mid+1
        return [n-lo+1]
    if pid=='845B':
        v=list(map(int,value));left=sum(v[:3]);right=sum(v[3:]);diff=abs(left-right)
        if not diff:return [0]
        improvements=([*v[:3],*(9-d for d in v[3:])] if left>right else
                      [*(9-d for d in v[:3]),*v[3:]])
        for i,change in enumerate(sorted(improvements,reverse=True),1):
            diff-=change
            if diff<=0:return [i]
        raise ValueError('ticket cannot be balanced')
    if pid=='910B':
        n,a,b=value;parts=[a]*4+[b]*2;weights=[sum(parts[i] for i in range(6) if mask>>i&1) for mask in range(64)]
        dp=[7]*64;dp[0]=0
        for mask in range(1,64):
            sub=mask
            while sub:
                if weights[sub]<=n:dp[mask]=min(dp[mask],dp[mask^sub]+1)
                sub=(sub-1)&mask
        return [dp[63]]
    x,k=value;return [0 if x==0 else (pow(2,k,1000000007)*(2*x-1)+1)%1000000007]


def brute_checks():
    checks=Counter(); rng=random.Random(160023)
    def check(pid,data,expected):
        assert answer(pid,data)==[expected],(pid,data,answer(pid,data),expected)
        checks[pid]+=1
    for x in range(-40,41):
        reach={0};steps=0
        while x not in reach:steps+=1;reach={a+steps for a in reach}|{a-steps for a in reach}
        check('11B',(x,),steps)
    for n in range(1,9):
        for m in range(1,9):
            black=[(i,j) for i in range(n) for j in range(m) if (i+j)%2==0]
            for x in range(1,7):
                expected=sum(min(i,j,n-i-1,m-j-1)==x-1 for i,j in black)
                check('40B',(n,m,x),expected)
    for _ in range(140):
        v=[rng.randint(0,10) for j in range(4)];ops=[rng.choice('+*') for j in range(3)];sets={tuple(v)}
        for op in ops:
            sets={tuple(sorted([values[i]+values[j] if op=='+' else values[i]*values[j]]+
                          [x for p,x in enumerate(values) if p not in (i,j)])) for values in sets
                  for i in range(len(values)) for j in range(i+1,len(values))}
        check('55B',(v,ops),min(v[0] for v in sets))
    for _ in range(120):
        a=rng.randint(1,200);b=rng.randint(1,200)
        q=[tuple(sorted(rng.sample(range(1,210),2))) for j in range(8)]
        expected=[max([d for d in range(l,r+1) if a%d==b%d==0],default=-1) for l,r in q]
        assert answer('75C',(a,b,q))==expected;checks['75C']+=1
        l=rng.randint(1,300);r=rng.randint(l,min(350,l+30))
        reflect=lambda n:int(''.join(str(9-int(c)) for c in str(n)))
        check('86A',(l,r),max(n*reflect(n) for n in range(l,r+1)))
        bound=rng.randint(1,500)
        check('244B',(bound,),sum(len(set(str(n)))<=2 for n in range(1,bound+1)))
        n=rng.randint(1,11);s='01'*(n//2)+'0'*(n%2)
        check('209A',(n,),sum(all(s[i]!=s[j] for i,j in zip(sub,sub[1:])) for r in range(1,n+1) for sub in itertools.combinations(range(n),r)))
    for n in range(1,8):
        for x in range(1<<n):
            check('319A',format(x,f'0{n}b'),sum((i^x)>(j^x) for i in range(1<<n) for j in range(i+1,1<<n)))
    for n in range(2,9):
        for m in range(n+1):
            for k in range(2,n+1):
                values=[]
                for chosen in itertools.combinations(range(n),m):
                    score=streak=0
                    for j in range(n):
                        if j in chosen:
                            streak+=1;score+=1
                            if streak==k:score*=2;streak=0
                        else:streak=0
                    values.append(score)
                check('337C',(n,m,k),min(values))
    for a in range(1,7):
        for b in range(1,7):
            if math.gcd(a,b)!=1:continue
            from fractions import Fraction
            values={Fraction(1):1}
            for step in range(2,12):
                for x in tuple(values):
                    for y in (x+1,x/(x+1)):
                        if y not in values:values[y]=step
            check('343A',(a,b),values[__import__('fractions').Fraction(a,b)])
    for a in range(1,10):
        for b in range(1,10):
            expect=sum(k*r*b+r for k in range(1,a+1) for r in range(1,b))
            check('476C',(a,b),expect)
    for n in range(0,70):
        def materialize(x):return [x] if x<=1 else materialize(x//2)+[x%2]+materialize(x//2)
        full=materialize(n)
        for l in range(1,len(full)+1):
            r=min(l+6,len(full));check('768B',(n,l,r),sum(full[l-1:r]))
    for n in range(1,100):
        for s in (1,3,9,41):
            check('817C',(n,s),sum(x-sum(map(int,str(x)))>=s for x in range(1,n+1)))
    for x in range(0,15):
        for k in range(0,7):
            # For x>0 the intermediate expectation is E_{j+1}=2E_j-1/2.
            expect=0 if x==0 else 2**k*(2*x-1)+1
            check('992C',(x,k),expect)
    return dict(checks)


def extras(pid):
    rng=random.Random(160000+int(pid[:-1]));cases=[]
    def add(text,reason,category='adversarial'):
        cases.append({'input':text,'output':'\n'.join(map(str,answer(pid,parse(pid,text))))+'\n',
                      'reason':reason,'category':category})
    scalar=lambda *a:' '.join(map(str,a))+'\n'
    if pid=='55B':
        for a in ((0,0,0,0),(1000,)*4,(1,1,1,1),(1,1000,0,2)):
            for op in itertools.product('+*',repeat=3):add(scalar(*a)+scalar(*op),'all operations, zeros, extreme products','maxSize' if a==(1000,)*4 else 'boundary')
        for _ in range(150):add(scalar(*(rng.randrange(1001) for i in range(4)))+scalar(*(rng.choice('+*') for i in range(3))),'random operation/order interactions')
    elif pid=='75C':
        for a,b in ((1,1),(10**9,10**9),(999999937,10**9),(6,15)):
            add(scalar(a,b)+'4\n1 1\n1 1000000000\n9 10\n999999999 1000000000\n','singleton/gcd extreme/no divisor','maxSize' if a==10**9 else 'boundary')
        for _ in range(150):
            a,b=(rng.randint(1,10**9),rng.randint(1,10**9))
            q=[sorted(rng.sample(range(1,10**9+1),2)) for j in range(8)]
            add(scalar(a,b)+'8\n'+''.join(scalar(*p) for p in q),'fixed-seed query range distribution')
    elif pid=='665A':
        for a,ta,b,tb,t in ((1,1,1,1,300),(120,120,120,120,300),(1,120,1,120,1439),(10,30,10,35,320)):
            if (t-300)%a==0:add(scalar(a,ta)+scalar(b,tb)+f'{t//60:02d}:{t%60:02d}\n','first/last bus, open endpoints','maxSize' if t==1439 else 'boundary')
        for _ in range(150):
            a,ta,b,tb=[rng.randint(1,120) for i in range(4)]
            t=300+a*rng.randint(0,(1439-300)//a)
            add(scalar(a,ta)+scalar(b,tb)+f'{t//60:02d}:{t%60:02d}\n','fixed-seed schedule crossings')
    elif pid=='768B':
        for n,l,r in ((0,1,1),(1,1,1),(7,2,5),(2**50-1,1,100001),(2**50-1,2**50-100001,2**50-1)):
            add(scalar(n,l,r),'zero/list extremes and full-span prefix','maxSize' if n>2**40 else 'boundary')
        for _ in range(150):
            n=rng.randint(0,2**50-1);size=(1<<max(0,n.bit_length()))-1
            l=rng.randint(1,size);r=min(size,l+rng.randint(0,100000))
            add(scalar(n,l,r),'fixed-seed recursive-subsequence positions')
    elif pid=='845B':
        for s in ('000000','999999','000999','123456','111000'):
            add(s+'\n','zero/saturated/equal one-edit tickets','boundary')
        for _ in range(150):add(''.join(str(rng.randrange(10)) for __ in range(6))+'\n','fixed-seed changes in each half')
    elif pid=='40B':
        for n,m,x in ((1,1,1),(2,2,1),(3,3,2),(5000,5000,1),(5000,5000,2500),(5000,5000,10**9)):
            add(scalar(n,m)+scalar(x),'parity/outer and innermost rings','maxSize' if n==5000 else 'boundary')
        for _ in range(150):add(scalar(rng.randint(1,5000),rng.randint(1,5000))+scalar(rng.randint(1,5000)),'fixed-seed rectangular color parity')
    elif pid=='317A':
        for x,y,m in ((0,0,1),(-10**18,1,10**18),(1,2,5),(-1,4,15),(-10**18,-10**18,10**18)):
            add(scalar(x,y,m),'impossible/negative recovery and huge step count','maxSize' if abs(x)==10**18 else 'boundary')
        for _ in range(150):add(scalar(rng.randint(-10**5,10**5),rng.randint(-10**5,10**5),rng.randint(-10**5,10**5)),'fixed-seed signed growth')
    elif pid=='319A':
        for s in ('0','1','01','11','0'*100,'1'*100):add(s+'\n','leading zeros/maximum inversions','maxSize' if len(s)==100 else 'boundary')
        for _ in range(150):add(''.join(rng.choice('01') for j in range(rng.randint(1,100)))+'\n','fixed-seed XOR-bit combinations')
    elif pid=='559A':
        for a,b,c,d,e,f in ((1,)*6,(1,2,1,2,1,2),(1000,)*6):
            add(scalar(a,b,c,d,e,f),'regular/unequal/bounding triangle','maxSize' if a==1000 else 'boundary')
        for _ in range(150):
            a,b,c,d,e,f=[rng.randint(1,1000) for j in range(3) for _ in (0,1)]
            add(scalar(a,b,c,a,b,c),'fixed-seed valid closed hexagon')
    elif pid=='910B':
        for n,a,b in ((1,1,1),(1000,1000,1000),(8,1,2),(20,5,6)):
            add('\n'.join(map(str,(n,a,b)))+'\n','six pieces, full bars, shared cuts','maxSize' if n==1000 else 'boundary')
        for _ in range(150):
            n=rng.randint(1,1000);add('\n'.join(map(str,(n,rng.randint(1,n),rng.randint(1,n))))+'\n','fixed-seed packing tightness')
    else:
        fixed={'11B':[(-10**9,),(-1,),(0,),(1,),(10**9,)],'86A':[(1,1),(8,10),(10**9,10**9),(1,10**9)],
               '197A':[(1,1,1),(100,100,100),(5,5,2),(6,7,4)],'209A':[(1,),(2,),(3,),(10**6,)],
               '244B':[(1,),(9,),(10,),(10**9,)],'337C':[(2,0,2),(2,2,2),(10**9,10**9,2),(10**9,0,10**9)],
               '343A':[(1,1),(3,2),(1,10**18),(10**18,1)],'476C':[(1,1),(2,2),(10**7,10**7)],
               '678B':[(1000,),(2000,),(2016,),(99999,)],'735C':[(2,),(3,),(4,),(10**18,)],
               '735D':[(2,),(27,),(2*10**9,)],'817C':[(1,1),(12,1),(10**18,10**18),(10**18,1)],
               '992C':[(0,0),(0,10**18),(2,0),(10**18,10**18)]}[pid]
        for values in fixed:add(scalar(*values),'minimum/max bounds and arithmetic discontinuities','boundary' if len(values)==1 and values[0]<100 else 'maxSize')
        for _ in range(150):
            values={'11B':lambda:(rng.randint(-10**9,10**9),),'86A':lambda:tuple(sorted((rng.randint(1,10**9),rng.randint(1,10**9)))),
                    '197A':lambda:tuple(rng.randint(1,100) for j in range(3)),
                    '209A':lambda:(rng.randint(1,10**6),),'244B':lambda:(rng.randint(1,10**9),),
                    '337C':lambda:(lambda n,k:(n,rng.randint(0,n),k))(rng.randint(2,10**9),2),
                    '343A':lambda:(lambda a,b:(a//math.gcd(a,b),b//math.gcd(a,b)))(rng.randint(1,10**18),rng.randint(1,10**18)),
                    '476C':lambda:(rng.randint(1,10**7),rng.randint(1,10**7)),
                    '678B':lambda:(rng.randint(1000,99999),),'735C':lambda:(rng.randint(2,10**18),),
                    '735D':lambda:(rng.randint(2,2*10**9),),'817C':lambda:(rng.randint(1,10**18),rng.randint(1,10**18)),
                    '992C':lambda:(rng.randint(0,10**18),rng.randint(0,10**18))}[pid]()
            add(scalar(*values),'fixed-seed boundary/interior distributions')
    return cases


def review(pid,tests,samples):
    failures=[]
    for name,pair in [*tests,*samples]:
        try:
            expected=list(map(str,answer(pid,parse(pid,pair['input']))))
            if pair['output'].split()!=expected:raise ValueError('oracle output differs from supplied bytes')
        except (ValueError,IndexError,KeyError,TypeError) as exc:
            failures.append({'test':name,'reason':str(exc)})
    return failures
