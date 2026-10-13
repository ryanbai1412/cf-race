"""Magical Boxes (269A): smallest power-of-two container for nested power-of-two boxes."""
import itertools
import random
import re


IDS = ('269A',)
SEMANTICS = {
    '269A': 'First line n, 1<=n<=10^5; then n lines "k_i a_i", 0<=k_i<=10^9 distinct, 1<=a_i<=10^9: a_i boxes of side 2^(k_i). '
            'A box fits inside any strictly larger box, so boxes nest. Equal-size boxes cannot nest, hence a box of side 2^p '
            'holds at most 4^(p-k) boxes of side 2^k (area) and needs p>k; quadtree-aligned placement achieves this for every '
            'size simultaneously because each placed box re-exposes its own cell. Unique answer p = max_i (k_i + max(1, ceil(log4 a_i))), '
            'one integer. Checked against bottom-up level carrying and top-down slot-feasibility brutes.',
}
MAX_N = 10 ** 5
MAX_K = 10 ** 9
MAX_A = 10 ** 9
_INT = re.compile(r'0|[1-9][0-9]*')


def _int(token, what):
    if not _INT.fullmatch(token):
        raise ValueError(f'{what} not a canonical nonnegative integer')
    return int(token)


def parse(pid, text):
    if pid != '269A':
        raise ValueError('unknown problem')
    lines = text.splitlines()
    if not lines:
        raise ValueError('empty input')
    head = lines[0].split()
    if len(head) != 1:
        raise ValueError('first line arity')
    n = _int(head[0], 'n')
    if not 1 <= n <= MAX_N:
        raise ValueError('n range')
    if len(lines) != n + 1:
        raise ValueError('line layout: expected n box lines')
    boxes = []
    seen = set()
    for line in lines[1:]:
        parts = line.split()
        if len(parts) != 2:
            raise ValueError('box line arity')
        k, a = _int(parts[0], 'k'), _int(parts[1], 'a')
        if not 0 <= k <= MAX_K or not 1 <= a <= MAX_A:
            raise ValueError('box constraints')
        if k in seen:
            raise ValueError('duplicate k')
        seen.add(k)
        boxes.append((k, a))
    return boxes


def _levels(a):
    return max(1, ((a - 1).bit_length() + 1) // 2)


def answer(pid, boxes):
    return max(k + _levels(a) for k, a in boxes)


def brute_carry(boxes):
    counts = dict(boxes)
    low, high = min(counts), max(counts)
    need = 0
    for level in range(low, high + 1):
        need = max(counts.get(level, 0), -(-need // 4))
    p = high + 1
    need = -(-need // 4)
    while need > 1:
        need = -(-need // 4)
        p += 1
    return p


def brute_slots(boxes):
    counts = dict(boxes)
    low = min(counts)
    p = 0
    while True:
        p += 1
        slots = 4
        ok = all(k < p for k in counts)
        level = p - 1
        while ok and level >= low:
            if counts.get(level, 0) > slots:
                ok = False
            slots *= 4
            level -= 1
        if ok:
            return p


def _render(boxes):
    return f'{len(boxes)}\n' + ''.join(f'{k} {a}\n' for k, a in boxes)


def extras(pid):
    rng = random.Random(269001)
    cases = []
    seen = set()

    def add(boxes, reason, category='adversarial'):
        text = _render(boxes)
        if text in seen:
            return
        seen.add(text)
        cases.append({'input': text, 'output': f'{answer(pid, parse(pid, text))}\n', 'reason': reason, 'category': category})

    add([(0, 1)], 'minimum: single unit box still needs a strictly larger container (p=1)', 'boundary')
    add([(MAX_K, 1)], 'k=10^9, a=1: answer k+1 (log4(1)=0 must still add one level)', 'boundary')
    add([(MAX_K, MAX_A)], 'k=10^9, a=10^9: answer 10^9+15, needs 64-bit range', 'boundary')
    add([(0, MAX_A)], 'a=10^9 lies between 4^14 and 4^15: answer 15', 'boundary')
    add([(MAX_K - 1, 2), (MAX_K, 1)], 'top two k values; one box at 10^9 dominates', 'boundary')
    for k in (0, 7, 123456789):
        add([(k, 1)], f'single box a=1 at k={k}: catches printing k when the carried count is already 1', 'boundary')
    for m in range(1, 15):
        add([(0, 4 ** m)], f'a=4^{m} exactly: largest count that fits in {m} levels', 'boundary')
        undershoot = '; floor-based log4 loops undershoot' if m >= 2 else ''
        add([(0, 4 ** m + 1)], f'a=4^{m}+1: smallest count needing {m + 1} levels{undershoot}', 'boundary')
        add([(5, 4 ** m - 1)], f'a=4^{m}-1 at k=5', 'boundary')
    add([(0, 4), (1, 4), (2, 4)], 'nesting: total area 84>64 but smaller boxes go inside larger ones (p=3); area-sum solutions say 4')
    add([(0, 4), (1, 4)], 'nesting: four unit boxes fit inside one side-2 box (p=2); area-sum gives 3')
    add([(0, 16), (1, 4), (2, 1)], 'each level exactly full and nested: p=3')
    add([(0, 17), (1, 4), (2, 1)], 'one extra unit box overflows the chain only at level 0: p=3 still')
    add([(0, 65), (1, 1), (2, 1)], 'carried count dominates own counts at levels 1 and 2: p=4')
    add([(0, 5), (1, 3)], 'carry ceil(5/4)=2 is absorbed by own count 3 (p=2); summing own+carry gives 5 boxes and p=3')
    add([(1, 10), (0, 3)], 'unsorted input order')
    add([(2, 1), (1, 1), (0, 1)], 'descending k order, all single boxes: p=3')
    add([(0, MAX_A), (14, 1)], 'tie: a huge count at k=0 and a single box at k=14 both give 15')
    add([(0, MAX_A), (15, 1)], 'single box at k=15 beats the k=0 pile (16)')
    add([(0, MAX_A), (MAX_K, 1)], 'gap 10^9 between sizes: 4**gap or level-by-level loops blow up')
    add([(3, 1), (MAX_K // 2, 2), (MAX_K, 1)], 'huge gaps with small counts')
    add([(i, 4) for i in range(30)], '4 boxes at each of 30 consecutive levels: p=30')
    add([(i, 5) for i in range(30)], '5 boxes at each of 30 consecutive levels: p=31')
    add([(i, 1) for i in range(0, 40, 2)], 'single boxes at even levels only')
    add([(10, 3), (25, 747)], 'larger k with moderate count dominates (747 needs 5 levels)')
    add([(0, 4 ** 14), (1, 4 ** 13), (2, 4 ** 12 + 1)], 'level 2 overflows by one: p=15 from k=2')
    for m in range(1, 8):
        add([(0, 4 ** m), (m, 1)], f'pile 4^{m} at k=0 exactly fills one box at level {m}, plus an own box there: p={m + 1}')
    add([(k, rng.randint(1, MAX_A)) for k in range(MAX_N)], 'maximum n=10^5, consecutive k from 0, random counts', 'maxSize')
    ks = rng.sample(range(MAX_K + 1), MAX_N)
    add([(k, rng.randint(1, MAX_A)) for k in ks], 'maximum n=10^5, random distinct k up to 10^9, random counts', 'maxSize')
    add([(MAX_K - i, MAX_A) for i in range(MAX_N)], 'maximum n=10^5, descending k from 10^9 with a=10^9: answer 10^9+15', 'maxSize')
    add([(i, 1) for i in range(MAX_N)], 'maximum n=10^5 all single boxes at consecutive k: p=10^5', 'maxSize')
    while len(cases) < 150:
        n = rng.randint(1, 6)
        ks = rng.sample(range(rng.choice((8, 40, MAX_K + 1))), n)
        bound = rng.choice((5, 70, MAX_A))
        add([(k, rng.randint(1, bound)) for k in ks], 'fixed-seed random small case', 'adversarial')
    return cases


def brute_checks():
    count = 0

    def check(boxes):
        nonlocal count
        expected = answer('269A', boxes)
        assert brute_carry(boxes) == expected, (boxes, expected)
        assert brute_slots(boxes) == expected, (boxes, expected)
        count += 2

    for size in range(1, 4):
        for ks in itertools.combinations(range(5), size):
            for counts in itertools.product(range(1, 18), repeat=size):
                check(list(zip(ks, counts)))
    rng = random.Random(269002)
    for _ in range(3000):
        n = rng.randint(1, 8)
        ks = rng.sample(range(40), n)
        check([(k, rng.randint(1, rng.choice((20, 300, MAX_A)))) for k in ks])
    for m in range(0, 16):
        for delta in (-1, 0, 1):
            a = 4 ** m + delta
            if 1 <= a <= MAX_A:
                check([(3, a)])
    return {'269A': count}


def review(pid, tests, samples):
    failures = []
    for name, pair in [*tests, *samples]:
        try:
            expected = str(answer(pid, parse(pid, pair['input'])))
            if pair['output'].split() != [expected]:
                failures.append({'test': name, 'reason': 'independent oracle disagreement', 'expected': [expected], 'actual': pair['output'].split()[:15]})
        except ValueError as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
