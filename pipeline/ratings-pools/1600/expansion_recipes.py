"""Exact integer/sequence recipes with independent exhaustive small checks."""
from collections import Counter
import heapq
import itertools
import math
import random

IDS = ('599C', '777C', '898E', '962D')
SEMANTICS = {
    '599C': 'n1..100000; heights1..10^9. A cut is valid exactly when left maximum <= right minimum; count all such cuts. Exhaustive contiguous partitions independently checked, including duplicate heights.',
    '777C': 'Positive rows/columns with product<=100000, entries1..10^9, q1..100000, queries1<=l<=r<=n. Minimum start of a nondecreasing suffix over columns at each row answers whether some column is sorted on the requested interval. Direct per-query column enumeration checked.',
    '898E': 'Even n2..200000; amounts0..10^9. Exactly half must be perfect squares, including0. Nearest square conversion cost or cheapest nonsquare conversion cost (2 for0,1 for positive squares) gives minimum. Exhaustive target-half subsets with direct linear conversion search checked.',
    '962D': 'n2..150000; values1..10^9. Always merge the leftmost two instances of the smallest repeated value, retaining the right index. A value/index heap reproduces the unique final array in original index order. Direct mutable-array operations independently checked.',
}


def parse(pid, text):
    a = list(map(int, text.split()))
    if pid == '777C':
        if len(a) < 4:
            raise ValueError('matrix arity')
        n, m = a[:2]
        if n < 1 or m < 1 or n*m > 100000 or len(a) < 3+n*m:
            raise ValueError('matrix dimensions/arity')
        values = a[2:2+n*m]
        q = a[2+n*m]
        pairs = list(zip(a[3+n*m::2], a[4+n*m::2]))
        if not 1 <= q <= 100000 or len(a) != 3+n*m+2*q:
            raise ValueError('query count/arity')
        if not all(1 <= x <= 10**9 for x in values) or not all(1 <= l <= r <= n for l,r in pairs):
            raise ValueError('matrix/query range')
        return [values[i*m:(i+1)*m] for i in range(n)], pairs
    if not a:
        raise ValueError('empty array')
    n, values = a[0], a[1:]
    lower, upper = {'599C':(1,100000), '898E':(2,200000), '962D':(2,150000)}[pid]
    if not lower <= n <= upper or len(values) != n or (pid == '898E' and n%2):
        raise ValueError('array count/parity')
    if not all((0 if pid == '898E' else 1) <= x <= 10**9 for x in values):
        raise ValueError('array value range')
    return values


def answer(pid, data):
    if pid == '599C':
        right = [0]*len(data)
        right[-1] = data[-1]
        for i in range(len(data)-2,-1,-1):
            right[i] = min(data[i], right[i+1])
        cuts, left = 1, 0
        for i,x in enumerate(data[:-1]):
            left = max(left,x)
            cuts += left <= right[i+1]
        return [cuts]
    if pid == '777C':
        rows, queries = data
        starts = [1]*len(rows[0])
        earliest = [1]
        for i in range(1,len(rows)):
            for j in range(len(starts)):
                if rows[i][j] < rows[i-1][j]:
                    starts[j] = i+1
            earliest.append(min(starts))
        return ['Yes' if earliest[r-1] <= l else 'No' for l,r in queries]
    if pid == '898E':
        squares = [x for x in data if math.isqrt(x)**2 == x]
        delta = len(data)//2-len(squares)
        if delta > 0:
            costs = [min(x-math.isqrt(x)**2,(math.isqrt(x)+1)**2-x) for x in data if math.isqrt(x)**2 != x]
        else:
            costs = [2 if x == 0 else 1 for x in squares]
        return [sum(sorted(costs)[:abs(delta)])]
    heap = [(x,i) for i,x in enumerate(data)]
    heapq.heapify(heap)
    final = []
    while heap:
        x,i = heapq.heappop(heap)
        if heap and heap[0][0] == x:
            _,j = heapq.heappop(heap)
            heapq.heappush(heap,(2*x,j))
        else:
            final.append((i,x))
    values = [x for _,x in sorted(final)]
    return [len(values), *values]


def brute(pid, data):
    if pid == '599C':
        best = 0
        for mask in range(1 << (len(data)-1)):
            start, sorted_blocks, blocks = 0, [], 0
            for i in range(len(data)):
                if i == len(data)-1 or mask & (1<<i):
                    sorted_blocks.extend(sorted(data[start:i+1]))
                    start, blocks = i+1, blocks+1
            if sorted_blocks == sorted(data):
                best = max(best,blocks)
        return [best]
    if pid == '777C':
        rows, queries = data
        return ['Yes' if any(all(rows[i][j] <= rows[i+1][j] for i in range(l-1,r-1)) for j in range(len(rows[0]))) else 'No' for l,r in queries]
    if pid == '898E':
        costs = []
        for x in data:
            pair = []
            for want_square in (False,True):
                distance = 0
                while not any(y >= 0 and (math.isqrt(y)**2 == y) == want_square for y in (x-distance,x+distance)):
                    distance += 1
                pair.append(distance)
            costs.append(pair)
        return [min(sum(costs[i][int(i in subset)] for i in range(len(data))) for subset in itertools.combinations(range(len(data)),len(data)//2))]
    values = list(data)
    while True:
        repeats = [x for x,count in Counter(values).items() if count >= 2]
        if not repeats:
            return [len(values), *values]
        x = min(repeats)
        i = values.index(x)
        j = values.index(x,i+1)
        values[j] = 2*x
        values.pop(i)


def brute_checks():
    counts = Counter()
    def check(pid,data):
        assert answer(pid,data) == brute(pid,data), (pid,data)
        counts[pid] += 1
    for n in range(1,7):
        for a in itertools.product(range(1,4),repeat=n):
            check('599C',a)
            if n >= 2:
                check('962D',a)
    for n in (2,4,6):
        for a in itertools.product(range(4),repeat=n):
            check('898E',a)
    for n,m in ((1,1),(1,3),(3,1),(2,2),(3,2)):
        for a in itertools.product(range(1,4),repeat=n*m):
            rows = [a[i*m:(i+1)*m] for i in range(n)]
            check('777C',(rows,[(l,r) for l in range(1,n+1) for r in range(l,n+1)]))
    return dict(counts)


def extras(pid):
    rng = random.Random(160000+int(pid[:-1]))
    cases = []
    def add(data,reason,category='adversarial'):
        if pid == '777C':
            rows,queries = data
            text = f'{len(rows)} {len(rows[0])}\n'+''.join(' '.join(map(str,row))+'\n' for row in rows)+f'{len(queries)}\n'+''.join(f'{l} {r}\n' for l,r in queries)
        else:
            text = str(len(data))+'\n'+' '.join(map(str,data))+'\n'
        expected = answer(pid,parse(pid,text))
        output = (str(expected[0])+'\n'+' '.join(map(str,expected[1:]))+'\n') if pid == '962D' else '\n'.join(map(str,expected))+'\n'
        cases.append({'input':text,'output':output,'category':category,'reason':reason})
    if pid == '777C':
        for rows in ([[1]],[[10**9]],[[1,10**9],[2,1],[1,2]],[[1,2],[2,1]]):
            add((rows,[(l,r) for l in range(1,len(rows)+1) for r in range(l,len(rows)+1)]),'singleton/extreme or changing only sorted column','boundary')
        add(([[i+1] for i in range(100000)],[(1,100000)]*100000),'maximum rows/elements and maximum queries','maxSize')
        add(([[10**9-i] for i in range(100000)],[(1,100000),(100000,100000)]),'maximum strictly decreasing column','maxSize')
        add(([[1]*100000],[(1,1)]*100000),'maximum width/elements and repeated singleton queries','maxSize')
        add(([[1+(i+j)%2 for j in range(100)] for i in range(1000)],[(1,1000),(998,1000),(999,1000),(1,1)]),'maximum matrix product with incompatible column decreases','maxSize')
        for _ in range(160):
            n,m = rng.randint(1,20),rng.randint(1,12)
            rows = [[rng.randint(1,10) for _ in range(m)] for _ in range(n)]
            add((rows,[tuple(sorted((rng.randint(1,n),rng.randint(1,n)))) for _ in range(30)]),'fixed-seed all interval/column direction combinations')
    else:
        fixed = {'599C':[[1],[10**9],[1,1,1],[3,1,2],[2,1,3,2]],'898E':[[0,0],[1,1],[2,2],[0,1,2,4],[999950884,10**9]],'962D':[[1,1],[1,2],[10**9,10**9],[1,1,3,1,1],[3,4,1,2,2,1,1]]}[pid]
        for data in fixed:
            add(data,'minimum dimensions, ties, zeros or adjacent-square/merge behavior','boundary')
        limit = {'599C':100000,'898E':200000,'962D':150000}[pid]
        if pid == '599C':
            for data in (list(range(1,limit+1)),list(range(limit,0,-1)),[10**9]*limit,([2,1]*(limit//2))):
                add(data,'maximum ascending/descending/tie/local inversions','maxSize')
        elif pid == '898E':
            for data in ([0]*limit,[10**9]*limit,[0,2]*(limit//2),[1,4,9,16]*(limit//4)):
                add(data,'maximum all zeros/nonsquares/balanced/positive squares','maxSize')
        else:
            for data in ([1]*limit,[10**9]*limit,list(range(1,limit+1)),[1,2,4,8,16]*(limit//5)):
                add(data,'maximum carry chains, overflow-sized output or distinct values','maxSize')
        for _ in range(160):
            n = rng.randint(1 if pid == '599C' else 2,100)
            if pid == '898E':
                n += n%2
            add([rng.randint(0 if pid == '898E' else 1,50 if rng.randrange(2) else 10**9) for _ in range(n)],'fixed-seed dense ties and sparse large values')
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
