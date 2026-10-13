"""1600/682C Alyona and the Tree: remove every subtree whose top vertex is sad-making."""
from collections import deque
import itertools
import random
import re

IDS = ('682C',)
SEMANTICS = {
    '682C': 'n 1..10^5, a_i 1..10^9, n-1 lines "p_i c_i" with 1<=p_i<=n and -10^9<=c_i<=10^9 joining vertices i+1 and p_i into a tree rooted at 1 '
            '(public statement 10<sup>5</sup>/10<sup>9</sup>; row text flattened to 105/109). '
            'Leaf removal can delete any root-free subtree and nothing else, and a vertex u must go iff some ancestor v has dist(v,u)>a_u, '
            'so the answer is the size of the union of those subtrees: one integer, unique. '
            'Oracle: BFS from 1 with best suffix sum max(0,best(parent))+c; checked against exhaustive leaf-removal state search and a prefix-minimum reference.',
}

MAX_N = 100000
MAX_A = 10 ** 9
POS = re.compile(r'[1-9][0-9]*')
SIGNED = re.compile(r'0|-?[1-9][0-9]*')


def _int(token, pattern, low, high, what):
    if not pattern.fullmatch(token):
        raise ValueError(what + ' token malformed')
    value = int(token)
    if not low <= value <= high:
        raise ValueError(what + ' out of range')
    return value


def parse(pid, text):
    if pid != '682C':
        raise ValueError('unknown problem ' + pid)
    rows = [line.split() for line in text.strip().splitlines()]
    if not rows or len(rows[0]) != 1:
        raise ValueError('first line must hold n only')
    n = _int(rows[0][0], POS, 1, MAX_N, 'n')
    if len(rows) != n + 1 or len(rows[1]) != n or any(len(row) != 2 for row in rows[2:]):
        raise ValueError('line layout must be 1, n, then n-1 lines of 2 tokens')
    a = [_int(t, POS, 1, MAX_A, 'a_i') for t in rows[1]]
    edges = []
    root = list(range(n + 1))

    def find(x):
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x

    for i, (pt, ct) in enumerate(rows[2:]):
        p = _int(pt, POS, 1, n, 'p_i')
        c = _int(ct, SIGNED, -MAX_A, MAX_A, 'c_i')
        x, y = find(i + 2), find(p)
        if x == y:
            raise ValueError('edges do not form a tree')
        root[x] = y
        edges.append((p, c))
    return n, a, edges


def _adjacency(n, edges):
    adj = [[] for _ in range(n + 1)]
    for i, (p, c) in enumerate(edges):
        adj[i + 2].append((p, c))
        adj[p].append((i + 2, c))
    return adj


def answer(pid, data):
    n, a, edges = data
    adj = _adjacency(n, edges)
    best = [0] * (n + 1)
    seen = [False] * (n + 1)
    seen[1] = True
    queue = deque([1])
    kept = 0
    while queue:
        u = queue.popleft()
        kept += 1
        for v, c in adj[u]:
            if not seen[v]:
                seen[v] = True
                d = max(best[u], 0) + c
                if d <= a[v - 1]:
                    best[v] = d
                    queue.append(v)
    return n - kept


def prefix_reference(data):
    n, a, edges = data
    adj = _adjacency(n, edges)
    parent = [0] * (n + 1)
    depth_sum = [0] * (n + 1)
    lowest_ancestor = [0] * (n + 1)
    bad = [False] * (n + 1)
    order = [1]
    parent[1] = -1
    for u in order:
        for v, c in adj[u]:
            if v != parent[u]:
                parent[v] = u
                depth_sum[v] = depth_sum[u] + c
                lowest_ancestor[v] = depth_sum[u] if u == 1 else min(lowest_ancestor[u], depth_sum[u])
                bad[v] = bad[u] or depth_sum[v] - lowest_ancestor[v] > a[v - 1]
                order.append(v)
    return sum(bad)


def brute(data):
    n, a, edges = data
    full = (1 << n) - 1
    neighbours = [[] for _ in range(n)]
    for i, (p, c) in enumerate(edges):
        neighbours[i + 1].append((p - 1, c))
        neighbours[p - 1].append((i + 1, c))

    def has_sad(mask):
        if not mask & 1:
            return False
        up = {0: (None, 0)}
        stack = [0]
        while stack:
            u = stack.pop()
            for v, c in neighbours[u]:
                if mask >> v & 1 and v not in up:
                    up[v] = (u, c)
                    stack.append(v)
        for u in up:
            dist, v = 0, u
            while up[v][0] is not None:
                dist += up[v][1]
                v = up[v][0]
                if dist > a[u]:
                    return True
        return False

    def leaves(mask):
        members = [v for v in range(n) if mask >> v & 1]
        if members == [0]:
            return [0]
        return [v for v in members if v != 0 and sum(mask >> w & 1 for w, _ in neighbours[v]) == 1]

    level, seen, removed = {full}, {full}, 0
    while level:
        if any(not has_sad(mask) for mask in level):
            return removed
        nxt = set()
        for mask in level:
            for v in leaves(mask):
                child = mask & ~(1 << v)
                if child not in seen:
                    seen.add(child)
                    nxt.add(child)
        level, removed = nxt, removed + 1
    raise AssertionError('no sad-free state reachable')


def render(n, a, edges):
    lines = [str(n), ' '.join(map(str, a))]
    lines += [f'{p} {c}' for p, c in edges]
    return '\n'.join(lines) + '\n'


def from_parents(n, a, parent, cost):
    return n, list(a), [(parent[v], cost[v]) for v in range(2, n + 1)]


def random_tree(rng, n, a_range, c_range, shape='random'):
    labels = list(range(2, n + 1))
    rng.shuffle(labels)
    order = [1] + labels
    parent, cost = {}, {}
    for idx in range(1, n):
        if shape == 'chain':
            j = idx - 1
        elif shape == 'star':
            j = 0
        elif shape == 'broom':
            j = idx - 1 if idx < n // 2 else rng.randrange(idx)
        else:
            j = rng.randrange(max(0, idx - 3) if shape == 'deep' else 0, idx)
        parent[order[idx]] = order[j]
        cost[order[idx]] = rng.randint(*c_range)
    a = [rng.randint(*a_range) for _ in range(n)]
    return from_parents(n, a, parent, cost)


def _labelled_trees(n):
    for parents in itertools.product(range(1, n + 1), repeat=n - 1):
        try:
            data = parse('682C', render(n, [1] * n, [(p, 0) for p in parents]))
        except ValueError:
            continue
        yield [p for p, _ in data[2]]


def brute_checks():
    total = 0
    rng = random.Random(682002)

    def check(data):
        nonlocal total
        expected = brute(data)
        assert answer('682C', data) == expected, data
        assert prefix_reference(data) == expected, data
        total += 1

    for value in (1, 5, MAX_A):
        check((1, [value], []))
    for a in itertools.product((1, 2, 3), repeat=2):
        for c in range(-4, 5):
            for p_of_2 in (1,):
                check((2, list(a), [(p_of_2, c)]))
    for n in (3, 4):
        trees = list(_labelled_trees(n))
        for parents in trees:
            for a in itertools.product((1, 2), repeat=n):
                for costs in itertools.product((-2, -1, 1, 3), repeat=n - 1):
                    check((n, list(a), list(zip(parents, costs))))
    for parents in _labelled_trees(5):
        for _ in range(12):
            check((5, [rng.randint(1, 4) for _ in range(5)], [(p, rng.randint(-3, 4)) for p in parents]))
    for _ in range(1500):
        n = rng.randint(6, 8)
        shape = rng.choice(('random', 'chain', 'star', 'deep', 'broom'))
        check(random_tree(rng, n, (1, rng.choice((3, 6, 20))), rng.choice(((-3, 4), (-1, 2), (-10, 10))), shape))
    for case in extras('682C'):
        data = parse('682C', case['input'])
        expected = brute(data) if data[0] <= 8 else prefix_reference(data)
        assert case['output'] == f'{expected}\n', case['reason']
        total += 1
    return {'682C': total}


def _chain(n, a, costs):
    return n, list(a), [(i + 1, c) for i, c in enumerate(costs)]


def _reversed_chain(n, a, costs):
    """Path 1 - n - (n-1) - ... - 2, so every p_i except the last equals i+2 (parent has the larger label)."""
    edges = [(i + 3, costs[i]) for i in range(n - 2)] + [(1, costs[n - 2])]
    return n, list(a), edges


_EXTRAS = None


def extras(pid):
    global _EXTRAS
    if pid != '682C':
        raise ValueError('unknown problem ' + pid)
    if _EXTRAS is not None:
        return [dict(case) for case in _EXTRAS]
    rng = random.Random(682001)
    cases, seen = [], set()

    def add(data, reason, category):
        text = render(*data)
        if text in seen:
            return
        parsed = parse(pid, text)
        seen.add(text)
        cases.append({'input': text, 'output': f'{answer(pid, parsed)}\n', 'reason': reason, 'category': category})

    add((1, [1], []), 'n=1 minimum: lone root is never sad, answer 0', 'boundary')
    add((1, [MAX_A], []), 'n=1 with a=10^9', 'boundary')
    add((2, [1, 1], [(1, 1)]), 'dist equals a_u: not sad, answer 0 [kills ge-instead-of-gt]', 'boundary')
    add((2, [1, 1], [(1, 2)]), 'dist exceeds a_u by one: remove the only leaf', 'boundary')
    add((2, [1, MAX_A], [(1, MAX_A)]), 'c=a=10^9 equality at the maximum [kills ge-instead-of-gt]', 'boundary')
    add((2, [1, MAX_A - 1], [(1, MAX_A)]), 'c=10^9 exceeds a=10^9-1 by one', 'boundary')
    add((2, [MAX_A, 1], [(1, -MAX_A)]), 'c=-10^9 minimum edge, nothing removed', 'boundary')
    add((2, [1, 1], [(1, 0)]), 'zero-weight edge', 'boundary')
    add((2, [5, 5], [(1, -1)]), 'single c=-1 edge, nothing removed', 'boundary')
    add((3, [9, 9, 1], [(1, -1), (2, 3)]), 'subtree hanging below a c=-1 edge must be inspected [kills skip-minus-one]', 'boundary')
    add((3, [9, 2, 9], [(3, 1), (1, 5)]), 'p_1=3 larger than i+1: vertex 2 hangs below 3, suffix 6>2 [kills index-order-dp]', 'boundary')
    add((3, [9, 1, 9], [(3, 2), (1, -1)]), 'p_1=3 with a c=-1 edge from the root', 'boundary')
    add((3, [1, 1, 1], [(1, 2), (1, 2)]), 'both leaves of a star removed', 'boundary')
    add((3, [1, 1, 5], [(1, 2), (2, 0)]), 'removed vertex takes its zero-cost child (a=5 itself safe) too [kills count-sad-only]', 'boundary')
    add((3, [1, 1, 9], [(1, 5), (2, -5)]), 'child of a removed vertex is fine itself but still removed [kills count-sad-only]', 'boundary')
    add(_chain(4, [10, 10, 10, 4], [5, -5, 3]), 'running max(d,d+c) overestimates after a negative edge (18888172) [kills positive-accumulation]', 'adversarial')
    add(_chain(4, [10, 10, 10, 4], [-10, 3, 2]), 'root distance 0-10+3+2=-5 hides suffix 5>4 (20764615) [kills root-distance]', 'adversarial')
    add(_chain(3, [10, 10, 1], [-5, 3]), 'negative prefix then positive edge: suffix 3>1 although root distance -2 [kills root-distance]', 'adversarial')
    add(_chain(5, [10, 10, 10, 10, 2], [-100, 50, -100, 3]), 'repeated resets: only the last suffix 3>2 matters [kills root-distance]', 'adversarial')
    add(_chain(4, [10, 10, 10, 2], [3, -1, 1]), 'c=-1 in the middle of a chain [kills skip-minus-one]', 'adversarial')
    add(_chain(4, [10, 1, 10, 10], [5, -1, 0]), 'cut vertex whose descendants sit behind a c=-1 edge [kills skip-minus-one]', 'adversarial')
    add(_chain(4, [10, 10, 10, 10], [4, 4, 3]), 'suffix sum 11>10 at depth 3 only: just the deepest leaf goes', 'adversarial')
    add(_reversed_chain(6, [9, 9, 9, 9, 9, 9], [1, 1, 1, 1, 6]), 'path 1-6-5-4-3-2 with parents of larger label [kills index-order-dp]', 'adversarial')
    add(_reversed_chain(6, [9, 1, 9, 9, 9, 9], [-1, 1, 1, 1, 6]), 'reversed path with a c=-1 edge near the bottom', 'adversarial')
    add((5, [10, 3, 10, 10, 10], [(1, 2), (1, 1), (3, 1), (4, 1)]), 'two branches: only sibling with small a removed', 'adversarial')
    add((6, [1, 1, 1, 1, 1, 1], [(1, 2), (1, 2), (1, 2), (1, 2), (1, 2)]), 'star with every leaf removed', 'adversarial')
    add((6, [100, 100, 1, 100, 100, 100], [(1, 0), (2, 2), (3, 0), (4, 0), (5, 0)]), 'removing vertex 3 takes the whole lower chain [kills count-sad-only]', 'adversarial')
    add((7, [50, 50, 50, 50, 50, 50, 50], [(1, -30), (2, 40), (3, 40), (1, 25), (5, 25), (6, 1)]), 'two arms crossing the threshold at different depths [kills root-distance]', 'adversarial')
    add(_chain(5, [MAX_A] * 5, [MAX_A, MAX_A, MAX_A, MAX_A]), 'chain of +10^9 edges: suffix 2*10^9 at depth 2 (64-bit sums)', 'adversarial')
    add(_chain(5, [MAX_A] * 5, [-MAX_A, -MAX_A, -MAX_A, MAX_A]), 'large negative prefix -3*10^9 then +10^9 equality, nothing removed [kills ge-instead-of-gt]', 'adversarial')
    add(_chain(5, [MAX_A, MAX_A, MAX_A, MAX_A, MAX_A - 1], [-MAX_A, -MAX_A, -MAX_A, MAX_A]), 'large negative prefix hides a final +10^9 > 10^9-1 [kills root-distance]', 'adversarial')
    add((4, [5, 1, 1, 5], [(4, 2), (4, 2), (1, -1)]), 'p_i=4 for vertices 2 and 3 below a c=-1 root edge; both removed [kills skip-minus-one]', 'adversarial')

    for _ in range(40):
        n = rng.randint(2, 8)
        shape = rng.choice(('random', 'chain', 'star', 'deep', 'broom'))
        add(random_tree(rng, n, (1, rng.choice((2, 5, 12))), rng.choice(((-3, 4), (-1, 2), (-6, 9))), shape),
            f'fixed-seed small {shape} tree n={n}, brute-checked', 'adversarial')
    for _ in range(40):
        n = rng.randint(9, 60)
        shape = rng.choice(('random', 'chain', 'deep', 'broom'))
        add(random_tree(rng, n, (1, rng.choice((10, 40, 200))), rng.choice(((-10, 12), (-1, 3), (-50, 60))), shape),
            f'fixed-seed medium {shape} tree n={n}', 'adversarial')
    for n in (1000, 2000):
        for shape in ('random', 'deep', 'chain'):
            add(random_tree(rng, n, (1, 10 ** 6), (-10 ** 5, 2 * 10 ** 5), shape), f'fixed-seed {shape} tree n={n} with mixed signs', 'adversarial')
    add(random_tree(rng, 3000, (MAX_A // 2, MAX_A), (-MAX_A, MAX_A), 'random'), 'n=3000 random tree with extreme weights', 'adversarial')

    big = MAX_N
    add(_chain(big, [MAX_A] * big, [1] * (big - 1)), 'maximum depth chain 1-2-...-n, all safe: recursion depth 10^5, answer 0', 'maxSize')
    add(_chain(big, [MAX_A] * (big - 1) + [1], [-1] * (big - 2) + [2]), 'maximum chain of c=-1 edges, last edge breaks only the deepest leaf [kills skip-minus-one]', 'maxSize')
    add(_reversed_chain(big, [MAX_A] * big, [MAX_A // 50000] * (big - 1)),
        'maximum reversed path (p_i=i+2) with suffix sums growing to 10^9 then exceeding [kills index-order-dp]', 'maxSize')
    add((big, [MAX_A] * big, [(1, MAX_A)] * (big - 1)), 'maximum star, every edge equals a: nothing removed', 'maxSize')
    add((big, [1] + [MAX_A - 1] * (big - 1), [(1, MAX_A)] * (big - 1)), 'maximum star, every leaf removed: answer n-1', 'maxSize')
    add(random_tree(rng, big, (1, MAX_A), (-MAX_A, MAX_A), 'random'), 'maximum random tree with full-range weights', 'maxSize')
    add(random_tree(rng, big, (5 * 10 ** 8, MAX_A), (-3 * 10 ** 8, 4 * 10 ** 8), 'deep'), 'maximum deep random tree with mixed-sign suffix resets', 'maxSize')
    add(random_tree(rng, big, (MAX_A // 2, MAX_A), (-10 ** 8, 10 ** 8), 'broom'), 'maximum broom: 5*10^4 chain then random fan-out', 'maxSize')
    _EXTRAS = cases
    return [dict(case) for case in cases]


def review(pid, tests, samples):
    failures = []
    for name, pair in [*tests, *samples]:
        try:
            data = parse(pid, pair['input'])
            expected = answer(pid, data)
            reference = brute(data) if data[0] <= 8 else prefix_reference(data)
            if reference != expected:
                raise ValueError('oracle and independent reference disagree')
            if pair['output'].split() != [str(expected)] or pair['output'].strip().splitlines() != [str(expected)]:
                raise ValueError(f'output differs from independent oracle (expected {expected})')
        except (ValueError, AssertionError) as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
