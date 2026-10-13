"""Source-attested recipe authoring for Dima and Two Sequences, not qualification."""
from collections import Counter
import itertools
import math
import random
import re


IDS = ('272D',)
SEMANTICS = {
    '272D': 'Public English HTML attests n1..100000, ai/bi1..1000000000, '
            'm2..1000000007, four lines n/a/b/m. All 2n points are used once '
            'in nondecreasing x order; equal (x,i) copies are indistinguishable. '
            'Unique scalar output is product_x count(x)! / 2^equal_pairs(x), '
            'modulo m. Cancel powers of two before modular multiplication, '
            'including even/composite m. Literal distinct-point sequence '
            'enumeration and binomial interleavings cross-check the oracle.',
}


def _require_id(pid):
    if pid not in IDS:
        raise ValueError('unsupported problem id')


def parse(pid, text):
    _require_id(pid)
    normalized = text.replace('\r\n', '\n')
    if re.fullmatch(r'[0-9 \t\n]*', normalized) is None:
        raise ValueError('expected decimal integers and ASCII horizontal whitespace')
    lines = normalized.split('\n')
    if lines[-1] == '':
        lines.pop()
    if len(lines) != 4:
        raise ValueError('expected four lines n/a/b/m')
    tokens = [line.split() for line in lines]
    if any(not line for line in tokens) or any(
            re.fullmatch(r'[0-9]+', token) is None
            for line in tokens for token in line):
        raise ValueError('expected unsigned decimal integer tokens')
    if len(tokens[0]) != 1 or len(tokens[3]) != 1:
        raise ValueError('n and m require one token each')
    n, modulus = int(tokens[0][0]), int(tokens[3][0])
    if not 1 <= n <= 100000 or not 2 <= modulus <= 1000000007:
        raise ValueError('n or modulus outside attested constraints')
    if len(tokens[1]) != n or len(tokens[2]) != n:
        raise ValueError('each array requires exactly n tokens on its own line')
    a, b = [list(map(int, line)) for line in tokens[1:3]]
    if any(not 1 <= value <= 1000000000 for value in a + b):
        raise ValueError('coordinate outside attested constraints')
    return a, b, modulus


def answer(pid, data):
    _require_id(pid)
    a, b, modulus = data
    counts = Counter(a)
    counts.update(b)
    duplicates = Counter(x for x, y in zip(a, b) if x == y)
    result = 1
    for value, count in counts.items():
        twos = duplicates[value]
        for factor in range(2, count + 1):
            while twos and factor % 2 == 0:
                factor //= 2
                twos -= 1
            result = result * factor % modulus
        if twos:
            raise AssertionError('duplicate denominator exceeds factorial two factors')
    return result


def _enumerated_count(a, b):
    remaining = Counter((x, i) for row in (a, b) for i, x in enumerate(row))
    points = sorted(remaining)

    def visit(left, last_x):
        if not left:
            return 1
        total = 0
        for point in points:
            if remaining[point] and point[0] >= last_x:
                remaining[point] -= 1
                total += visit(left - 1, point[0])
                remaining[point] += 1
        return total

    return visit(len(a) + len(b), 0)


def _interleaving_answer(data):
    a, b, modulus = data
    points = Counter((x, i) for row in (a, b) for i, x in enumerate(row))
    used = Counter()
    result = 1
    for (x, _), copies in sorted(points.items()):
        result = result * math.comb(used[x] + copies, copies) % modulus
        used[x] += copies
    return result


def _input(a, b, modulus):
    return (str(len(a)) + '\n' + ' '.join(map(str, a)) + '\n'
            + ' '.join(map(str, b)) + '\n' + str(modulus) + '\n')


def extras(pid):
    _require_id(pid)
    cases, seen = [], set()

    def add(a, b, modulus, reason, category='adversarial'):
        text = _input(a, b, modulus)
        if text not in seen:
            seen.add(text)
            cases.append({'input': text, 'output': str(answer(pid, parse(pid, text))) + '\n',
                          'reason': reason, 'category': category})

    for a, b, modulus in (([1], [1], 2), ([1], [2], 2),
                          ([1000000000], [1000000000], 1000000007),
                          ([1], [1000000000], 1000000007),
                          ([1, 2], [1, 2], 4), ([1, 2], [2, 2], 4)):
        add(a, b, modulus, 'minimum n, coordinate endpoints and identical-point distinction', 'boundary')
    special = [
        ([1, 1], [1, 1], 4),
        ([1, 1, 1], [1, 1, 1], 8),
        ([1, 1, 1, 1], [1, 1, 1, 1], 12),
        ([1, 2, 3, 4], [4, 3, 2, 1], 1009),
        ([1, 2, 3, 3, 5], [1, 2, 3, 5, 3], 12),
        ([1, 1, 2], [2, 1, 1], 9),
        ([1, 2, 1, 2], [2, 1, 2, 1], 25),
        ([7, 7, 7], [9, 9, 9], 1000),
        ([1, 2, 3], [4, 5, 6], 2),
        ([1, 2, 3, 3], [1, 2, 3, 3], 8),
    ]
    for a, b, modulus in special:
        add(a, b, modulus, 'factorial multiplicities, cross-index ties and cancellation before reduction')
    patterns = [
        ([5] * 5, [5] * 5),
        ([1, 1, 1, 1], [2, 2, 2, 2]),
        ([1, 2, 1, 2, 3], [1, 1, 2, 3, 3]),
        ([2, 1, 2, 3, 1, 3], [1, 2, 3, 2, 3, 1]),
        ([1, 2, 3, 4, 4], [5, 2, 3, 4, 4]),
    ]
    for modulus in (2, 3, 4, 6, 8, 9, 10, 12, 16, 25, 27, 97, 1000000007):
        for a, b in patterns:
            add(a, b, modulus, 'even/composite/prime moduli; no inverse of two or reduction before division')
    n = 100000
    add([1] * n, [1] * n, 1000000007,
        'maximum n and 200000-point multiplicity with 100000 identical pairs', 'maxSize')
    add(list(range(1, n + 1)), list(range(1000000000 - n + 1, 1000000001)), 1000000007,
        'maximum n with 200000 distinct x coordinates and largest coordinate', 'maxSize')
    add(list(range(1, n + 1)), list(range(1, n + 1)), 2,
        'maximum n with 100000 separate duplicate-point groups under even modulus', 'maxSize')
    add([1000000000] * n, [1000000000, 1] * (n // 2), 1000000006,
        'maximum n with mixed identical pairs, unequal group sizes and large even modulus', 'maxSize')
    rng = random.Random(2721600)
    for index in range(80):
        size = rng.randint(2, 35)
        palette = [1, 2, 3, 7, 1000000000][:rng.randint(1, 5)]
        a = [rng.choice(palette) for _ in range(size)]
        b = [x if rng.randrange(3) == 0 else rng.choice(palette) for x in a]
        if index % 3 == 0:
            rng.shuffle(b)
        add(a, b, rng.choice((2, 4, 6, 8, 9, 12, 25, 97, 1009, 1000000007)),
            'fixed-seed duplicate points vs cross-index equal x and unequal multiplicities')
    return cases


def brute_checks():
    count = 0
    moduli = (2, 3, 4, 6, 8, 9, 97, 1000000007)
    for n in range(1, 4):
        for values in itertools.product((1, 2, 3), repeat=2 * n):
            a, b = values[:n], values[n:]
            exact = _enumerated_count(a, b)
            for modulus in moduli:
                actual = answer('272D', (a, b, modulus))
                if actual != exact % modulus:
                    raise AssertionError((a, b, modulus, exact, actual))
                count += 1
    rng = random.Random(2721601)
    for _ in range(128):
        a = [rng.randint(1, 4) for _ in range(4)]
        b = [rng.randint(1, 4) for _ in range(4)]
        exact = _enumerated_count(a, b)
        for modulus in moduli:
            actual = answer('272D', (a, b, modulus))
            if actual != exact % modulus:
                raise AssertionError((a, b, modulus, exact, actual))
            count += 1
    for case in extras('272D'):
        data = parse('272D', case['input'])
        actual, expected = answer('272D', data), _interleaving_answer(data)
        if actual != expected:
            raise AssertionError((case['reason'], actual, expected))
        count += 1
    return {'272D': count}


def review(pid, tests, samples):
    _require_id(pid)
    failures = []
    for name, pair in tests + samples:
        try:
            expected = [str(answer(pid, parse(pid, pair['input'])))]
            actual = pair['output'].split()
            if expected != actual:
                failures.append({'test': name, 'reason': 'exact oracle disagreement',
                                 'expected': expected, 'actual': actual})
        except (ValueError, IndexError) as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
