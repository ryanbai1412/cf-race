"""Exact 150B recipe: counting length-n strings whose every length-k substring is a palindrome."""
import itertools
import random
import re


IDS = ('150B',)
MOD = 1000000007
SEMANTICS = {
    '150B': 'Single line n m k, each 1..2000. Count strings of length exactly n over an m-letter alphabet whose every length-k substring is a palindrome, modulo 1000000007. '
            'No length-k substring exists when k>n, so every string counts (m^n); k=1 also gives m^n; k=n forces one palindrome (m^ceil(n/2)); 1<k<n forces period-2 equality for odd k (m^2) and a constant string for even k (m). '
            'The count is unique; small domains are checked by literal enumeration of all m^n strings and by an independent position-union component count.',
}
INTEGER = re.compile(r'[0-9]+')


def parse(pid, text):
    if pid not in IDS:
        raise ValueError('unknown problem: ' + pid)
    lines = text.splitlines()
    while lines and not lines[-1].strip():
        lines.pop()
    if len(lines) != 1:
        raise ValueError('150B line layout: exactly one line n m k')
    tokens = lines[0].split()
    if len(tokens) != 3 or not all(INTEGER.fullmatch(t) for t in tokens):
        raise ValueError('150B arity: three nonnegative decimal integers')
    values = tuple(map(int, tokens))
    if not all(1 <= v <= 2000 for v in values):
        raise ValueError('150B constraints: 1 <= n, m, k <= 2000')
    return values


def answer(pid, data):
    n, m, k = data
    if k == 1 or k > n:
        return pow(m, n, MOD)
    if k == n:
        return pow(m, (n + 1) // 2, MOD)
    return m * m % MOD if k % 2 else m % MOD


def components(n, k):
    parent = list(range(n))

    def find(u):
        while parent[u] != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u
    for start in range(n - k + 1):
        for offset in range(k // 2):
            x, y = find(start + offset), find(start + k - 1 - offset)
            if x != y:
                parent[x] = y
    return sum(find(u) == u for u in range(n))


def union_count(data):
    n, m, k = data
    return pow(m, components(n, k), MOD)


def exhaustive(data):
    n, m, k = data
    total = 0
    for word in itertools.product(range(m), repeat=n):
        if all(word[i:i + k] == word[i:i + k][::-1] for i in range(n - k + 1)):
            total += 1
    return total % MOD


def extras(pid):
    rng = random.Random(16001500)
    cases = []
    seen = set()

    def add(n, m, k, reason, category='adversarial'):
        text = f'{n} {m} {k}\n'
        if text in seen:
            return
        seen.add(text)
        cases.append({'input': text, 'output': f'{answer(pid, parse(pid, text))}\n', 'reason': reason, 'category': category})
    for n, m, k in ((1, 1, 1), (1, 1, 2000), (1, 2000, 1), (1, 2000, 2000), (1, 7, 2), (2000, 1, 1), (2000, 1, 2000),
                    (2000, 1, 2), (2000, 1, 3), (2, 2000, 1), (2, 2000, 2), (2, 2000, 3), (2, 1, 2), (3, 2, 2), (3, 2, 3), (3, 2, 4)):
        add(n, m, k, 'minimum n/m/k, single-letter alphabet, and n=1..3 regime edges', 'boundary')
    for n in (4, 5, 6, 7):
        for k in range(1, n + 3):
            add(n, 3, k, 'every regime k=1, 1<k<n odd/even, k=n odd/even, k>n for small n', 'boundary')
    for n, m, k in ((2000, 2000, 1), (2000, 2000, 2), (2000, 2000, 3), (2000, 2000, 1000), (2000, 2000, 1001),
                    (2000, 2000, 1998), (2000, 2000, 1999), (2000, 2000, 2000), (1999, 2000, 2000), (1999, 1999, 1999),
                    (2000, 1999, 2000), (1998, 2000, 1999), (1000, 2000, 2000), (2000, 1999, 1), (2000, 1009, 1997)):
        add(n, m, k, 'maximum n/m/k: largest exponent m^n, m^ceil(n/2), and k=n+-1 parity boundaries', 'maxSize')
    for n, m, k in ((5, 3, 6), (10, 7, 12), (100, 50, 102), (1000, 2000, 1002), (1999, 1000, 2000), (5, 3, 7), (11, 9, 13), (999, 2000, 1001)):
        add(n, m, k, 'k>n counts every string: kills parity-only answers that ignore k>n', 'adversarial')
    for n, m in ((4, 5), (10, 3), (100, 100), (1000, 1000), (1500, 1777), (2, 9)):
        add(n, m, n, 'even k=n gives m^(n/2): kills answer m for even full-length palindrome', 'adversarial')
    for n, m in ((5, 2), (9, 3), (101, 100), (1001, 1999), (1777, 1234)):
        add(n, m, n, 'odd k=n gives m^((n+1)/2) with large exponent: kills float exponents and unreduced powers', 'adversarial')
    for n, m in ((2, 2), (10, 10), (100, 1999), (1999, 2000), (500, 1234)):
        add(n, m, 1, 'k=1 with k<n gives m^n: kills odd-k branch returning m^2', 'adversarial')
    for n, m, k in ((5, 3, 3), (10, 2000, 3), (2000, 1999, 5), (7, 2, 5), (100, 1000, 99), (50, 2000, 49)):
        add(n, m, k, 'odd 1<k<n gives m^2: kills m*(m-1) and m(m-1)/2 variants and component-count*m', 'adversarial')
    for n, m, k in ((5, 3, 2), (10, 2000, 4), (2000, 1999, 2), (100, 1000, 98), (7, 1, 6)):
        add(n, m, k, 'even 1<k<n gives m: constant string only', 'adversarial')
    for n, m in ((40, 2), (64, 2), (30, 3), (2000, 2), (1000, 3)):
        add(n, m, 1, 'm^n wraps 1000000007: kills missing modulo and float modular exponentiation', 'adversarial')
    while len(cases) < 130:
        n = rng.randint(1, 12)
        add(n, rng.randint(1, 6), rng.randint(1, n + 2), 'fixed-seed small regime mix')
    while len(cases) < 160:
        n = rng.randint(1, 2000)
        add(n, rng.randint(1, 2000), rng.choice((1, 2, 3, n - 1 or 1, n, n + 1 if n < 2000 else n, rng.randint(1, 2000))), 'fixed-seed full-range regime mix')
    return cases


def brute_checks():
    count = 0
    for n in range(1, 8):
        for m in range(1, 5):
            if m ** n > 20000:
                continue
            for k in range(1, n + 3):
                expected = exhaustive((n, m, k))
                assert answer('150B', (n, m, k)) == expected, (n, m, k)
                assert union_count((n, m, k)) == expected, (n, m, k)
                count += 2
    rng = random.Random(16001501)
    for n in range(1, 61):
        for k in range(1, n + 3):
            m = rng.randint(1, 2000)
            assert answer('150B', (n, m, k)) == union_count((n, m, k)), (n, m, k)
            count += 1
    return {'150B': count}


def review(pid, tests, samples):
    failures = []
    for name, pair in tests + samples:
        try:
            data = parse(pid, pair['input'])
            expected = answer(pid, data)
            if pair['output'].split() != [str(expected)]:
                failures.append({'test': name, 'reason': 'independent oracle disagreement', 'expected': [str(expected)], 'actual': pair['output'].split()[:15]})
        except (ValueError, IndexError) as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
