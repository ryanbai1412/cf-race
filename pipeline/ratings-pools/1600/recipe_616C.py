"""616C: independent wall removal on a side-connected rectangular grid."""
from array import array
from collections import deque
import itertools
import random
import re


IDS = ('616C',)
SEMANTICS = {
    '616C': 'Original English statement attests 1<=n,m<=1000, n rows of exactly m '
            'dots/stars, side adjacency only. Each original star is removed independently; '
            'print its reachable-cell count modulo 10, preserving dots. The unique '
            'n-by-m output is found by summing distinct adjacent empty-component sizes '
            'plus one. Literal per-wall flood fills independently check small grids.'
}


def _require_pid(pid):
    if pid not in IDS:
        raise ValueError('unsupported problem id')


def parse(pid, text):
    _require_pid(pid)
    lines = text.replace('\r\n', '\n').split('\n')
    if lines[-1] == '':
        lines.pop()
    if not lines:
        raise ValueError('empty input')
    header = lines[0].split()
    if len(header) != 2 or any(not re.fullmatch(r'[0-9]+', v) for v in header):
        raise ValueError('grid header requires two decimal integers')
    n, m = map(int, header)
    if not (1 <= n <= 1000 and 1 <= m <= 1000):
        raise ValueError('grid dimensions outside 1..1000')
    rows = lines[1:]
    if len(rows) != n or any(len(row) != m for row in rows):
        raise ValueError('grid line layout requires n rows of m characters')
    if any(set(row) - set('.*') for row in rows):
        raise ValueError('grid alphabet must be dots and stars')
    return tuple(rows)


def answer(pid, data):
    _require_pid(pid)
    n, m = len(data), len(data[0])
    cells = ''.join(data).encode('ascii')
    total = len(cells)
    labels = array('i', [-1]) * total
    sizes = array('i')
    for start, cell in enumerate(cells):
        if cell != 46 or labels[start] != -1:
            continue
        label = len(sizes)
        labels[start] = label
        stack = [start]
        size = 0
        while stack:
            u = stack.pop()
            size += 1
            column = u % m
            for v in (u - m if u >= m else -1,
                      u + m if u + m < total else -1,
                      u - 1 if column else -1,
                      u + 1 if column + 1 < m else -1):
                if v >= 0 and cells[v] == 46 and labels[v] == -1:
                    labels[v] = label
                    stack.append(v)
        sizes.append(size)
    result = []
    for r, row in enumerate(data):
        output = bytearray(row, 'ascii')
        for c, cell in enumerate(row):
            if cell != '*':
                continue
            u = r * m + c
            adjacent = set()
            for v in (u - m if r else -1,
                      u + m if r + 1 < n else -1,
                      u - 1 if c else -1,
                      u + 1 if c + 1 < m else -1):
                if v >= 0 and labels[v] >= 0:
                    adjacent.add(labels[v])
            output[c] = 48 + (1 + sum(sizes[label] for label in adjacent)) % 10
        result.append(output.decode('ascii'))
    return result


def _literal_brute(rows):
    n, m = len(rows), len(rows[0])
    result = []
    for r, row in enumerate(rows):
        output = []
        for c, cell in enumerate(row):
            if cell == '.':
                output.append('.')
                continue
            removed = (r, c)
            visited = {removed}
            queue = deque([removed])
            while queue:
                x, y = queue.popleft()
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    v = (x + dx, y + dy)
                    if (0 <= v[0] < n and 0 <= v[1] < m and v not in visited
                            and (v == removed or rows[v[0]][v[1]] == '.')):
                        visited.add(v)
                        queue.append(v)
            output.append(str(len(visited) % 10))
        result.append(''.join(output))
    return result


def brute_checks():
    count = 0

    def check(rows):
        nonlocal count
        fast = answer('616C', rows)
        slow = _literal_brute(rows)
        assert fast == slow, (rows, fast, slow)
        count += 1

    for n in range(1, 4):
        for m in range(1, 4):
            for cells in itertools.product('.*', repeat=n * m):
                check([''.join(cells[i * m:(i + 1) * m]) for i in range(n)])
    for length in range(4, 8):
        for cells in itertools.product('.*', repeat=length):
            check([''.join(cells)])
            check(list(cells))
    rng = random.Random(61601600)
    for _ in range(400):
        n, m = rng.randint(1, 6), rng.randint(1, 6)
        density = rng.choice((0.15, 0.35, 0.5, 0.65, 0.85))
        check([''.join('*' if rng.random() < density else '.' for _ in range(m))
               for _ in range(n)])
    return {'616C': count}


def extras(pid):
    _require_pid(pid)
    cases = []
    seen = set()

    def add(rows, reason, category='adversarial'):
        text = f'{len(rows)} {len(rows[0])}\n' + '\n'.join(rows) + '\n'
        if text in seen:
            return
        seen.add(text)
        data = parse(pid, text)
        cases.append({'input': text, 'output': '\n'.join(answer(pid, data)) + '\n',
                      'reason': reason, 'category': category})

    add(['.'], 'minimum singleton empty cell remains a dot', 'boundary')
    add(['*'], 'minimum isolated removed wall counts itself', 'boundary')
    add(['...', '.*.', '...'], 'same eight-cell component touches wall on four sides')
    add(['***', '*.*', '***'], 'isolated dot and thick obstacle border')
    add(['*.*', '.*.', '*.*'], 'four distinct components around center; no diagonal edges')
    add(['.*', '*.'], 'diagonal empty cells are not directly adjacent')
    add(['.**.'], 'remove each adjacent wall independently, never both at once')
    add(['*..', '***'], 'asymmetric dimensions and boundary neighbors')
    add(['**', '..', '*.', '.*', '..'], 'transposed rectangle and connected side branches')
    for count in (8, 9, 10, 18, 19, 20, 98, 99, 100):
        row = '*' + '.' * count
        add([row], 'reachable size crosses modulo-10 boundary; selected WA omits modulo', 'boundary')
        add(list(row), 'vertical modulo boundary and one-column layout', 'boundary')
    for row in ('.' * 1000, '*' * 1000, '.*' * 500, '.' * 499 + '*' + '.' * 500):
        add([row], 'maximum width with minimum height', 'maxSize')
        add(list(row), 'maximum height with minimum width', 'maxSize')
    for n, m in ((7, 13), (13, 7), (31, 32), (32, 31)):
        add([''.join('*' if (r + c) % 2 else '.' for c in range(m)) for r in range(n)],
            'many singleton components; up to four different component IDs')
        add(['*' * m if r % 3 == 1 else '.' * m for r in range(n)],
            'parallel empty chambers separated by solid wall rows')
        add([''.join('*' if r % 4 == 2 and c != m // 2 else '.' for c in range(m))
             for r in range(n)], 'single narrow doorway joins otherwise separate chambers')
    snake = []
    for r in range(121):
        if r % 2 == 0:
            snake.append('.' * 151)
        else:
            opening = 150 if r % 4 == 1 else 0
            snake.append('*' * opening + '.' + '*' * (150 - opening))
    add(snake, 'long serpentine single component; iterative traversal and repeated contact')
    add(['.' * 1000] * 1000, 'legal maximum n=m=1000, one million empty cells', 'maxSize')
    add([''.join('*' if (r + c) % 2 else '.' for c in range(1000)) for r in range(1000)],
        'legal maximum checkerboard: 500000 distinct empty components', 'maxSize')
    rows = ['.' * 1000] * 1000
    rows[500] = '.' * 500 + '*' + '.' * 499
    add(rows, 'legal maximum: wall touches one 999999-cell component four times; answer zero', 'maxSize')
    rng = random.Random(6161600)
    while len(cases) < 160:
        n, m = rng.randint(2, 12), rng.randint(2, 12)
        density = rng.choice((0.1, 0.25, 0.5, 0.75, 0.9))
        add([''.join('*' if rng.random() < density else '.' for _ in range(m))
             for _ in range(n)], 'fixed-seed small mixed rectangles and component contacts')
    return cases


def review(pid, tests, samples):
    _require_pid(pid)
    failures = []
    for name, pair in tests + samples:
        try:
            data = parse(pid, pair['input'])
            lines = pair['output'].replace('\r\n', '\n').split('\n')
            if lines[-1] == '':
                lines.pop()
            if (len(lines) != len(data) or any(len(row) != len(data[0]) for row in lines)
                    or any(set(row) - set('.0123456789') for row in lines)):
                raise ValueError('output requires n rows of m dots/digits without spaces')
            expected = answer(pid, data)
            if lines != expected:
                failures.append({'test': name, 'reason': 'exact oracle disagreement',
                                 'expected': expected, 'actual': lines})
        except (ValueError, KeyError, TypeError) as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
