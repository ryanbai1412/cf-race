"""1600 single-answer recipes, strict constraints, and small exhaustive oracles."""
import itertools
import math
import random

IDS = ('235A', '322B', '371C', '888D')


def parse(pid, text):
    tokens = text.split()
    if pid == '371C':
        if len(tokens) != 8 or not 1 <= len(tokens[0]) <= 100 or set(tokens[0]) - set('BSC'):
            raise ValueError('invalid hamburger recipe/arity')
        values = tuple(map(int, tokens[1:]))
        if not all(1 <= x <= 100 for x in values[:6]) or not 1 <= values[6] <= 10**12:
            raise ValueError('hamburger constraints')
        return tokens[0], values[:3], values[3:6], values[6]
    values = tuple(map(int, tokens))
    if pid == '235A' and len(values) == 1 and 1 <= values[0] <= 10**6:
        return values
    if pid == '322B' and len(values) == 3 and all(0 <= x <= 10**9 for x in values):
        return values
    if pid == '888D' and len(values) == 2 and 4 <= values[0] <= 1000 and 1 <= values[1] <= 4:
        return values
    raise ValueError('constraint/arity violation: ' + pid)


def answer(pid, data):
    if pid == '235A':
        n, = data
        if n <= 2:
            return n
        if n % 2:
            return n * (n - 1) * (n - 2)
        if n % 3:
            return n * (n - 1) * (n - 3)
        return (n - 1) * (n - 2) * (n - 3)
    if pid == '322B':
        return max(t + sum((x - t) // 3 for x in data) for t in range(min(2, min(data)) + 1))
    if pid == '888D':
        n, k = data
        return sum(math.comb(n, i) * (1, 0, 1, 2, 9)[i] for i in range(k + 1))
    recipe, stock, price, money = data
    counts = [recipe.count(c) for c in 'BSC']
    def cost(n):
        return sum(max(0, n * c - s) * p for c, s, p in zip(counts, stock, price))
    lo, hi = 0, 1
    while cost(hi) <= money:
        hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if cost(mid) <= money:
            lo = mid
        else:
            hi = mid
    assert cost(lo) <= money < cost(lo + 1)
    return lo


def brute_checks():
    counts = {}
    for n in range(1, 33):
        expected = max(math.lcm(*triple) for triple in itertools.combinations_with_replacement(range(1, n + 1), 3))
        assert answer('235A', (n,)) == expected
    counts['235A'] = 32
    for flowers in itertools.product(range(10), repeat=3):
        expected = max(t + sum((x - t) // 3 for x in flowers) for t in range(min(flowers) + 1))
        assert answer('322B', flowers) == expected
    counts['322B'] = 1000
    for n in range(4, 9):
        distribution = [0] * (n + 1)
        for perm in itertools.permutations(range(n)):
            distribution[sum(i != p for i, p in enumerate(perm))] += 1
        for k in range(1, 5):
            assert answer('888D', (n, k)) == sum(distribution[:k + 1])
    counts['888D'] = 20
    total = 0
    for recipe in ['B', 'S', 'C', 'BS', 'SC', 'BSC', 'BBSC', 'CCCC']:
        for stock in [(1, 1, 1), (2, 3, 4), (4, 4, 4)]:
            for price in [(1, 1, 1), (1, 3, 2), (4, 2, 1)]:
                for money in range(1, 31):
                    data = (recipe, stock, price, money)
                    valid = [x for x in range(100) if sum(max(0, recipe.count(c) * x - s) * p
                             for c, s, p in zip('BSC', stock, price)) <= money]
                    assert answer('371C', data) == max(valid)
                    total += 1
    counts['371C'] = total
    return counts


def extras(pid):
    rng = random.Random(1600 + int(pid[:-1]))
    cases = []
    def add(text, reason, category='adversarial'):
        data = parse(pid, text)
        cases.append({'input': text, 'output': str(answer(pid, data)) + '\n', 'reason': reason, 'category': category})
    if pid == '235A':
        for n in [1, 2, 3, 4, 6, 9, 12, 18, 999999, 999998, 1000000]:
            add(f'{n}\n', 'parity/divisibility by3 and repeated-number lower limits', 'maxSize' if n == 1000000 else 'boundary')
        for _ in range(60):
            add(f'{rng.randint(1, 10**6)}\n', 'fixed-seed 64-bit LCM range')
    elif pid == '322B':
        for values in [(0, 0, 0), (1, 1, 1), (2, 2, 2), (0, 10**9, 10**9), (10**9,) * 3,
                       (3, 4, 5), (1, 100, 100), (999999998, 999999999, 1000000000)]:
            add(' '.join(map(str, values)) + '\n', 'zero stock, residue classes, color imbalance', 'maxSize' if values == (10**9,) * 3 else 'boundary')
        for values in itertools.product(range(3), repeat=3):
            add(' '.join(map(str, values)) + '\n', 'all27 residue tuples')
        for _ in range(40):
            add(' '.join(str(rng.randint(0, 10**9)) for _ in range(3)) + '\n', 'fixed-seed large color stocks')
    elif pid == '888D':
        for n in [4, 5, 8, 999, 1000]:
            for k in range(1, 5):
                add(f'{n} {k}\n', 'identity, forbidden single displacement, derangements of2/3/4', 'maxSize' if n == 1000 else 'boundary')
        for _ in range(40):
            add(f'{rng.randint(4, 1000)} {rng.randint(1, 4)}\n', 'fixed-seed displacement budget')
    else:
        fixed = [('B', (1, 100, 100), (1, 100, 100), 10**12),
                 ('BSC' * 33 + 'B', (1, 1, 1), (100, 100, 100), 1),
                 ('C' * 100, (100, 100, 100), (1, 1, 1), 10**12),
                 ('BBSSC', (1, 100, 1), (100, 1, 100), 1),
                 ('BSC', (100, 100, 100), (100, 100, 100), 1),
                 ('BC', (2, 100, 2), (3, 100, 5), 8),
                 ('BC', (2, 100, 2), (3, 100, 5), 7)]
        for recipe, stock, price, money in fixed:
            text = recipe + '\n' + ' '.join(map(str, stock)) + '\n' + ' '.join(map(str, price)) + '\n' + str(money) + '\n'
            add(text, 'absent ingredients, inventory breakpoints, exact budget and64-bit answer', 'maxSize' if money == 10**12 else 'boundary')
        for _ in range(50):
            recipe = ''.join(rng.choice('BSC') for _ in range(rng.randint(1, 100)))
            text = recipe + '\n' + ' '.join(str(rng.randint(1, 100)) for _ in range(3)) + '\n' + ' '.join(str(rng.randint(1, 100)) for _ in range(3)) + '\n' + str(rng.randint(1, 10**12)) + '\n'
            add(text, 'fixed-seed all ingredient mixtures and budgets')
    return cases


def review(pid, tests, samples):
    failures = []
    for name, pair in [*tests, *samples]:
        try:
            expected = str(answer(pid, parse(pid, pair['input'])))
            if pair['output'].split() != [expected]:
                raise ValueError('output differs from independent oracle')
        except (ValueError, AssertionError) as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
