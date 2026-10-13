"""Rating-1600 recipe for 333A Secrets (powers-of-three coins)."""
from fractions import Fraction
import itertools
import random
import re


IDS = ('333A',)
LIMIT = 10**17
SEMANTICS = {
    '333A': 'Single line with one integer n, 1<=n<=10^17 (public English statement shows 10<sup>17</sup>; pinned row flattened it to 1017 and official test 100000000000000000 confirms 10^17). '
            'Over all coin multisets of powers of three that cannot pay exactly n, maximize the minimum number of coins reaching at least n. '
            'Unique integer: with 3^k the least power of three not dividing n, the answer is floor(n/3^k)+1. '
            'Exhaustive coin-multiset enumeration (exact-sum infeasibility plus minimum cover) cross-checks small n; ternary-digit and exact-rational ceil(n/3^k) derivations cross-check large n.',
}
NUMBER = re.compile(r'([1-9][0-9]*)(?:\r?\n)?')


def parse(pid, text):
    if pid not in IDS:
        raise ValueError('unknown problem')
    match = NUMBER.fullmatch(text)
    if not match:
        raise ValueError('expected exactly one line holding one positive integer token')
    n = int(match.group(1))
    if not 1 <= n <= LIMIT:
        raise ValueError('n outside 1..10^17')
    return n


def answer(pid, data):
    n = data
    while n % 3 == 0:
        n //= 3
    return n // 3 + 1


def ternary_answer(n):
    digits = []
    while n:
        n, digit = divmod(n, 3)
        digits.append(digit)
    while digits[0] == 0:
        digits.pop(0)
    prefix = 0
    for digit in reversed(digits[1:]):
        prefix = prefix * 3 + digit
    return prefix + 1


def rational_answer(n):
    power = 1
    while n % power == 0:
        power *= 3
    quotient = Fraction(n, power)
    return -((-quotient.numerator) // quotient.denominator)


def coin_brute(n):
    denominations = []
    power = 1
    while power <= n:
        denominations.append(power)
        power *= 3
    denominations.append(power)
    caps = [-(-n // d) if d < n else 1 for d in denominations]
    best = 0
    for counts in itertools.product(*(range(c + 1) for c in caps)):
        sums = 1
        for d, c in zip(denominations, counts):
            for _ in range(c):
                sums |= sums << d
        if sums >> n & 1:
            continue
        if sum(d * c for d, c in zip(denominations, counts)) < n:
            continue
        cover = [0] + [None] * n
        for d, c in zip(denominations, counts):
            for _ in range(c):
                for total in range(n, -1, -1):
                    if cover[total] is not None:
                        target = min(n, total + d)
                        if cover[target] is None or cover[target] > cover[total] + 1:
                            cover[target] = cover[total] + 1
        best = max(best, cover[n])
    return best


def brute(pid, data):
    return coin_brute(data)


def powers():
    result, power = [], 1
    while power <= LIMIT:
        result.append(power)
        power *= 3
    return result


def extras(pid):
    rng = random.Random(16003330)
    cases, seen = [], set()

    def add(n, reason, category='adversarial'):
        if n in seen or not 1 <= n <= LIMIT:
            return
        seen.add(n)
        text = f'{n}\n'
        cases.append({'input': text, 'output': f'{answer(pid, parse(pid, text))}\n',
                      'reason': reason, 'category': category})

    top = powers()
    for n in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 26, 27, 28):
        add(n, 'minimum and smallest ternary transitions', 'boundary')
    for index, p in enumerate(top):
        if index % 4 == 1 or p == top[-1]:
            add(p, 'exact power of three: every coin reaching n alone pays it, answer 1', 'boundary')
        if index in (2, 9, 20, 30, len(top) - 1):
            add(p - 1, 'one below a power of three (all ternary digits 2)', 'boundary')
            add(p + 1, 'one above a power of three', 'boundary')
            add(2 * p, 'twice a power of three', 'boundary')
    add(LIMIT, 'maximum n = 10^17 (not divisible by 3, float division inexact)', 'maxSize')
    add(LIMIT - 1, 'maximum-1 = 10^17-1 divisible by 27 only, answer far from ceil(n/3)', 'maxSize')
    add(LIMIT - 2, 'maximum-2, n%3==1 near 10^17', 'maxSize')
    add(LIMIT - 3, 'maximum-3, 10^17-3 divisible by 3 once', 'maxSize')
    add(top[-1], 'largest power of three <= 10^17 (3^35), answer 1', 'maxSize')
    add(2 * top[-1], 'largest 2*3^35 <= 10^17, answer 1', 'maxSize')
    for p in (3**5, 3**12, 3**20, 3**30):
        add(LIMIT // p * p, 'largest multiple of a high power of three <= 10^17', 'maxSize')
    for k in range(1, 6):
        add(LIMIT - 3 * k + 1, 'near-maximum n where float(n) is inexact (int(n/p)+1 and ceil(n/p) off by one)', 'maxSize')
    for p in (1, 3, 9, 27, 81):
        for r in (1, 2):
            add(3 * p * (LIMIT // (3 * p) - 7) + r * p,
                'large n whose float quotient by the stripped power of three rounds across an integer')
    for _ in range(12):
        j = rng.randint(1, 30)
        m = rng.randrange(LIMIT // 3**j // 3) * 3 + rng.choice((1, 2))
        add(m * 3**j, 'large n with many trailing ternary zeros (ceil(n/3) and digit-sum both wrong)')
    for n in (11, 14, 17, 25, 40, 41, 53, 80, 82, 107, 108, 120, 242, 728, 1000):
        add(n, 'small values where greedy ternary decomposition, ceil(n/3), digit-sum or n%3+1 disagree')
    for p in (3, 9, 27, 81, 243):
        add(p * 4, 'multiple of 3^k with quotient 4: n//(p+1)+1 and ceil(n/3) wrong')
        add(p * 5, 'multiple of 3^k with quotient 5')
    for _ in range(30):
        add(rng.randint(1, 2000), 'fixed-seed random small n')
    for _ in range(30):
        add(rng.randint(1, LIMIT), 'fixed-seed random 64-bit-range n')
    return cases


def brute_checks():
    count = 0
    for n in range(1, 61):
        expected = coin_brute(n)
        assert answer('333A', n) == expected, (n, answer('333A', n), expected)
        count += 1
    rng = random.Random(16003331)
    samples = list(range(1, 3001)) + [rng.randint(1, LIMIT) for _ in range(3000)]
    samples += [p * m for p in powers() for m in (1, 2, 4, 5, 7, 8)]
    for n in samples:
        if n > LIMIT:
            continue
        expected = answer('333A', n)
        assert ternary_answer(n) == expected, (n, ternary_answer(n), expected)
        assert rational_answer(n) == expected, (n, rational_answer(n), expected)
        count += 2
    return {'333A': count}


def review(pid, tests, samples):
    failures = []
    for name, pair in tests + samples:
        try:
            expected = [str(answer(pid, parse(pid, pair['input'])))]
        except ValueError as exc:
            failures.append({'test': name, 'reason': str(exc)})
            continue
        if expected != pair['output'].split():
            failures.append({'test': name, 'reason': 'independent oracle disagreement',
                             'expected': expected, 'actual': pair['output'].split()[:5]})
    return failures
