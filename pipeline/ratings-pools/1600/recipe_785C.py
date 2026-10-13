"""Rating-1600 recipe for 785C Anton and Fairy Tale (barn emptying day)."""
import math
import random
import re


IDS = ('785C',)
LIMIT = 10**18
SEMANTICS = {
    '785C': 'Single line "n m" with 1<=n,m<=10^18 (public English statement shows 10<sup>18</sup>; pinned row flattened it to 1018 and official tests use 1000000000000000000). '
            'Barn of capacity n starts full; on day i, m grains are added (capped at n), then i sparrows each eat one grain if any remain. '
            'Unique integer: first day at whose end the barn is empty. If m>=n the barn is full every morning and day n empties it, so the answer is n; '
            'otherwise the barn stays full through day m and afterwards loses (i-m) net per day, so the answer is m+k for the least k with k(k+1)/2>=n-m. '
            'Literal day-by-day simulation exhaustively cross-checks small n,m; an integer-isqrt closed form cross-checks large cases.',
}
LINE = re.compile(r'([1-9][0-9]*) ([1-9][0-9]*)')


def parse(pid, text):
    if pid not in IDS:
        raise ValueError('unknown problem')
    body = text
    if body.endswith('\n'):
        body = body[:-1]
        if body.endswith('\r'):
            body = body[:-1]
    if '\n' in body or '\r' in body:
        raise ValueError('input must be exactly one line')
    match = LINE.fullmatch(body)
    if not match:
        raise ValueError('line must be "n m": two unsigned integers separated by one space')
    n, m = int(match.group(1)), int(match.group(2))
    if not (1 <= n <= LIMIT and 1 <= m <= LIMIT):
        raise ValueError('n or m outside 1..10^18')
    return n, m


def answer(pid, data):
    n, m = data
    if m >= n:
        return n
    rest = n - m
    lo, hi = 1, 2 * 10**9
    while lo < hi:
        mid = (lo + hi) // 2
        if mid * (mid + 1) // 2 >= rest:
            hi = mid
        else:
            lo = mid + 1
    return m + lo


def closed_form(data):
    n, m = data
    if m >= n:
        return n
    rest = n - m
    k = (math.isqrt(8 * rest + 1) - 1) // 2
    if k * (k + 1) // 2 < rest:
        k += 1
    return m + k


def brute(pid, data, max_days=10**6):
    n, m = data
    grain = n
    for day in range(1, max_days + 1):
        grain = min(n, grain + m)
        grain = max(0, grain - day)
        if grain == 0:
            return day
    raise ValueError('simulation bound exceeded')


def _tri(k):
    return k * (k + 1) // 2


def _float_sqrt_answer(n, m):
    if m >= n:
        return n
    return math.ceil((-1 + math.sqrt(1 + 8 * (n - m))) / 2) + m


def extras(pid):
    if pid not in IDS:
        raise ValueError('unknown problem')
    cases, seen = [], set()

    def add(n, m, category, reason):
        text = f'{n} {m}\n'
        if text in seen:
            return
        parse(pid, text)
        seen.add(text)
        cases.append({'input': text, 'output': str(answer(pid, (n, m))) + '\n',
                      'reason': reason, 'category': category})

    add(1, 1, 'boundary', 'minimum n and m; day 1 empties a one-grain barn')
    add(1, LIMIT, 'boundary', 'minimum n with maximum m; answer n=1, not m or m+1')
    add(2, 1, 'boundary', 'smallest m<n case')
    add(1, 2, 'boundary', 'm=n+1; answer n')
    add(3, 1, 'boundary', 'n-m=2 needs k=2')
    add(4, 1, 'boundary', 'n-m=3 is triangular T2')
    add(5, 1, 'boundary', 'n-m=4 just above T2')
    for n in (2, 3, 7, 10, 100, 12345, 10**9, 10**12, LIMIT - 1, LIMIT):
        add(n, n, 'boundary', 'm=n: barn refills fully every day, answer n (m+1 is wrong)')
    for n in (2, 3, 10, 1000, 10**9 + 7, 10**15, LIMIT):
        add(n, n - 1, 'boundary', 'm=n-1: n-m=1 so the answer is m+1=n')
    for n in (5, 50, 999, 10**9, 10**17):
        add(n, n + 1, 'boundary', 'm=n+1: m>=n branch')
        add(n, 2 * n, 'boundary', 'm much larger than n: answer n')

    add(LIMIT, 1, 'maxSize', 'maximum n with minimum m: largest answer, k about 1.414e9 exceeds a 1e9 search bound')
    add(LIMIT, LIMIT, 'maxSize', 'both maximum; answer 10^18')
    add(LIMIT, 2, 'maxSize', 'maximum n, small m')
    add(LIMIT, 10**9, 'maxSize', 'maximum n, m=10^9')
    add(LIMIT, LIMIT // 2, 'maxSize', 'maximum n, m=n/2')
    add(LIMIT, LIMIT - 10**9, 'maxSize', 'maximum n, n-m=10^9')
    add(LIMIT - 1, LIMIT, 'maxSize', 'm>n near the maximum')
    add(LIMIT, LIMIT - 1, 'maxSize', 'maximum n with n-m=1')

    kmax = closed_form((LIMIT, 1)) - 1
    for k in (kmax, kmax - 1, kmax - 2, 10**9, 10**9 + 1, 999999999, 1 << 30, (1 << 30) + 1, 1414213562):
        t = _tri(k)
        for m in (1, 7):
            for delta in (-1, 0, 1):
                n = t + m + delta
                if 1 <= n <= LIMIT and m < n:
                    add(n, m, 'adversarial',
                        f'n-m at triangular threshold T({k}){delta:+d}: >= vs > and isqrt/floating rounding near k~1e9')

    for k in (1, 2, 3, 4, 10, 44, 45, 1000, 65535, 65536, 10**8):
        t = _tri(k)
        for delta in (-1, 0, 1):
            m = 10**6 + k
            n = t + m + delta
            if m < n <= LIMIT:
                add(n, m, 'adversarial', f'triangular threshold T({k}){delta:+d} with m=10^6+{k}; off-by-one on the day count')

    rng = random.Random(785003)
    float_hits = 0
    attempts = 0
    while float_hits < 20 and attempts < 200000:
        attempts += 1
        k = rng.randrange(10**8, kmax + 1)
        m = rng.randrange(1, 10**6)
        n = _tri(k) + m + rng.choice((-1, 0, 1, -2, 2))
        if not (m < n <= LIMIT):
            continue
        if _float_sqrt_answer(n, m) != closed_form((n, m)):
            before = len(cases)
            add(n, m, 'adversarial', 'double-precision sqrt formula (selected WA 207785393) rounds to the wrong day here')
            float_hits += len(cases) - before

    for _ in range(12):
        m = rng.randrange(1, 10**18)
        n = rng.randrange(m + 1, LIMIT + 1) if m < LIMIT else LIMIT
        add(n, m, 'adversarial', 'random large m<n: integer square-root region, 64-bit overflow in k(k+1) with wide search bounds')
    for _ in range(6):
        n = rng.randrange(1, 10**18)
        m = rng.randrange(n, LIMIT + 1)
        add(n, m, 'adversarial', 'random large m>=n: answer n, sources printing m+1 or m are wrong')
    for _ in range(20):
        n = rng.randrange(1, 300)
        m = rng.randrange(1, 300)
        add(n, m, 'adversarial', 'fixed-seed random small case (literal-simulation checkable)')
    for _ in range(8):
        n = rng.randrange(10**3, 10**6)
        m = rng.randrange(1, 5000)
        add(n, m, 'adversarial', 'fixed-seed random medium case (literal-simulation checkable)')
    return cases


def review(pid, tests, samples):
    failures = []
    for name, pair in list(tests) + list(samples):
        try:
            expected = [str(answer(pid, parse(pid, pair['input'])))]
        except ValueError as exc:
            failures.append({'test': name, 'reason': str(exc)})
            continue
        if expected != pair['output'].split():
            failures.append({'test': name, 'reason': 'independent oracle disagreement',
                             'expected': expected, 'actual': pair['output'].split()[:5]})
    return failures


def brute_checks():
    count = 0
    for n in range(1, 151):
        for m in range(1, 151):
            expected = brute('785C', (n, m))
            if answer('785C', (n, m)) != expected or closed_form((n, m)) != expected:
                raise AssertionError(f'785C mismatch at n={n} m={m}')
            count += 1
    rng = random.Random(7851)
    for _ in range(400):
        m = rng.randrange(1, 4000)
        n = rng.randrange(1, 10**6)
        expected = brute('785C', (n, m))
        if answer('785C', (n, m)) != expected or closed_form((n, m)) != expected:
            raise AssertionError(f'785C mismatch at n={n} m={m}')
        count += 1
    for _ in range(20000):
        n = rng.randrange(1, LIMIT + 1)
        m = rng.randrange(1, LIMIT + 1) if rng.random() < 0.3 else rng.randrange(1, 10**rng.randrange(1, 19))
        got = answer('785C', (n, m))
        if got != closed_form((n, m)):
            raise AssertionError(f'785C closed-form mismatch at n={n} m={m}')
        if m < n:
            k = got - m
            if not (_tri(k) >= n - m > _tri(k - 1)):
                raise AssertionError(f'785C minimality failure at n={n} m={m}')
        count += 1
    for case in extras('785C'):
        data = parse('785C', case['input'])
        if int(case['output']) != closed_form(data):
            raise AssertionError('785C extras mismatch')
        count += 1
    return {'785C': count}
