"""The Elder Trolls IV: Oblivon (73A): most pieces of an x*y*z grid box after at most k planar cuts."""
import itertools
import random
import re


IDS = ('73A',)
SEMANTICS = {
    '73A': 'One line "x y z k", 1<=x,y,z<=10^6, 0<=k<=10^9 (exponents attested from the original English statement). '
           'Cuts are grid planes parallel to a face and pass through every part, so a, b, c cuts along the three axes '
           '(a<=x-1, b<=y-1, c<=z-1, a+b+c<=k) give exactly (a+1)(b+1)(c+1) pieces. Unique answer: one integer, the maximum '
           'of that product, at most 10^18. Oracle: sort sides, give the smallest axis min(s1-1, k//3), the middle '
           'min(s2-1, rest//2), the largest min(s3-1, rest). Checked against exhaustive (a,b,c) enumeration and an unsorted '
           'per-a enumeration with an interval-clipped two-axis optimum.',
}
MAX_SIDE = 10 ** 6
MAX_K = 10 ** 9
_INT = re.compile(r'0|[1-9][0-9]*')


def _int(token, what):
    if not _INT.fullmatch(token):
        raise ValueError(f'{what} not a canonical nonnegative integer')
    return int(token)


def parse(pid, text):
    if pid != '73A':
        raise ValueError('unknown problem')
    lines = text.splitlines()
    if len(lines) != 1:
        raise ValueError('line layout: expected exactly one line')
    parts = lines[0].split()
    if len(parts) != 4:
        raise ValueError('line arity: expected x y z k')
    x, y, z, k = (_int(t, name) for t, name in zip(parts, 'xyzk'))
    if not all(1 <= v <= MAX_SIDE for v in (x, y, z)):
        raise ValueError('side range')
    if not 0 <= k <= MAX_K:
        raise ValueError('k range')
    return x, y, z, k


def answer(pid, data):
    x, y, z, k = data
    s1, s2, s3 = sorted((x, y, z))
    a = min(s1 - 1, k // 3)
    k -= a
    b = min(s2 - 1, k // 2)
    k -= b
    c = min(s3 - 1, k)
    return (a + 1) * (b + 1) * (c + 1)


def brute_exhaustive(data):
    x, y, z, k = data
    best = 0
    for a in range(min(x - 1, k) + 1):
        for b in range(min(y - 1, k - a) + 1):
            for c in range(min(z - 1, k - a - b) + 1):
                best = max(best, (a + 1) * (b + 1) * (c + 1))
    return best


def _two_axis(p, q, r):
    lo, hi = max(0, r - (q - 1)), min(p - 1, r)
    if lo > hi:
        b_values = [min(p - 1, r)]
    else:
        b_values = {min(max(v, lo), hi) for v in (r // 2, (r + 1) // 2)}
    best = 0
    for b in b_values:
        c = min(q - 1, r - b)
        best = max(best, (b + 1) * (c + 1))
    return best


def brute_scan(data):
    x, y, z, k = data
    return max((a + 1) * _two_axis(y, z, k - a) for a in range(min(x - 1, k) + 1))


def _render(x, y, z, k):
    return f'{x} {y} {z} {k}\n'


def extras(pid):
    rng = random.Random(73001)
    cases = []
    seen = set()
    M = MAX_SIDE

    def add(x, y, z, k, reason, category='adversarial'):
        text = _render(x, y, z, k)
        if text in seen:
            return
        seen.add(text)
        cases.append({'input': text, 'output': f'{answer(pid, parse(pid, text))}\n', 'reason': reason, 'category': category})

    add(1, 1, 1, 0, 'all minima: one piece', 'boundary')
    add(1, 1, 1, MAX_K, '1x1x1 with k=10^9: cuts are useless, answer 1 (2^k / x^k / uncapped loops fail)', 'boundary')
    add(M, M, M, 0, 'maximum sides, k=0: answer 1', 'boundary')
    add(M, M, M, 1, 'maximum sides, k=1: answer 2', 'boundary')
    add(M, M, M, MAX_K, 'all maxima: answer 10^18 exactly (64-bit)', 'maxSize')
    add(M, M, M, 3 * M - 3, 'k exactly x+y+z-3 at maximum sides: full grid 10^18', 'maxSize')
    add(M, M, M, 3 * M - 4, 'one cut short of the full maximum grid', 'maxSize')
    add(M, M, M, 3 * M - 5, 'two cuts short of the full maximum grid', 'maxSize')
    add(M, M, M, 3 * M - 2, 'one cut more than needed at maximum sides', 'maxSize')
    add(M, M, M, 1500000, 'k=1.5*10^6 balanced over maximum sides: 500001^3, far above 32-bit', 'maxSize')
    add(M, M, M, 2 * M, 'k=2*10^6 at maximum sides', 'maxSize')
    add(1, 1, M, MAX_K, 'single long axis capped at 10^6 pieces', 'maxSize')
    add(1, M, M, MAX_K, 'two long axes: 10^12 pieces', 'maxSize')
    add(1, M, M, 1999997, 'two long axes, one cut short: 10^12 - 10^6', 'maxSize')
    add(M, 1, M, 1000001, 'two long axes with a middle unit side and odd k', 'maxSize')
    add(2, M, M, MAX_K, 'thin slab at maximum: 2*10^12', 'maxSize')
    add(M - 1, M, M - 3, MAX_K, 'near-maximum distinct sides, k unlimited', 'maxSize')
    add(M, M - 1, 2, 999998, 'large k exhausts smallest side early (cap at 1 cut)', 'maxSize')
    for k in range(0, 13):
        add(2, 2, 2, k, f'2x2x2 with k={k}: grows 1,2,4,8 then saturates at 8', 'boundary')
    for k in range(0, 10):
        add(1, 1, 5, k, f'two unit sides, one axis of 5, k={k}: answer min(k,4)+1 (uncapped k+1 is wrong once k>4)', 'boundary')
    for k in range(0, 8):
        add(1, 3, 4, k, f'one unit side, k={k}: cuts must split between the other two axes only', 'boundary')
    for k in (0, 1, 2, 3, 4, 5, 6):
        add(1, 2, 3, k, f'1x2x3 with k={k}: the unit side takes no cuts', 'boundary')
    add(1, 2, 3, 3, 'official-style trap: largest-first k//(i+1) split gives 4 instead of 6')
    for k in (4, 5, 6, 7, 8, 9, 10):
        add(2, 5, 5, k, f'smallest side caps at 1 cut, k={k}: leftover must be rebalanced to the two larger axes')
    for k in (5, 10, 15, 20, 25, 26, 27, 28):
        add(3, 10, 20, k, f'3x10x20, k={k}: cap on smallest then middle side, largest absorbs the rest')
    for k in (3, 4, 5, 6, 7, 8):
        add(20, 4, 5, k, f'unsorted sides 20 4 5, k={k}: greedy must sort before capping')
    for k in (10, 11, 12, 13, 25):
        add(20, 4, 5, k, f'unsorted sides 20 4 5, k={k}: middle cap binds before the largest')
    for k in (2, 11, 20, 21, 22):
        add(11, 1, 11, k, f'middle unit side between two equal sides, k={k}')
    add(1000, 1, 1, 1, 'single axis k=1', 'boundary')
    add(1000, 1, 1, 998, 'single axis one short of cap', 'boundary')
    add(1000, 1, 1, 999, 'single axis exactly at cap', 'boundary')
    add(1, 1000, 1, 1000, 'single axis (middle position) over cap', 'boundary')
    for k in (49, 50, 51, 52):
        add(91839, 2, 3, k, f'two tiny sides and a big one, k={k}: tiny caps bind, rest on the big axis')
    for k in (127, 128, 129, 130):
        add(999900, 999990, 4, k, f'smallest side 4 (cap 3 cuts), k={k}: remaining split between two huge axes')
    add(1024, 100000, 4, 13, 'cap 3 on the smallest side with odd remainder')
    for k in (3 * 46340, 3 * 46341, 3 * 65535, 3 * 65536, 3 * 1625):
        add(M, M, M, k, f'balanced k={k}: product exceeds 32-bit range (int overflow in C++)')
    add(65536, 65536, 2, MAX_K, 'product 2^33 exceeds 32-bit with uncapped k')
    add(46341, 46341, 1, MAX_K, 'product just above 2^31')
    add(46340, 46340, 1, MAX_K, 'product just below 2^31')
    add(500000, 1000000, 750000, 100000, 'balanced split far below every cap')
    add(33334, 66667, 1000000, 100000, 'smallest side 33334 caps exactly at k/3 boundary')
    add(33333, 66667, 1000000, 100000, 'smallest side cap 33332 just below k//3=33333')
    add(33335, 66667, 1000000, 100000, 'smallest side cap 33334 just above k//3=33333')
    for r in range(3):
        add(M, M, M, 999999 + r, f'k mod 3 = {(999999 + r) % 3}: remainder cuts go to the larger axes')
    for k in (0, 1, 2, 3):
        add(2, 3, 4, 6 + k, f'k={6 + k} at or above x+y+z-3=6: full grid 24')
    for d in (1, 2, 3, 4, 5):
        add(10, 20, 30, 57 - d, f'k = x+y+z-3-{d}: removing cuts from the full grid, not proportionally')
    for d in (1, 2, 3, 4):
        add(5, 5, 5, 12 - d, f'equal sides 5, k = 12-{d}: removal from the full grid must stay balanced')
    add(2, 1000, 1000, 3, 'smallest side capped at 1 when k//3=1; rest 2 split 1/1')
    add(2, 1000, 1000, 4, 'smallest capped at 1; rest 3 split 1/2')
    add(3, 3, 1000, 100, 'two small caps, large axis absorbs almost all of k')
    while len(cases) < 145:
        bound = rng.choice((4, 12, 60, 1000, M))
        x, y, z = (rng.randint(1, bound) for _ in range(3))
        k = rng.choice((rng.randint(0, x + y + z), rng.randint(0, 3 * bound), rng.randint(0, MAX_K)))
        add(x, y, z, k, 'fixed-seed random case', 'adversarial')
    return cases


def brute_checks():
    count = 0

    def check(data, exhaustive=True):
        nonlocal count
        expected = answer('73A', data)
        if exhaustive:
            assert brute_exhaustive(data) == expected, (data, expected)
            count += 1
        assert brute_scan(data) == expected, (data, expected)
        count += 1

    for x, y, z in itertools.product(range(1, 9), repeat=3):
        for k in range(0, x + y + z + 1):
            check((x, y, z, k))
    rng = random.Random(73002)
    for _ in range(4000):
        x, y, z = (rng.randint(1, rng.choice((10, 25))) for _ in range(3))
        check((x, y, z, rng.randint(0, x + y + z)))
    for _ in range(600):
        x = rng.randint(1, 300)
        y, z = rng.randint(1, MAX_SIDE), rng.randint(1, MAX_SIDE)
        check((x, y, z, rng.randint(0, MAX_K if rng.random() < 0.3 else x + y + z)), exhaustive=False)
    return {'73A': count}


def review(pid, tests, samples):
    failures = []
    for name, pair in [*tests, *samples]:
        try:
            expected = str(answer(pid, parse(pid, pair['input'])))
            if pair['output'].split() != [expected]:
                failures.append({'test': name, 'reason': 'independent oracle disagreement', 'expected': [expected], 'actual': pair['output'].split()[:15]})
        except ValueError as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
