"""Source-attested Chain Reaction recipe, not a pool qualification."""
from bisect import bisect_left
import itertools
import random
import re


IDS = ('607A',)
SEMANTICS = {
    '607A': 'Original English 607/A: n1..100000; n separate (a,b) rows, '
            'distinct a0..1000000 in arbitrary order, b1..1000000. '
            'An activated beacon destroys only others to its left at distance '
            '<=b; destroyed beacons never activate. The added rightmost beacon '
            'can delete any suffix, including none. Unique output is the minimum '
            'number of original beacons destroyed. Sorted prefix-survivor DP '
            'uses the last coordinate strictly below a-b; literal activation '
            'over every suffix cutoff independently checks small inputs. '
            'Attestation: https://codeforces.me/problemset/problem/607/A?locale=en.'
}


def _require_pid(pid):
    if pid not in IDS:
        raise ValueError('unsupported problem: ' + str(pid))


def parse(pid, text):
    _require_pid(pid)
    lines = [line.split() for line in text.splitlines()]
    if not lines or len(lines[0]) != 1:
        raise ValueError('beacon header line must contain exactly n')
    if not re.fullmatch(r'[0-9]+', lines[0][0]):
        raise ValueError('n must be an unsigned decimal integer')
    n = int(lines[0][0])
    if not 1 <= n <= 100000:
        raise ValueError('n outside 1..100000')
    if len(lines) != n + 1 or any(len(line) != 2 for line in lines[1:]):
        raise ValueError('expected exactly n separate two-integer beacon lines')
    beacons = []
    positions = set()
    for line in lines[1:]:
        if any(not re.fullmatch(r'[0-9]+', token) for token in line):
            raise ValueError('position/power must be unsigned decimal integers')
        a, b = map(int, line)
        if not 0 <= a <= 1000000 or not 1 <= b <= 1000000:
            raise ValueError('position/power outside source constraints')
        if a in positions:
            raise ValueError('beacon positions must be distinct')
        positions.add(a)
        beacons.append((a, b))
    return tuple(beacons)


def answer(pid, data):
    _require_pid(pid)
    beacons = sorted(data)
    positions = [a for a, _ in beacons]
    survivors = [0] * (len(beacons) + 1)
    best = 0
    for i, (a, b) in enumerate(beacons):
        untouched = bisect_left(positions, a - b, 0, i)
        survivors[i + 1] = survivors[untouched] + 1
        best = max(best, survivors[i + 1])
    return len(beacons) - best


def _literal_destroyed(data, retained):
    beacons = sorted(data)[:retained]
    destroyed = set()
    for i in range(retained - 1, -1, -1):
        if i in destroyed:
            continue
        a, b = beacons[i]
        for j in range(i):
            if a - beacons[j][0] <= b:
                destroyed.add(j)
    return len(data) - retained + len(destroyed)


def brute(data):
    return min(_literal_destroyed(data, retained)
               for retained in range(len(data) + 1))


def brute_checks():
    count = 0
    for n in range(1, 7):
        for positions in itertools.combinations(range(6), n):
            for powers in itertools.product(range(1, 5), repeat=n):
                data = tuple(zip(positions, powers))
                if answer('607A', data) != brute(data):
                    raise AssertionError(('exhaustive activation disagreement', data))
                count += 1
    rng = random.Random(6071600)
    for _ in range(400):
        n = rng.randint(1, 12)
        positions = rng.sample(range(80), n)
        data = tuple((a, rng.choice((1, 2, 4, 17, 80, 1000000)))
                     for a in positions)
        if answer('607A', data) != brute(data):
            raise AssertionError(('random activation disagreement', data))
        count += 1
    return {'607A': count}


def _input(data):
    return str(len(data)) + '\n' + ''.join(f'{a} {b}\n' for a, b in data)


def extras(pid):
    _require_pid(pid)
    cases = []
    seen = set()

    def add(data, reason, category='adversarial'):
        text = _input(data)
        if text in seen:
            return False
        seen.add(text)
        parsed = parse(pid, text)
        cases.append({'input': text, 'output': str(answer(pid, parsed)) + '\n',
                      'reason': reason, 'category': category})
        return True

    fixed = [
        ([(0, 1)], 'minimum n and coordinate; beacon never destroys itself'),
        ([(0, 1000000)], 'minimum coordinate and maximum power'),
        ([(1000000, 1)], 'maximum coordinate and minimum power'),
        ([(1000000, 1000000)], 'both numeric upper bounds at minimum n'),
        ([(0, 1), (1, 1)], 'inclusive distance: equality destroys the left beacon'),
        ([(0, 1), (2, 1)], 'zero coordinate must contribute a survivor'),
        ([(0, 1), (999999, 1000000)], 'negative blast cutoff destroys every predecessor'),
        ([(0, 1), (1000000, 1000000)], 'zero blast cutoff includes coordinate zero'),
        ([(0, 1), (1000000, 999999)], 'one-unit positive cutoff leaves zero intact'),
        ([(10, 1), (20, 9)], 'gap just outside blast radius'),
        ([(10, 1), (20, 10)], 'gap exactly equals blast radius'),
        ([(10, 1), (20, 11)], 'gap just inside blast radius'),
        ([(3, 3), (2, 2), (1, 1), (0, 1)], 'unsorted dense all-left destruction'),
        ([(90, 1), (0, 1), (30, 1), (60, 1)], 'unsorted sparse coordinates, no destruction'),
        ([(0, 1), (2, 1), (4, 1), (6, 100), (8, 100)],
         'optimal added beacon removes two suffix beacons, not just zero or one'),
        ([(8, 100), (0, 1), (6, 100), (4, 1), (2, 1)],
         'same two-suffix optimum in arbitrary input order'),
        ([(0, 1), (2, 2), (4, 1), (6, 2), (8, 1)],
         'destroyed beacons cannot activate and cause further destruction'),
        ([(0, 1), (10, 1), (20, 20), (30, 1), (40, 1)],
         'later harmless beacons rebuild the survivor chain after a reset'),
        ([(1000, 1), (2000, 1), (3000, 1000000), (4000, 1)],
         'index is not a coordinate; blast may pass left of all coordinates'),
        ([(0, 1), (5, 1), (10, 5), (15, 1), (20, 10), (25, 1)],
         'nested inclusive blast intervals and nonmonotone prefix survivor counts'),
    ]
    for data, reason in fixed:
        add(data, reason, 'boundary')
    rng = random.Random(1600607)
    added = 0
    while added < 120:
        n = rng.randint(1, 12)
        positions = rng.sample(range(50), n)
        data = [(a, rng.choice((1, 2, 3, 7, 20, 50, 1000000))) for a in positions]
        added += add(data, 'fixed-seed small activation/suffix interactions and unsorted rows')
    for i in range(16):
        n = 20 + i * 3
        positions = rng.sample(range(1000001), n)
        data = [(a, rng.choice((1, 999999, 1000000, rng.randint(1, 1000000))))
                for a in positions]
        add(data, 'fixed-seed sparse large coordinates, negative cutoffs and full-range powers')
    add([(a, 1) for a in range(100000)],
        'n=100000 dense unit-power chain; exactly 50000 destroyed', 'maxSize')
    add([(10 * i, 1) for i in range(100000, 0, -1)],
        'n=100000 reverse-sorted spaced beacons ending at a=1000000; none destroyed',
        'maxSize')
    add([(a, 1000000) for a in range(100000)],
        'n=100000 each activation destroys all left beacons; exactly n-1 destroyed',
        'maxSize')
    add([(1000000, 1)] + [(a, 1) for a in range(99999)],
        'n=100000 odd dense prefix plus detached endpoint; exactly 49999 destroyed',
        'maxSize')
    return cases


def review(pid, tests, samples):
    _require_pid(pid)
    errors = []
    for name, pair in [*tests, *samples]:
        try:
            expected = str(answer(pid, parse(pid, pair['input'])))
            if pair['output'].split() != [expected]:
                errors.append({'test': name, 'reason': 'independent oracle disagreement',
                               'expected': expected, 'actual': pair['output'].split()})
        except (ValueError, TypeError, KeyError) as exc:
            errors.append({'test': name, 'reason': str(exc)})
    return errors
