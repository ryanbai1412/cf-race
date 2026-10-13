"""Exact-answer recipes with small state-space and combinatorial cross-checks."""
from collections import Counter, deque
from functools import lru_cache
import itertools
import random


IDS = ('23B', '28B', '46C', '71C', '246D', '407B', '525C', '534C', '601A')
SEMANTICS = {
    '23B': 't,n1..100000. Simultaneous departure rounds for degrees0..n-1 leave at most max(n-2,0); exhaustive undirected friendships independently maximize survivors for n<=6.',
    '28B': 'n1..100, permutation1..n, favourite distances1..n. Swaps are undirected even when only one endpoint can initiate. Target tokens must remain inside each connected component; exhaustive permutation-state searches independently check this.',
    '46C': 'n2..1000, exactly n H/T characters, both species present. Cyclic contiguous hamster blocks minimize misplaced tigers; one arbitrary swap repairs two mismatches. All target rotations independently enumerated.',
    '71C': 'n3..100000, binary moods. Regular polygons require at least three good vertices with equal positive circular gaps dividing n; exhaustive subsets independently check the divisor search.',
    '246D': 'n,m1..100000, colors1..100000, simple undirected graph. Count distinct different neighbor colors, then choose minimum present color on ties. Exhaustive small graphs/colorings independently cross-checked.',
    '407B': 'n1..1000, pi1..i. An odd visit uses pi and an even visit uses i+1; prefix move count recurrence modulo1000000007 is independently checked by literal portal simulation.',
    '525C': 'n1..100000, lengths2..1000000. Each stick may be shortened by at most1, only once. Pair longest feasible sides then longest sides into rectangles. Exhaustive disjoint four-stick groupings independently maximize area.',
    '534C': 'n1..200000, di1..1000000, n<=A<=sum(di). For die i feasible interval is max(1,A-sum(other maxima))..min(di,A-(n-1)). Exhaustive roll outcomes independently check each impossible-value count.',
    '601A': 'n2..400, simple rail graph, m0..n(n-1)/2; roads are its complement. One network has a direct1-to-n edge, so shortest paths can avoid simultaneous intermediate stations. Independent simultaneous two-vehicle state search checks the maximum of both shortest distances.',
}


def parse(pid, text):
    if pid == '46C':
        values = text.split()
        if len(values) != 2:
            raise ValueError('animal input arity')
        n, word = int(values[0]), values[1]
        if not 2 <= n <= 1000 or len(word) != n or set(word) != {'H', 'T'}:
            raise ValueError('animal range/species')
        return word
    a = list(map(int, text.split()))
    if not a:
        raise ValueError('empty input')
    n = a[0]
    if pid == '23B':
        if not 1 <= n <= 100000 or len(a) != n+1 or not all(1 <= x <= 100000 for x in a[1:]):
            raise ValueError('party arity/range')
        return a[1:]
    if pid == '28B':
        if not 1 <= n <= 100 or len(a) != 2*n+1 or sorted(a[1:n+1]) != list(range(1,n+1)) or not all(1 <= x <= n for x in a[n+1:]):
            raise ValueError('permutation/distance arity/range')
        return a[1:n+1], a[n+1:]
    if pid == '71C':
        if not 3 <= n <= 100000 or len(a) != n+1 or not all(x in (0,1) for x in a[1:]):
            raise ValueError('knight arity/range')
        return a[1:]
    if pid == '407B':
        if not 1 <= n <= 1000 or len(a) != n+1 or not all(1 <= p <= i for i,p in enumerate(a[1:],1)):
            raise ValueError('portal arity/range')
        return a[1:]
    if pid == '525C':
        if not 1 <= n <= 100000 or len(a) != n+1 or not all(2 <= x <= 1000000 for x in a[1:]):
            raise ValueError('stick arity/range')
        return a[1:]
    if len(a) < 2:
        raise ValueError('header arity')
    if pid == '534C':
        amount, dice = a[1], a[2:]
        if not 1 <= n <= 200000 or len(dice) != n or not all(1 <= d <= 1000000 for d in dice) or not n <= amount <= sum(dice):
            raise ValueError('dice arity/range')
        return amount, dice
    m = a[1]
    offset = n+2 if pid == '246D' else 2
    edges = list(zip(a[offset::2],a[offset+1::2]))
    if (not (1 if pid == '246D' else 2) <= n <= (100000 if pid == '246D' else 400)
            or not (1 if pid == '246D' else 0) <= m <= (100000 if pid == '246D' else n*(n-1)//2)
            or len(a) != offset+2*m or not all(1 <= u <= n and 1 <= v <= n and u != v for u,v in edges)
            or len({tuple(sorted(edge)) for edge in edges}) != m):
        raise ValueError('graph arity/range/loops/duplicates')
    if pid == '246D':
        colors = a[2:offset]
        if len(colors) != n or not all(1 <= c <= 100000 for c in colors):
            raise ValueError('color arity/range')
        return colors, edges
    return n, edges


def answer(pid, data):
    if pid == '23B':
        return [max(n-2,0) for n in data]
    if pid == '28B':
        target, distances = data
        n = len(target)
        parent = list(range(n))
        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u
        for i,d in enumerate(distances):
            for j in (i-d,i+d):
                if 0 <= j < n:
                    parent[find(i)] = find(j)
        return ['YES' if all(find(i) == find(value-1) for i,value in enumerate(target)) else 'NO']
    if pid == '46C':
        n, width = len(data), data.count('H')
        doubled = data+data
        inside = doubled[:width].count('T')
        best = inside
        for start in range(1,n):
            inside += (doubled[start+width-1] == 'T') - (doubled[start-1] == 'T')
            best = min(best,inside)
        return [best]
    if pid == '71C':
        n = len(data)
        for step in range(1,n//3+1):
            if n%step == 0 and any(all(data[j] for j in range(start,n,step)) for start in range(step)):
                return ['YES']
        return ['NO']
    if pid == '246D':
        colors, edges = data
        adjacent = {c:set() for c in colors}
        for u,v in edges:
            x,y = colors[u-1],colors[v-1]
            if x != y:
                adjacent[x].add(y)
                adjacent[y].add(x)
        return [min(adjacent,key=lambda c:(-len(adjacent[c]),c))]
    if pid == '407B':
        prefix = [0]
        for p in data:
            prefix.append((2*prefix[-1] - prefix[p-1] + 2)%1000000007)
        return [prefix[-1]]
    if pid == '525C':
        sticks = sorted(data,reverse=True)
        sides = []
        i = 0
        while i+1 < len(sticks):
            if sticks[i]-sticks[i+1] <= 1:
                sides.append(sticks[i+1])
                i += 2
            else:
                i += 1
        return [sum(sides[i]*sides[i+1] for i in range(0,len(sides)-1,2))]
    if pid == '534C':
        amount,dice = data
        total,n = sum(dice),len(dice)
        return [d-(min(d,amount-n+1)-max(1,amount-total+d)+1) for d in dice]
    n,edges = data
    rail = [set() for _ in range(n)]
    for u,v in edges:
        rail[u-1].add(v-1)
        rail[v-1].add(u-1)
    def distance(complement):
        distances = [-1]*n
        distances[0] = 0
        queue = deque([0])
        while queue:
            u = queue.popleft()
            for v in range(n):
                if u != v and ((v in rail[u]) != complement) and distances[v] == -1:
                    distances[v] = distances[u]+1
                    queue.append(v)
        return distances[-1]
    x,y = distance(False),distance(True)
    return [-1 if min(x,y) == -1 else max(x,y)]


def brute(pid, data):
    if pid == '28B':
        target, distances = data
        n = len(target)
        initial = tuple(range(1,n+1))
        seen, queue = {initial},deque([initial])
        while queue:
            state = queue.popleft()
            for i,d in enumerate(distances):
                for j in (i-d,i+d):
                    if 0 <= j < n:
                        successor = list(state)
                        successor[i],successor[j] = successor[j],successor[i]
                        successor = tuple(successor)
                        if successor not in seen:
                            seen.add(successor)
                            queue.append(successor)
        return ['YES' if tuple(target) in seen else 'NO']
    if pid == '46C':
        h,n = data.count('H'),len(data)
        target = 'H'*h+'T'*(n-h)
        return [min(sum(a != b for a,b in zip(data,target[i:]+target[:i]))//2 for i in range(n))]
    if pid == '71C':
        good = [i for i,x in enumerate(data) if x]
        for size in range(3,len(good)+1):
            for polygon in itertools.combinations(good,size):
                gaps = [(polygon[(i+1)%size]-polygon[i])%len(data) for i in range(size)]
                if len(set(gaps)) == 1:
                    return ['YES']
        return ['NO']
    if pid == '246D':
        colors,edges = data
        score = {}
        for c in set(colors):
            neighbors = set()
            for i,color in enumerate(colors,1):
                if color == c:
                    for u,v in edges:
                        if u == i and colors[v-1] != c:
                            neighbors.add(colors[v-1])
                        if v == i and colors[u-1] != c:
                            neighbors.add(colors[u-1])
            score[c] = len(neighbors)
        return [min(score,key=lambda c:(-score[c],c))]
    if pid == '407B':
        visits = [0]*len(data)
        room,moves = 0,0
        while room < len(data):
            visits[room] += 1
            room = data[room]-1 if visits[room]%2 else room+1
            moves += 1
        return [moves%1000000007]
    if pid == '525C':
        @lru_cache(None)
        def solve(mask):
            indices = [i for i in range(len(data)) if mask>>i&1]
            best = 0
            for i,j,k,l in itertools.combinations(indices,4):
                for a,b,c,d in ((i,j,k,l),(i,k,j,l),(i,l,j,k)):
                    if abs(data[a]-data[b]) <= 1 and abs(data[c]-data[d]) <= 1:
                        area = min(data[a],data[b])*min(data[c],data[d])
                        best = max(best,area+solve(mask^sum(1<<x for x in (i,j,k,l))))
            return best
        return [solve((1<<len(data))-1)]
    if pid == '534C':
        amount,dice = data
        possible = [set() for _ in dice]
        for roll in itertools.product(*(range(1,d+1) for d in dice)):
            if sum(roll) == amount:
                for values,value in zip(possible,roll):
                    values.add(value)
        return [d-len(values) for d,values in zip(dice,possible)]
    n,edges = data
    rail = [set() for _ in range(n)]
    for u,v in edges:
        rail[u-1].add(v-1)
        rail[v-1].add(u-1)
    road = [set(range(n))-{u}-rail[u] for u in range(n)]
    queue,seen = deque([(0,0,0)]),{(0,0)}
    while queue:
        train,bus,time = queue.popleft()
        if train == bus == n-1:
            return [time]
        for x in ([n-1] if train == n-1 else rail[train]):
            for y in ([n-1] if bus == n-1 else road[bus]):
                if (x != y or x == n-1) and (x,y) not in seen:
                    seen.add((x,y))
                    queue.append((x,y,time+1))
    return [-1]


def extras(pid):
    rng = random.Random(16007100+IDS.index(pid))
    cases = []
    def add(text, reason, category='adversarial'):
        result = answer(pid,parse(pid,text))
        cases.append({'input':text,'output':' '.join(map(str,result))+'\n','reason':reason,'category':category})
    def array(values, reason, category='adversarial'):
        add(str(len(values))+'\n'+' '.join(map(str,values))+'\n',reason,category)
    if pid == '23B':
        for n in (1,2,3,4,99999,100000):
            add(f'1\n{n}\n','minimum/survivor threshold/maximum party','boundary')
        array([1,2,3,100000]*25000,'maximum100000 independent party queries','maxSize')
        array(list(range(1,100001)),'all100000 possible party sizes','maxSize')
        for _ in range(35):
            array([rng.randint(1,100000) for _ in range(rng.randint(1,200))],'fixed-seed multiple queries')
    elif pid == '28B':
        for p,d in (([1],[1]),([2,1],[1,2]),([2,1],[2,2]),([3,2,1],[2,3,3])):
            add(f'{len(p)}\n'+ ' '.join(map(str,p))+'\n'+' '.join(map(str,d))+'\n','isolated/asymmetric swap components','boundary')
        for n in (100,100,100):
            p = list(range(1,n+1));rng.shuffle(p)
            d = ([1]*n if len(cases)==4 else [n]*n if len(cases)==5 else [2]*n)
            add(f'{n}\n'+' '.join(map(str,p))+'\n'+' '.join(map(str,d))+'\n','maximum connected/isolated/parity components','maxSize')
        for _ in range(55):
            n = rng.randint(1,50);p=list(range(1,n+1));rng.shuffle(p);d=[rng.randint(1,n) for _ in p]
            add(f'{n}\n'+' '.join(map(str,p))+'\n'+' '.join(map(str,d))+'\n','fixed-seed directed initiation but undirected swaps')
    elif pid == '46C':
        for word in ('HT','TH','HTH','HTHT','HHTT','THHT','HTHTHTHHT'):
            add(f'{len(word)}\n{word}\n','wraparound/already grouped/interleaved','boundary')
        for word in ('HT'*500,'H'+'T'*999,'T'+'H'*999,'H'*250+'T'*500+'H'*250):
            add(f'1000\n{word}\n','maximum cyclic animal ring','maxSize')
        for _ in range(55):
            word='HT'+''.join(rng.choice('HT') for _ in range(rng.randint(0,90)))
            add(f'{len(word)}\n{word}\n','fixed-seed animal ring')
    elif pid == '71C':
        for values in ([0,0,0],[1,1,1],[1,1,0],[1,0,1,0,1,0],[0,1,0,1,0,1],[1,0,0,1,0,1]):
            array(values,'minimum polygon/cyclic residue/no two-vertex polygon','boundary')
        for values in ([0]*100000,[1]*100000,[int(i%25000==7) for i in range(100000)]):
            array(values,'maximum100000 knights/no polygon/all good/offset square','maxSize')
        for _ in range(55):
            array([rng.randrange(2) for _ in range(rng.randint(3,120))],'fixed-seed composite and prime-sized rings')
    elif pid == '246D':
        def graph(colors,edges,reason,category='adversarial'):
            add(f'{len(colors)} {len(edges)}\n'+' '.join(map(str,colors))+'\n'+''.join(f'{u} {v}\n' for u,v in edges),reason,category)
        graph([1,1],[(1,2)],'same color contributes no neighbor color','boundary')
        graph([100000,1],[(1,2)],'maximum color and minimum tie-break','boundary')
        graph([1,4,4,8,8],[(2,4),(2,5),(3,4),(3,5)],'count distinct colors not edge multiplicity or absent colors')
        graph(list(range(1,100001)),[(i,i+1) for i in range(1,100000)]+[(100000,1)],'maximum colors/n/m cycle','maxSize')
        graph([100000]+[i%9+1 for i in range(1,100000)],[(1,i) for i in range(2,100001)]+[(2,3)],'maximum star with repeated neighbor colors','maxSize')
        for _ in range(55):
            n=rng.randint(2,30);possible=list(itertools.combinations(range(1,n+1),2));rng.shuffle(possible)
            graph([rng.randint(1,10) for _ in range(n)],possible[:rng.randint(1,len(possible))],'fixed-seed simple disconnected/dense graphs')
    elif pid == '407B':
        for values in ([1],[1,1],[1,2],[1,1,2,3],[1]*30):
            array(values,'minimum/backtracking/modulus transition','boundary')
        for values in ([1]*1000,list(range(1,1001)),[max(1,i//2) for i in range(1,1001)]):
            array(values,'maximum1000 rooms/long detours/immediate advance','maxSize')
        for _ in range(55):
            array([rng.randint(1,i) for i in range(1,rng.randint(1,100)+1)],'fixed-seed valid backwards portals')
    elif pid == '525C':
        for values in ([2],[2,2,2],[2]*4,[2,3,4,5],[2,2,3,5],[100003,100004,100005,100006],[5,5,4,3,3,2,2,2]):
            array(values,'minimum/no rectangle/one-unit shortening/64-bit area','boundary')
        for values in ([1000000]*100000,[999999,1000000]*50000,[i%999999+2 for i in range(100000)]):
            array(values,'maximum100000 sticks and side lengths','maxSize')
        for _ in range(55):
            array([rng.randint(2,40) for _ in range(rng.randint(1,80))],'fixed-seed spare sticks and competing pairings')
    elif pid == '534C':
        def dice(values,amount,reason,category='adversarial'):
            add(f'{len(values)} {amount}\n'+' '.join(map(str,values))+'\n',reason,category)
        for values,amount in (([1],1),([5],3),([4,4],8),([2,3],3),([1,1,7],3),([1,1,7],9)):
            dice(values,amount,'minimum/single die/both feasible bounds','boundary')
        for amount in (200000,200000000000,100000100000):
            dice([1000000]*200000,amount,'maximum n/di and 64-bit sum','maxSize')
        for _ in range(55):
            values=[rng.randint(1,100) for _ in range(rng.randint(1,80))]
            dice(values,rng.randint(len(values),sum(values)),'fixed-seed dice feasible interval intersection')
    else:
        def graph(n,edges,reason,category='adversarial'):
            add(f'{n} {len(edges)}\n'+''.join(f'{u} {v}\n' for u,v in edges),reason,category)
        graph(2,[],'minimum rail-disconnected graph','boundary')
        graph(2,[(1,2)],'minimum road-disconnected graph','boundary')
        graph(4,[(1,3),(3,4)],'one network direct and the other takes two hops','boundary')
        graph(400,[],'maximum nodes/no railways','maxSize')
        graph(400,list(itertools.combinations(range(1,401),2)),'maximum nodes/all79800 railways/no roads','maxSize')
        graph(400,[(i,i+1) for i in range(1,400)],'maximum399-hop train route and direct road','maxSize')
        for _ in range(55):
            n=rng.randint(2,25)
            graph(n,[edge for edge in itertools.combinations(range(1,n+1),2) if rng.randrange(2)],'fixed-seed graph and complement connectivity')
    return cases


def brute_checks():
    counts = Counter()
    def check(pid,data):
        assert answer(pid,data) == brute(pid,data), (pid,data)
        counts[pid] += 1
    for n in range(1,7):
        edges = list(itertools.combinations(range(n),2))
        best = 0
        for mask in range(1<<len(edges)):
            adjacency = [set() for _ in range(n)]
            for i,(u,v) in enumerate(edges):
                if mask>>i&1:
                    adjacency[u].add(v);adjacency[v].add(u)
            remaining = set(range(n))
            for degree in range(n):
                remaining -= {u for u in remaining if len(adjacency[u]&remaining)==degree}
            best=max(best,len(remaining));counts['23B'] += 1
        assert answer('23B',[n]) == [best]
    for n in range(1,5):
        for distances in itertools.product(range(1,n+1),repeat=n):
            for target in itertools.permutations(range(1,n+1)):
                check('28B',(target,distances))
    for n in range(2,10):
        for word in itertools.product('HT',repeat=n):
            if len(set(word))==2:
                check('46C',''.join(word))
    for n in range(3,11):
        for moods in itertools.product((0,1),repeat=n):
            check('71C',moods)
    for n in range(2,5):
        edges=list(itertools.combinations(range(1,n+1),2))
        for mask in range(1,1<<len(edges)):
            selected=[e for i,e in enumerate(edges) if mask>>i&1]
            for colors in itertools.product(range(1,4),repeat=n):
                check('246D',(colors,selected))
    for n in range(1,7):
        for portals in itertools.product(*(range(1,i+1) for i in range(1,n+1))):
            check('407B',portals)
    for n in range(1,7):
        for sticks in itertools.product(range(2,6),repeat=n):
            check('525C',sticks)
    rng=random.Random(1600534)
    for _ in range(40):
        check('525C',[rng.randint(2,8) for _ in range(8)])
    for n in range(1,5):
        for dice in itertools.product(range(1,5),repeat=n):
            for amount in range(n,sum(dice)+1):
                check('534C',(amount,dice))
    for n in range(2,6):
        edges=list(itertools.combinations(range(1,n+1),2))
        for mask in range(1<<len(edges)):
            check('601A',(n,[e for i,e in enumerate(edges) if mask>>i&1]))
    return dict(counts)


def review(pid, tests, samples):
    failures = []
    for name,pair in [*tests,*samples]:
        try:
            expected = list(map(str,answer(pid,parse(pid,pair['input']))))
            actual = pair['output'].split()
            if pid in ('28B','71C'):
                actual = [value.upper() for value in actual]
            if actual != expected:
                raise ValueError('oracle output differs from supplied bytes')
        except (ValueError,IndexError,KeyError,TypeError) as exc:
            failures.append({'test':name,'reason':str(exc)})
    return failures
