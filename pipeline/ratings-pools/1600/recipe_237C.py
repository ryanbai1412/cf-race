"""Primes on Interval (237C): minimum window length that always holds k primes."""
from bisect import bisect_left
from itertools import accumulate
from math import isqrt
from operator import sub
import random
import re

IDS = ('237C',)
LIMIT = 10**6
SEMANTICS = {
    '237C': 'One line a b k, 1<=a,b,k<=10^6 and a<=b (10^6 confirmed from codeforces.me statement TeX). '
            'Unique integer: minimum l in 1..b-a+1 such that every window x..x+l-1 with a<=x<=b-l+1 holds at least k primes, else -1. '
            'Oracle takes the maximum over window starts a and p+1 (p prime) of min(k-th prime from x minus x plus 1, b-x+2); '
            'literal statement brute with trial division and a linear-sieve prefix-count binary search independently check it.',
}

_TOKEN = re.compile(r'[1-9][0-9]*')
_PRIMES = None
_REFERENCE_FLAGS = None


def _primes():
    global _PRIMES
    if _PRIMES is None:
        sieve = bytearray([1]) * (LIMIT + 1)
        sieve[0] = sieve[1] = 0
        for i in range(2, isqrt(LIMIT) + 1):
            if sieve[i]:
                sieve[i * i::i] = bytes(len(range(i * i, LIMIT + 1, i)))
        _PRIMES = [i for i, flag in enumerate(sieve) if flag]
    return _PRIMES


def parse(pid, text):
    if pid != '237C':
        raise ValueError('unknown problem ' + pid)
    lines = text.strip().splitlines()
    if len(lines) != 1:
        raise ValueError('237C line layout')
    tokens = lines[0].split()
    if len(tokens) != 3 or not all(_TOKEN.fullmatch(t) for t in tokens):
        raise ValueError('237C arity/integer format')
    a, b, k = map(int, tokens)
    if not (1 <= a <= b <= LIMIT and 1 <= k <= LIMIT):
        raise ValueError('237C constraints')
    return a, b, k


def answer(pid, data):
    a, b, k = data
    primes = _primes()
    lo, hi = bisect_left(primes, a), bisect_left(primes, b + 1)
    if hi - lo < k:
        return -1
    best = 0
    for first in range(lo, hi + 1):
        x = a if first == lo else primes[first - 1] + 1
        if x > b:
            break
        last = first + k - 1
        best = max(best, primes[last] - x + 1 if last < hi else b - x + 2)
    assert 1 <= best <= b - a + 1
    return best


def _is_prime_trial(n):
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def brute(pid, data):
    a, b, k = data
    flags = {x: _is_prime_trial(x) for x in range(a, b + 1)}
    for length in range(1, b - a + 2):
        if all(sum(flags[y] for y in range(x, x + length)) >= k for x in range(a, b - length + 2)):
            return length
    return -1


def _reference_flags():
    global _REFERENCE_FLAGS
    if _REFERENCE_FLAGS is None:
        smallest = [0] * (LIMIT + 1)
        primes = []
        for i in range(2, LIMIT + 1):
            if not smallest[i]:
                smallest[i] = i
                primes.append(i)
            for p in primes:
                if p > smallest[i] or i * p > LIMIT:
                    break
                smallest[i * p] = p
        _REFERENCE_FLAGS = bytes(int(i >= 2 and smallest[i] == i) for i in range(LIMIT + 1))
    return _REFERENCE_FLAGS


def _prefix(a, b):
    return [0] + list(accumulate(_reference_flags()[a:b + 1]))


def _windows_ok(prefix, length, k):
    size = len(prefix) - 1
    return min(map(sub, prefix[length:], prefix[:size + 1 - length])) >= k


def certify(data, value):
    """Check value against the statement with linear-sieve prefix counts, without the oracle's formula."""
    a, b, k = data
    prefix = _prefix(a, b)
    if value == -1:
        return not _windows_ok(prefix, b - a + 1, k)
    return 1 <= value <= b - a + 1 and _windows_ok(prefix, value, k) and (value == 1 or not _windows_ok(prefix, value - 1, k))


def bisect_reference(data):
    a, b, k = data
    prefix = _prefix(a, b)
    size = b - a + 1
    if not _windows_ok(prefix, size, k):
        return -1
    lo, hi = 0, size
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if _windows_ok(prefix, mid, k):
            hi = mid
        else:
            lo = mid
    return hi


def extras(pid):
    rng = random.Random(16000237)
    cases = []
    seen = set()

    def add(a, b, k, reason, category='adversarial'):
        text = f'{a} {b} {k}\n'
        if text in seen:
            return
        seen.add(text)
        cases.append({'input': text, 'output': f'{answer(pid, parse(pid, text))}\n', 'reason': reason, 'category': category})

    for a, b, k in ((1, 1, 1), (1, 1, 2), (2, 2, 1), (2, 2, 2), (2, 4, 1), (1, 2, 2), (2, 3, 1), (2, 3, 2),
                    (2, 3, 3), (4, 4, 1), (3, 3, 1), (LIMIT, LIMIT, 1), (LIMIT, LIMIT, LIMIT), (999983, 999983, 1),
                    (999983, LIMIT, 1), (999984, LIMIT, 1), (999979, 999983, 2), (1, 10, 4), (1, 10, 5), (2, 7, 4),
                    (2, 11, 5), (1, 7, 4), (4, 6, 1), (24, 28, 1), (1, LIMIT - 1, LIMIT)):
        add(a, b, k, 'minimum/singleton/global endpoint/exact total-prime count transitions', 'boundary')
    for k in (1, 2, 3, 5, 10, 100, 1000, 9592, 39249, 50000, 70000, 78496, 78500, 100000):
        add(1, LIMIT, k, 'maximum interval 1..10^6 (includes 1 and 2) across k', 'maxSize')
    for a, b, k in ((2, LIMIT, 1), (2, LIMIT, 78498), (3, LIMIT, 78497), (2, LIMIT, 78497), (500000, LIMIT, 1),
                    (500000, LIMIT, 1000), (1, 999983, 78498), (1, 999982, 78498), (1, 999982, 78497),
                    (999000, LIMIT, 1), (999000, LIMIT, 17), (1, 492226, 1), (1, 492227, 1), (492113, 492227, 1),
                    (492114, 492226, 1), (492113, LIMIT, 1)):
        add(a, b, k, 'near-maximum interval / largest prime gap below 10^6 / top primes 999979 and 999983', 'maxSize')
    for a, b, k in ((1, 100, 1), (2, 1000, 3), (1, 30, 2), (100, 200, 5), (1, 1000, 10), (50, 5000, 7), (4, 8, 1)):
        add(a, b, k, 'answer strictly below b-a+1: rejects printing the full length whenever enough primes exist')
    for a, b, k in ((1, 9, 4), (1, 6, 3), (1, 7, 3), (1, 8, 4), (1, 12, 5), (1, 20, 8)):
        add(a, b, k, 'interval starting at 1: rejects counting 1 as prime')
    for a, b, k in ((2, 13, 6), (3, 7, 3), (5, 11, 3), (11, 13, 2), (89, 97, 2), (999961, 999983, 3)):
        add(a, b, k, 'primes at both ends with total exactly k: answer equals b-a+1, not -1')
    for a, b, k in ((2, 22, 2), (8, 28, 2), (90, 113, 1), (14, 23, 1), (1328, 1361, 1), (24, 100, 3)):
        add(a, b, k, 'prime-free tail before b: suffix windows set the answer via b-x+2 bound')
    for a, b, k in ((97, 97, 1), (13, 13, 1), (7919, 7919, 1), (999983, 999983, 2), (2, 2, 1000)):
        add(a, b, k, 'b itself prime / sieve inclusive of b')
    for a, b, k in ((14, 16, 1), (24, 28, 1), (90, 96, 1), (114, 126, 1), (1, 1000, 1000), (10, 20, 10)):
        add(a, b, k, 'no l works: k exceeds primes in range or composite-only range')
    for a, b, k in ((3, 1000, 1), (2, 1000, 1), (1, 1000, 1), (6, 14, 1), (10, 100, 4)):
        add(a, b, k, 'window starts on and just after primes: two-pointer/sliding update order')
    while len(cases) < 145:
        a = rng.randint(1, 200)
        b = rng.randint(a, min(LIMIT, a + rng.randint(0, 60)))
        add(a, b, rng.randint(1, max(1, (b - a + 1) // 3 + 2)), 'fixed-seed small interval checked by literal brute')
    while len(cases) < 165:
        a = rng.randint(1, LIMIT)
        b = min(LIMIT, a + rng.randint(0, 3000))
        add(a, b, rng.randint(1, max(1, (b - a + 1) // 12)), 'fixed-seed interval anywhere up to 10^6')
    return cases


def brute_checks():
    count = 0
    rng = random.Random(16000238)

    def check(data, expected):
        nonlocal count
        got = answer('237C', data)
        assert got == expected, (data, got, expected)
        count += 1

    for n in (1, 2, 3, 97, 1009, 7919, 492113, 492227, 999983, LIMIT):
        assert (n in set(_primes())) == _is_prime_trial(n) == bool(_reference_flags()[n]), n
        count += 1
    assert len(_primes()) == sum(_reference_flags()) == 78498
    count += 1
    for b in range(1, 41):
        for a in range(1, b + 1):
            for k in range(1, 15):
                check((a, b, k), brute('237C', (a, b, k)))
    for _ in range(300):
        a = rng.randint(1, LIMIT)
        b = min(LIMIT, a + rng.randint(0, 120))
        data = (a, b, rng.randint(1, 8))
        check(data, brute('237C', data))
    for _ in range(40):
        a = rng.randint(1, LIMIT)
        b = min(LIMIT, a + rng.randint(0, 20000))
        data = (a, b, rng.randint(1, 60))
        check(data, bisect_reference(data))
    for data in ((1, LIMIT, 1), (1, LIMIT, 78498), (1, LIMIT, 78499), (2, LIMIT, 50000)):
        check(data, bisect_reference(data))
    return {'237C': count}


def review(pid, tests, samples):
    failures = []
    for name, pair in list(tests) + list(samples):
        try:
            expected = [str(answer(pid, parse(pid, pair['input'])))]
        except ValueError as exc:
            failures.append({'test': name, 'reason': str(exc)})
            continue
        actual = pair['output'].split()
        if actual != expected:
            failures.append({'test': name, 'reason': 'independent oracle disagreement', 'expected': expected, 'actual': actual[:15]})
    return failures
