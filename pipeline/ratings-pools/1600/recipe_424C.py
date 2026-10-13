"""Magic Formulas (424C): xor of p_i and every i mod k for 1<=i,k<=n."""
from functools import reduce
from operator import xor
import random
import re


IDS = ('424C',)
SEMANTICS = {
    '424C': 'Line 1: n, 1<=n<=10^6. Line 2: exactly n integers 0<=p_i<=2*10^9 (exponents attested from the public English statement). '
            'Unique integer Q = q_1 xor ... xor q_n with q_i = p_i xor (i mod 1) xor ... xor (i mod n); the formula image and the sample fix the last term as q_n, not the upstream text q_{n-1}. '
            'Oracle: Q = xor(p) xor, for each modulus k, (prefix xor 0..k-1 when n//k is odd) xor (prefix xor 0..n mod k). '
            'Independently checked by the literal n^2 double loop over all (i, k) on exhaustive small domains and fixed-seed random arrays.',
}

MAX_N = 10 ** 6
MAX_P = 2 * 10 ** 9
INTEGER = re.compile(r'0|[1-9][0-9]*')


def parse(pid, text):
    if pid not in IDS:
        raise ValueError('unknown problem')
    lines = text.splitlines()
    if len(lines) != 2:
        raise ValueError('magic formulas line layout')
    head, body = lines[0].split(), lines[1].split()
    if len(head) != 1 or not INTEGER.fullmatch(head[0]):
        raise ValueError('n token')
    n = int(head[0])
    if not 1 <= n <= MAX_N:
        raise ValueError('n constraints')
    if len(body) != n:
        raise ValueError('sequence arity')
    if not all(INTEGER.fullmatch(token) for token in body):
        raise ValueError('sequence tokens')
    values = list(map(int, body))
    if max(values) > MAX_P:
        raise ValueError('p_i constraints')
    return values


def prefix_xor(x):
    return (x, 1, x + 1, 0)[x & 3]


def answer(pid, data):
    n = len(data)
    total = reduce(xor, data, 0)
    for k in range(1, n + 1):
        if (n // k) & 1:
            total ^= prefix_xor(k - 1)
        total ^= prefix_xor(n % k)
    return total


def literal(data):
    n = len(data)
    total = 0
    for i in range(1, n + 1):
        q = data[i - 1]
        for k in range(1, n + 1):
            q ^= i % k
        total ^= q
    return total


def render(values):
    return f'{len(values)}\n' + ' '.join(map(str, values)) + '\n'


def extras(pid):
    if pid not in IDS:
        raise ValueError('unknown problem')
    rng = random.Random(16004240)
    cases = []

    def add(values, reason, category='adversarial'):
        text = render(values)
        cases.append({'input': text, 'output': str(answer(pid, parse(pid, text))) + '\n',
                      'reason': reason, 'category': category})

    add([0], 'minimum n and value', 'boundary')
    add([MAX_P], 'minimum n with maximum value', 'boundary')
    add([1], 'n=1 single positive value', 'boundary')
    add([MAX_P, MAX_P], 'n=2 equal maximum values cancel', 'boundary')
    add([MAX_P, 0, MAX_P - 1], 'n=3 maximum/zero/near-maximum values', 'boundary')
    for n in range(2, 41):
        add([0] * n, 'zero sequence isolates the modulus part for every n mod 4 residue and missing k=n / q_n terms', 'boundary')
    for n in (64, 65, 127, 128, 129, 255, 256, 1023, 1024, 1025):
        add([0] * n, 'zero sequence at power-of-two block boundaries of the prefix xor')
    for n in (2, 3, 5, 8, 13, 21):
        add(list(range(1, n + 1)), 'p_i = i repeats the modulus values')
    for n in (3, 4, 5, 7, 9):
        add([MAX_P] * n, 'repeated maximum values: xor parity differs from sum and carries')
    for _ in range(40):
        n = rng.randint(1, 60)
        add([rng.randint(0, MAX_P) for _ in range(n)], 'fixed-seed small arrays over the full value range')
    for _ in range(25):
        n = rng.randint(61, 3000)
        add([rng.randint(0, MAX_P) for _ in range(n)], 'fixed-seed medium arrays over the full value range')
    for n in (65535, 65536, 99999, 100000, 131071, 131072):
        add([rng.randint(MAX_P - 1000, MAX_P) for _ in range(n)], 'large n with values near 2*10^9, high-bit xor and int32 range')
    for n in (999997, 999998, 999999):
        add([0] * n, 'near-maximum n with zero values for each n mod 4 residue')
    add([i % 10 for i in range(1, MAX_N + 1)], 'maximum n=10^6, digit values', 'maxSize')
    add([0] * MAX_N, 'maximum n=10^6, pure modulus part', 'maxSize')
    return cases


def brute_checks():
    count = 0
    rng = random.Random(16004241)

    def check(values):
        nonlocal count
        expected = literal(values)
        assert answer('424C', values) == expected, (values, expected)
        count += 1

    for n in range(1, 7):
        for mask in range(4 ** n):
            check([(mask >> (2 * j)) & 3 for j in range(n)])
    for n in range(1, 151):
        check([0] * n)
        check([rng.randint(0, MAX_P) for _ in range(n)])
    for _ in range(100):
        check([rng.randint(0, MAX_P) for _ in range(rng.randint(151, 400))])
    return {'424C': count}


def review(pid, tests, samples):
    failures = []
    for name, pair in [*tests, *samples]:
        try:
            expected = str(answer(pid, parse(pid, pair['input'])))
            lines = pair['output'].splitlines()
            if len(lines) != 1 or lines[0].split() != [expected]:
                failures.append({'test': name, 'reason': 'independent oracle disagreement or output layout',
                                 'expected': expected, 'actual': pair['output'][:64]})
        except ValueError as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
