"""793B: exact two-turn reachability and bounded direction-state cross-checks."""
from collections import deque
import itertools
import random
import re


IDS = ('793B',)
SEMANTICS = {
    '793B': 'Public English statement: 1<=n,m<=1000; exactly n rows of m ./*/S/T characters, one S and one T. Orthogonal movement, free initial direction, at most two direction changes. Unique YES/NO. Enumerate clear HVH and VHV paths including zero-length end segments in O(n*m); independent direction/turn-state BFS checks all obstacle masks and ordered endpoints on grids through 3x3 plus fixed-seed small grids.'
}


def _require_pid(pid):
    if pid not in IDS:
        raise ValueError('unsupported problem: ' + str(pid))


def parse(pid, text):
    _require_pid(pid)
    lines = text.replace('\r\n', '\n').split('\n')
    if lines[-1] == '':
        lines.pop()
    if not lines or not re.fullmatch(r'[ \t]*[0-9]+[ \t]+[0-9]+[ \t]*', lines[0]):
        raise ValueError('first line must contain exactly n and m')
    n, m = map(int, lines[0].split())
    if not (1 <= n <= 1000 and 1 <= m <= 1000):
        raise ValueError('grid dimensions outside 1..1000')
    rows = tuple(lines[1:])
    if len(rows) != n or any(len(row) != m for row in rows):
        raise ValueError('grid must have exactly n separate rows of m characters')
    if any(set(row) - set('.*ST') for row in rows):
        raise ValueError('invalid grid character')
    if sum(row.count('S') for row in rows) != 1 or sum(row.count('T') for row in rows) != 1:
        raise ValueError('grid must contain exactly one S and one T')
    return rows


def _endpoints(rows):
    return tuple(next((r, row.index(ch)) for r, row in enumerate(rows) if ch in row)
                 for ch in 'ST')


def answer(pid, data):
    _require_pid(pid)
    rows = data
    n, m = len(rows), len(rows[0])
    (sr, sc), (tr, tc) = _endpoints(rows)

    def horizontal(r, c):
        left = right = c
        while left > 0 and rows[r][left - 1] != '*':
            left -= 1
        while right + 1 < m and rows[r][right + 1] != '*':
            right += 1
        return left, right

    def vertical(r, c):
        up = down = r
        while up > 0 and rows[up - 1][c] != '*':
            up -= 1
        while down + 1 < n and rows[down + 1][c] != '*':
            down += 1
        return up, down

    sl, sh = horizontal(sr, sc)
    tl, th = horizontal(tr, tc)
    for c in range(max(sl, tl), min(sh, th) + 1):
        if all(rows[r][c] != '*' for r in range(min(sr, tr), max(sr, tr) + 1)):
            return 'YES'
    sl, sh = vertical(sr, sc)
    tl, th = vertical(tr, tc)
    for r in range(max(sl, tl), min(sh, th) + 1):
        if all(rows[r][c] != '*' for c in range(min(sc, tc), max(sc, tc) + 1)):
            return 'YES'
    return 'NO'


def _brute(rows):
    n, m = len(rows), len(rows[0])
    start, target = _endpoints(rows)
    initial = (*start, -1, 0)
    queue = deque([initial])
    seen = {initial}
    while queue:
        r, c, previous, turns = queue.popleft()
        if (r, c) == target:
            return 'YES'
        for direction, (dr, dc) in enumerate(((1, 0), (-1, 0), (0, 1), (0, -1))):
            nr, nc = r + dr, c + dc
            used = turns + int(previous != -1 and previous != direction)
            state = (nr, nc, direction, used)
            if (used <= 2 and 0 <= nr < n and 0 <= nc < m
                    and rows[nr][nc] != '*' and state not in seen):
                seen.add(state)
                queue.append(state)
    return 'NO'


def _board(n, m, start, target, obstacles):
    cells = ['*' if i in obstacles else '.' for i in range(n * m)]
    cells[start], cells[target] = 'S', 'T'
    return tuple(''.join(cells[r * m:(r + 1) * m]) for r in range(n))


def brute_checks():
    count = 0
    for n, m in ((1, 2), (2, 1), (1, 3), (3, 1), (2, 2), (2, 3), (3, 2), (3, 3)):
        for start, target in itertools.permutations(range(n * m), 2):
            others = [i for i in range(n * m) if i not in (start, target)]
            for mask in range(1 << len(others)):
                rows = _board(n, m, start, target,
                              {v for j, v in enumerate(others) if mask & (1 << j)})
                assert answer('793B', rows) == _brute(rows), rows
                count += 1
    rng = random.Random(7931600)
    for _ in range(500):
        n, m = rng.randint(1, 8), rng.randint(1, 8)
        if n * m == 1:
            m = 2
        start, target = rng.sample(range(n * m), 2)
        rows = _board(n, m, start, target,
                      {i for i in range(n * m) if rng.random() < rng.choice((0.15, 0.4, 0.7))})
        assert answer('793B', rows) == _brute(rows), rows
        count += 1
    return {'793B': count}


def extras(pid):
    _require_pid(pid)
    cases, inputs = [], set()

    def add(rows, reason, category='adversarial'):
        text = f'{len(rows)} {len(rows[0])}\n' + '\n'.join(rows) + '\n'
        if text not in inputs:
            data = parse(pid, text)
            inputs.add(text)
            cases.append({'input': text, 'output': answer(pid, data) + '\n',
                          'reason': reason, 'category': category})

    fixed = [
        (('ST',), 'minimum legal area; free initial direction', 'boundary'),
        (('S', 'T'), 'minimum legal area; free initial direction', 'boundary'),
        (('S*T',), 'collinear endpoints separated by road works', 'boundary'),
        (('S', '*', 'T'), 'blocked single-axis grid', 'boundary'),
        (('S*', '.T'), 'exactly one turn; endpoint cells are traversable', 'boundary'),
        (('S**', '...', '**T'), 'only VHV succeeds; checking HVH alone is incomplete', 'adversarial'),
        (('S.*', '*.*', '*.T'), 'only HVH succeeds; checking VHV alone is incomplete', 'adversarial'),
        (('S**', '...', '**.', 'T..'), 'connected corridor requires three turns, not two', 'adversarial'),
        (('*S.', '...', '.T*'), 'obstacles outside the used segment must not block whole rows/columns', 'adversarial'),
        (('S..', '...', '..T'), 'open grid has many paths but one unique decision token', 'boundary'),
        (('..S..', '****.', 'T....', '****.', '.....'), 'two turns via a pivot outside the endpoint rectangle', 'adversarial'),
        (('S....', '****.', '.....', '.****', '..T..'), 'connected serpentine sample requires four turns', 'adversarial'),
    ]
    for rows, reason, category in fixed:
        for transpose in (False, True):
            oriented = tuple(''.join(col) for col in zip(*rows)) if transpose else rows
            oriented_reason = reason.translate(str.maketrans('HV', 'VH')) if transpose else reason
            for flip_rows, flip_columns in itertools.product((False, True), repeat=2):
                transformed = oriented[::-1] if flip_rows else oriented
                transformed = tuple(row[::-1] for row in transformed) if flip_columns else transformed
                add(transformed, oriented_reason + '; reflected/transposed orientation', category)

    add(('S' + '.' * 998 + 'T',), 'maximum width in one row; long zero-turn ray', 'boundary')
    add(tuple('S' if r == 0 else 'T' if r == 999 else '.' for r in range(1000)),
        'maximum height in one column; long zero-turn ray', 'boundary')
    add(('S' + '.' * 498 + '*' + '.' * 498 + 'T',),
        'maximum-width skinny blocked ray', 'boundary')
    add(tuple('S' if r == 0 else 'T' if r == 999 else '*' if r == 500 else '.'
              for r in range(1000)), 'maximum-height skinny blocked ray', 'boundary')

    rng = random.Random(1600793)
    while len(cases) < 156:
        n, m = rng.randint(1, 12), rng.randint(1, 12)
        if n * m == 1:
            m = 2
        start, target = rng.sample(range(n * m), 2)
        density = rng.choice((0.0, 0.15, 0.35, 0.6, 0.85))
        rows = _board(n, m, start, target, {i for i in range(n * m) if rng.random() < density})
        add(rows, 'fixed-seed small grids: varied obstacle density, interior/border endpoints and alternate arrival directions')

    n = 1000
    add(('S' + '.' * (n - 1),) + ('.' * n,) * (n - 2) + ('.' * (n - 1) + 'T',),
        'full 1000x1000 open grid; one-turn route', 'maxSize')
    rows = ['.' * n for _ in range(n)]
    rows[0], rows[500], rows[-1] = 'S' + '.' * (n - 1), '*' * n, '.' * (n - 1) + 'T'
    add(tuple(rows), 'full 1000x1000 disconnected by a complete obstacle row', 'maxSize')
    rows = ['*' * (n - 1) + '.' for _ in range(n)]
    rows[0], rows[-1] = 'S' + '.' * (n - 1), 'T' + '.' * (n - 1)
    add(tuple(rows), 'full 1000x1000 forced HVH perimeter route with exactly two turns', 'maxSize')
    rows = ['*' * n for _ in range(n)]
    rows[0] = 'S' + '.' * (n - 1)
    for r in range(1, 500):
        rows[r] = '*' * (n - 1) + '.'
    rows[500] = '.' * n
    for r in range(501, n):
        rows[r] = '.' + '*' * (n - 1)
    rows[-1] = 'T' + '*' * (n - 1)
    add(tuple(rows), 'full 1000x1000 connected one-cell corridor requires three turns', 'maxSize')
    return cases


def review(pid, tests, samples):
    _require_pid(pid)
    errors = []
    for name, pair in [*tests, *samples]:
        try:
            expected = answer(pid, parse(pid, pair['input']))
            if pair['output'].split() != [expected]:
                raise ValueError('output differs from exact two-turn reachability oracle: ' + expected)
        except (ValueError, AssertionError) as exc:
            errors.append({'test': name, 'reason': str(exc)})
    return errors
