"""570C Replacement: exact recipe with literal-replacement and run-count cross checks."""
import itertools
import random
import re

IDS = ('570C',)
SEMANTICS = {
    '570C': ('n,m 1..300000 (literal "300 000" in the public statement, no flattened exponent); line 2 is s of exactly '
             'n characters from a-z and "."; then exactly m lines "x c" with 1<=x<=n and c one of a-z or ".". Each '
             'replacement turns the first ".." into ".", shortening one period run by one and lowering the number of '
             'adjacent ".." pairs by exactly one, so f(s) is that pair count. The unique output is m integers, one per '
             'line, each in 0..n-1. answer() updates the pair count locally around x; independently checked by literal '
             'first-occurrence replacement simulation, exhaustive single assignments, and a periods-minus-runs count.'),
}

MAX_N = 300000
ALPHABET = frozenset('abcdefghijklmnopqrstuvwxyz.')
INTEGER = re.compile(r'[1-9][0-9]*')


def _int(token, low, high, what):
    if not INTEGER.fullmatch(token):
        raise ValueError(f'non-canonical integer for {what}')
    value = int(token)
    if not low <= value <= high:
        raise ValueError(f'{what} out of range')
    return value


def parse(pid, text):
    if pid != '570C':
        raise ValueError('unknown problem: ' + pid)
    lines = text.strip().splitlines()
    if len(lines) < 3:
        raise ValueError('replacement line layout')
    header = lines[0].split()
    if len(header) != 2:
        raise ValueError('header arity')
    n = _int(header[0], 1, MAX_N, 'n')
    m = _int(header[1], 1, MAX_N, 'm')
    if len(lines) != m + 2:
        raise ValueError('replacement line layout')
    row = lines[1].split()
    if len(row) != 1 or len(row[0]) != n or not set(row[0]) <= ALPHABET:
        raise ValueError('string length/alphabet')
    queries = []
    for line in lines[2:]:
        parts = line.split()
        if len(parts) != 2 or len(parts[1]) != 1 or parts[1] not in ALPHABET:
            raise ValueError('query arity/symbol')
        queries.append((_int(parts[0], 1, n, 'x'), parts[1]))
    return row[0], tuple(queries)


def answer(pid, data):
    s, queries = data
    chars = list(s)
    n = len(chars)
    pairs = sum(chars[i] == chars[i + 1] == '.' for i in range(n - 1))
    result = []
    for x, c in queries:
        i = x - 1
        for j in (i - 1, i):
            if 0 <= j and j + 1 < n and chars[j] == chars[j + 1] == '.':
                pairs -= 1
        chars[i] = c
        for j in (i - 1, i):
            if 0 <= j and j + 1 < n and chars[j] == chars[j + 1] == '.':
                pairs += 1
        result.append(pairs)
    return result


def literal_f(s):
    operations = 0
    while '..' in s:
        s = s.replace('..', '.', 1)
        operations += 1
    return operations


def literal_answers(data):
    s, queries = data
    chars = list(s)
    out = []
    for x, c in queries:
        chars[x - 1] = c
        out.append(literal_f(''.join(chars)))
    return out


def run_answers(data):
    s, queries = data
    dot = [c == '.' for c in s]
    n = len(dot)
    periods = sum(dot)
    runs = sum(d and (i == 0 or not dot[i - 1]) for i, d in enumerate(dot))
    out = []
    for x, c in queries:
        i = x - 1
        new = c == '.'
        if new != dot[i]:
            neighbours = (i > 0 and dot[i - 1]) + (i + 1 < n and dot[i + 1])
            sign = 1 if new else -1
            periods += sign
            runs += sign * (1 - neighbours)
            dot[i] = new
        out.append(periods - runs)
    return out


def _render(s, queries):
    return f'{len(s)} {len(queries)}\n{s}\n' + ''.join(f'{x} {c}\n' for x, c in queries)


def extras(pid):
    rng = random.Random(570300)
    cases = []

    def add(s, queries, reason, category='adversarial'):
        text = _render(s, queries)
        data = parse(pid, text)
        values = answer(pid, data)
        cases.append({'input': text, 'output': ''.join(f'{v}\n' for v in values),
                      'reason': reason, 'category': category})

    add('.', [(1, '.')], 'minimum n=m=1 period kept')
    add('a', [(1, '.')], 'minimum n=m=1 letter to period', 'boundary')
    add('.', [(1, 'z')], 'minimum n=m=1 period to letter', 'boundary')
    add('.', [(1, '.'), (1, 'w'), (1, 'w'), (1, '.'), (1, '.'), (1, 'a'), (1, '.')],
        'n=1 must print every query and always 0 (prints-1 / single-line n=1 shortcuts)', 'boundary')
    add('z', [(1, c) for c in 'z.y..x.'], 'n=1 alternating classes with repeated no-op assignments', 'boundary')
    for s in ('..', '.a', 'a.', 'ab'):
        for x in (1, 2):
            for c in '.q':
                add(s, [(x, c)], 'n=2 every edge assignment', 'boundary')
    add('a.', [(1, '.'), (2, 'b'), (2, '.'), (1, 'c')], 'prepend to a run at its left edge must lengthen it')
    add('ab.', [(2, '.'), (1, '.'), (3, 'c'), (1, 'd')], 'repeated left-edge prepends to an existing run')
    add('.a...', [(2, '.'), (2, 'b'), (2, '.')], 'merge two runs (+2) and split at the same point (-2)')
    add('ba.', [(1, '.'), (1, 'c'), (2, '.')], 'x=1 must not look at s[n] via negative index')
    add('.ab', [(3, '.'), (3, 'c'), (2, '.'), (3, '.')], 'x=n must not read past the end')
    add('..b', [(3, '.'), (3, '.'), (1, '.'), (2, 'x'), (2, 'x')], 'assign period over period and letter over letter (no-op)')
    add('abc', [(3, '.'), (2, '.'), (1, '.'), (2, 'z')], 'grow a run from the right end then split it')
    add('.....', [(5, 'z')], 'official-style trailing removal from a 5-run')
    add('.....', [(3, 'a'), (3, '.'), (1, 'a'), (5, 'a'), (2, 'a'), (4, 'a')], 'split a run at middle and edges')
    add('a.b.c.d', [(2, 'x'), (4, '.'), (2, '.'), (6, '.'), (3, '.'), (5, '.')], 'isolated periods joined one by one')
    add('.' * 20, [(i, 'k') for i in range(2, 20, 2)], 'all-period run broken into single periods')
    add('ab' * 10, [(i, '.') for i in range(1, 21)], 'letters turned into one growing run left to right')
    add('ab' * 10, [(i, '.') for i in range(20, 0, -1)], 'letters turned into one growing run right to left')
    add('.' * 9 + 'a' + '.' * 9, [(10, '.'), (10, 'a'), (10, 'b'), (10, '.')], 'join two long runs through one cell')
    add('ab.cd..ef...g', [(3, 'h'), (6, 'i'), (11, 'j'), (11, '.'), (6, '.')], 'runs of length1,2,3 shrunk and regrown')
    add('.b..bz....', [(1, 'h'), (3, 'c'), (9, 'f'), (9, '.'), (5, '.'), (5, 'b')], 'sample 1 continued with reversals')

    for s in itertools.product('.a', repeat=3):
        s = ''.join(s)
        add(s, [(x, c) for x in (1, 2, 3) for c in '.b'], 'every n=3 period/letter string with all edge queries', 'boundary')

    for _ in range(70):
        n = rng.randint(1, 12)
        density = rng.choice((0.2, 0.5, 0.8, 0.95))
        s = ''.join('.' if rng.random() < density else rng.choice('abz') for _ in range(n))
        queries = [(rng.randint(1, n), '.' if rng.random() < density else rng.choice('abz'))
                   for _ in range(rng.randint(1, 12))]
        add(s, queries, 'fixed-seed small random string and assignments')
    for n, m in ((1000, 1000), (2500, 4000), (5000, 2000), (77, 5000)):
        s = ''.join(rng.choice('..x') for _ in range(n))
        add(s, [(rng.randint(1, n), rng.choice('..x')) for _ in range(m)], 'fixed-seed medium random')

    big = MAX_N
    add('.' * big, [(i, 'a' if i % 2 else '.') for i in range(1, big + 1)],
        'maximum n=m all periods, maximum answer 299999 then alternating removals', 'maxSize')
    add(''.join(rng.choice('.a') for _ in range(big)),
        [(rng.randint(1, big), rng.choice('.a')) for _ in range(big)], 'maximum n=m random half periods', 'maxSize')
    add('a' * big, [(i, '.') for i in range(1, big + 1)],
        'maximum n=m letters turned into one 300000 run, answer climbs to n-1', 'maxSize')
    add('.' * big, [((1, big)[i % 2], 'a.'[(i // 2) % 2]) for i in range(big)],
        'maximum n=m toggling both string ends only', 'maxSize')
    add('.', [(1, '.a'[i % 2]) for i in range(big)], 'minimum n=1 with maximum m=300000', 'maxSize')
    add('.' * (big - 1) + 'q', [(big, '.')], 'maximum n=300000 with m=1 last-position period', 'maxSize')
    return cases


def review(pid, tests, samples):
    failures = []
    for name, pair in [*tests, *samples]:
        try:
            data = parse(pid, pair['input'])
            expected = [str(v) for v in answer(pid, data)]
            if len(pair['output'].strip().splitlines()) != len(expected):
                raise ValueError('output line count differs from m')
            if pair['output'].split() != expected:
                raise ValueError('output differs from independent oracle')
        except (ValueError, AssertionError) as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures


def brute_checks():
    checked = 0
    for n in range(1, 7):
        for s in itertools.product('.ab', repeat=n):
            s = ''.join(s)
            for x in range(1, n + 1):
                for c in '.ab':
                    data = (s, ((x, c),))
                    expected = literal_answers(data)
                    assert answer('570C', data) == expected == run_answers(data)
                    checked += 1
    rng = random.Random(5703)
    for _ in range(600):
        n = rng.randint(1, 15)
        s = ''.join(rng.choice('..ab') for _ in range(n))
        data = (s, tuple((rng.randint(1, n), rng.choice('..ab')) for _ in range(rng.randint(1, 15))))
        expected = literal_answers(data)
        assert answer('570C', data) == expected == run_answers(data)
        checked += len(expected)
    return {'570C': checked}
