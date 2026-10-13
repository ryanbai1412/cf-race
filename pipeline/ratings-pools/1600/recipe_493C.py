"""Source-attested exact scores for Vasya and Basketball; not qualification."""
import itertools
import random
import re


IDS = ('493C',)
SEMANTICS = {
    '493C': 'Public English statement confirms n,m1..200000 and distances1..2000000000; '
            'preserved sample/test layout is n, n distances, m, m distances on four lines. '
            'Nonnegative integer d gives 2 points at distance<=d, otherwise3. '
            'Maximize (first score-second score, first score), yielding unique a:b. '
            'Sweep whole equal-distance groups; independent literal threshold scoring '
            'checks exhaustive small ordered arrays and fixed-seed cases.',
}


def _pid(pid):
    if pid not in IDS:
        raise ValueError('unsupported problem')


def parse(pid, text):
    _pid(pid)
    lines = [line.split() for line in text.strip().splitlines()]
    if len(lines) != 4 or len(lines[0]) != 1 or len(lines[2]) != 1:
        raise ValueError('expected four-line team layout')
    if any(re.fullmatch(r'[0-9]+', token) is None for line in lines for token in line):
        raise ValueError('expected decimal integers')
    n, m = int(lines[0][0]), int(lines[2][0])
    if not (1 <= n <= 200000 and 1 <= m <= 200000):
        raise ValueError('team size range')
    if len(lines[1]) != n or len(lines[3]) != m:
        raise ValueError('team distance arity')
    a, b = [int(v) for v in lines[1]], [int(v) for v in lines[3]]
    if any(not 1 <= v <= 2000000000 for v in a + b):
        raise ValueError('distance range')
    return a, b


def answer(pid, data):
    _pid(pid)
    a, b = map(sorted, data)
    first, second = 3 * len(a), 3 * len(b)
    best = first - second, first, second
    i = j = 0
    while i < len(a) or j < len(b):
        distance = min(a[i] if i < len(a) else 2000000001,
                       b[j] if j < len(b) else 2000000001)
        while i < len(a) and a[i] == distance:
            first -= 1
            i += 1
        while j < len(b) and b[j] == distance:
            second -= 1
            j += 1
        candidate = first - second, first, second
        if candidate[:2] > best[:2]:
            best = candidate
    return f'{best[1]}:{best[2]}'


def _literal_best(data, thresholds=None):
    a, b = data
    if thresholds is None:
        thresholds = {0, *a, *b}
    scores = []
    for d in thresholds:
        first = sum(2 if v <= d else 3 for v in a)
        second = sum(2 if v <= d else 3 for v in b)
        scores.append((first - second, first, second))
    _, first, second = max(scores)
    return f'{first}:{second}'


def _input(a, b):
    return f'{len(a)}\n' + ' '.join(map(str, a)) + f'\n{len(b)}\n' + ' '.join(map(str, b)) + '\n'


def extras(pid):
    _pid(pid)
    rng = random.Random(4931600)
    cases = []
    seen = set()

    def add(a, b, reason, category='adversarial'):
        text = _input(a, b)
        if text not in seen:
            seen.add(text)
            cases.append({'input': text, 'output': answer(pid, (a, b)) + '\n',
                          'reason': reason, 'category': category})

    for a, b in (([1], [1]), ([2000000000], [2000000000]),
                 ([1], [2000000000]), ([2000000000], [1])):
        add(a, b, 'minimum dimensions and inclusive distance endpoints', 'boundary')
    for a, b, reason in (
        ([1], [1, 1], 'negative optimum; zero is not a feasible initial score'),
        ([1], [1, 2], 'best occurs after the first team is exhausted; include all-two endpoint'),
        ([3], [3], 'equal advantages select largest first score, not last threshold'),
        ([1, 1], [1, 1], 'equal-distance groups must cross threshold atomically'),
        ([3, 3, 4], [2, 2, 3, 3, 3, 3], 'shared duplicates and a strict interior optimum'),
        ([2, 2, 2], [1, 1, 1], 'threshold exactly equal to second-team distance gives two points'),
        ([5, 5, 5], [1, 1, 4, 4, 9], 'optimum at a distance present only in the second team'),
        ([1, 2000000000], [2, 4], 'sparse distance gaps require cumulative counts'),
        ([9, 1, 4, 3], [10, 1, 2], 'unsorted inputs require sorting before a sweep'),
        ([2, 2, 2, 10], [1, 1, 1, 3, 3, 3, 9, 9, 9], 'multiple rises and falls; advantage is not unimodal'),
        ([3, 3, 9], [1, 1, 7, 7], 'same optimum advantage at separated thresholds; keep higher first score'),
        ([2, 2], [1, 2000000000, 1], 'unequal team sizes and a large trailing distance'),
        ([2000000000, 1999999999], [1999999998, 2000000000], 'adjacent distances near numeric maximum'),
        ([8, 1, 8, 1, 8], [7, 2, 7, 2], 'descending and interleaved repeated distances'),
    ):
        add(a, b, reason)
    for x, y in itertools.product(range(1, 5), repeat=2):
        add([x], [y], 'exhaustive singleton threshold orderings', 'boundary')
    for a, b in itertools.product(itertools.product((1, 2), repeat=2), repeat=2):
        add(a, b, 'exhaustive length-two duplicate orderings')
    add([1] * 200000, [1] * 200000,
        'maximum both dimensions; ties retain 600000:600000', 'maxSize')
    add([2000000000] * 200000, [1] * 200000,
        'maximum both dimensions and distance; strict threshold split', 'maxSize')
    add([1] * 200000, [2000000000],
        'maximum first-team size against minimum second team', 'maxSize')
    add([1], [2000000000] * 200000,
        'maximum second-team size against minimum first team; all-two optimum', 'maxSize')
    while len(cases) < 160:
        if len(cases) % 3:
            a = [rng.randint(1, 12) for _ in range(rng.randint(1, 16))]
            b = [rng.randint(1, 12) for _ in range(rng.randint(1, 16))]
            reason = 'fixed-seed small duplicate-heavy thresholds and unequal counts'
        else:
            domain = (1, 2, 37, 1000000000, 1999999999, 2000000000)
            a = [rng.choice(domain) for _ in range(rng.randint(10, 60))]
            b = [rng.choice(domain) for _ in range(rng.randint(10, 60))]
            reason = 'fixed-seed sparse high distances, plateaus and mixed input ordering'
        rng.shuffle(a)
        rng.shuffle(b)
        add(a, b, reason)
    return cases


def review(pid, tests, samples):
    _pid(pid)
    failures = []
    for name, pair in [*tests, *samples]:
        try:
            expected = answer(pid, parse(pid, pair['input']))
            if pair['output'].split() != [expected]:
                failures.append({'test': name, 'reason': 'exact score disagreement',
                                 'expected': expected, 'actual': pair['output']})
        except (ValueError, KeyError, TypeError) as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures


def brute_checks():
    count = 0

    def check(data, thresholds=None):
        nonlocal count
        actual = answer('493C', data)
        expected = _literal_best(data, thresholds)
        assert actual == expected, (data, expected, actual)
        count += 1

    arrays = [a for n in range(1, 5) for a in itertools.product((1, 2, 3), repeat=n)]
    for data in itertools.product(arrays, repeat=2):
        check(data, range(4))
    rng = random.Random(4931601)
    for _ in range(500):
        a = [rng.randint(1, 25) for _ in range(rng.randint(1, 12))]
        b = [rng.randint(1, 25) for _ in range(rng.randint(1, 12))]
        check((a, b), range(26))
    for _ in range(200):
        a = [rng.randint(1, 2000000000) for _ in range(rng.randint(1, 12))]
        b = [rng.randint(1, 2000000000) for _ in range(rng.randint(1, 12))]
        check((a, b))
    for pair in extras('493C'):
        check(parse('493C', pair['input']))
    return {'493C': count}
