"""Fish Weight: exact dominance oracle and deterministic author-only cases."""
from collections import Counter
import itertools
import random
import re


IDS = ('297B',)
SEMANTICS = {
    '297B': 'Public English HTML attests n,m1..100000, k1..1000000000; '
            'exactly three lines with n Alice species and m Bob species, each1..k, '
            'duplicates allowed. Positive nondecreasing real weights are existential, '
            'not equal to species IDs. Unique YES iff some suffix of species has '
            'more Alice fish than Bob fish; equivalently n>m or a descending '
            'Alice rank exceeds the matching Bob rank. Otherwise unique NO. '
            'Literal finite weight-vector enumeration independently checks small cases.'
}


def _pid(pid):
    if pid not in IDS:
        raise ValueError('unsupported problem: ' + str(pid))


def parse(pid, text):
    _pid(pid)
    lines = [line.split() for line in text.strip().splitlines()]
    if len(lines) != 3 or len(lines[0]) != 3:
        raise ValueError('expected header and two fish-array lines')
    if any(re.fullmatch(r'[1-9][0-9]*', token) is None
           for line in lines for token in line):
        raise ValueError('expected positive decimal integer tokens')
    n, m, k = map(int, lines[0])
    if not (1 <= n <= 100000 and 1 <= m <= 100000 and 1 <= k <= 1000000000):
        raise ValueError('fish-count/species-count range')
    if len(lines[1]) != n or len(lines[2]) != m:
        raise ValueError('fish-array line arity')
    alice, bob = tuple(map(int, lines[1])), tuple(map(int, lines[2]))
    if any(not 1 <= fish <= k for fish in alice + bob):
        raise ValueError('fish species outside1..k')
    return k, alice, bob


def answer(pid, data):
    _pid(pid)
    _, alice, bob = data
    if len(alice) > len(bob):
        return ['YES']
    a, b = sorted(alice, reverse=True), sorted(bob, reverse=True)
    return ['YES' if any(x > y for x, y in zip(a, b)) else 'NO']


def _suffix_reference(data):
    _, alice, bob = data
    deltas = Counter(alice)
    deltas.subtract(bob)
    balance = 0
    for species in sorted(deltas, reverse=True):
        balance += deltas[species]
        if balance > 0:
            return ['YES']
    return ['NO']


def _weight_reference(data):
    k, alice, bob = data
    # A positive suffix coefficient is witnessed by one jump of n+m above base1.
    for weights in itertools.combinations_with_replacement(
            range(1, len(alice) + len(bob) + 2), k):
        left = sum(weights[x - 1] for x in alice)
        right = sum(weights[x - 1] for x in bob)
        if left > right:
            return ['YES']
    return ['NO']


def extras(pid):
    _pid(pid)
    rng = random.Random(1600297)
    cases, seen = [], set()

    def add(k, alice, bob, reason, category='adversarial'):
        text = (f'{len(alice)} {len(bob)} {k}\n'
                + ' '.join(map(str, alice)) + '\n'
                + ' '.join(map(str, bob)) + '\n')
        if text in seen:
            return
        seen.add(text)
        cases.append({'input': text, 'output': answer(pid, (k, alice, bob))[0] + '\n',
                      'reason': reason, 'category': category})

    for k, alice, bob, reason in (
        (1, [1], [1], 'minimum dimensions; equality must be NO'),
        (1, [1, 1], [1], 'constant positive weights: multiplicity beats species count'),
        (1, [1], [1, 1], 'fewer identical fish can never win'),
        (2, [2], [1], 'single higher species; first occurrences count'),
        (2, [1], [2], 'single lower species cannot win'),
        (3, [2, 2, 2], [1, 1, 3], 'intermediate suffix beats a larger maximum'),
        (3, [3], [2, 2, 2, 2, 2], 'one heavy fish can outweigh many lighter fish'),
        (3, [1, 1, 1], [3, 3], 'more fish wins even if all species are lower'),
        (3, [3, 1], [3, 2], 'cancel common maximum; remaining Alice fish is dominated'),
        (6, [5, 2], [6, 1], 'equal species sums, but intermediate suffix permits YES'),
        (10, [5, 5], [10], 'equal species sums, but more fish permits YES'),
        (10, [10], [6, 6], 'smaller species sum but an unbounded heavy species permits YES'),
        (10, [6, 6], [10, 1], 'larger species sum is not the general criterion'),
        (10, [9, 1, 1], [10, 8, 2], 'every descending rank is dominated despite local surplus'),
        (10, [1, 9, 4], [4, 1, 9], 'permuted equal multisets remain NO'),
        (10, [8, 2, 8], [9, 1, 1], 'maximum Alice species is lower, lower rank still wins'),
        (1000000000, [1000000000], [999999999], 'maximum species ID and unit gap'),
        (1000000000, [999999999], [1000000000], 'unit gap in the opposite direction'),
        (1000000000, [1], [1], 'unused species do not change the result'),
        (1000000000, [1000000000, 1], [1000000000, 2], 'equal upper suffix then dominated tail'),
        (4, [4, 3, 3, 1], [4, 4, 2, 2, 1], 'surplus at species3 after one upper deficit'),
        (4, [3, 3, 3, 1], [4, 4, 2, 2, 1], 'surplus eventually crosses zero at species3'),
    ):
        add(k, alice, bob, reason, 'boundary')

    arrays = [values for n in range(1, 3) for values in itertools.product((1, 2), repeat=n)]
    for alice, bob in itertools.product(arrays, repeat=2):
        add(2, alice, bob, 'exhaustive two-species ordered arrays of lengths1..2')
    while len(cases) < 110:
        k = rng.randint(1, 6)
        alice = [rng.randint(1, k) for _ in range(rng.randint(1, 8))]
        bob = [rng.randint(1, k) for _ in range(rng.randint(1, 8))]
        add(k, alice, bob, 'fixed-seed small duplicate-heavy arrays and unequal counts')
    while len(cases) < 155:
        k = rng.choice((10, 1000000000))
        n, m = rng.randint(10, 80), rng.randint(10, 80)
        pool = sorted({1, k, rng.randint(1, k), rng.randint(1, k)})
        alice = [rng.choice(pool) for _ in range(n)]
        bob = [rng.choice(pool) for _ in range(m)]
        add(k, alice, bob, 'fixed-seed sparse species gaps, shuffled duplicates, rank transitions')

    add(1000000000, [1] * 100000, [1000000000] * 100000,
        'legal maximum n=m=100000 and k=10^9; all Alice ranks dominated', 'maxSize')
    add(1000000000, [1] * 99999 + [1000000000], [999999999] * 100000,
        'legal maximum arrays; a single upper-suffix witness at the last input position', 'maxSize')
    add(1000000000, [1] * 100000, [1000000000] * 99999,
        'maximum Alice size, one extra fish suffices with almost equal weights', 'maxSize')
    add(1000000000, [1000000000], [999999999] * 100000,
        'maximum Bob size; one heavier species can defeat100000 lighter fish', 'maxSize')
    add(1000000000, list(range(1, 100001)), list(range(100000, 0, -1)),
        'maximum equal multisets in reversed input order; many distinct species', 'maxSize')
    return cases


def brute_checks():
    count = 0
    for k in range(1, 4):
        arrays = [values for n in range(1, 4)
                  for values in itertools.product(range(1, k + 1), repeat=n)]
        for alice, bob in itertools.product(arrays, repeat=2):
            data = k, alice, bob
            expected = _weight_reference(data)
            assert answer('297B', data) == expected, data
            count += 1
    rng = random.Random(2971600)
    for _ in range(600):
        k = rng.choice((1, 2, 3, 10, 1000000000))
        data = (k, tuple(rng.randint(1, k) for _ in range(rng.randint(1, 25))),
                tuple(rng.randint(1, k) for _ in range(rng.randint(1, 25))))
        assert answer('297B', data) == _suffix_reference(data), data
        count += 1
    for pair in extras('297B'):
        data = parse('297B', pair['input'])
        assert pair['output'].split() == _suffix_reference(data), pair['reason']
        count += 1
    return {'297B': count}


def review(pid, tests, samples):
    _pid(pid)
    failures = []
    for name, pair in [*tests, *samples]:
        try:
            expected = answer(pid, parse(pid, pair['input']))
            actual = pair['output'].split()
            if expected != actual:
                failures.append({'test': name, 'reason': 'exact oracle disagreement',
                                 'expected': expected, 'actual': actual})
        except (ValueError, TypeError, KeyError) as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
