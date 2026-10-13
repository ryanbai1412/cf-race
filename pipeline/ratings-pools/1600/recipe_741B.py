"""Arpa's weak amphitheater and Mehrdad's valuable Hoses (741B): grouped 0/1 knapsack over friendship components."""
from collections import deque
import itertools
import random
import re


IDS = ('741B',)
SEMANTICS = {
    '741B': 'Line 1: n m w (1<=n<=1000, 0<=m<=min(n(n-1)/2,10^5), 1<=w<=1000); line 2: n weights 1..1000; '
            'line 3: n beauties 1..10^6; then m lines x y (1<=x,y<=n, x!=y, all pairs distinct). Friendship groups are '
            'connected components; from each group invite all of it, exactly one member, or nobody. Print the unique '
            'maximum total beauty with total weight <= w (0 when nothing fits; at most 1000*10^6 = 10^9). Oracle: '
            'union-find components plus grouped knapsack over capacities in O((n+groups)*w); checked against subset '
            'enumeration with transitive-closure groups, per-group option enumeration, and a sparse exact-weight DP.',
}
MAX_N = 1000
MAX_M = 10 ** 5
MAX_W = 1000
MAX_WEIGHT = 1000
MAX_B = 10 ** 6
_INT = re.compile(r'0|[1-9][0-9]*')


def _int(token, what):
    if not _INT.fullmatch(token):
        raise ValueError(f'{what} not a canonical nonnegative integer')
    return int(token)


def _row(line, count, what):
    tokens = line.split()
    if len(tokens) != count:
        raise ValueError(f'{what} arity')
    return [_int(t, what) for t in tokens]


def parse(pid, text):
    if pid != '741B':
        raise ValueError('unknown problem')
    lines = text.splitlines()
    if len(lines) < 3:
        raise ValueError('line layout: expected at least three lines')
    n, m, w = _row(lines[0], 3, 'header')
    if not 1 <= n <= MAX_N:
        raise ValueError('n range')
    if not 0 <= m <= min(n * (n - 1) // 2, MAX_M):
        raise ValueError('m range')
    if not 1 <= w <= MAX_W:
        raise ValueError('w range')
    if len(lines) != 3 + m:
        raise ValueError('line layout: expected 3 + m lines')
    weights = _row(lines[1], n, 'weights')
    beauties = _row(lines[2], n, 'beauties')
    if not all(1 <= x <= MAX_WEIGHT for x in weights):
        raise ValueError('w_i range')
    if not all(1 <= x <= MAX_B for x in beauties):
        raise ValueError('b_i range')
    edges = [tuple(_row(line, 2, 'friend pair')) for line in lines[3:]]
    if not all(1 <= x <= n and 1 <= y <= n and x != y for x, y in edges):
        raise ValueError('friend pair range/self-pair')
    if len(set(edges)) != m:
        raise ValueError('friend pairs not distinct')
    return w, weights, beauties, edges


def groups_dsu(n, edges):
    parent = list(range(n))

    def find(u):
        root = u
        while parent[root] != root:
            root = parent[root]
        while parent[u] != root:
            parent[u], u = root, parent[u]
        return root

    for x, y in edges:
        a, b = find(x - 1), find(y - 1)
        if a != b:
            parent[a] = b
    members = {}
    for i in range(n):
        members.setdefault(find(i), []).append(i)
    return list(members.values())


def answer(pid, data):
    cap, weights, beauties, edges = data
    best = [0] * (cap + 1)
    for group in groups_dsu(len(weights), edges):
        options = [(weights[i], beauties[i]) for i in group]
        if len(group) > 1:
            options.append((sum(weights[i] for i in group), sum(beauties[i] for i in group)))
        new = best[:]
        for wt, b in options:
            if wt <= cap:
                new[wt:] = map(max, new[wt:], [x + b for x in best[:cap + 1 - wt]])
        best = new
    return best[cap]


def groups_closure(n, edges):
    reach = [[i == j for j in range(n)] for i in range(n)]
    for x, y in edges:
        reach[x - 1][y - 1] = reach[y - 1][x - 1] = True
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = True
    return [min(j for j in range(n) if reach[i][j]) for i in range(n)]


def brute_subsets(data):
    cap, weights, beauties, edges = data
    n = len(weights)
    label = groups_closure(n, edges)
    size = {g: label.count(g) for g in set(label)}
    best = 0
    for mask in range(1 << n):
        chosen = [i for i in range(n) if mask >> i & 1]
        if sum(weights[i] for i in chosen) > cap:
            continue
        count = {}
        for i in chosen:
            count[label[i]] = count.get(label[i], 0) + 1
        if all(c == 1 or c == size[g] for g, c in count.items()):
            best = max(best, sum(beauties[i] for i in chosen))
    return best


def groups_propagation(n, edges):
    label = list(range(n))
    changed = True
    while changed:
        changed = False
        for x, y in edges:
            low = min(label[x - 1], label[y - 1])
            if label[x - 1] != low or label[y - 1] != low:
                label[x - 1] = label[y - 1] = low
                changed = True
    groups = {}
    for i, g in enumerate(label):
        groups.setdefault(g, []).append(i)
    return list(groups.values())


def brute_choices(data):
    cap, weights, beauties, edges = data
    per_group = []
    for group in groups_propagation(len(weights), edges):
        options = [[]] + [[i] for i in group]
        if len(group) > 1:
            options.append(list(group))
        per_group.append(options)
    best = 0
    for pick in itertools.product(*per_group):
        chosen = [i for option in pick for i in option]
        if sum(weights[i] for i in chosen) <= cap:
            best = max(best, sum(beauties[i] for i in chosen))
    return best


def sparse_exact(data):
    cap, weights, beauties, edges = data
    n = len(weights)
    adj = [[] for _ in range(n)]
    for x, y in edges:
        adj[x - 1].append(y - 1)
        adj[y - 1].append(x - 1)
    seen = [False] * n
    reach = {0: 0}
    for start in range(n):
        if seen[start]:
            continue
        seen[start] = True
        group, queue = [], deque([start])
        while queue:
            u = queue.popleft()
            group.append(u)
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    queue.append(v)
        items = {(weights[i], beauties[i]) for i in group}
        if len(group) > 1:
            items.add((sum(weights[i] for i in group), sum(beauties[i] for i in group)))
        nxt = dict(reach)
        for total, value in reach.items():
            for wt, b in items:
                if total + wt <= cap and nxt.get(total + wt, -1) < value + b:
                    nxt[total + wt] = value + b
        reach = nxt
    return max(reach.values())


def render(cap, weights, beauties, edges):
    head = f'{len(weights)} {len(edges)} {cap}\n' + ' '.join(map(str, weights)) + '\n' + ' '.join(map(str, beauties)) + '\n'
    return head + ''.join(f'{x} {y}\n' for x, y in edges)


def random_edges(rng, n, m):
    if m * 4 > n * (n - 1) // 2:
        chosen = rng.sample(list(itertools.combinations(range(1, n + 1), 2)), m)
    else:
        found = set()
        while len(found) < m:
            a, b = rng.sample(range(1, n + 1), 2)
            found.add((min(a, b), max(a, b)))
        chosen = sorted(found)
        rng.shuffle(chosen)
    return [(a, b) if rng.random() < 0.5 else (b, a) for a, b in chosen]


def extras(pid):
    rng = random.Random(741002)
    cases = []
    seen = {'3 1 5\n3 2 5\n2 4 2\n1 2\n', '4 2 11\n2 4 6 6\n6 4 2 1\n1 2\n2 3\n'}

    def add(cap, weights, beauties, edges, reason, category='adversarial'):
        text = render(cap, weights, beauties, edges)
        if text in seen:
            return
        seen.add(text)
        output = f'{answer(pid, parse(pid, text))}\n'
        cases.append({'input': text, 'output': output, 'reason': reason, 'category': category})

    add(1, [1], [1], [], 'minimum n=1 m=0 w=1: the single Hos fits', 'boundary')
    add(1, [2], [5], [], 'minimum n=1 with w_1 > w: nothing fits, answer 0', 'boundary')
    add(MAX_W, [MAX_WEIGHT], [MAX_B], [], 'n=1 weight exactly w=1000, beauty 10^6', 'boundary')
    add(MAX_W, [MAX_WEIGHT, 1], [1, MAX_B], [], 'n=2 m=0 total weight 1001 > w=1000: take only the light 10^6 Hos', 'boundary')
    add(3, [1, 2], [4, 5], [(1, 2)], 'n=2 one group whose total weight equals w exactly: invite both (9)', 'boundary')
    add(2, [1, 2], [4, 5], [(2, 1)], 'n=2 group total 3 > w=2: only one member, the heavier one (5)', 'boundary')
    add(1, [2, 3, 4], [1, 1, 1], [(1, 2)], 'all weights exceed w: answer 0', 'boundary')
    add(10, [1] * 5, [1, 2, 3, 4, 5], [(a, b) for a, b in itertools.combinations(range(1, 6), 2)],
        'complete graph n=5 (m=n(n-1)/2=10): whole group fits (15)', 'boundary')
    add(4, [1] * 5, [1, 2, 3, 4, 5], [(a, b) for a, b in itertools.combinations(range(1, 6), 2)],
        'complete graph n=5 whole group too heavy: best single member 5', 'boundary')
    add(MAX_W, [1] * 10, [MAX_B] * 10, [], 'ten singletons of weight 1 and beauty 10^6 all fit', 'boundary')
    add(5, [1, 1, 1, 1, 1], [5, 1, 1, 1, 1], [(1, 2), (2, 3), (3, 4), (4, 5)],
        'one path group of total weight exactly w=5: whole group (9) beats any one member (5)', 'boundary')
    add(4, [1, 1, 1, 1, 1], [5, 1, 1, 1, 1], [(1, 2), (2, 3), (3, 4), (4, 5)],
        'same path group with w=4 one less than total: only one member (5)', 'boundary')

    add(10, [2, 4, 6, 6], [6, 4, 2, 1], [(1, 2), (2, 3)],
        'w=10 variant of sample 2: Hos 1 and 2 of one group together (10) are illegal, whole group weighs 12; correct 7')
    add(4, [2, 2, 2], [5, 5, 1], [(1, 2), (2, 3)],
        'path group of three with total 6 > w=4: two members (10) are illegal; correct single 5')
    add(6, [4, 4, 2], [1, 1, 1], [(1, 3), (2, 3)],
        'path 1-3-2 total 10 > w=6: group-blind knapsack and one-directional adjacency both take two members (2); correct 1')
    add(2, [1, 1, 1, 1], [5, 5, 1, 5], [(4, 1), (4, 2)],
        'star centred at Hos 4 listed as (4,1),(4,2): BFS from Hos 1 over one-directional edges never reaches 4 (10); correct 6')
    add(2, [1, 1, 1], [5, 1, 5], [(2, 1), (3, 2)],
        'chain listed high-to-low (2,1),(3,2): one-directional adjacency splits it and takes Hos 1 and 3 (10); correct 5')
    add(6, [3, 2, 5], [2, 4, 2], [(1, 2)],
        'w=6 variant of sample 1: friend-skipping beauty greedy takes Hos 2 (4) and then nothing fits; correct whole group {1,2} = 6')
    add(10, [9, 2, 2], [10, 8, 8], [],
        'beauty greedy takes the 10 of weight 9 and is stuck at 10; correct 8+8 = 16')
    add(4, [3, 1], [1, 1], [(1, 2)],
        'group {1,2} total exactly w=4: whole group 2; friend-skipping greedy and whole-group-forgotten DP print 1')
    add(1, [2, 2], [1, 1], [],
        'index-as-weight: Hos 1 of real weight 2 is costed by its index 1 and fits w=1 (prints 1); correct 0')
    add(3, [2, 1, 1, 1], [9, 1, 1, 9], [(1, 3)],
        'group {1,3} with heavy Hos 1: index-as-weight costing lets the mutant exceed capacity (19); correct 18')
    add(2, [1, 3], [1, 1], [],
        'second group heavier than w: a DP row that leaves dp[i][j]=0 instead of carrying dp[i-1][j] prints 0; correct 1')
    add(6, [3, 3, 9, 9], [4, 4, 100, 100], [(3, 4)],
        'last group cannot fit at all: the dropped carry prints 0 instead of 8')
    add(3, [1, 3], [2, 5], [(1, 2)],
        'best-ratio representative Hos 1 (2 per unit) replaces the best affordable single Hos 2 (5): prints 2; correct 5')
    add(1, [3, 1], [1, 1], [(1, 2)],
        'group {1,2} total 4 > w=1: only Hos 2 alone fits; forgetting single members prints 0; correct 1')
    add(3, [1, 2, 1], [1, 1, 1], [(1, 3)],
        'independent member items stack on the whole-group item (whole {1,3} plus Hos 1 again, 3); correct 2')
    add(6, [3, 3, 3], [10, 10, 10], [(1, 2), (1, 3)],
        'star group: member-outer in-place updates take two members (20); whole group 9 > 6 so correct 10')
    add(5, [1, 2, 1, 4], [1, 2, 1, 1], [(2, 3), (3, 4)],
        'group {2,3,4} listed before loner 1: consecutive-index slicing treats Hos 1..3 as the group (prints 4); correct 3')
    add(4, [1, 3, 1, 3], [1, 9, 1, 9], [(1, 3), (2, 4)],
        'interleaved groups {1,3},{2,4}: one member from each (10)')
    add(4, [1, 3], [3, 1], [],
        'ascending-capacity in-place knapsack reuses the weight-1 Hos four times (12); correct 4')
    add(10, [3, 3, 3, 4], [5, 5, 5, 1], [(1, 2), (2, 3), (3, 4)],
        'group total 13 > w=10: exactly one member allowed (5), never three (15)')
    add(9, [3, 3, 3], [5, 5, 5], [(1, 2), (2, 3)],
        'group total exactly w=9: whole group 15; whole-group-forgotten solutions print 5', 'boundary')
    add(9, [3, 3, 3, 1], [5, 5, 5, 20], [(1, 2), (2, 3)],
        'one member plus loner (25) beats the whole group alone (15); whole group plus loner weighs 10 > 9')
    add(10, [3, 3, 3, 1], [5, 5, 5, 20], [(1, 2), (2, 3)],
        'loner plus whole group fits exactly w=10 (35)')
    add(6, [2, 2, 2], [4, 4, 4], [],
        'three singletons all fit: loners are unconstrained (12)')
    add(6, [2, 2, 2], [4, 4, 4], [(1, 2)],
        'pair group plus loner: whole pair (8) + loner (4) = 12 fits exactly')
    add(5, [2, 2, 2], [4, 4, 4], [(1, 2), (2, 3)],
        'group of three total 6 > w=5: two members (8) illegal, correct 4')
    add(7, [3, 4, 3, 4], [6, 7, 6, 7], [(1, 2), (3, 4)],
        'two pair groups: whole pair (13) ties one member from each (6+7); two heavy members would weigh 8 > 7')
    add(1000, [500, 500, 1], [1, 1, MAX_B], [(1, 2)],
        'whole pair weighs exactly 1000 = w with beauty 2, but one member plus the 10^6 loner (1000001) is better')
    add(1000, [999, 2], [MAX_B, MAX_B], [(1, 2)],
        'group total 1001 just over w=1000: only one member', 'boundary')
    add(1000, [999, 1], [MAX_B, MAX_B], [(1, 2)],
        'group total exactly 1000: both members (2*10^6)', 'boundary')

    for size in (2, 3, 4, 6, 8):
        n = size * 3
        groups = [list(range(k * size + 1, (k + 1) * size + 1)) for k in range(3)]
        edges = [(g[i], g[i + 1]) for g in groups for i in range(size - 1)]
        rng.shuffle(edges)
        ws = [rng.randint(1, 6) for _ in range(n)]
        bs = [rng.randint(1, 50) for _ in range(n)]
        add(sum(ws) // 3, ws, bs, edges, f'three path groups of size {size}, capacity a third of total weight')

    n = 447
    clique = list(itertools.combinations(range(1, n + 1), 2))
    add(MAX_W, [rng.randint(1, 5) for _ in range(n)], [rng.randint(1, MAX_B) for _ in range(n)],
        random_edges(rng, n, len(clique)), 'complete graph n=447 (m=99681=n(n-1)/2 <= 10^5): one group, whole vs single', 'maxSize')

    n = MAX_N
    add(MAX_W, [1] * n, [MAX_B] * n, [], 'n=1000 m=0 w=1000 all weight 1, beauty 10^6: maximum answer 10^9', 'maxSize')
    add(MAX_W, [rng.randint(1, MAX_WEIGHT) for _ in range(n)], [rng.randint(1, MAX_B) for _ in range(n)],
        random_edges(rng, n, MAX_M), 'maximum n=1000 m=10^5 w=1000 random graph: one giant group', 'maxSize')
    edges = list(itertools.combinations(range(1, 448), 2))
    rest = list(range(448, n + 1))
    for start in range(0, len(rest), 5):
        chunk = rest[start:start + 5]
        edges += [(chunk[i], chunk[i + 1]) for i in range(len(chunk) - 1)][:MAX_M - len(edges)]
    rng.shuffle(edges)
    edges = [(a, b) if rng.random() < 0.5 else (b, a) for a, b in edges]
    add(MAX_W, [rng.randint(1, 60) for _ in range(n)], [rng.randint(1, MAX_B) for _ in range(n)], edges,
        'maximum n=1000 m=10^5: a 447-clique (99681 edges) plus 319 path edges over groups of up to 5 and 154 loners', 'maxSize')
    order = list(range(1, n + 1))
    rng.shuffle(order)
    add(MAX_W, [rng.randint(1, 3) for _ in range(n)], [rng.randint(1, MAX_B) for _ in range(n)],
        [(order[i], order[i + 1]) for i in range(n - 1)],
        'n=1000 single random-order path (m=999): 1000-deep recursive DFS/find exceeds Python default recursion', 'maxSize')
    pairs = [(2 * i + 1, 2 * i + 2) for i in range(n // 2)]
    add(MAX_W, [rng.randint(1, 20) for _ in range(n)], [rng.randint(1, MAX_B) for _ in range(n)], pairs,
        'n=1000 m=500 disjoint pairs: 500 groups, full O((n+groups)*w) DP work', 'maxSize')

    while len(cases) < 150:
        n = rng.randint(1, 10)
        m = rng.randint(0, n * (n - 1) // 2)
        wmax = rng.choice((1, 3, 10, 1000))
        ws = [rng.randint(1, wmax) for _ in range(n)]
        bs = [rng.randint(1, rng.choice((3, 100, MAX_B))) for _ in range(n)]
        cap = rng.randint(1, min(MAX_W, max(1, sum(ws))))
        add(cap, ws, bs, random_edges(rng, n, m), f'fixed-seed random small case (n={n}, m={m}, weights<={wmax})')
    return cases


def brute_checks():
    count = 0

    def check(data, exhaustive=True):
        nonlocal count
        expected = answer('741B', data)
        assert sparse_exact(data) == expected, data
        count += 1
        if exhaustive:
            assert brute_subsets(data) == expected, data
            assert brute_choices(data) == expected, data
            count += 2

    for n in range(1, 4):
        pairs = list(itertools.combinations(range(1, n + 1), 2))
        graphs = [[p for p, keep in zip(pairs, bits) if keep] for bits in itertools.product((0, 1), repeat=len(pairs))]
        for ws in itertools.product((1, 2, 3), repeat=n):
            for bs in itertools.product((1, 2, 4), repeat=n):
                for edges in graphs:
                    for cap in range(1, sum(ws) + 1):
                        check((cap, list(ws), list(bs), edges))
    rng = random.Random(741001)
    for _ in range(1500):
        n = rng.randint(1, 10)
        m = rng.randint(0, n * (n - 1) // 2)
        ws = [rng.randint(1, rng.choice((2, 5, 1000))) for _ in range(n)]
        bs = [rng.randint(1, rng.choice((3, 1000, MAX_B))) for _ in range(n)]
        cap = rng.randint(1, min(MAX_W, sum(ws)))
        check((cap, ws, bs, random_edges(rng, n, m)))
    for _ in range(60):
        n = rng.randint(20, 200)
        m = rng.randint(0, min(n * (n - 1) // 2, 3 * n))
        ws = [rng.randint(1, rng.choice((10, 100, 1000))) for _ in range(n)]
        bs = [rng.randint(1, MAX_B) for _ in range(n)]
        check((rng.randint(1, MAX_W), ws, bs, random_edges(rng, n, m)), False)
    return {'741B': count}


def review(pid, tests, samples):
    failures = []
    for name, pair in [*tests, *samples]:
        try:
            expected = str(answer(pid, parse(pid, pair['input'])))
            lines = [line.split() for line in pair['output'].splitlines()]
            if len(lines) != 1 or len(lines[0]) != 1:
                failures.append({'test': name, 'reason': 'output layout: expected exactly one integer line'})
            elif lines[0][0] != expected:
                failures.append({'test': name, 'reason': 'independent oracle disagreement', 'expected': expected,
                                 'actual': lines[0][0]})
        except ValueError as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
