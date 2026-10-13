"""Single-answer integer/string recipes and exhaustive small independent searches."""
from collections import Counter
import itertools
import random

IDS = ('1003D', '214B', '597B', '1006E')
SEMANTICS = {
    '1003D': 'n,q1..200000; coin values powers of2 up to2*10^9; independent requested totals1..10^9. Consume largest available powers first to minimize count, or return-1. Exhaustive subset-sum minimum counts independently checked.',
    '214B': 'n1..100000, decimal digits0..9. A multiple of30 needs a zero and digit sum divisible by3. Remove the fewest lowest digits of the required residue then sort decreasing; zero canonically printed0. Exhaustive subsets independently checked for maximal integer.',
    '597B': 'n1..500000; inclusive intervals1<=l<=r<=10^9. Choose by earliest finish with strict next-start>last-finish; touching endpoints conflict. Exhaustive subsets independently checked.',
    '1006E': 'n2..200000,q1..200000; parent[i]1..i-1; u,k1..n. Ascending-child DFS preorder yields contiguous subtree ranges and unique kth officer or-1. Recursive per-query traversal independently checked on exhaustive small parent assignments.',
}


def parse(pid,text):
    a = list(map(int,text.split()))
    if not a:
        raise ValueError('empty input')
    n = a[0]
    if pid == '214B':
        if not 1 <= n <= 100000 or len(a) != n+1 or not all(0 <= x <= 9 for x in a[1:]):
            raise ValueError('digit arity/range')
        return a[1:]
    if pid == '597B':
        intervals = list(zip(a[1::2],a[2::2]))
        if not 1 <= n <= 500000 or len(a) != 1+2*n or not all(1 <= l <= r <= 10**9 for l,r in intervals):
            raise ValueError('interval arity/range')
        return intervals
    if len(a) < 2:
        raise ValueError('header arity')
    q = a[1]
    if not (2 if pid == '1006E' else 1) <= n <= 200000 or not 1 <= q <= 200000:
        raise ValueError('array/query count')
    if pid == '1003D':
        coins,queries = a[2:n+2],a[n+2:]
        if len(a) != n+q+2 or not all(1 <= x <= 2*10**9 and x&(x-1)==0 for x in coins) or not all(1 <= x <= 10**9 for x in queries):
            raise ValueError('coin power/amount/arity')
        return coins,queries
    parents = a[2:n+1]
    queries = list(zip(a[n+1::2],a[n+2::2]))
    if len(a) != n+1+2*q or not all(1 <= p < i for i,p in enumerate(parents,2)) or not all(1 <= u <= n and 1 <= k <= n for u,k in queries):
        raise ValueError('parent/query arity/range')
    return parents,queries


def answer(pid,data):
    if pid == '1003D':
        coins,queries = data
        counts = sorted(Counter(coins).items(),reverse=True)
        result = []
        for x in queries:
            used = 0
            for value,count in counts:
                take = min(count,x//value)
                x -= take*value
                used += take
            result.append(-1 if x else used)
        return result
    if pid == '214B':
        counts = Counter(data)
        if not counts[0]:
            return ['-1']
        residue = sum(data)%3
        if residue:
            choices = [d for d in range(residue,10,3) if counts[d]]
            if choices:
                counts[choices[0]] -= 1
            else:
                remaining = 2
                for d in range(3-residue,10,3):
                    take = min(remaining,counts[d])
                    counts[d] -= take
                    remaining -= take
                if remaining:
                    return ['-1']
        result = ''.join(str(d)*counts[d] for d in range(9,-1,-1)).lstrip('0')
        return [result or '0']
    if pid == '597B':
        last,count = 0,0
        for l,r in sorted(data,key=lambda pair:(pair[1],pair[0])):
            if l > last:
                last,count = r,count+1
        return [count]
    parents,queries = data
    n = len(parents)+1
    children = [[] for _ in range(n+1)]
    for i,p in enumerate(parents,2):
        children[p].append(i)
    order,start,size = [],[0]*(n+1),[1]*(n+1)
    stack = [1]
    while stack:
        u = stack.pop()
        start[u] = len(order)
        order.append(u)
        stack.extend(reversed(children[u]))
    for u in reversed(order[1:]):
        size[parents[u-2]] += size[u]
    return [order[start[u]+k-1] if k <= size[u] else -1 for u,k in queries]


def brute(pid,data):
    if pid == '1003D':
        coins,queries = data
        minima = {}
        for mask in range(1<<len(coins)):
            total = sum(x for i,x in enumerate(coins) if mask&(1<<i))
            minima[total] = min(minima.get(total,len(coins)+1),mask.bit_count())
        return [minima.get(x,-1) for x in queries]
    if pid == '214B':
        best = -1
        for mask in range(1,1<<len(data)):
            digits = sorted((x for i,x in enumerate(data) if mask&(1<<i)),reverse=True)
            value = int(''.join(map(str,digits)))
            if value%30 == 0:
                best = max(best,value)
        return [str(best)]
    if pid == '597B':
        best = 0
        for mask in range(1<<len(data)):
            selected = [pair for i,pair in enumerate(data) if mask&(1<<i)]
            if all(r1 < l2 or r2 < l1 for (l1,r1),(l2,r2) in itertools.combinations(selected,2)):
                best = max(best,len(selected))
        return [best]
    parents,queries = data
    children = [[] for _ in range(len(parents)+2)]
    for i,p in enumerate(parents,2):
        children[p].append(i)
    def visit(u):
        return [u]+[x for child in sorted(children[u]) for x in visit(child)]
    result = []
    for u,k in queries:
        subtree = visit(u)
        result.append(subtree[k-1] if k <= len(subtree) else -1)
    return result


def brute_checks():
    counts = Counter()
    def check(pid,data):
        assert answer(pid,data) == brute(pid,data), (pid,data)
        counts[pid] += 1
    for n in range(1,7):
        for coins in itertools.combinations_with_replacement((1,2,4,8),n):
            check('1003D',(coins,list(range(1,33))))
        for digits in itertools.combinations_with_replacement(range(10),n):
            check('214B',digits)
    intervals = [(l,r) for l in range(1,4) for r in range(l,4)]
    for n in range(1,6):
        for data in itertools.combinations_with_replacement(intervals,n):
            check('597B',data)
    for n in range(2,8):
        for parents in itertools.product(*(range(1,i) for i in range(2,n+1))):
            check('1006E',(parents,[(u,k) for u in range(1,n+1) for k in range(1,n+1)]))
    return dict(counts)


def extras(pid):
    rng = random.Random(160000+int(pid[:-1]))
    cases = []
    def add(data,reason,category='adversarial'):
        if pid == '1003D':
            coins,queries = data
            text = f'{len(coins)} {len(queries)}\n'+' '.join(map(str,coins))+'\n'+''.join(str(x)+'\n' for x in queries)
        elif pid == '1006E':
            parents,queries = data
            text = f'{len(parents)+1} {len(queries)}\n'+' '.join(map(str,parents))+'\n'+''.join(f'{u} {k}\n' for u,k in queries)
        elif pid == '597B':
            text = str(len(data))+'\n'+''.join(f'{l} {r}\n' for l,r in data)
        else:
            text = str(len(data))+'\n'+' '.join(map(str,data))+'\n'
        cases.append({'input':text,'output':'\n'.join(map(str,answer(pid,parse(pid,text))))+'\n','reason':reason,'category':category})
    if pid == '1003D':
        for coins in ([1],[2**30],[1,1,2,4],[2,2,8]):
            add((coins,[1,2,3,7,8,10**9]),'singleton, missing odd value, reuse and query upper bound','boundary')
        for coins in ([1]*200000,[2**30]*200000,[1<<(i%31) for i in range(200000)]):
            add((coins,[1,10**9]*100000),'maximum coins and queries, power coverage or unavailable totals','maxSize')
        for _ in range(140):
            add(([1<<rng.randrange(31) for _ in range(rng.randint(1,100))],[rng.randint(1,10**9) for _ in range(40)]),'fixed-seed denomination capacities and independent totals')
    elif pid == '214B':
        for digits in ([0],[1],[1,0],[1,1,0],[2,2,0],[3,0],[9,8,7,6,5,4,3,2,1,0]):
            add(digits,'zero, no trailing zero, remove one/two residue digits','boundary')
        for digits in ([0]*100000,[9]*99999+[0],list(range(10))*10000,[1]*99999+[0]):
            add(digits,'maximum digit count with long or canonical-zero output','maxSize')
        for _ in range(140):
            add([rng.randrange(10) for _ in range(rng.randint(1,300))],'fixed-seed digit residues and lexicographic maximum')
    elif pid == '597B':
        for data in ([(1,1)],[(10**9,10**9)],[(1,2),(2,3)],[(1,4),(2,2),(3,3)],[(1,1)]*3):
            add(data,'point/saturated, touching/nested and duplicate intervals','boundary')
        for data in ([(2*i+1,2*i+1) for i in range(500000)],[(1,10**9)]*500000,[(i+1,i+2) for i in range(500000)]):
            add(data,'maximum count with disjoint, identical or endpoint touching intervals','maxSize')
        for _ in range(140):
            add([tuple(sorted((rng.randint(1,100),rng.randint(1,100)))) for _ in range(rng.randint(1,100))],'fixed-seed inclusive overlap patterns')
    else:
        for parents in ([1],[1,1,2,2,3],[1,2,3,4]):
            n = len(parents)+1
            add((parents,[(u,k) for u in range(1,n+1) for k in range(1,n+1)]),'minimum tree, branches, subtree leaf and excessive kth index','boundary')
        for parents in ([1]*199999,list(range(1,200000))):
            add((parents,[(1,200000),(200000,1),(2,199999),(200000,200000)]*50000),'maximum tree and queries, star/chain with stack-safe traversal','maxSize')
        for _ in range(140):
            n = rng.randint(2,150)
            add(([rng.randint(1,i-1) for i in range(2,n+1)],[(rng.randint(1,n),rng.randint(1,n)) for _ in range(80)]),'fixed-seed child ordering and subtree ranks')
    return cases


def review(pid,tests,samples):
    failures = []
    for name,pair in [*tests,*samples]:
        try:
            if pair['output'].split() != list(map(str,answer(pid,parse(pid,pair['input'])))):
                raise ValueError('oracle output differs from supplied bytes')
        except (ValueError,IndexError,KeyError,TypeError) as exc:
            failures.append({'test':name,'reason':str(exc)})
    return failures
