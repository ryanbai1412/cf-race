"""340C author recipe: exact expected route length, not qualification evidence."""
from fractions import Fraction
import itertools
import math
import random
import re


IDS = ('340C',)
SEMANTICS = {
    '340C': 'Original English statement: 2<=n<=10^5; second line has n '
             'distinct integers 1<=ai<=10^7. Each permutation visits all '
             'destinations once from 0, with no return. The unique positive '
             'irreducible numerator/denominator is (sum(ai)+2*sum(i<j, '
             '|ai-aj|))/n. Sorting with prefix sums is exact O(n log n); '
             'literal route enumeration independently checks small cases.'
}
MAX_N = 100000
MAX_A = 10000000


def _pid(pid):
    if pid not in IDS:
        raise ValueError('unsupported problem: ' + str(pid))


def parse(pid, text):
    _pid(pid)
    if not isinstance(text, str):
        raise ValueError('input must be text')
    lines = text.strip().splitlines()
    if len(lines) != 2:
        raise ValueError('expected exactly two input lines')
    header, coordinates = (line.split() for line in lines)
    if len(header) != 1 or not re.fullmatch(r'[0-9]+', header[0]):
        raise ValueError('expected one integer n on the first line')
    n = int(header[0])
    if not 2 <= n <= MAX_N or len(coordinates) != n:
        raise ValueError('n range or second-line arity violation')
    if any(not re.fullmatch(r'[0-9]+', token) for token in coordinates):
        raise ValueError('coordinates must be decimal integer tokens')
    values = tuple(map(int, coordinates))
    if any(not 1 <= value <= MAX_A for value in values):
        raise ValueError('coordinate range violation')
    if len(set(values)) != n:
        raise ValueError('destinations must be distinct')
    return values


def answer(pid, data):
    _pid(pid)
    ordered = sorted(data)
    prefix = pair_distances = 0
    for index, value in enumerate(ordered):
        pair_distances += index * value - prefix
        prefix += value
    numerator, denominator = prefix + 2 * pair_distances, len(ordered)
    divisor = math.gcd(numerator, denominator)
    return numerator // divisor, denominator // divisor


def _route_brute(values):
    total = routes = 0
    for route in itertools.permutations(values):
        previous = 0
        for destination in route:
            total += abs(destination - previous)
            previous = destination
        routes += 1
    expected = Fraction(total, routes)
    return expected.numerator, expected.denominator


def brute_checks():
    count = 0

    def check(values):
        nonlocal count
        expected = _route_brute(values)
        actual = answer('340C', values)
        assert actual == expected, (values, actual, expected)
        count += 1

    for n in range(2, 6):
        for values in itertools.permutations(range(1, 6), n):
            check(values)
    for n in range(2, 7):
        for values in itertools.combinations(range(1, 10), n):
            check(values)
            check(values[::-1])
    rng = random.Random(3401600)
    for _ in range(200):
        check(tuple(rng.sample(range(1, MAX_A + 1), rng.randint(2, 7))))
    return {'340C': count}


def extras(pid):
    _pid(pid)
    rng = random.Random(1600340)
    cases, seen = [], set()

    def add(values, reason, category='adversarial'):
        text = str(len(values)) + '\n' + ' '.join(map(str, values)) + '\n'
        if text in seen:
            return
        data = parse(pid, text)
        output = ' '.join(map(str, answer(pid, data))) + '\n'
        seen.add(text)
        cases.append({'input': text, 'output': output,
                      'reason': reason, 'category': category})

    for values in ((1, 2), (2, 1), (1, 3), (3, 1), (1, MAX_A),
                   (MAX_A, 1), (MAX_A - 1, MAX_A),
                   (MAX_A, MAX_A - 1), (1, 2, 3, 4), (2, 3, 5)):
        add(values, 'minimum n, coordinate endpoints, full/partial/no gcd '
                    'cancellation, and sample; no return to origin', 'boundary')
    for values in ((5, 2, 3), (3, 5, 2), (9, 1, 8, 2),
                   (1, 100, 2, 99, 3), tuple(range(10, 0, -1)),
                   tuple(range(1, 13)), (1, 2, MAX_A)):
        add(values, 'unsorted rank/gap formulas, wrong factorial denominator, '
                    'and reading only the first digit of n')

    for values, reason in (
        (list(range(1, MAX_N + 1)), 'maximum n, consecutive low coordinates'),
        (list(range(MAX_A, MAX_A - MAX_N, -1)),
         'maximum n, descending high coordinates and 64-bit sums'),
        (list(range(1, MAX_N // 2 + 1)) +
         list(range(MAX_A - MAX_N // 2 + 1, MAX_A + 1)),
         'maximum n, two distant clusters and large pair-distance total'),
        (rng.sample(range(1, MAX_A + 1), MAX_N),
         'maximum n, fixed-seed unique unsorted wide coordinates')):
        add(values, reason, 'maxSize')

    for _ in range(20):
        n = rng.randint(3, 40)
        start = rng.randint(1, MAX_A - 1000)
        step = rng.randint(1, 20)
        values = [start + step * index for index in range(n)]
        rng.shuffle(values)
        add(values, 'translated and shuffled arithmetic progressions; '
                    'pair distances unchanged but starting leg changes')
    for _ in range(20):
        n = rng.randint(10, 200)
        values = rng.sample(range(1, 1001), n // 2)
        values += rng.sample(range(MAX_A - 1000, MAX_A + 1), n - n // 2)
        rng.shuffle(values)
        add(values, 'separated clusters, input-order invariance, and '
                    'non-factorial denominator for multi-digit n')
    while len(cases) < 160:
        n = rng.randint(2, 8)
        domain = range(1, 41) if len(cases) % 2 else range(1, MAX_A + 1)
        add(rng.sample(domain, n), 'fixed-seed unique small routes, uneven '
                                  'gaps, sorting, and fraction reduction')
    return cases


def review(pid, tests, samples):
    _pid(pid)
    failures = []
    for name, pair in [*tests, *samples]:
        try:
            expected = list(map(str, answer(pid, parse(pid, pair['input']))))
            actual = pair['output'].split()
            if actual != expected:
                failures.append({'test': name, 'reason': 'exact oracle disagreement',
                                 'expected': expected, 'actual': actual})
        except (ValueError, KeyError, TypeError, AttributeError) as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
