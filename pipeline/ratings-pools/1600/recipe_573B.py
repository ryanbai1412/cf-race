"""Rating-1600 recipe for 573B Bear and Blocks (simultaneous boundary-block destruction)."""
import itertools
import random
import re


IDS = ('573B',)
MAX_N = 10**5
MAX_H = 10**9
SEMANTICS = {
    '573B': 'Line 1: n, 1<=n<=10^5; line 2: n integers h_i, 1<=h_i<=10^9 (public English statement shows 10<sup>5</sup>/10<sup>9</sup>; pinned row flattened them to 105/109). '
            'Each operation simultaneously destroys every block lacking a block or floor on any of its four sides; print the unique integer number of operations until no block remains. '
            'Oracle: L_i=min(L_{i-1}+1,h_i), R_i=min(R_{i+1}+1,h_i) with zero outside the row; answer max_i min(L_i,R_i). '
            'Literal cell-set simulation exhaustively cross-checks small rows and an O(n^2) distance formula min(i+1,n-i,min_j h_j+|i-j|) cross-checks large heights.',
}
NUMBER = r'[1-9][0-9]*'
FIRST = re.compile(NUMBER)
ROW = re.compile(rf'{NUMBER}(?: {NUMBER})*')


def parse(pid, text):
    if pid not in IDS:
        raise ValueError('unknown problem')
    if text.endswith('\n'):
        text = text[:-1]
    lines = text.split('\n')
    if len(lines) != 2:
        raise ValueError('expected exactly two lines')
    lines = [line[:-1] if line.endswith('\r') else line for line in lines]
    if not FIRST.fullmatch(lines[0]) or not ROW.fullmatch(lines[1]):
        raise ValueError('malformed line layout')
    n = int(lines[0])
    heights = [int(token) for token in lines[1].split(' ')]
    if not 1 <= n <= MAX_N:
        raise ValueError('n outside 1..10^5')
    if len(heights) != n:
        raise ValueError('height count differs from n')
    if not all(1 <= h <= MAX_H for h in heights):
        raise ValueError('height outside 1..10^9')
    return heights


def answer(pid, data):
    n = len(data)
    left = [0] * n
    previous = 0
    for i, h in enumerate(data):
        previous = left[i] = min(previous + 1, h)
    best = previous = 0
    for i in range(n - 1, -1, -1):
        previous = min(previous + 1, data[i])
        best = max(best, min(previous, left[i]))
    return best


def distance_answer(heights):
    n = len(heights)
    return max(min(i + 1, n - i, min(h + abs(i - j) for j, h in enumerate(heights))) for i in range(n))


def simulate(heights):
    cells = {(i, j) for i, h in enumerate(heights) for j in range(1, h + 1)}
    operations = 0
    while cells:
        cells = {(i, j) for i, j in cells
                 if (i, j + 1) in cells and (j == 1 or (i, j - 1) in cells) and (i - 1, j) in cells and (i + 1, j) in cells}
        operations += 1
    return operations


def _row(heights):
    return f'{len(heights)}\n' + ' '.join(map(str, heights)) + '\n'


def extras(pid):
    rng = random.Random(15730573)
    cases = []
    seen = set()

    def add(heights, reason, category='adversarial'):
        text = _row(heights)
        if text in seen:
            return
        seen.add(text)
        cases.append({'input': text, 'output': f'{answer(pid, parse(pid, text))}\n', 'reason': reason, 'category': category})

    for heights in ([1], [MAX_H], [1, 1], [MAX_H, MAX_H], [1, MAX_H], [2, 2, 2], [3, 3, 3], [1, 3, 1], [5, 5, 5, 5],
                    [MAX_H] * 3, [1, MAX_H, 1], [MAX_H, 1, MAX_H], [2, 3, 2], [3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3]):
        add(heights, 'minimum n/heights, n<=2 edge columns, flat rows with odd/even width', 'boundary')
    for n in (7, 9, 10, 11):
        add([n] * n, 'flat square row: answer limited by width (n+1)//2, not height', 'boundary')
        add([1] + [n] * (n - 2) + [1], 'flat interior between unit edges', 'boundary')
    add([2] * 10, 'flat low row: height-limited answer 2', 'boundary')
    add(list(range(1, 12)) + list(range(10, 0, -1)), 'perfect pyramid: answer equals peak', 'boundary')

    add([MAX_H] * MAX_N, 'maximum n and heights: width-limited answer 50000', 'maxSize')
    add([1] * MAX_N, 'maximum n with unit heights', 'maxSize')
    add([MAX_H if i % 2 else 1 for i in range(MAX_N)], 'maximum n alternating unit/maximal towers', 'maxSize')
    add(list(range(1, MAX_N + 1)), 'maximum n strictly increasing staircase (quadratic propagation adversary)', 'maxSize')
    add(list(range(MAX_N, 0, -1)), 'maximum n strictly decreasing staircase', 'maxSize')
    add([min(i + 1, MAX_N - i) for i in range(MAX_N)], 'maximum n exact pyramid peak 50000', 'maxSize')
    add([MAX_H] * (MAX_N // 2 - 1) + [1, 1] + [MAX_H] * (MAX_N // 2 - 1), 'maximum n split by a central unit pair', 'maxSize')
    add([MAX_H - (i * 7919) % 1000 for i in range(MAX_N)], 'maximum n near-maximal noisy heights', 'maxSize')
    add([rng.randint(1, MAX_H) for _ in range(MAX_N)], 'maximum n fixed-seed full-range heights', 'maxSize')
    add([rng.randint(30000, 70000) for _ in range(MAX_N)], 'maximum n heights around the width bound', 'maxSize')

    targeted = [
        [5, 5, 5, 1, 5, 5, 5, 5, 5], [3, 3, 3, 1, 3, 3, 3], [4, 4, 4, 4, 1, 4, 4, 4], [2, 2, 2, 3, 2, 2, 2],
        [1, 2, 3, 4, 4, 3, 2, 1], [9, 9, 2, 9, 9, 9, 9, 9, 9, 9, 9], [6, 6, 6, 6, 6, 6, 1], [1, 6, 6, 6, 6, 6, 6],
        [3, 4, 5, 6, 6, 6, 6], [100, 1, 100, 100, 100, 100, 100, 100, 100], [2, 1, 4, 6, 2, 2], [5, 4, 3, 2, 3, 4, 5],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 2, 10, 10, 10, 10, 10, 10, 10],
        [4, 4, 4, 4, 4, 4, 4, 4], [7, 7, 7, 7, 7, 7, 7, 7, 3, 7, 7, 7], [1, 1, 5, 5, 5, 5, 5, 5, 5, 1, 1],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [2, 3, 3, 3, 3, 3, 2], [3, 2, 3, 2, 3, 2, 3],
        [MAX_H, 2, MAX_H, MAX_H, MAX_H, MAX_H, MAX_H, MAX_H], [1, 2, 1, 2, 1, 2, 1, 2, 1], [4, 5, 4, 5, 4, 5, 4, 5, 4],
    ]
    for heights in targeted:
        add(heights, 'local-min/valley, flat-plateau width and near-edge shapes separating selected wrong heuristics')
    for _ in range(60):
        n = rng.randint(3, 12)
        add([rng.randint(1, 8) for _ in range(n)], 'fixed-seed small rows checkable by literal block simulation')
    for _ in range(25):
        n = rng.randint(13, 200)
        top = rng.choice((3, 10, 60, MAX_H))
        add([rng.randint(1, top) for _ in range(n)], 'fixed-seed medium rows with mixed height scales')
    for _ in range(10):
        n = rng.randint(20, 300)
        add([max(1, min(i + 1, n - i) + rng.randint(-2, 2) * (rng.randrange(3) == 0)) for i in range(n)],
            'fixed-seed perturbed pyramids where every column is nearly binding')
    return cases


def brute_checks():
    count = 0
    rng = random.Random(15739999)

    def check(heights, reference):
        nonlocal count
        got = answer('573B', heights)
        assert got == reference, (heights, got, reference)
        count += 1

    for n in range(1, 7):
        for heights in itertools.product(range(1, 6 if n <= 5 else 5), repeat=n):
            check(list(heights), simulate(heights))
    for _ in range(1500):
        heights = [rng.randint(1, 10) for _ in range(rng.randint(1, 14))]
        check(heights, simulate(heights))
    for _ in range(600):
        n = rng.randint(1, 250)
        top = rng.choice((5, 100, 10**4, MAX_H))
        heights = [rng.randint(1, top) for _ in range(n)]
        check(heights, distance_answer(heights))
    return {'573B': count}


def review(pid, tests, samples):
    failures = []
    for name, pair in tests + samples:
        try:
            expected = [str(answer(pid, parse(pid, pair['input'])))]
            if expected != pair['output'].split():
                failures.append({'test': name, 'reason': 'independent oracle disagreement', 'expected': expected, 'actual': pair['output'].split()[:15]})
        except (ValueError, IndexError) as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
