"""Source-attested deterministic scheduling recipe for 730G; not qualification."""
from bisect import insort
import itertools
import random
import re


IDS = ('730G',)
SEMANTICS = {
    '730G': 'Original English statement: 1<=n<=200; each of n request lines '
            'has 1<=s<=10^9, 1<=d<=5*10^6. Process in input order. Use s '
            'if all d days are free, otherwise the smallest positive free '
            'start (possibly before s). Print the unique inclusive start/end '
            'for each request. Sorted half-open occupied intervals give an '
            'O(n^2) exact oracle; independent exhaustive day-set simulation '
            'cross-checks small schedules. Public HTML attestation and exact '
            'exponent correction proposal are in recipe-reports/730G.json.'
}


def _check_pid(pid):
    if pid not in IDS:
        raise ValueError('unsupported problem: ' + str(pid))


def _integers(line, arity):
    tokens = line.split()
    if (len(tokens) != arity
            or any(not re.fullmatch(r'[+-]?[0-9]+', token) for token in tokens)):
        raise ValueError('integer line arity/lexical form')
    return tuple(map(int, tokens))


def parse(pid, text):
    _check_pid(pid)
    lines = text.splitlines()
    if not lines:
        raise ValueError('missing request count')
    n, = _integers(lines[0], 1)
    if not 1 <= n <= 200 or len(lines) != n + 1:
        raise ValueError('request count/range/line layout')
    requests = tuple(_integers(line, 2) for line in lines[1:])
    if not all(1 <= s <= 10**9 and 1 <= d <= 5 * 10**6 for s, d in requests):
        raise ValueError('start/duration range')
    return requests


def answer(pid, data):
    _check_pid(pid)
    occupied = []
    result = []
    for preferred, duration in data:
        start = preferred
        if any(left < start + duration and start < right
               for left, right in occupied):
            start = 1
            for left, right in occupied:
                if left - start >= duration:
                    break
                start = max(start, right)
        finish = start + duration
        insort(occupied, (start, finish))
        result.extend((start, finish - 1))
    return result


def _day_brute(requests):
    occupied = set()
    result = []
    for preferred, duration in requests:
        start = preferred
        if not occupied.isdisjoint(range(start, start + duration)):
            start = 1
            while not occupied.isdisjoint(range(start, start + duration)):
                start += 1
        occupied.update(range(start, start + duration))
        result.extend((start, start + duration - 1))
    return result


def brute_checks():
    checked = 0
    choices = tuple(itertools.product(range(1, 5), range(1, 4)))
    for n in range(1, 5):
        for requests in itertools.product(choices, repeat=n):
            if answer('730G', requests) != _day_brute(requests):
                raise AssertionError(('exhaustive schedule disagreement', requests))
            checked += 1
    rng = random.Random(730_1600)
    for _ in range(500):
        requests = tuple((rng.randint(1, 40), rng.randint(1, 8))
                         for _ in range(rng.randint(1, 12)))
        if answer('730G', requests) != _day_brute(requests):
            raise AssertionError(('random schedule disagreement', requests))
        checked += 1
    return {'730G': checked}


def _input(requests):
    return str(len(requests)) + '\n' + ''.join(f'{s} {d}\n' for s, d in requests)


def _output(tokens):
    return ''.join(f'{tokens[i]} {tokens[i + 1]}\n'
                   for i in range(0, len(tokens), 2))


def extras(pid):
    _check_pid(pid)
    tests, seen = [], set()

    def add(requests, reason, category='adversarial'):
        text = _input(requests)
        if text not in seen:
            seen.add(text)
            tests.append({'input': text, 'output': _output(answer(pid, requests)),
                          'reason': reason, 'category': category})

    cases = [
        ([(10, 1)], 'Preferred start wins even with a free earlier day; sequential-only mutant'),
        ([(10, 3), (9, 2)], 'Preferred overlap must restart search at day one'),
        ([(1, 2), (10, 2), (10, 3)], 'Interior gap beats tail; prefix-or-tail-only mutant'),
        ([(2, 1), (10, 1), (2, 8)], 'Gap length is a difference, not a sum; selected 21708503 predicate'),
        ([(1, 3), (2, 2)], 'Fallback must recompute finish; selected 32760690 stale-end defect'),
        ([(5, 2), (1, 2), (5, 2)], 'Exact-fit interior gap is legal'),
        ([(5, 2), (1, 2), (5, 3)], 'One-too-short interior gap must be skipped'),
        ([(5, 2), (1, 1), (5, 2)], 'First free block need not fill its whole gap'),
        ([(10, 2), (12, 1)], 'Touching half-open intervals do not conflict'),
        ([(10, 2), (11, 1)], 'Inclusive last occupied day does conflict'),
        ([(5, 2), (4, 4)], 'Preferred interval contains a whole occupied interval'),
        ([(5, 6), (7, 1)], 'Preferred interval is contained inside an occupied interval'),
        ([(1, 3), (1, 2)], 'No prefix or interior gap; extend unbounded tail'),
        ([(8, 2), (2, 2), (5, 2), (7, 2)], 'Input order differs from chronological order'),
        ([(20, 2), (1, 2), (20, 2), (3, 1)], 'Fallback occupies an earlier preferred start'),
        ([(10, 2), (10, 2), (10, 2), (10, 2)], 'Repeated fallback grows a contiguous prefix'),
        ([(5, 1), (10, 1), (7, 1)], 'Free preferred time wins over every available gap'),
        ([(1, 1), (3, 1), (5, 1), (1, 2)], 'Skip multiple one-day gaps for a two-day request'),
        ([(1, 1), (4, 1), (7, 1), (4, 2), (7, 2)], 'Fill earliest of equal-length gaps in order'),
        ([(4, 2), (2, 2), (6, 2), (4, 1)], 'Adjacent reservations have no artificial free day'),
    ]
    for requests, reason in cases:
        add(requests, reason)
    for s in (1, 2, 10**9 - 1, 10**9):
        for d in (1, 2, 5 * 10**6 - 1, 5 * 10**6):
            add([(s, d)], f'Single request boundary s={s}, d={d}', 'boundary')
    for gap in range(1, 13):
        for duration in (gap, gap + 1):
            add([(1, 2), (gap + 3, 2), (gap + 3, duration)],
                f'Interior gap={gap} with fallback duration={duration}')

    add([(1, 5 * 10**6)] * 200,
        'Maximum n and duration, contiguous repairs reach day 10^9', 'maxSize')
    add([(10**9, 5 * 10**6)] * 200,
        'Maximum n, s, d; high preferred repair and 199 prefix fallbacks', 'maxSize')
    add([(1 + i * 5 * 10**6, 5 * 10**6) for i in reversed(range(200))],
        'Maximum n,d with reverse chronological adjacent intervals', 'maxSize')
    add([(10**9 - 2 * i, 1) for i in range(200)],
        'Maximum n, descending singleton reservations near maximum start', 'maxSize')
    add([(i + 1, 1) for i in range(200)],
        'Maximum n, consecutive singleton preferred repairs', 'maxSize')
    add([(1, 1)] * 200,
        'Maximum n, repeated minimum start/duration must keep extending tail', 'maxSize')
    add([(i * 3 + 1, 1) for i in range(100)] + [(1, 2)] * 100,
        'Maximum n, 100 exact-fit interior gaps consumed before tail', 'maxSize')
    add([(10**9, 5 * 10**6), (10**9 - 1, 5 * 10**6)],
        'Maximum duration crossing preferred repair; relocate below s', 'boundary')

    rng = random.Random(730_2026)
    for i in range(60):
        requests = [(rng.randint(1, 60), rng.randint(1, 12))
                    for _ in range(rng.randint(2, 20))]
        add(requests, f'Fixed-seed small request-order/overlap schedule {i}')
    i = 0
    while len(tests) < 160:
        choices = (1, 2, 5 * 10**6 - 1, 5 * 10**6)
        requests = [(rng.choice((1, rng.randint(1, 10**9), 10**9)),
                     rng.choice(choices)) for _ in range(rng.randint(2, 40))]
        add(requests, f'Fixed-seed large-coordinate gap/end boundary schedule {i}')
        i += 1
    return tests


def review(pid, tests, samples):
    _check_pid(pid)
    failures = []
    for name, pair in [*tests, *samples]:
        try:
            data = parse(pid, pair['input'])
            lines = pair['output'].splitlines()
            if len(lines) != len(data):
                raise ValueError('output line count differs from request count')
            for line in lines:
                _integers(line, 2)
            if pair['output'].split() != list(map(str, answer(pid, data))):
                raise ValueError('oracle output differs from supplied bytes')
        except (ValueError, IndexError, KeyError, TypeError) as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
