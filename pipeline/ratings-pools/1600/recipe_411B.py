"""Source-attested processor simulation with a separate pairwise reference."""
import itertools
import random
import re


IDS = ('411B',)
SEMANTICS = {
    '411B': 'Original English 411/B: 1<=n,m,k<=100; exactly n rows of m '
            'commands in 0..k. Zero is idle. Only live cores participate in '
            'each simultaneous cycle; collisions permanently lock their cell '
            'and all writers, and later writes to locked cells lock the core. '
            'Output is uniquely n first-lock times, one per line, or 0 for '
            'survivors. O(m*(n+k)) counts plus persistent cell locks are '
            'cross-checked by frozen-active-set pairwise simulation.'
}


def _check_pid(pid):
    if pid != '411B':
        raise ValueError('unsupported problem: ' + str(pid))


def parse(pid, text):
    _check_pid(pid)
    lines = [line.split() for line in text.splitlines()]
    if not lines or len(lines[0]) != 3:
        raise ValueError('expected n m k on the first line')
    if any(not re.fullmatch(r'[0-9]+', token) for row in lines for token in row):
        raise ValueError('commands and dimensions must be decimal integers')
    n, m, k = map(int, lines[0])
    if not all(1 <= x <= 100 for x in (n, m, k)):
        raise ValueError('n, m, k must be in 1..100')
    if len(lines) != n + 1 or any(len(row) != m for row in lines[1:]):
        raise ValueError('expected exactly n instruction rows of m commands')
    rows = tuple(tuple(map(int, row)) for row in lines[1:])
    if any(not 0 <= value <= k for row in rows for value in row):
        raise ValueError('command must be in 0..k')
    return n, m, k, rows


def answer(pid, data):
    _check_pid(pid)
    n, m, k, rows = data
    times = [0] * n
    locked = [False] * (k + 1)
    for cycle in range(m):
        counts = [0] * (k + 1)
        for core in range(n):
            cell = rows[core][cycle]
            if times[core] == 0 and cell != 0:
                counts[cell] += 1
        for cell in range(1, k + 1):
            if counts[cell] > 1:
                locked[cell] = True
        for core in range(n):
            cell = rows[core][cycle]
            if times[core] == 0 and cell != 0 and locked[cell]:
                times[core] = cycle + 1
    return times


def _pairwise(data):
    n, m, _, rows = data
    live = set(range(n))
    blocked = set()
    result = [0] * n
    for cycle in range(m):
        writers = {core: rows[core][cycle] for core in sorted(live)
                   if rows[core][cycle] != 0}
        dying = {core for core, cell in writers.items() if cell in blocked}
        newly_blocked = set()
        for left, right in itertools.combinations(writers, 2):
            if writers[left] == writers[right]:
                dying.update((left, right))
                newly_blocked.add(writers[left])
        for core in dying:
            result[core] = cycle + 1
        live.difference_update(dying)
        blocked.update(newly_blocked)
    return result


def _text(k, rows):
    return f'{len(rows)} {len(rows[0])} {k}\n' + ''.join(
        ' '.join(map(str, row)) + '\n' for row in rows)


def extras(pid):
    _check_pid(pid)
    cases = []
    seen = set()

    def add(k, rows, reason, category='adversarial'):
        text = _text(k, rows)
        if text in seen:
            return
        data = parse(pid, text)
        seen.add(text)
        cases.append({'input': text,
                      'output': ''.join(f'{value}\n' for value in answer(pid, data)),
                      'reason': reason, 'category': category})

    fixed = [
        (1, ((0,),), 'minimum idle processor'),
        (1, ((1,),), 'one writer cannot collide with itself'),
        (100, ((100,),), 'highest numbered cell with minimum n and m'),
        (1, ((0,), (0,)), 'shared zero is idle, not a memory conflict'),
        (1, ((1,), (1,)), 'two writers collide on the first cycle'),
        (3, ((1,), (2,), (1,)), 'nonadjacent cores must collide'),
        (3, ((3,), (3,), (3,)), 'all writers in a three-core conflict lock'),
        (3, ((1,), (2,), (3,)), 'distinct nonzero commands do not collide'),
        (2, ((1, 2), (1, 2), (2, 2)), 'dead cores cannot create later conflicts'),
        (2, ((1, 2), (1, 2), (0, 1)), 'first-lock times cannot be overwritten'),
        (2, ((1, 0, 0), (1, 0, 0), (0, 0, 1)),
         'a lone survivor writing a permanently locked cell also locks'),
        (2, ((1, 2), (0, 1), (0, 0)), 'single writes do not reserve cells across cycles'),
        (3, ((1, 1, 1), (1, 2, 2), (0, 1, 2), (0, 0, 2)),
         'locked cores ignore later destinations during a cascade'),
        (100, ((100, 0), (100, 100), (0, 100)),
         'k differs from m; include cell k and permanent-lock propagation'),
        (2, ((0, 0, 0), (1, 2, 1)), 'idle core survives another core reusing cells'),
        (2, ((1, 0, 2), (1, 0, 2), (0, 0, 2)),
         'ignored future writes must not poison an unused cell'),
        (3, ((1, 0, 0), (2, 1, 0), (2, 3, 1)),
         'dead later instructions do not collide with a live core'),
        (4, ((1, 2), (1, 2), (3, 4), (3, 4)),
         'two disjoint simultaneous conflicts'),
    ]
    for k, rows, reason in fixed:
        add(k, rows, reason, 'boundary')
        add(k, tuple(reversed(rows)), 'row-order reversal: ' + reason)

    for delay in range(1, 13):
        row = [0] * (delay + 2)
        row[delay - 1] = 1
        survivor = [0] * len(row)
        survivor[-1] = 1
        add(1, (row, row, survivor), 'delayed collision then lone locked-cell access')
    for k in range(1, 11):
        add(k, ((k, 0, k), (0, k, 0), (k, k, k), (0, 0, k)),
            'permanent locks and immutable first-lock times at the highest cell')

    add(100, [[0] * 100 for _ in range(100)],
        'all dimensions maximum; all commands idle', 'maxSize')
    add(100, [[(core + cycle) % 100 + 1 for cycle in range(100)]
              for core in range(100)],
        'all dimensions maximum; every cycle is a cell permutation', 'maxSize')
    add(100, [[100] * 100 for _ in range(100)],
        'all dimensions maximum; all cores collide at cell 100', 'maxSize')
    add(100, [[0] * 99 + [100] for _ in range(100)],
        'all dimensions maximum; first collision on cycle 100', 'maxSize')
    cascade = [[0] * 100 for _ in range(100)]
    cascade[0][0] = cascade[1][0] = 100
    for core in range(2, 100):
        cascade[core][core] = 100
    add(100, cascade, 'all dimensions maximum; staggered lone hits on one locked cell', 'maxSize')
    add(1, [[1] * 100], 'maximum cycles; repeated lone writes never lock', 'boundary')
    add(100, [[core + 1] for core in range(100)],
        'maximum cores and cells, one cycle with distinct writers', 'boundary')

    rng = random.Random(4111600)
    while len(cases) < 160:
        n, m, k = rng.randint(1, 8), rng.randint(1, 12), rng.randint(1, 8)
        mode = rng.randrange(3)
        rows = [[0 if rng.random() < (0.65 if mode else 0.15)
                 else rng.randint(1, k) for _ in range(m)] for _ in range(n)]
        if mode == 2:
            for row in rows:
                delay = rng.randrange(m)
                row[:delay] = [0] * delay
        add(k, rows, 'fixed-seed small dense/sparse simultaneous command schedules')
    return cases


def review(pid, tests, samples):
    _check_pid(pid)
    errors = []
    for name, pair in [*tests, *samples]:
        try:
            data = parse(pid, pair['input'])
            expected = answer(pid, data)
            output = [line.split() for line in pair['output'].splitlines()]
            if len(output) != data[0] or any(len(row) != 1 for row in output):
                raise ValueError('expected one lock time per core, one per line')
            if any(not re.fullmatch(r'[0-9]+', row[0]) for row in output):
                raise ValueError('lock times must be decimal integers')
            actual = [int(row[0]) for row in output]
            if actual != expected:
                raise ValueError(f'output differs from oracle: expected {expected}, got {actual}')
        except (ValueError, KeyError, TypeError) as exc:
            errors.append({'test': name, 'reason': str(exc)})
    return errors


def brute_checks():
    count = 0
    dimensions = ((1, 1, 1), (1, 3, 2), (2, 1, 3), (2, 2, 2),
                  (2, 3, 2), (3, 2, 2), (3, 3, 1), (3, 2, 3), (4, 2, 1))
    for n, m, k in dimensions:
        for flat in itertools.product(range(k + 1), repeat=n * m):
            rows = tuple(flat[start:start + m] for start in range(0, n * m, m))
            data = n, m, k, rows
            assert answer('411B', data) == _pairwise(data), data
            count += 1
    rng = random.Random(4112026)
    for _ in range(500):
        n, m, k = rng.randint(1, 8), rng.randint(1, 9), rng.randint(1, 6)
        rows = tuple(tuple(rng.randrange(k + 1) for _ in range(m)) for _ in range(n))
        data = n, m, k, rows
        assert answer('411B', data) == _pairwise(data), data
        count += 1
    for case in extras('411B'):
        data = parse('411B', case['input'])
        expected = _pairwise(data)
        assert [int(x) for x in case['output'].split()] == expected, data
        count += 1
    return {'411B': count}
