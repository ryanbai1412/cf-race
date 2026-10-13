"""Primes or Palindromes? (568A): largest n with pi(n) <= (p/q) * rub(n)."""
from bisect import bisect_left, bisect_right
from fractions import Fraction
from functools import lru_cache
import itertools
import random
import re


IDS = ('568A',)
SEMANTICS = {
    '568A': 'One line "p q", positive integers p,q<=10^4 with 1/42<=p/q<=42 (bounds in the Codeforces TeX image, also in the row TeX). '
            'pi(n) counts primes <=n, rub(n) counts positive decimal palindromes <=n. Unique output: the maximum n with q*pi(n)<=p*rub(n), '
            'one integer. n=1 always qualifies (pi=0) and for A<=42 no n>=2*10^6 qualifies (sieve to 10^7 plus a concave Rosser-bound tail), '
            'so the maximum exists and the "Palindromic tree" sentence is unreachable. The maximum is always some prime minus one; '
            'the oracle binary-searches suffix records of pi/rub over those candidates with exact integer cross-multiplication. '
            'Checked against a per-palindrome-segment nth-prime brute and a literal trial-division scan.',
}
LIMIT = 2 * 10 ** 6
MAX_PQ = 10 ** 4
MAX_A = 42
_INT = re.compile(r'[1-9][0-9]*')


def parse(pid, text):
    if pid != '568A':
        raise ValueError('unknown problem')
    lines = text.strip().splitlines()
    if len(lines) != 1:
        raise ValueError('line layout: expected exactly one line "p q"')
    parts = lines[0].split()
    if len(parts) != 2 or not all(_INT.fullmatch(t) for t in parts):
        raise ValueError('expected two canonical positive integers')
    p, q = map(int, parts)
    if not (p <= MAX_PQ and q <= MAX_PQ):
        raise ValueError('p,q range')
    if not (q <= MAX_A * p and p <= MAX_A * q):
        raise ValueError('1/42 <= p/q <= 42 violated')
    return p, q


def _primes(limit):
    sieve = bytearray([1]) * (limit + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytes(len(range(i * i, limit + 1, i)))
    return list(itertools.compress(range(limit + 1), sieve))


def _palindromes(limit):
    out = []
    for length in range(1, len(str(limit)) + 1):
        half = (length + 1) // 2
        for h in range(10 ** (half - 1), 10 ** half):
            s = str(h)
            value = int(s + s[-1 - (length % 2)::-1]) if length > 1 else h
            if value <= limit:
                out.append(value)
    return sorted(out)


@lru_cache(maxsize=None)
def _records():
    primes = _primes(LIMIT + 1)
    pals = _palindromes(LIMIT)
    candidates = []
    j = 0
    for i, prime in enumerate(primes):
        n = prime - 1
        if n > LIMIT:
            break
        while j < len(pals) and pals[j] <= n:
            j += 1
        if n >= 1:
            candidates.append((n, i, j))
    records = []
    for n, pi, rub in reversed(candidates):
        if not records or pi * records[-1][2] < records[-1][1] * rub:
            records.append((n, pi, rub))
    return tuple(records)


def answer(pid, data):
    p, q = data
    records = _records()
    lo, hi = 0, len(records)
    while lo < hi:
        mid = (lo + hi) // 2
        _, pi, rub = records[mid]
        if q * pi <= p * rub:
            hi = mid
        else:
            lo = mid + 1
    if lo == len(records):
        raise ValueError('no qualifying n below LIMIT')
    return records[lo][0]


@lru_cache(maxsize=None)
def _brute_tables():
    flags = [True] * (LIMIT + 2)
    flags[0] = flags[1] = False
    p = 2
    while p * p <= LIMIT + 1:
        if flags[p]:
            for m in range(p * p, LIMIT + 2, p):
                flags[m] = False
        p += 1
    primes = [i for i, f in enumerate(flags) if f]
    pals = []
    for n in range(1, LIMIT + 1):
        x, r = n, 0
        while x:
            r = r * 10 + x % 10
            x //= 10
        if r == n:
            pals.append(n)
    return primes, pals


def brute(pid, data):
    """Segment brute: on [P_k, P_{k+1}-1] rub=k, so the best n there is just before the (floor(pk/q)+1)-th prime."""
    p, q = data
    primes, pals = _brute_tables()
    best = None
    for k in range(1, len(pals) + 1):
        start = pals[k - 1]
        end = pals[k] - 1 if k < len(pals) else LIMIT
        t = p * k // q
        n = min(end, primes[t] - 1) if t < len(primes) else end
        if n >= start:
            best = n
    return best


def _is_prime_trial(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def literal_scan(p, q, upto):
    pi = rub = 0
    last = None
    for n in range(1, upto + 1):
        pi += _is_prime_trial(n)
        rub += str(n) == str(n)[::-1]
        if pi * q <= p * rub:
            last = n
    return last


def _valid(p, q):
    return 1 <= p <= MAX_PQ and 1 <= q <= MAX_PQ and q <= MAX_A * p and p <= MAX_A * q


def _equality_pairs():
    pairs = []
    for n, pi, rub in _records():
        f = Fraction(pi, rub)
        if f.numerator and _valid(f.numerator, f.denominator):
            pairs.append((n, f.numerator, f.denominator))
    return pairs


def extras(pid):
    rng = random.Random(568001)
    cases = []
    seen = set()

    def add(p, q, reason, category='adversarial'):
        text = f'{p} {q}\n'
        if text in seen or not _valid(p, q):
            return
        seen.add(text)
        cases.append({'input': text, 'output': f'{answer(pid, parse(pid, text))}\n', 'reason': reason, 'category': category})

    add(1, 42, 'minimum A=1/42: only n=1 qualifies (pi(1)=0)', 'boundary')
    add(238, 9996, 'A=1/42 written with large p,q: answer 1', 'boundary')
    add(1, 1, 'p=q=1 minimum integers, A=1', 'boundary')
    add(10000, 10000, 'p=q=10^4, A=1 (scale-invariance)', 'boundary')
    add(1, 41, 'A=1/41 just above minimum', 'boundary')
    add(1, 2, 'A=1/2: pi(2)=1 equals A*rub(2) exactly so n=2 is included', 'boundary')
    add(1, 3, 'A=1/3: n=2 fails, answer 1', 'boundary')
    add(2, 3, 'A=2/3', 'boundary')
    add(9999, 10000, 'A just below 1 with maximal p,q', 'boundary')
    add(10000, 9999, 'A just above 1 with maximal p,q', 'boundary')
    for p, q in ((42, 1), (84, 2), (420, 10), (9996, 238)):
        add(p, q, 'maximum A=42 exactly: answer 1179858 needs a table above 10^6', 'maxSize')
    add(10000, 239, 'A=10000/239 just below 42 (official max-size analogue)', 'maxSize')
    add(9995, 238, 'A=9995/238 just below 42', 'maxSize')
    add(41, 1, 'A=41', 'maxSize')
    add(9997, 239, 'A=9997/239 near 41.8', 'maxSize')
    for p in (35, 36, 37, 38, 39, 40):
        add(p, 1, f'large integer A={p}: answer near or above 10^6 (999999-limit tables fail)', 'maxSize')
    for p in range(1, 42):
        add(p, 1, f'integer A={p}; small limits (170, 2*10^5, 999999) fail once the answer exceeds them')
    for q in range(2, 42):
        add(1, q, f'A=1/{q}')
    eq = _equality_pairs()
    picks = sorted(set(eq[i] for i in range(0, len(eq), max(1, len(eq) // 20))) | set(eq[:5]) | set(eq[-5:]), reverse=True)
    for n, a, b in picks:
        add(a, b, f'A equals pi(n)/rub(n) exactly at suffix-record n={n}: equality must be included')
        m = MAX_PQ // b
        if m >= 1:
            add(a * m - 1, b * m, f'A just below pi({n})/rub({n}): answer drops below the record n={n}')
    by_n = {n: (pi, rub) for n, pi, rub in _records()}
    float_traps = [(n, a, b) for n, a, b in eq if a / b * by_n[n][1] < by_n[n][0]]
    for n, a, b in float_traps[::max(1, len(float_traps) // 15)]:
        add(a, b, f'A=pi({n})/rub({n}) exactly but float(p/q)*rub(n) rounds below pi(n): float comparison loses n={n}')
    for p, q in ((3, 2), (6, 4), (5, 3), (7, 4), (2, 1), (5, 2), (12, 5)):
        add(p, q, 'pi/rub is not monotone: scanning upward and stopping at the first failure undershoots')
    for p, q in ((17, 10), (171, 100), (13, 4), (100, 29), (7, 1), (25, 3)):
        add(p, q, 'fractional A where p//q truncation or first-failure stop changes the answer')
    for _ in range(20):
        q = rng.randint(1, MAX_PQ)
        p = rng.randint(max(1, -(-q // MAX_A)), min(MAX_PQ, MAX_A * q))
        add(p, q, 'fixed-seed random valid fraction', 'adversarial')
    return cases


def brute_checks():
    counts = {'568A': 0}
    rng = random.Random(568002)

    def check(p, q):
        expected = brute('568A', (p, q))
        assert answer('568A', (p, q)) == expected, (p, q, expected)
        counts['568A'] += 1

    primes, pals = _brute_tables()
    for n, pi in ((10, 4), (100, 25), (10 ** 4, 1229), (10 ** 5, 9592), (10 ** 6, 78498), (2 * 10 ** 6, 148933)):
        assert bisect_right(primes, n) == pi
        counts['568A'] += 1
    for n, rub in ((9, 9), (99, 18), (999, 108), (10 ** 6, 1998), (2 * 10 ** 6, 2998)):
        assert bisect_right(pals, n) == rub
        counts['568A'] += 1
    assert primes[:len(_primes(LIMIT + 1))] == _primes(LIMIT + 1)
    assert pals == _palindromes(LIMIT)
    counts['568A'] += 2
    for p in range(1, 61):
        for q in range(1, 61):
            if _valid(p, q):
                check(p, q)
    for _ in range(1500):
        q = rng.randint(1, MAX_PQ)
        p = rng.randint(max(1, -(-q // MAX_A)), min(MAX_PQ, MAX_A * q))
        check(p, q)
    for n, a, b in _equality_pairs():
        check(a, b)
    for case in extras('568A'):
        check(*parse('568A', case['input']))
    for p in range(1, 9):
        for q in range(1, 9):
            if _valid(p, q):
                expected = answer('568A', (p, q))
                if expected < 3000:
                    assert literal_scan(p, q, 30000) == expected, (p, q)
                    counts['568A'] += 1
    return counts


def review(pid, tests, samples):
    failures = []
    for name, pair in tests + samples:
        try:
            expected = [str(answer(pid, parse(pid, pair['input'])))]
            if expected != pair['output'].split():
                failures.append({'test': name, 'reason': 'independent oracle disagreement', 'expected': expected, 'actual': pair['output'].split()[:15]})
        except (ValueError, IndexError) as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
