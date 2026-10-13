"""Matrix (364A / 365C): rectangles of b_ij = s_i*s_j whose cell sum equals a."""
import itertools
import random
import re


IDS = ('364A',)
SEMANTICS = {
    '364A': 'Line 1: integer a, 0<=a<=10^9 (exponent attested from the public English statement). Line 2: digit string s, 1<=|s|<=4000. '
            'Unique integer: number of (x<=y, z<=t) whose rectangle sum of s_i*s_j equals a; the sum factorises as (s_x+..+s_y)*(s_z+..+s_t), so the answer is the number of ordered pairs of substrings whose digit sums multiply to a. '
            'Oracle: interval-sum counts for the divisors d of a with d, a/d <= 9|s|; a=0 gives 2*c0*T-c0^2 with T=|s|(|s|+1)/2. '
            'Independently checked by literal rectangle enumeration on the product matrix and a full big-integer autocorrelation histogram with a complete divisor scan.',
}

MAX_LENGTH = 4000
MAX_A = 10 ** 9
INTEGER = re.compile(r'0|[1-9][0-9]*')
DIGITS = re.compile(r'[0-9]+')


def parse(pid, text):
    if pid not in IDS:
        raise ValueError('unknown problem')
    lines = text.splitlines()
    if len(lines) != 2:
        raise ValueError('matrix line layout')
    a, s = lines
    if not INTEGER.fullmatch(a) or int(a) > MAX_A:
        raise ValueError('a constraints')
    if not DIGITS.fullmatch(s) or len(s) > MAX_LENGTH:
        raise ValueError('digit string constraints')
    return int(a), s


def prefix_counts(s):
    counts, total = {0: 1}, 0
    for c in s:
        total += ord(c) - 48
        counts[total] = counts.get(total, 0) + 1
    return counts, total


def interval_count(counts, value):
    if value == 0:
        return sum(h * (h - 1) // 2 for h in counts.values())
    return sum(h * counts.get(p + value, 0) for p, h in counts.items())


def answer(pid, data):
    a, s = data
    counts, top = prefix_counts(s)
    if a == 0:
        zero, every = interval_count(counts, 0), len(s) * (len(s) + 1) // 2
        return 2 * zero * every - zero * zero
    cache, total, d = {}, 0, 1
    while d * d <= a and d <= top:
        if a % d == 0 and a // d <= top:
            for v in {d, a // d}:
                if v not in cache:
                    cache[v] = interval_count(counts, v)
            total += cache[d] * cache[a // d] * (1 if d * d == a else 2)
        d += 1
    return total


def literal_rectangles(data):
    a, s = data
    digits = [int(c) for c in s]
    n = len(digits)
    pre = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(n):
            pre[i + 1][j + 1] = digits[i] * digits[j] + pre[i][j + 1] + pre[i + 1][j] - pre[i][j]
    return sum(pre[y + 1][t + 1] - pre[x][t + 1] - pre[y + 1][z] + pre[x][z] == a
               for x in range(n) for y in range(x, n) for z in range(n) for t in range(z, n))


def histogram(s):
    digits = [int(c) for c in s]
    top = sum(digits)
    hist = [0] * (top + 1)
    p = 0
    hist[0] += 1
    for v in digits:
        p += v
        hist[p] += 1
    forward = int.from_bytes(b''.join(h.to_bytes(8, 'little') for h in hist), 'little')
    backward = int.from_bytes(b''.join(h.to_bytes(8, 'little') for h in reversed(hist)), 'little')
    product = (forward * backward).to_bytes((2 * top + 2) * 8, 'little')
    lag = [int.from_bytes(product[(top + k) * 8:(top + k + 1) * 8], 'little') for k in range(top + 1)]
    lag[0] = (lag[0] - len(digits) - 1) // 2
    return lag


def histogram_oracle(data):
    a, s = data
    cnt = histogram(s)
    top = len(cnt) - 1
    total = 0
    for x in range(top + 1):
        if a == 0:
            total += cnt[x] * (sum(cnt) if x == 0 else cnt[0])
        elif x and a % x == 0 and a // x <= top:
            total += cnt[x] * cnt[a // x]
    return total


def quadratic_oracle(data):
    a, s = data
    digits = [int(c) for c in s]
    sums = {}
    for i in range(len(digits)):
        run = 0
        for j in range(i, len(digits)):
            run += digits[j]
            sums[run] = sums.get(run, 0) + 1
    return sum(cx * cy for x, cx in sums.items() for y, cy in sums.items() if x * y == a)


def render(a, s):
    return f'{a}\n{s}\n'


def extras(pid):
    rng = random.Random(3640364)
    cases, seen = [], set()

    def add(a, s, reason, category='adversarial'):
        text = render(a, s)
        if text in seen:
            return
        seen.add(text)
        cases.append({'input': text, 'output': f'{answer(pid, parse(pid, text))}\n', 'reason': reason, 'category': category})

    for d in '0123456789':
        add(int(d) ** 2, d, f'|s|=1, single cell {d}*{d} equal to a', 'boundary')
    add(0, '5', 'a=0 with a single nonzero cell', 'boundary')
    add(1, '0', 'a=1 with a single zero cell', 'boundary')
    add(MAX_A, '9', 'maximum a with minimum string', 'boundary')
    add(MAX_A, '0', 'maximum a, all-zero minimum string', 'boundary')
    add(0, '00', 'a=0, every rectangle zero', 'boundary')
    add(0, '10', 'a=0, zero row/column times anything', 'boundary')
    add(0, '01', 'a=0, zero digit first', 'boundary')
    add(81, '99', 'square a with equal factors', 'boundary')
    add(9, '91', 'a=9 from 9*1 and 1*9 ordered pairs', 'boundary')

    add(0, '1230', 'a=0 mixing zero and nonzero sums (not |s|^2, not zero-only)')
    add(0, '0011', 'a=0: zero interval times nonzero interval counted in both orders')
    add(0, '123', 'a=0 without any zero digit: answer 0, not |s|^2')
    add(0, '9' * 30, 'a=0 with no zero interval')
    add(0, '000', 'a=0 all zeros: all T^2 rectangles')
    add(0, '0' * 40 + '7', 'a=0 dominated by zeros with one nonzero tail')
    add(0, '7' + '0' * 40, 'a=0 nonzero head then zeros')
    add(0, '1010101', 'a=0 alternating zeros')
    add(0, '5005', 'a=0 zero block inside nonzero')
    add(1, '000000', 'a>0 with all-zero string: no divisor search over zero sums')
    add(7, '0' * 25, 'all-zero string and positive a (sum(s)=0 division trap)')
    add(5, '15', 'a=5: pairs (1,5) and (5,1) each counted, not once')
    add(6, '16', 'a=s1*s2 single-interval factors counted twice')
    add(12, '1111111111111', 'a=12 from many divisor pairs of ones')
    add(16, '11111111111111111', 'square a=16 with diagonal pair counted once')
    add(36, '123', 'a=36 only from whole-string sum 6*6; 2*18 and 3*12 unreachable')
    add(4, '2020', 'square a with zero padding around factor intervals')
    add(1, '1', 'a=1 single one')
    add(1, '101', 'a=1 with zero-extended unit intervals')
    add(2, '10001', 'a=2 needs interval sum 2 spanning zeros')
    add(100, '55' * 10, 'a=100 from 10*10 and 5*20 etc')
    add(999999937, '9' * 50, 'large prime a: only 1*a pair exceeds the digit-sum range')
    add(2 * 36001, '9' * 200, 'divisor 36001 beyond maximal sum must be skipped')
    add(36000 * 9, '9' * 4000, 'interval sum exactly 36000 (array sized 36000 off-by-one)', 'maxSize')
    add(36000 * 36000 // 1296, '9' * 4000, 'a=10^6 from many balanced factor pairs of nine-multiples', 'maxSize')
    add(31250 * 32000, '8' * 4000, 'a=10^9=31250*32000 with all eights', 'maxSize')
    add(0, '0' * 4000, 'maximum all-zero string a=0: answer T^2=64032004000000 overflows 32-bit', 'maxSize')
    add(1, '0' * 3999 + '1', 'maximum length single one, huge zero-extended counts', 'maxSize')
    add(1, '1' * 4000, 'a=1 with 4000 unit intervals squared', 'maxSize')
    add(16000000, '1' * 4000, 'a=4000^2 whole string squared', 'maxSize')
    add(0, '9' * 4000, 'a=0 no zero digit at maximum length', 'maxSize')
    add(81, '09' * 2000, 'alternating 0/9, a=81', 'maxSize')
    add(735134400, ''.join(rng.choice('0123456789') for _ in range(MAX_LENGTH)), 'highly composite a (1344 divisors), random digits', 'maxSize')
    add(MAX_A, ''.join(rng.choice('789') for _ in range(MAX_LENGTH)), 'maximum a with large interval sums', 'maxSize')
    add(0, ''.join(rng.choice('0000000001') for _ in range(MAX_LENGTH)), 'a=0, sparse ones, overflow-sized answer', 'maxSize')
    add(1, ''.join(rng.choice('0000000001') for _ in range(MAX_LENGTH)), 'a=1, sparse ones, many zero-extended unit intervals', 'maxSize')
    add(720720, ''.join(rng.choice('0123456789') for _ in range(MAX_LENGTH)), 'composite a, random digits', 'maxSize')

    for _ in range(60):
        n = rng.randint(1, 8)
        pool = rng.choice(['01', '012', '0123456789', '19', '0009', '5'])
        s = ''.join(rng.choice(pool) for _ in range(n))
        sums = [sum(map(int, s[i:j])) for i in range(n) for j in range(i + 1, n + 1)]
        a = rng.choice([0, rng.choice(sums) * rng.choice(sums), rng.randint(0, 100)])
        add(a, s, 'fixed-seed small case (literal-rectangle checkable)')
    for _ in range(45):
        n = rng.randint(9, 200)
        pool = rng.choice(['01', '0123', '0123456789', '789', '0009'])
        s = ''.join(rng.choice(pool) for _ in range(n))
        x, y = rng.randint(0, n * 9), rng.randint(1, 60)
        a = rng.choice([0, x * y, rng.randint(1, MAX_A), rng.randint(1, 1000)])
        add(min(a, MAX_A), s, 'fixed-seed medium case with achievable products')
    return cases


def brute_checks():
    rng = random.Random(3640365)
    count = 0

    def check(data, literal):
        nonlocal count
        expected = answer('364A', data)
        assert expected == histogram_oracle(data), data
        assert expected == quadratic_oracle(data), data
        count += 2
        if literal:
            assert expected == literal_rectangles(data), data
            count += 1

    for n in range(1, 5):
        for word in itertools.product('0129', repeat=n):
            s = ''.join(word)
            for a in (0, 1, 2, 4, 9, 18, 36, 81, 144, 1000):
                check((a, s), True)
    for _ in range(400):
        n = rng.randint(1, 9)
        s = ''.join(rng.choice('0123456789') for _ in range(n))
        a = rng.choice([0, rng.randint(1, 400), rng.randint(1, MAX_A)])
        check((a, s), True)
    for _ in range(150):
        n = rng.randint(10, 300)
        s = ''.join(rng.choice(rng.choice(['01', '0123456789', '9', '00001'])) for _ in range(n))
        product = rng.randint(0, 9 * n) * rng.randint(0, 9 * n)
        check((rng.choice([0, min(product, MAX_A), rng.randint(1, MAX_A)]), s), False)
    return {'364A': count}


def review(pid, tests, samples):
    failures = []
    for name, pair in list(tests) + list(samples):
        try:
            expected = str(answer(pid, parse(pid, pair['input'])))
        except ValueError as exc:
            failures.append({'test': name, 'reason': str(exc)})
            continue
        if pair['output'].split() != [expected]:
            failures.append({'test': name, 'reason': 'independent oracle disagreement', 'expected': [expected], 'actual': pair['output'].split()[:15]})
    return failures
