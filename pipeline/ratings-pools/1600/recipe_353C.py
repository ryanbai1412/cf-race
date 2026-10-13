"""Find Maximum (353C): best subset sum of a over x <= m with m given little-endian in binary."""
import random
import re


IDS = ('353C',)
SEMANTICS = {
    '353C': 'Three lines: n (1<=n<=10^5); n integers 0<=a_i<=10^4; one string s_0..s_{n-1} of exactly n binary digits, '
            'm = sum 2^i*s_i (s_0 is the least significant bit, trailing zeros of s are leading zeros of m). '
            'Output max over 0<=x<=m of f(x) = sum of a_i over set bits i of x, as one integer (<=10^9). '
            'Since a_i>=0, the optimum is x=m or, for some set bit i of m, clear bit i, keep every higher set bit and '
            'set every lower bit: prefix(a_0..a_{i-1}) + sum of a_j over set bits j>i. Unique integer output; '
            'cross-checked against direct enumeration of every x in [0, m] and an independent tight/free bit DP.',
}
MAX_N = 10 ** 5
MAX_A = 10 ** 4
_INT = re.compile(r'0|[1-9][0-9]*')
_BITS = re.compile(r'[01]+')


def parse(pid, text):
    if pid != '353C':
        raise ValueError('unknown problem')
    lines = text.splitlines()
    if len(lines) != 3:
        raise ValueError('expected exactly three lines')
    head = lines[0].split()
    if len(head) != 1 or not _INT.fullmatch(head[0]):
        raise ValueError('n line arity')
    n = int(head[0])
    if not 1 <= n <= MAX_N:
        raise ValueError('n range')
    tokens = lines[1].split()
    if len(tokens) != n:
        raise ValueError('array arity')
    a = []
    for token in tokens:
        if not _INT.fullmatch(token):
            raise ValueError('array token')
        value = int(token)
        if value > MAX_A:
            raise ValueError('a_i range')
        a.append(value)
    bits = lines[2].split()
    if len(bits) != 1 or not _BITS.fullmatch(bits[0]) or len(bits[0]) != n:
        raise ValueError('binary string of length n')
    return n, a, bits[0]


def answer(pid, data):
    n, a, s = data
    suffix = 0
    prefix = sum(a)
    best = 0
    for i in range(n - 1, -1, -1):
        prefix -= a[i]
        if s[i] == '1':
            best = max(best, prefix + suffix)
            suffix += a[i]
    return max(best, suffix)


def brute_enumerate(a, s):
    m = int(s[::-1], 2)
    best = 0
    for x in range(m + 1):
        total, i, y = 0, 0, x
        while y:
            if y & 1:
                total += a[i]
            y >>= 1
            i += 1
        best = max(best, total)
    return best


def brute_dp(a, s):
    tight, free = 0, None
    for i in range(len(a) - 1, -1, -1):
        options = [] if free is None else [free + a[i]]
        if s[i] == '1':
            options.append(tight)
            tight += a[i]
        free = max(options) if options else None
    return tight if free is None else max(tight, free)


def _text(a, s):
    return f'{len(a)}\n' + ' '.join(map(str, a)) + f'\n{s}\n'


def extras(pid):
    rng = random.Random(353003)
    cases = []
    seen = set()

    def add(a, s, reason, category='adversarial'):
        text = _text(a, s)
        if text in seen:
            return
        seen.add(text)
        cases.append({'input': text, 'output': f'{answer(pid, parse(pid, text))}\n', 'reason': reason, 'category': category})

    for a0 in (0, 1, 10000):
        for s in ('0', '1'):
            add([a0], s, 'minimum n=1 with m in {0,1} and a_0 extremes', 'boundary')
    add([0, 0], '00', 'n=2 all zero a and m=0', 'boundary')
    add([10000, 10000], '01', 'n=2 single top bit: clearing it gives a_0', 'boundary')
    add([10000, 0], '01', 'n=2 top bit worth 0: drop top to take a_0', 'boundary')
    add([0, 10000], '01', 'n=2 keep top bit (x=m) beats prefix', 'boundary')
    add([10000, 10000, 10000], '000', 'm=0 forces answer 0 despite large a', 'boundary')
    add([10, 1, 10], '011', 'best drops the lower set bit 1 (not the top bit): catches m-or-drop-top-only (28011242, 110514694, 111994560)')
    add([5, 1, 5, 1], '0101', 'only one set bit may be cleared: catches per-segment greedy summing max(con,a_i) (99587139)')
    add([7, 2, 9, 3, 1, 4], '010101', 'middle set bit optimum among three ones')
    add([1, 2, 3, 100], '1001', 'answer is x=m using the high bit')
    add([100, 1, 1, 1], '1001', 'answer clears the top bit and fills below')
    add([3, 1, 4, 1, 5, 9], '111111', 'm = 2^n-1: answer is sum(a), no clearing beats it')
    add([3, 1, 4, 1, 5, 9], '100000', 'm=1: answer a_0')
    add([3, 1, 4, 1, 5, 9], '000001', 'single top bit: max(a_{n-1}, prefix of n-1)')
    add([9, 9, 9, 9, 1, 0, 0, 0], '00001000', 'trailing zeros in s are leading zeros of m: highest set bit is index 4, not n-1')
    add([0, 0, 0, 5, 0], '10010', 'drop bit 3 gains only zeros: keep x=m')
    add([1, 1, 1, 1], '0011', 'clear lowest set bit at index 2 vs top bit tie')
    add([2, 0, 0, 0, 0, 0, 7], '0000011', 'two high set bits: drop index 5, keep 6, take prefix')
    add([8, 1, 1, 1, 9], '01001', 'lowest set bit at index 1 is the optimal bit to clear')
    add([1, 1, 1, 1, 9, 0], '000011', 'last set bit at index n-1 must be considered for clearing (82906026 loop bound)')
    add([4, 4, 4, 4], '1111', 'x=m strictly optimal and equals sum')
    add([5, 5], '11', 'm=3 all bits set, tiny')

    for _ in range(60):
        n = rng.randint(1, 10)
        a = [rng.choice((0, rng.randint(0, 20), rng.randint(0, MAX_A))) for _ in range(n)]
        s = ''.join(rng.choice('01') for _ in range(n))
        add(a, s, 'fixed-seed random small case, verified by full enumeration of x in [0, m]')
    while len(cases) < 135:
        n = rng.randint(11, 60)
        a = [rng.randint(0, MAX_A) for _ in range(n)]
        density = rng.choice((0.1, 0.5, 0.9))
        s = ''.join('1' if rng.random() < density else '0' for _ in range(n))
        add(a, s, f'fixed-seed random medium case (bit density {density}), verified by tight/free bit DP')

    for n in (2000, 5000):
        a = [rng.randint(0, MAX_A) for _ in range(n)]
        s = ''.join(rng.choice('01') for _ in range(n))
        add(a, s, f'n={n} random: m has thousands of bits, far beyond 64-bit m')
    a = [MAX_A] * MAX_N
    add(a, '1' * MAX_N, 'maximum n=10^5, a_i=10^4, m=2^n-1: answer 10^9 = sum(a)', 'maxSize')
    add(a, '0' * (MAX_N - 1) + '1', 'maximum n, only top bit set: answer (n-1)*10^4', 'maxSize')
    add(a, '0' * MAX_N, 'maximum n with m=0: answer 0', 'maxSize')
    a = [rng.randint(0, MAX_A) for _ in range(MAX_N)]
    add(a, ''.join(rng.choice('01') for _ in range(MAX_N)), 'maximum n random a and random m', 'maxSize')
    a = [MAX_A] * (MAX_N // 2) + [0] * (MAX_N // 2 - 1) + [MAX_A]
    s = '1' + '0' * (MAX_N // 2 - 1) + '1' + '0' * (MAX_N // 2 - 2) + '1'
    add(a, s, 'maximum n: optimum clears the middle set bit at n/2, neither x=m nor clearing the top bit', 'maxSize')
    return cases


def brute_checks():
    count = 0
    rng = random.Random(353101)
    for n in range(1, 9):
        for mask in range(1 << n):
            s = ''.join('1' if mask >> i & 1 else '0' for i in range(n))
            for _ in range(3):
                a = [rng.choice((0, rng.randint(0, 9), rng.randint(0, MAX_A))) for _ in range(n)]
                expected = brute_enumerate(a, s)
                assert answer('353C', (n, a, s)) == expected, (a, s)
                assert brute_dp(a, s) == expected, (a, s)
                count += 2
    for _ in range(400):
        n = rng.randint(30, 400)
        a = [rng.randint(0, MAX_A) for _ in range(n)]
        s = ''.join(rng.choice('01') for _ in range(n))
        assert answer('353C', (n, a, s)) == brute_dp(a, s), (a, s)
        count += 1
    for case in extras('353C'):
        n, a, s = parse('353C', case['input'])
        reference = brute_enumerate(a, s) if n <= 12 else brute_dp(a, s)
        assert case['output'] == f'{reference}\n', case['reason']
        count += 1
    return {'353C': count}


def review(pid, tests, samples):
    failures = []
    for name, pair in [*tests, *samples]:
        try:
            data = parse(pid, pair['input'])
        except ValueError as exc:
            failures.append({'test': name, 'reason': str(exc)})
            continue
        n, a, s = data
        expected = str(answer(pid, data))
        reference = str(brute_enumerate(a, s) if n <= 12 else brute_dp(a, s))
        if expected != reference:
            failures.append({'test': name, 'reason': 'oracle/brute disagreement', 'expected': [reference], 'actual': [expected]})
        elif pair['output'].split() != [expected]:
            failures.append({'test': name, 'reason': 'independent oracle disagreement', 'expected': [expected], 'actual': pair['output'].split()[:15]})
    return failures
