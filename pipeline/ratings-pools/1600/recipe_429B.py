"""Rating-1600 recipe for 429B Working out (two crossing monotone paths)."""
import itertools
import random
import re


IDS = ('429B',)
MAX_DIM = 1000
MAX_VALUE = 10**5
SEMANTICS = {
    '429B': 'First line n m (3<=n,m<=1000); then exactly n lines of m integers a[i][j], 0<=a[i][j]<=10^5 (public English statement shows 10<sup>5</sup>; pinned row flattened it to 105 and official test values 100000 confirm 10^5). '
            'Iahub walks (1,1)->(n,m) moving down/right, Iahubina walks (n,1)->(1,m) moving up/right; their paths share exactly one cell, which neither counts. '
            'Unique integer: maximum total of all other visited cells. The shared cell is necessarily interior (2<=i<=n-1, 2<=j<=m-1) and the paths cross it orthogonally, '
            'so answer = max over interior cells and both crossing orientations of four corner path DPs. '
            'Exhaustive enumeration of all path pairs with exactly one common cell cross-checks small grids; a flip-based second DP and reconstructed witness paths cross-check large ones.',
}
TOKEN = r'(?:0|[1-9][0-9]*)'
ROW = re.compile(TOKEN + r'(?: ' + TOKEN + r')*')


def _lines(text):
    body = text
    if body.endswith('\n'):
        body = body[:-1]
        if body.endswith('\r'):
            body = body[:-1]
    return re.split(r'\r?\n', body)


def parse(pid, text):
    if pid not in IDS:
        raise ValueError('unknown problem')
    lines = _lines(text)
    for index, line in enumerate(lines):
        if not ROW.fullmatch(line):
            raise ValueError(f'line {index + 1} is not single-space separated unsigned integers')
    header = lines[0].split(' ')
    if len(header) != 2:
        raise ValueError('first line must hold exactly n and m')
    n, m = int(header[0]), int(header[1])
    if not (3 <= n <= MAX_DIM and 3 <= m <= MAX_DIM):
        raise ValueError('n or m outside 3..1000')
    if len(lines) != n + 1:
        raise ValueError(f'expected {n} matrix lines, found {len(lines) - 1}')
    grid = []
    for index, line in enumerate(lines[1:], 2):
        row = [int(token) for token in line.split(' ')]
        if len(row) != m:
            raise ValueError(f'line {index} must hold exactly m={m} integers')
        if max(row) > MAX_VALUE:
            raise ValueError(f'line {index} has a value above 10^5')
        grid.append(row)
    return n, m, grid


def _tables(n, m, a):
    down_right = [[0] * (m + 2) for _ in range(n + 2)]
    to_end = [[0] * (m + 2) for _ in range(n + 2)]
    up_right = [[0] * (m + 2) for _ in range(n + 2)]
    to_top_right = [[0] * (m + 2) for _ in range(n + 2)]
    for i in range(1, n + 1):
        row, prev, cur = a[i - 1], down_right[i - 1], down_right[i]
        for j in range(1, m + 1):
            cur[j] = row[j - 1] + (prev[j] if prev[j] > cur[j - 1] else cur[j - 1])
    for i in range(n, 0, -1):
        row, nxt, cur = a[i - 1], to_end[i + 1], to_end[i]
        for j in range(m, 0, -1):
            cur[j] = row[j - 1] + (nxt[j] if nxt[j] > cur[j + 1] else cur[j + 1])
    for i in range(n, 0, -1):
        row, nxt, cur = a[i - 1], up_right[i + 1], up_right[i]
        for j in range(1, m + 1):
            cur[j] = row[j - 1] + (nxt[j] if nxt[j] > cur[j - 1] else cur[j - 1])
    for i in range(1, n + 1):
        row, prev, cur = a[i - 1], to_top_right[i - 1], to_top_right[i]
        for j in range(m, 0, -1):
            cur[j] = row[j - 1] + (prev[j] if prev[j] > cur[j + 1] else cur[j + 1])
    return down_right, to_end, up_right, to_top_right


def _best(n, m, a):
    p, q, r, s = _tables(n, m, a)
    best, where = -1, None
    for i in range(2, n):
        for j in range(2, m):
            vertical = p[i - 1][j] + q[i + 1][j] + r[i][j - 1] + s[i][j + 1]
            horizontal = p[i][j - 1] + q[i][j + 1] + r[i + 1][j] + s[i - 1][j]
            if vertical > best:
                best, where = vertical, (i, j, 'vertical')
            if horizontal > best:
                best, where = horizontal, (i, j, 'horizontal')
    return best, where, (p, q, r, s)


def answer(pid, data):
    n, m, a = data
    return _best(n, m, a)[0]


def _corner_dp(grid):
    rows, cols = len(grid), len(grid[0])
    table = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            up = table[i - 1][j] if i else None
            left = table[i][j - 1] if j else None
            options = [v for v in (up, left) if v is not None]
            table[i][j] = grid[i][j] + (max(options) if options else 0)
    return table


def flip_answer(data):
    n, m, a = data
    flip_rows = a[::-1]
    flip_cols = [row[::-1] for row in a]
    flip_both = [row[::-1] for row in a[::-1]]
    from_tl = _corner_dp(a)
    from_br = _corner_dp(flip_both)
    from_bl = _corner_dp(flip_rows)
    from_tr = _corner_dp(flip_cols)

    def tl(i, j):
        return from_tl[i][j]

    def br(i, j):
        return from_br[n - 1 - i][m - 1 - j]

    def bl(i, j):
        return from_bl[n - 1 - i][j]

    def tr(i, j):
        return from_tr[i][m - 1 - j]

    return max(max(tl(i - 1, j) + br(i + 1, j) + bl(i, j - 1) + tr(i, j + 1),
                   tl(i, j - 1) + br(i, j + 1) + bl(i + 1, j) + tr(i - 1, j))
               for i in range(1, n - 1) for j in range(1, m - 1))


def _trace(table, start, step_options):
    path = [start]
    i, j = start
    while True:
        options = [(table[x][y], (x, y)) for x, y in step_options(i, j)]
        if not options:
            return path
        _, (i, j) = max(options)
        path.append((i, j))


def witness(data):
    """Reconstruct optimal 1-based paths (Iahub, Iahubina) from the oracle tables."""
    n, m, a = data
    best, (mi, mj, kind), (p, q, r, s) = _best(n, m, a)

    def inside(cells):
        return [(x, y) for x, y in cells if 1 <= x <= n and 1 <= y <= m]

    def back_tl(i, j):
        return inside([(i - 1, j), (i, j - 1)])

    def fwd_br(i, j):
        return inside([(i + 1, j), (i, j + 1)])

    def back_bl(i, j):
        return inside([(i + 1, j), (i, j - 1)])

    def fwd_tr(i, j):
        return inside([(i - 1, j), (i, j + 1)])

    if kind == 'vertical':
        h_in, h_out, g_in, g_out = (mi - 1, mj), (mi + 1, mj), (mi, mj - 1), (mi, mj + 1)
    else:
        h_in, h_out, g_in, g_out = (mi, mj - 1), (mi, mj + 1), (mi + 1, mj), (mi - 1, mj)
    iahub = _trace(p, h_in, back_tl)[::-1] + [(mi, mj)] + _trace(q, h_out, fwd_br)
    iahubina = _trace(r, g_in, back_bl)[::-1] + [(mi, mj)] + _trace(s, g_out, fwd_tr)
    return best, iahub, iahubina


def check_witness(data, value, iahub, iahubina):
    n, m, a = data
    if iahub[0] != (1, 1) or iahub[-1] != (n, m):
        return False
    if iahubina[0] != (n, 1) or iahubina[-1] != (1, m):
        return False
    for (x, y), (u, v) in zip(iahub, iahub[1:]):
        if (u - x, v - y) not in ((1, 0), (0, 1)):
            return False
    for (x, y), (u, v) in zip(iahubina, iahubina[1:]):
        if (u - x, v - y) not in ((-1, 0), (0, 1)):
            return False
    common = set(iahub) & set(iahubina)
    if len(common) != 1:
        return False
    total = sum(a[x - 1][y - 1] for x, y in set(iahub) ^ set(iahubina))
    return total == value


def _paths(n, m, down):
    result = []
    for moves in itertools.combinations(range(n + m - 2), n - 1):
        x, y = (0 if down else n - 1), 0
        cells = [(x, y)]
        vertical = set(moves)
        for k in range(n + m - 2):
            if k in vertical:
                x += 1 if down else -1
            else:
                y += 1
            cells.append((x, y))
        result.append(cells)
    return result


def brute(pid, data):
    n, m, a = data
    index = lambda x, y: x * m + y

    def encode(cells):
        mask = 0
        for x, y in cells:
            mask |= 1 << index(x, y)
        return mask, sum(a[x][y] for x, y in cells)

    first = [encode(c) for c in _paths(n, m, True)]
    second = [encode(c) for c in _paths(n, m, False)]
    flat = [v for row in a for v in row]
    best = None
    for mask1, sum1 in first:
        for mask2, sum2 in second:
            common = mask1 & mask2
            if common and not common & (common - 1):
                value = sum1 + sum2 - 2 * flat[common.bit_length() - 1]
                if best is None or value > best:
                    best = value
    return best


def _text(n, m, grid):
    return f'{n} {m}\n' + ''.join(' '.join(map(str, row)) + '\n' for row in grid)


def _random_grid(rng, n, m, high):
    return [[rng.randint(0, high) for _ in range(m)] for _ in range(n)]


def _mutants(n, m, a):
    p, q, r, s = _tables(n, m, a)

    def vertical(i, j):
        return p[i - 1][j] + q[i + 1][j] + r[i][j - 1] + s[i][j + 1]

    def horizontal(i, j):
        return p[i][j - 1] + q[i][j + 1] + r[i + 1][j] + s[i - 1][j]

    interior = [(i, j) for i in range(2, n) for j in range(2, m)]
    everywhere = [(i, j) for i in range(1, n + 1) for j in range(1, m + 1)]
    return {
        'border meetings allowed': max(max(vertical(i, j), horizontal(i, j)) for i, j in everywhere),
        'vertical-crossing only': max(vertical(i, j) for i, j in interior),
        'horizontal-crossing only': max(horizontal(i, j) for i, j in interior),
        'four-way sum minus 4a': max(p[i][j] + q[i][j] + r[i][j] + s[i][j] - 4 * a[i - 1][j - 1] for i, j in everywhere),
    }


def extras(pid):
    rng = random.Random(16004292)
    cases, seen = [], set()

    def add(grid, reason, category='adversarial'):
        n, m = len(grid), len(grid[0])
        text = _text(n, m, grid)
        if text in seen:
            return
        seen.add(text)
        data = parse(pid, text)
        cases.append({'input': text, 'output': f'{answer(pid, data)}\n', 'reason': reason, 'category': category})

    add([[0] * 3 for _ in range(3)], 'minimum 3x3 all zeros', 'boundary')
    add([[MAX_VALUE] * 3 for _ in range(3)], 'minimum 3x3 all 10^5', 'boundary')
    add([[1] * 3 for _ in range(3)], 'minimum 3x3 all ones', 'boundary')
    for k in range(9):
        grid = [[0] * 3 for _ in range(3)]
        grid[k // 3][k % 3] = MAX_VALUE
        add(grid, f'3x3 single 10^5 at cell {k // 3 + 1},{k % 3 + 1}: forced centre meeting', 'boundary')
    for n, m in ((3, 4), (4, 3), (3, 5), (5, 3), (4, 4), (3, 1000), (1000, 3)):
        add([[1] * m for _ in range(n)], f'{n}x{m} all ones (thin dimension boundary)', 'boundary')
    add([[MAX_VALUE] * 1000 for _ in range(3)], '3x1000 all 10^5: widest legal row length', 'maxSize')
    add([[MAX_VALUE] * 3 for _ in range(1000)], '1000x3 all 10^5: tallest legal column', 'maxSize')
    add(_random_grid(rng, 3, 1000, MAX_VALUE), '3x1000 random full range', 'maxSize')
    add(_random_grid(rng, 1000, 3, MAX_VALUE), '1000x3 random full range', 'maxSize')
    add(_random_grid(rng, 257, 257, MAX_VALUE), '257x257 random full-range values', 'adversarial')
    add([[MAX_VALUE] * 1000 for _ in range(1000)], 'maximum 1000x1000 all 10^5: largest possible answer 399600000', 'maxSize')
    add([[MAX_VALUE if (i == j or i + j == 256) else rng.randint(0, 3) for j in range(257)] for i in range(257)],
        '257x257 heavy diagonals crossing at the centre', 'adversarial')

    for n, m in ((3, 3), (3, 4), (4, 3), (4, 4), (5, 7), (7, 5)):
        grid = [[0] * m for _ in range(n)]
        for j in range(m):
            grid[0][j] = grid[n - 1][j] = MAX_VALUE
        for i in range(n):
            grid[i][0] = grid[i][m - 1] = MAX_VALUE
        add(grid, f'{n}x{m} heavy border ring, zero interior: border-meeting heuristics overcount', 'adversarial')
    for n, m in ((3, 6), (6, 3), (4, 8), (8, 4)):
        grid = [[0] * m for _ in range(n)]
        for j in range(m):
            grid[n // 2][j] = MAX_VALUE
        add(grid, f'{n}x{m} heavy middle row: only one crossing orientation collects it', 'adversarial')
        grid = [[0] * m for _ in range(n)]
        for i in range(n):
            grid[i][m // 2] = MAX_VALUE
        add(grid, f'{n}x{m} heavy middle column: the other crossing orientation', 'adversarial')

    targets = {name: 0 for name in _mutants(3, 3, [[0] * 3 for _ in range(3)])}
    attempts = 0
    while min(targets.values()) < 6 and attempts < 4000:
        attempts += 1
        n, m = rng.randint(3, 7), rng.randint(3, 7)
        high = rng.choice((1, 3, 9, 100, MAX_VALUE))
        grid = _random_grid(rng, n, m, high)
        truth = answer(pid, (n, m, grid))
        killed = [name for name, value in _mutants(n, m, grid).items() if value != truth and targets[name] < 6]
        if killed:
            for name in killed:
                targets[name] += 1
            add(grid, f'fixed-seed small grid separating: {", ".join(killed)}', 'adversarial')

    for _ in range(60):
        n, m = rng.randint(3, 8), rng.randint(3, 8)
        add(_random_grid(rng, n, m, rng.choice((2, 10, MAX_VALUE))), 'fixed-seed random small grid (exhaustively brute-checkable)', 'adversarial')
    for _ in range(12):
        n, m = rng.randint(9, 60), rng.randint(9, 60)
        add(_random_grid(rng, n, m, MAX_VALUE), 'fixed-seed random medium grid, non-square (n != m index-swap bugs)', 'adversarial')
    for n, m in ((3, 50), (50, 3), (17, 4), (4, 17)):
        grid = _random_grid(rng, n, m, 5)
        grid[1][1] = grid[n - 2][m - 2] = MAX_VALUE
        add(grid, f'{n}x{m} rectangular with heavy cells next to the excluded corners', 'adversarial')
    return cases


def brute_checks():
    count = 0
    for values in itertools.product(range(3), repeat=9):
        grid = [list(values[0:3]), list(values[3:6]), list(values[6:9])]
        data = (3, 3, grid)
        expected = brute('429B', data)
        assert answer('429B', data) == expected, (grid, answer('429B', data), expected)
        count += 1
    rng = random.Random(16004293)
    for _ in range(500):
        n, m = rng.randint(3, 6), rng.randint(3, 6)
        grid = _random_grid(rng, n, m, rng.choice((1, 4, 50, MAX_VALUE)))
        data = (n, m, grid)
        expected = brute('429B', data)
        assert answer('429B', data) == expected, (grid, expected)
        assert flip_answer(data) == expected, (grid, expected)
        count += 2
    for _ in range(150):
        n, m = rng.randint(3, 45), rng.randint(3, 45)
        data = (n, m, _random_grid(rng, n, m, MAX_VALUE))
        value, iahub, iahubina = witness(data)
        assert flip_answer(data) == value
        assert check_witness(data, value, iahub, iahubina)
        count += 2
    return {'429B': count}


def review(pid, tests, samples):
    failures = []
    for name, pair in tests + samples:
        try:
            expected = [str(answer(pid, parse(pid, pair['input'])))]
        except ValueError as exc:
            failures.append({'test': name, 'reason': str(exc)})
            continue
        if expected != pair['output'].split():
            failures.append({'test': name, 'reason': 'independent oracle disagreement',
                             'expected': expected, 'actual': pair['output'].split()[:5]})
    return failures
