"""446A: one integer replacement in a contiguous strictly increasing segment."""
import itertools
import random
import re


IDS = ('446A',)
SEMANTICS = {
    '446A': 'Original English HTML attests n=1..10^5 and ai=1..10^9 on two '
            'lines. Replace at most one element by ANY integer, not necessarily '
            'inside the input range. Output is the unique maximum contiguous '
            'strictly increasing length. O(n) left/right runs join across a '
            'replacement only when its two neighbors have an integer gap >=2; '
            'small exhaustive replacement enumeration independently checks it.'
}


def _pid(pid):
    if pid not in IDS:
        raise ValueError('unsupported problem id')


def parse(pid, text):
    _pid(pid)
    if not isinstance(text, str):
        raise ValueError('input must be text')
    lines = text.splitlines()
    while lines and not lines[-1].strip():
        lines.pop()
    if len(lines) != 2:
        raise ValueError('expected n line and one array line')
    header, tokens = lines[0].split(), lines[1].split()
    if len(header) != 1 or not re.fullmatch(r'[0-9]+', header[0]):
        raise ValueError('expected one decimal n')
    n = int(header[0])
    if not 1 <= n <= 100000 or len(tokens) != n:
        raise ValueError('n range or array arity')
    if any(not re.fullmatch(r'[0-9]+', token) for token in tokens):
        raise ValueError('expected decimal array integers')
    values = tuple(map(int, tokens))
    if any(not 1 <= value <= 1000000000 for value in values):
        raise ValueError('array value range')
    return values


def answer(pid, data):
    _pid(pid)
    n = len(data)
    left, right = [1] * n, [1] * n
    for i in range(1, n):
        if data[i - 1] < data[i]:
            left[i] = left[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if data[i] < data[i + 1]:
            right[i] = right[i + 1] + 1
    best = max(left)
    for i in range(n):
        if i:
            best = max(best, left[i - 1] + 1)
        if i + 1 < n:
            best = max(best, right[i + 1] + 1)
        if 0 < i < n - 1 and data[i + 1] - data[i - 1] >= 2:
            best = max(best, left[i - 1] + 1 + right[i + 1])
    return best


def brute(data):
    """Enumerate replacements, including values outside the input bounds.

    An integer between retained neighbors can be chosen next to a neighbor;
    an endpoint can likewise use the smallest/largest value minus/plus one.
    Thus these representatives cover all feasible replacement orderings.
    """
    candidates = {value + delta for value in data for delta in (-1, 0, 1)}
    best = 1
    for position in range(len(data)):
        for replacement in candidates:
            changed = list(data)
            changed[position] = replacement
            length = 1
            for i, value in enumerate(changed):
                length = length + 1 if i and changed[i - 1] < value else 1
                best = max(best, length)
    return best


def extras(pid):
    _pid(pid)
    rng = random.Random(4461600)
    cases, seen = [], set()

    def add(values, reason, category='adversarial'):
        values = tuple(values)
        if values in seen:
            return
        seen.add(values)
        text = f'{len(values)}\n' + ' '.join(map(str, values)) + '\n'
        cases.append({'input': text, 'output': f'{answer(pid, values)}\n',
                      'reason': reason, 'category': category})

    for values in ([1], [1000000000], [1, 1], [1, 2], [2, 1],
                   [1000000000, 1000000000], [1, 1000000000]):
        add(values, 'minimum lengths and input value bounds', 'boundary')
    add([1, 1, 2, 3], 'first replacement may be zero', 'boundary')
    add([999999997, 999999998, 1000000000, 1000000000],
        'last replacement may exceed 10^9', 'boundary')
    for values in ([1, 2, 2, 3], [1, 2, 3, 3, 4], [1, 2, 2, 3, 4],
                   [1, 2, 3, 3, 4, 5], [1, 3, 3, 4, 5],
                   [2, 3, 5, 5, 6, 7], [1, 2, 100, 3, 4],
                   [1, 2, 100, 4, 5], [1, 3, 2, 3, 4], [1, 3, 2, 5, 6],
                   [4, 3, 2, 1], [1, 2, 1, 2, 1, 2], [5, 5, 5, 5, 5],
                   [5, 1, 2, 3], [1, 2, 3, 1], [7, 2, 3, 1, 5, 6]):
        add(values, 'integer bridge gap, strict equality, endpoints or multiple breaks')
    for n in (3, 5, 9, 17):
        base = [3 * i + 3 for i in range(n)]
        for position in (0, n // 2, n - 1):
            values = base.copy()
            values[position] = 1000000000
            add(values, 'isolated high outlier at first/middle/last position')
            values[position] = 1
            add(values, 'isolated low outlier at first/middle/last position')
    add(range(1, 100001), 'maximum n; no edit needed', 'maxSize')
    add([1000000000] * 100000, 'maximum n; strict equality', 'maxSize')
    add(range(100000, 0, -1), 'maximum n; many unrepairable breaks', 'maxSize')
    values = [2 * i + 1 for i in range(100000)]
    values[50000] = 1000000000
    add(values, 'maximum n; one interior high outlier with legal integer bridge', 'maxSize')
    values = list(range(1, 100001))
    values[50000] = values[49999]
    add(values, 'maximum n; consecutive-neighbor gap forbids full repair', 'maxSize')
    palette = (1, 2, 3, 4, 5, 999999998, 999999999, 1000000000)
    while len(cases) < 160:
        n = rng.randint(3, 12)
        if len(cases) % 3 == 0:
            values = sorted(rng.sample(range(1, 101), n))
            for _ in range(rng.randint(1, 3)):
                values[rng.randrange(n)] = rng.choice(palette)
        elif len(cases) % 3 == 1:
            values = [rng.choice(palette) for _ in range(n)]
        else:
            values = [rng.randint(1, 25) for _ in range(n)]
        add(values, 'fixed-seed small strict runs, duplicates, gaps and input extremes')
    return cases


def review(pid, tests, samples):
    _pid(pid)
    errors = []
    for name, pair in [*tests, *samples]:
        try:
            expected = answer(pid, parse(pid, pair['input']))
            lines = pair['output'].splitlines()
            while lines and not lines[-1].strip():
                lines.pop()
            if len(lines) != 1 or len(lines[0].split()) != 1:
                raise ValueError('expected one output integer on one line')
            token = lines[0].strip()
            if not re.fullmatch(r'[0-9]+', token) or int(token) != expected:
                raise ValueError(f'output differs from oracle; expected {expected}')
        except (ValueError, KeyError, TypeError, AttributeError) as exc:
            errors.append({'test': name, 'reason': str(exc)})
    return errors


def brute_checks():
    count = 0
    for n in range(1, 7):
        for data in itertools.product(range(1, 5), repeat=n):
            expected, actual = brute(data), answer('446A', data)
            if actual != expected:
                raise AssertionError((data, actual, expected))
            count += 1
    rng = random.Random(4461601)
    for _ in range(400):
        data = tuple(rng.choice((1, 2, 3, 4, 10, 99, 1000000000))
                     for _ in range(rng.randint(1, 10)))
        expected, actual = brute(data), answer('446A', data)
        if actual != expected:
            raise AssertionError((data, actual, expected))
        count += 1
    return {'446A': count}
