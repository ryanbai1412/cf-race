"""595B Pasha and Phone: per-block counts of multiples of a_i outside the b_i leading-digit band."""
import itertools
import random
import re

IDS = ('595B',)
MOD = 10 ** 9 + 7
SEMANTICS = {
    '595B': 'Three lines: n k (1<=n<=100000, 1<=k<=min(n,9), k divides n); m=n/k values a_i with 1<=a_i<10^k; '
            'm digits b_i in 0..9 (exponents attested from the public English statement). A block is the k-digit '
            'zero-padded integer, so its first digit is 0 for values below 10^(k-1). Unique integer: product over '
            'blocks of (multiples of a_i in [0,10^k-1]) minus (multiples in [b_i*10^(k-1),(b_i+1)*10^(k-1)-1]), '
            'modulo 10^9+7. Floor-difference oracle; independently checked by per-leading-digit ceil counts, '
            'zero-padded multiple enumeration for every a_i,b_i with k<=4, and literal phone-number enumeration n<=4.',
}

_NUMBER = re.compile(r'0|[1-9][0-9]*')


def _line_tokens(line):
    tokens = line.split(' ')
    if not all(_NUMBER.fullmatch(t) for t in tokens):
        raise ValueError('malformed token or spacing')
    return [int(t) for t in tokens]


def parse(pid, text):
    if pid != '595B':
        raise ValueError('unknown problem ' + pid)
    body = text.replace('\r\n', '\n')
    if '\r' in body:
        raise ValueError('stray carriage return')
    lines = body.split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    if len(lines) != 3:
        raise ValueError('expected exactly three lines')
    header = _line_tokens(lines[0])
    if len(header) != 2:
        raise ValueError('header arity')
    n, k = header
    if not (1 <= n <= 100000 and 1 <= k <= min(n, 9) and n % k == 0):
        raise ValueError('n/k constraints')
    a, b = _line_tokens(lines[1]), _line_tokens(lines[2])
    m = n // k
    if len(a) != m or len(b) != m:
        raise ValueError('sequence arity')
    if not all(1 <= x < 10 ** k for x in a):
        raise ValueError('a_i range')
    if not all(0 <= y <= 9 for y in b):
        raise ValueError('b_i range')
    return n, k, tuple(a), tuple(b)


def block_count(k, a, b):
    p = 10 ** (k - 1)
    return (10 * p - 1) // a + 1 - (((b + 1) * p - 1) // a - (b * p - 1) // a)


def answer(pid, data):
    _, k, a, b = data
    result = 1
    for x, y in zip(a, b):
        result = result * block_count(k, x, y) % MOD
    return result


def band_count(k, a, b):
    p = 10 ** (k - 1)
    total = 0
    for digit in range(10):
        if digit != b:
            lo, hi = digit * p, (digit + 1) * p - 1
            total += max(0, hi // a - -(-lo // a) + 1)
    return total


def _tree_product(values):
    values = list(values) or [1]
    while len(values) > 1:
        values = [values[i] * values[i + 1] % MOD if i + 1 < len(values) else values[i]
                  for i in range(0, len(values), 2)]
    return values[0] % MOD


def band_oracle(data):
    _, k, a, b = data
    return _tree_product(band_count(k, x, y) for x, y in zip(a, b))


def leading_histogram(k, a):
    histogram = [0] * 10
    for value in range(0, 10 ** k, a):
        histogram[int(str(value).zfill(k)[0])] += 1
    return histogram


def enumerated_count(k, a, b):
    histogram = leading_histogram(k, a)
    return sum(histogram) - histogram[b]


def phone_brute(data):
    n, k, a, b = data
    good = 0
    for digits in itertools.product('0123456789', repeat=n):
        phone = ''.join(digits)
        blocks = [phone[i:i + k] for i in range(0, n, k)]
        good += all(block[0] != str(y) and int(block) % x == 0 for block, x, y in zip(blocks, a, b))
    return good % MOD


def _format(n, k, a, b):
    return f'{n} {k}\n' + ' '.join(map(str, a)) + '\n' + ' '.join(map(str, b)) + '\n'


def extras(pid):
    if pid != '595B':
        raise ValueError('unknown problem ' + pid)
    rng = random.Random(5950595)
    cases, seen = [], set()

    def add(k, a, b, reason, category):
        text = _format(len(a) * k, k, a, b)
        if text in seen:
            return
        seen.add(text)
        cases.append({'input': text, 'output': f'{answer(pid, parse(pid, text))}\n',
                      'reason': reason, 'category': category})

    for a, b in ((1, 0), (1, 9), (9, 0), (9, 9), (1, 5), (5, 5), (7, 0), (3, 3)):
        add(1, [a], [b], 'minimum n=k=1; digit 0 is itself a block starting with 0', 'boundary')
    add(1, list(range(1, 10)), [0] * 9, 'k=1 with b=0 for every a: zero excluded (10*(k-1) typo, clamped floor(-1/a))', 'boundary')
    add(1, list(range(1, 10)), [9] * 9, 'k=1 with b=9 for every a', 'boundary')
    for k in range(2, 10):
        p = 10 ** (k - 1)
        add(k, [10 * p - 1], [0], 'a=10^k-1 divides the top value (ceil total off by one); only 0 and 10^k-1', 'boundary')
        add(k, [10 * p - 1], [9], 'a=10^k-1 with b=9 excludes 10^k-1', 'boundary')
        add(k, [p], [0], 'a=10^(k-1): one multiple per leading digit', 'boundary')
        add(k, [2 ** k, 5 ** k], [1, 0], 'a divides 10^k (10^k//a+1 total off by one)', 'boundary')
        add(k, [1, 1], [0, 9], 'a=1: 9*10^(k-1) per block', 'boundary')
        add(k, [3, 7], [0, 0], 'b=0 band [0,10^(k-1)-1] includes zero', 'boundary')
    for a in (2, 5, 10 ** 8, 999999999, 111111111, 333333333, 500000000, 999999998, 512, 1953125, 536870912, 142857):
        add(9, [a], [int(str(a).zfill(9)[0])], 'k=9 single block, b equals the leading digit of a', 'boundary')
    for _ in range(25):
        k = rng.randint(1, 9)
        p = 10 ** (k - 1)
        m = rng.randint(1, 12)
        a = [rng.randint(1, min(p - 1, 999)) if p > 1 and rng.randrange(2) else rng.randint(1, 10 * p - 1) for _ in range(m)]
        add(k, a, [0] * m, 'fixed-seed b=0 blocks with small a: zero-padded leading digit is 0 (unpadded str(v)[0] trap)', 'adversarial')
    for _ in range(25):
        k = rng.randint(1, 9)
        p = 10 ** (k - 1)
        m = rng.randint(2, 30)
        a = [rng.choice([d for d in (1, 2, 4, 5, 8, 10, 16, 20, 25, 3, 9, 11, 27, 37, 99, 101, 111, 333, 999, 1001, 3367, 9091, 11111)
                         if d < 10 * p] + [rng.randint(1, 10 * p - 1)]) for _ in range(m)]
        add(k, a, [rng.randrange(10) for _ in range(m)], 'fixed-seed divisors of 10^k and 10^k-1; product exceeds 10^9+7', 'adversarial')
    for _ in range(35):
        k = rng.randint(1, 9)
        p = 10 ** (k - 1)
        m = rng.randint(1, 40)
        a = [rng.randint(max(1, 10 * p - 1 - rng.randint(0, 3 * p)), 10 * p - 1) if rng.randrange(3) == 0 else rng.randint(1, 10 * p - 1)
             for _ in range(m)]
        add(k, a, [rng.randrange(10) for _ in range(m)], 'fixed-seed mixed a including near 10^k, all b digits', 'adversarial')
    add(1, [1] * 100000, [0] * 100000, 'maximum n=100000, k=1: 9^100000 mod 10^9+7', 'maxSize')
    add(1, [rng.randint(1, 9) for _ in range(100000)], [rng.randrange(10) for _ in range(100000)], 'maximum n=100000, k=1 random', 'maxSize')
    for k in (2, 4, 5, 8):
        m = 100000 // k
        add(k, [rng.randint(1, 10 ** k - 1) for _ in range(m)], [rng.randrange(10) for _ in range(m)], f'maximum n=100000, k={k} random', 'maxSize')
    add(9, [1] * 11111, [9] * 11111, 'largest legal n=99999 with k=9, a=1: (9*10^8)^11111', 'maxSize')
    add(9, [rng.randint(1, 999999999) for _ in range(11111)], [rng.randrange(10) for _ in range(11111)], 'largest legal n=99999 with k=9 random', 'maxSize')
    add(9, [999999999] * 11111, [0] * 11111, 'n=99999, k=9, a=10^9-1, b=0: one choice per block', 'maxSize')
    return cases


def brute_checks():
    count = 0
    for k in range(1, 5):
        for a in range(1, 10 ** k):
            histogram = leading_histogram(k, a)
            for b in range(10):
                assert answer('595B', (k, k, (a,), (b,))) == sum(histogram) - histogram[b], (k, a, b)
                count += 1
    rng = random.Random(5959595)
    for _ in range(300):
        k = rng.randint(5, 9)
        a = rng.randint(max(1, 10 ** k // 20000), 10 ** k - 1)
        histogram = leading_histogram(k, a)
        for b in range(10):
            assert answer('595B', (k, k, (a,), (b,))) == sum(histogram) - histogram[b], (k, a, b)
            count += 1
    for n in range(1, 5):
        for k in (d for d in range(1, n + 1) if n % d == 0):
            for _ in range(12 if n == 4 else 30):
                m = n // k
                data = (n, k, tuple(rng.randint(1, 10 ** k - 1) for _ in range(m)), tuple(rng.randrange(10) for _ in range(m)))
                assert answer('595B', data) == phone_brute(data), data
                count += 1
    cache = {}
    for _ in range(300):
        k = rng.randint(1, 4)
        m = rng.randint(2, 300)
        a = [rng.randint(1, 10 ** k - 1) for _ in range(m)]
        b = [rng.randrange(10) for _ in range(m)]
        exact = 1
        for x, y in zip(a, b):
            if (k, x) not in cache:
                cache[k, x] = leading_histogram(k, x)
            exact *= sum(cache[k, x]) - cache[k, x][y]
        assert answer('595B', (m * k, k, tuple(a), tuple(b))) == exact % MOD
        count += 1
    return {'595B': count}


def review(pid, tests, samples):
    failures = []
    for name, pair in [*tests, *samples]:
        try:
            data = parse(pid, pair['input'])
            expected = answer(pid, data)
            if band_oracle(data) != expected:
                raise ValueError('oracle self-inconsistency')
            actual = pair['output'].replace('\r\n', '\n').rstrip('\n').split('\n')
            if actual != [str(expected)]:
                failures.append({'test': name, 'reason': 'output differs from independent oracle',
                                 'expected': [str(expected)], 'actual': pair['output'].split()[:5]})
        except ValueError as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
