"""Ivan and Powers of Two (305C): binary carry normalisation of sorted exponents."""
import itertools
import random
import re


IDS = ('305C',)
SEMANTICS = {
    '305C': 'Line 1: n, 1<=n<=10^5; line 2: n integers 0<=a_i<=2*10^9, non-decreasing (exponent markup restored from the '
            'original statement). Output the minimum count of added powers 2^b (b>=0) making the total 2^v-1 for some v>=0. '
            'With S=sum 2^a_i, the optimum is v=bitlength(S) and the answer bitlength(S)-popcount(S), a unique integer '
            '(up to 2000000011). Oracle carries equal exponents upward in one sorted pass; independently checked by '
            'exhaustive minimum-coin DP over every v for small inputs and by big-integer bit-plane popcount for large ones.',
}
MAX_N = 10 ** 5
MAX_A = 2 * 10 ** 9
_COUNT = re.compile(r'[1-9][0-9]*')
_VALUE = re.compile(r'0|[1-9][0-9]*')


def parse(pid, text):
    if pid != '305C':
        raise ValueError('unknown problem')
    lines = text.strip().splitlines()
    if len(lines) != 2:
        raise ValueError('powers line layout')
    head = lines[0].split()
    if len(head) != 1 or not _COUNT.fullmatch(head[0]):
        raise ValueError('powers n arity')
    n = int(head[0])
    if not 1 <= n <= MAX_N:
        raise ValueError('powers n range')
    tokens = lines[1].split()
    if len(tokens) != n or not all(_VALUE.fullmatch(t) for t in tokens):
        raise ValueError('powers array arity')
    a = [int(t) for t in tokens]
    if not all(0 <= x <= MAX_A for x in a):
        raise ValueError('powers exponent range')
    if any(x > y for x, y in zip(a, a[1:])):
        raise ValueError('powers not non-decreasing')
    return a


def answer(pid, a):
    ones = 0
    top = -1
    pos = 0
    carry = 0
    for value, group in itertools.groupby(a):
        while carry and pos < value:
            if carry & 1:
                ones += 1
                top = pos
            carry >>= 1
            pos += 1
        if not carry:
            pos = value
        carry += len(list(group))
    while carry:
        if carry & 1:
            ones += 1
            top = pos
        carry >>= 1
        pos += 1
    return top + 1 - ones


_COIN_LIMIT = 1 << 15
_COINS = []


def _min_coins():
    if not _COINS:
        best = [0] + [None] * (_COIN_LIMIT - 1)
        for total in range(1, _COIN_LIMIT):
            b = 1
            while b <= total:
                prev = best[total - b]
                if best[total] is None or prev + 1 < best[total]:
                    best[total] = prev + 1
                b <<= 1
        _COINS.extend(best)
    return _COINS


def brute_small(a):
    """Literal search: every target 2^v-1 >= S, fewest powers of two summing to the gap (coin DP)."""
    coins = _min_coins()
    total = sum(1 << x for x in a)
    results = []
    v = 0
    while (1 << v) - 1 - total < _COIN_LIMIT:
        gap = (1 << v) - 1 - total
        if gap >= 0:
            results.append(coins[gap])
        v += 1
    if not results:
        raise ValueError('brute bound exceeded')
    return min(results)


def brute_bigint(a):
    """Exact big-integer evaluation; runs of exponents separated by gaps > 40 cannot share carries."""
    groups = []
    for x in a:
        if groups and x - groups[-1][-1] <= 40:
            groups[-1].append(x)
        else:
            groups.append([x])
    ones = 0
    top = -1
    for group in groups:
        low = group[0]
        width = group[-1] - low + 1
        counts = [0] * width
        for x in group:
            counts[x - low] += 1
        total = 0
        for plane in range(max(counts).bit_length()):
            bits = ''.join('1' if c >> plane & 1 else '0' for c in reversed(counts))
            total += int(bits, 2) << plane
        ones += bin(total).count('1')
        top = low + total.bit_length() - 1
    return top + 1 - ones


def _render(a):
    return f'{len(a)}\n{" ".join(map(str, a))}\n'


def extras(pid):
    rng = random.Random(305003)
    cases = []
    seen = set()

    def add(a, reason, category='adversarial'):
        a = sorted(a)
        text = _render(a)
        if text in seen:
            return
        parse(pid, text)
        seen.add(text)
        cases.append({'input': text, 'output': f'{answer(pid, a)}\n', 'reason': reason, 'category': category})

    add([0], 'minimum n=1, a=0: sum 1 = 2^1-1 already, answer 0', 'boundary')
    add([1], 'n=1, a=1: answer 1 (only 2^0 missing)', 'boundary')
    add([MAX_A], 'n=1 at maximum exponent 2*10^9: answer 2000000000, catches big-int 2**a evaluation', 'boundary')
    add([MAX_A - 1], 'n=1 at exponent 2*10^9-1', 'boundary')
    add([0, 0], 'two zeros carry to 2^1: answer 1; a set that never inserts the carried value (39338055) prints 0', 'boundary')
    add([0, 0, 0], 'three zeros give 3 = 2^2-1: answer 0', 'boundary')
    add([MAX_A, MAX_A], 'two maximum exponents carry past 2*10^9 to 2^(2*10^9+1): answer 2000000001', 'boundary')
    add([0, MAX_A], 'extreme span 0 and 2*10^9 with no carry: answer 1999999999', 'boundary')
    add([MAX_A - 1, MAX_A], 'adjacent top exponents 2^(2e9-1)+2^(2e9): answer 1999999999', 'boundary')
    add([MAX_A, MAX_A, MAX_A], 'three maximum exponents: 3*2^(2e9), answer 2000000000', 'boundary')
    add(list(range(0, 20)), 'distinct 0..19 already 2^20-1: answer 0', 'boundary')
    add([0] * 7, 'seven zeros = 2^3-1: answer 0 with carries only', 'boundary')
    add([0] * 8, 'eight zeros collapse to single 2^3: answer 3', 'boundary')
    add([0, 0, 0, 0], 'four zeros: one-pass adjacent merge (51991582) leaves 1,0,1 instead of carrying to 2^2', 'adversarial')
    add([0, 0, 1, 1, 1], 'carry 0,0->1 meets three 1s: one-pass adjacent merge (51991582) leaves 2,1 unmerged', 'adversarial')
    add([0, 0, 1, 2, 3, 4], 'cascading carry chain 0,0,1,..,4 collapses to single 2^5', 'adversarial')
    add([1, 1], 'min(a)=1 but answer 2: refutes printing min(a) (3911483)', 'adversarial')
    add([2, 2], 'pair carry to 2^3: answer 3', 'adversarial')
    add([0, 2], 'gap with no carry: answer 1 (bit 1 missing)', 'adversarial')
    add([5, 5, 5, 5, 5], 'odd count 5 of same exponent: leftover bit plus carry', 'adversarial')
    add([0, 0, 0, 3], 'carry from zeros stops before a gap: 3+8=11, answer 1', 'adversarial')
    add([0, 0, 0, 0, 2], 'carry from zeros lands exactly on next value 2 and merges further', 'adversarial')
    add([0, 0, 0, 0, 3], 'carry from zeros reaches 2 and stops before value 3', 'adversarial')
    add([0, 0, 1, 1, 1, 1, 1], 'carry merges into an odd run of the next value', 'adversarial')
    add([3, 3, 3, 3, 4], 'four 3s carry 2 into position 4, merging with the existing 4 to reach 2^5', 'adversarial')
    add([10] * 4 + [11], 'four 10s carry 2 into position 11, merging with the existing 11 into bits 11 and 12', 'adversarial')
    add([0] * 26 + [2, 2], 'many zeros carry into a pair of 2s, like official test 6 shape', 'adversarial')
    add([MAX_A - 5] * 64, '64 equal exponents near maximum collapse to 2^(2e9+1)', 'adversarial')
    add([MAX_A - 3] * 3 + [MAX_A - 1] * 3 + [MAX_A] * 3, 'carries interleaving with runs near the maximum', 'adversarial')
    add([0, 1] + [MAX_A] * 2, 'low exact prefix and top carry past 2*10^9', 'adversarial')
    add([30, 31, 31], 'carry crossing bit 31: 32-bit shift/overflow in 1<<a based solutions', 'adversarial')
    add([62, 63, 63], 'carry crossing bit 63/64: 64-bit mask based solutions', 'adversarial')
    add([0, 31, 32, 63, 64], 'sparse bits at 32/64-bit word boundaries', 'adversarial')
    for k in range(1, 17):
        add([7] * ((1 << k) - 1), f'2^{k}-1 equal exponents 7: carry leaves k consecutive bits from 7', 'adversarial')
    for k in range(1, 12):
        add([0] * (1 << k), f'2^{k} zeros collapse to single 2^{k}: answer {k}', 'adversarial')

    for _ in range(40):
        n = rng.randint(1, 8)
        add([rng.randint(0, 6) for _ in range(n)], 'fixed-seed random small exponents 0..6 with frequent carries', 'adversarial')
    for _ in range(20):
        n = rng.randint(2, 40)
        hi = rng.choice((10, 50, 1000, MAX_A))
        lo = rng.randint(0, hi)
        add([rng.randint(lo, min(hi, lo + 12)) for _ in range(n)], 'fixed-seed random clustered exponents (carry runs)', 'adversarial')
    for _ in range(10):
        n = rng.randint(2, 30)
        add([rng.randint(0, MAX_A) for _ in range(n)], 'fixed-seed random wide-range exponents up to 2*10^9', 'adversarial')

    add([MAX_A] * MAX_N, 'maximum n=10^5 all a=2*10^9: answer 2000000011 (largest possible), TLE for 2**a sums', 'maxSize')
    add([0] * MAX_N, 'maximum n=10^5 all zeros: carry-only, answer 17-popcount(10^5)', 'maxSize')
    add(list(range(MAX_A - MAX_N + 1, MAX_A + 1)), 'maximum n distinct consecutive top exponents: answer 2*10^9-10^5+1', 'maxSize')
    add([0, 0] + list(range(1, MAX_N - 1)), 'maximum n carry chain 0,0,1,..,99998 cascading through every value to 2^99999', 'maxSize')
    add([rng.randint(0, MAX_A) for _ in range(MAX_N)], 'maximum n random sorted wide exponents with few collisions', 'maxSize')
    add([rng.randint(MAX_A - 40, MAX_A) for _ in range(MAX_N)], 'maximum n random exponents in [2e9-40, 2e9]: deep carries past 2*10^9', 'maxSize')
    add([rng.randint(0, 16) for _ in range(MAX_N)], 'maximum n random tiny exponents 0..16: long carry cascades', 'maxSize')
    return cases


def _non_decreasing(n, hi):
    return itertools.combinations_with_replacement(range(hi + 1), n)


def brute_checks():
    count = 0
    for n, hi in ((1, 13), (2, 11), (3, 9), (4, 7), (5, 6), (6, 5), (7, 4), (8, 3)):
        for a in _non_decreasing(n, hi):
            a = list(a)
            expected = brute_small(a)
            assert answer('305C', a) == expected, a
            assert brute_bigint(a) == expected, a
            count += 1
    rng = random.Random(305777)
    for _ in range(400):
        n = rng.randint(1, 12)
        a = sorted(rng.randint(0, 10) for _ in range(n))
        assert answer('305C', a) == brute_small(a), a
        count += 1
    for _ in range(300):
        n = rng.randint(1, 300)
        hi = rng.choice((5, 60, 3000, MAX_A))
        lo = rng.randint(0, hi)
        span = rng.choice((3, 20, 200, MAX_A))
        a = sorted(rng.randint(lo, min(MAX_A, lo + span)) for _ in range(n))
        assert answer('305C', a) == brute_bigint(a), a
        count += 1
    for case in extras('305C'):
        a = parse('305C', case['input'])
        assert case['output'] == f'{brute_bigint(a)}\n', case['reason']
        count += 1
    return {'305C': count}


def review(pid, tests, samples):
    failures = []
    for name, pair in [*tests, *samples]:
        try:
            expected = str(answer(pid, parse(pid, pair['input'])))
            if pair['output'].split() != [expected]:
                failures.append({'test': name, 'reason': 'independent oracle disagreement', 'expected': [expected],
                                 'actual': pair['output'].split()[:15]})
        except ValueError as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
