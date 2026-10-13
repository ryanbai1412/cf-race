"""Destroying Array (722C): maximum alive-segment sum after each destruction."""
import itertools
import random
import re


IDS = ('722C',)
SEMANTICS = {
    '722C': 'Three lines: n (1<=n<=10^5); n integers 0<=a_i<=10^9; a permutation of 1..n giving the destruction order. '
            'Print n lines, the i-th being the maximum sum of a contiguous segment with no destroyed element after the first i '
            'destructions (empty segment = 0, so the last line is 0). Values are non-negative, so only maximal alive runs matter; '
            'the unique integer sequence fits in 64 bits (<=10^14). Oracle: reverse insertion with union-find run sums; '
            'checked against a literal run scan, an all-segments enumeration, and a forward max-subarray segment tree.',
}
MAX_N = 10 ** 5
MAX_A = 10 ** 9
_INT = re.compile(r'0|[1-9][0-9]*')


def _int(token, what):
    if not _INT.fullmatch(token):
        raise ValueError(f'{what} not a canonical nonnegative integer')
    return int(token)


def parse(pid, text):
    if pid != '722C':
        raise ValueError('unknown problem')
    lines = text.splitlines()
    if len(lines) != 3:
        raise ValueError('line layout: expected exactly three lines')
    head = lines[0].split()
    if len(head) != 1:
        raise ValueError('first line arity')
    n = _int(head[0], 'n')
    if not 1 <= n <= MAX_N:
        raise ValueError('n range')
    values = [_int(t, 'a_i') for t in lines[1].split()]
    order = [_int(t, 'order') for t in lines[2].split()]
    if len(values) != n or len(order) != n:
        raise ValueError('array/permutation arity')
    if any(v > MAX_A for v in values):
        raise ValueError('a_i range')
    if sorted(order) != list(range(1, n + 1)):
        raise ValueError('destruction order is not a permutation of 1..n')
    return values, order


def answer(pid, data):
    values, order = data
    n = len(values)
    parent = list(range(n))
    total = [0] * n
    alive = [False] * n

    def find(u):
        root = u
        while parent[root] != root:
            root = parent[root]
        while parent[u] != root:
            parent[u], u = root, parent[u]
        return root

    best = 0
    result = [0] * n
    for step in range(n - 1, 0, -1):
        i = order[step] - 1
        alive[i] = True
        total[i] = values[i]
        for j in (i - 1, i + 1):
            if 0 <= j < n and alive[j]:
                r, s = find(i), find(j)
                parent[s] = r
                total[r] += total[s]
        best = max(best, total[find(i)])
        result[step - 1] = best
    return result


def brute_scan(data):
    values, order = data
    dead = [False] * len(values)
    result = []
    for position in order:
        dead[position - 1] = True
        best = run = 0
        for v, d in zip(values, dead):
            run = 0 if d else run + v
            best = max(best, run)
        result.append(best)
    return result


def brute_segments(data):
    values, order = data
    n = len(values)
    dead = set()
    result = []
    for position in order:
        dead.add(position - 1)
        best = 0
        for left in range(n):
            for right in range(left, n):
                if not dead.intersection(range(left, right + 1)):
                    best = max(best, sum(values[left:right + 1]))
        result.append(best)
    return result


def forward_tree(data):
    values, order = data
    size = 1
    while size < len(values):
        size *= 2
    empty = (0, 0, 0, 0)
    tree = [empty] * (2 * size)
    for i, v in enumerate(values):
        tree[size + i] = (v, v, v, v)

    def merge(left, right):
        full = None if left[0] is None or right[0] is None else left[0] + right[0]
        prefix = left[1] if left[0] is None else left[0] + right[1]
        suffix = right[2] if right[0] is None else left[2] + right[0]
        return full, prefix, suffix, max(left[3], right[3], left[2] + right[1])

    for node in range(size - 1, 0, -1):
        tree[node] = merge(tree[2 * node], tree[2 * node + 1])
    result = []
    for position in order:
        node = size + position - 1
        tree[node] = (None, 0, 0, 0)
        node //= 2
        while node:
            tree[node] = merge(tree[2 * node], tree[2 * node + 1])
            node //= 2
        result.append(tree[1][3])
    return result


def render(values, order):
    return f'{len(values)}\n' + ' '.join(map(str, values)) + '\n' + ' '.join(map(str, order)) + '\n'


def extras(pid):
    rng = random.Random(722003)
    cases = []
    seen = set()

    def add(values, order, reason, category='adversarial'):
        text = render(values, order)
        if text in seen:
            return
        seen.add(text)
        output = ''.join(f'{x}\n' for x in answer(pid, parse(pid, text)))
        cases.append({'input': text, 'output': output, 'reason': reason, 'category': category})

    add([0], [1], 'minimum n=1 with a=0: single line 0', 'boundary')
    add([MAX_A], [1], 'minimum n=1 with a=10^9: first destruction already leaves nothing', 'boundary')
    add([0, 0], [1, 2], 'n=2 all zeros', 'boundary')
    add([MAX_A, MAX_A], [1, 2], 'n=2 both 10^9, left destroyed first', 'boundary')
    add([MAX_A, MAX_A], [2, 1], 'n=2 both 10^9, right destroyed first: surviving last element', 'boundary')
    add([1, 2], [1, 2], 'surviving suffix run reaches the array end; scans that only close runs at destroyed cells miss it', 'boundary')
    add([2, 1], [2, 1], 'surviving prefix run at the array start', 'boundary')
    add([MAX_A] * 3, [2, 1, 3], 'middle destroyed first: two separate 10^9 halves must not be joined (10^9, 10^9, 0)', 'boundary')
    add([MAX_A] * 4, [1, 4, 2, 3], 'first answer 3*10^9 exceeds signed 32-bit', 'boundary')
    add([MAX_A] * 5, [5, 4, 3, 2, 1], 'answers 4*10^9..10^9 exceed unsigned 32-bit', 'boundary')
    add([0] * 6 + [MAX_A], [1, 2, 3, 4, 5, 6, 7], 'only the last element is positive; zeros destroyed first', 'boundary')
    add([0] * 10, list(range(10, 0, -1)), 'all zeros: every answer 0', 'boundary')
    add([1] * 10, list(range(1, 11)), 'destroy from the left: answers 9..0', 'boundary')
    add([1] * 10, list(range(10, 0, -1)), 'destroy from the right: answers 9..0', 'boundary')
    add([1, 5, 0, 5], [1, 2, 3, 4], 'zero inside the surviving run 5 0 5 must not split it (first answer 10)')
    add([0, 1, 0, 1], [1, 2, 3, 4], 'zero values used as destroyed sentinels split 1 0 1 and print 1 instead of 2')
    add([3, 0, 0, 4, 0, 5], [1, 6, 2, 3, 4, 5], 'several zero values inside one alive run')
    add([0, 7, 0, 0, 7, 0], [1, 6, 3, 2, 5, 4], 'zeros at both ends and inside; sentinel solutions undercount')
    add([10, 1], [2, 1], 'value 10 contains digit 0: string split on "0" breaks it into digits')
    add([100, 205, 1], [3, 1, 2], 'digit-concatenation solutions sum digits 1,2,5 instead of values')
    add([1000000000, 999999999], [2, 1], 'multi-digit values with zeros; digit-sum tricks fail')
    add([1000, 1000, 1000], [2, 1, 3], 'a negative sentinel of magnitude 512 is bridged: Kadane gives 1488 instead of 1000')
    add([600, 600, 600, 600], [2, 4, 3, 1], 'bridging a small negative sentinel joins runs 600 and 600')
    add([MAX_A, 1, MAX_A], [2, 1, 3], 'destroyed middle between two 10^9 runs: sentinel -inf required')
    add([1, 1, 1, 1], [1, 2, 4, 3], 'union-find adding the neighbour value instead of its root total: reverse insert 3,4 then 2 gives 2, not 3')
    add([1, 1, 1, 1, 1], [3, 1, 2, 4, 5], 'two equal run sums 2 and 2; erasing a multiset value removes both and prints 1')
    add([4, 4, 4, 4, 4, 4, 4], [4, 2, 6, 1, 3, 5, 7], 'many equal run sums; multiset erase-by-value bug')
    add([5, 1, 1, 9, 1, 1, 5], [4, 2, 6, 1, 3, 5, 7], 'answer comes from an older run, not one of the two halves just split')
    add([1, 1, 50, 1, 1], [1, 5, 2, 4, 3], 'max stays in the untouched middle run while edges are trimmed')
    add([9, 1, 1, 1, 1, 9], [3, 4, 2, 5, 1, 6], 'largest run is not adjacent to the most recent destruction')
    add([3, 1, 4, 1, 5, 9, 2, 6], [8, 7, 6, 5, 4, 3, 2, 1], 'destroy right to left: prefix sums only')
    add([3, 1, 4, 1, 5, 9, 2, 6], [1, 2, 3, 4, 5, 6, 7, 8], 'destroy left to right: suffix sums only')
    add([1, 2, 3, 4, 5, 6, 7, 8, 9], [5, 4, 6, 3, 7, 2, 8, 1, 9], 'middle-out destruction order')
    add([1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 9, 2, 8, 3, 7, 4, 6, 5], 'outside-in destruction order')
    add([2] * 12, [2, 4, 6, 8, 10, 12, 1, 3, 5, 7, 9, 11], 'even positions first: runs of length one remain')
    for gap in range(2, 8):
        n = gap * 4
        values = [rng.randint(0, 9) for _ in range(n)]
        order = list(range(gap, n + 1, gap)) + [i for i in range(1, n + 1) if i % gap]
        add(values, order, f'periodic cuts every {gap} cells, then the rest', 'adversarial')
    n = 1000
    add([MAX_A] * n, list(range(1, n + 1)), 'n=1000, all 10^9, left to right: answers up to 9.99*10^11', 'boundary')
    order = list(range(1, n + 1))
    rng.shuffle(order)
    add([rng.randint(0, MAX_A) for _ in range(n)], order, 'n=1000 random values and random order')
    add([rng.choice((0, MAX_A)) for _ in range(n)], order, 'n=1000 values only 0 or 10^9: zero-sentinel bugs')

    for n in (MAX_N,):
        order = list(range(1, n + 1))
        rng.shuffle(order)
        add([MAX_A] * n, order, 'maximum n=10^5, all a=10^9, random order: first answer near 10^14 needs 64-bit', 'maxSize')
        add([rng.randint(0, MAX_A) for _ in range(n)], order[::-1], 'maximum n=10^5 random values and random order', 'maxSize')
        add([MAX_A] * n, list(range(1, n + 1)), 'maximum n=10^5 destroyed left to right: deep union-find chain on reverse insertion; O(n^2) rescans time out', 'maxSize')
        middle = sorted(range(1, n + 1), key=lambda i: (abs(2 * i - n - 1), i))
        add([rng.randint(0, 1) * MAX_A for _ in range(n)], middle, 'maximum n=10^5 values 0/10^9, middle-out order: zero-sentinel and recursion-depth traps', 'maxSize')
        add([0] * n, list(range(n, 0, -1)), 'maximum n=10^5 all zeros, destroyed right to left', 'maxSize')

    while len(cases) < 150:
        n = rng.randint(1, 10)
        bound = rng.choice((0, 1, 3, 9, 1000, MAX_A))
        values = [rng.randint(0, bound) for _ in range(n)]
        order = list(range(1, n + 1))
        rng.shuffle(order)
        add(values, order, f'fixed-seed random small case (n={n}, values<={bound})', 'adversarial')
    return cases


def brute_checks():
    count = 0

    def check(values, order, segments=True):
        nonlocal count
        data = (list(values), list(order))
        expected = answer('722C', data)
        assert brute_scan(data) == expected, data
        assert forward_tree(data) == expected, data
        count += 2
        if segments:
            assert brute_segments(data) == expected, data
            count += 1

    for n in range(1, 6):
        for values in itertools.product((0, 1, 2), repeat=n):
            for order in itertools.permutations(range(1, n + 1)):
                check(values, order, n <= 4)
    rng = random.Random(722002)
    for _ in range(2000):
        n = rng.randint(1, 12)
        bound = rng.choice((1, 5, 100, MAX_A))
        order = list(range(1, n + 1))
        rng.shuffle(order)
        check([rng.randint(0, bound) for _ in range(n)], order, n <= 8)
    for _ in range(20):
        n = rng.randint(50, 200)
        order = list(range(1, n + 1))
        rng.shuffle(order)
        check([rng.randint(0, MAX_A) for _ in range(n)], order, False)
    return {'722C': count}


def review(pid, tests, samples):
    failures = []
    for name, pair in [*tests, *samples]:
        try:
            expected = [str(x) for x in answer(pid, parse(pid, pair['input']))]
            actual_lines = [line.split() for line in pair['output'].splitlines()]
            actual = [t for line in actual_lines for t in line]
            if actual != expected:
                failures.append({'test': name, 'reason': 'independent oracle disagreement', 'expected': expected[:15], 'actual': actual[:15]})
            elif any(len(line) != 1 for line in actual_lines):
                failures.append({'test': name, 'reason': 'output line layout: expected one integer per line'})
        except ValueError as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
