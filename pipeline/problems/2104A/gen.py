import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

MAX = 10**8
rng = random.Random(2104)
w = Writer(sys.argv[1])


def case(a, b, c):
    assert 1 <= a < b < c <= MAX
    return f"{a} {b} {c}"


def rand_case(lo=1, hi=MAX):
    vals = rng.sample(range(lo, hi + 1), 3)
    vals.sort()
    return case(*vals)


def yes_case(hi=MAX):
    # construct a YES: pick m, a<b<=m, c = 3m-a-b, ensure ordering
    while True:
        m = rng.randint(2, hi // 3 * 2)
        a = rng.randint(1, m - 1)
        b = rng.randint(a + 1, m)
        c = 3 * m - a - b
        if b < c <= hi:
            return case(a, b, c)


# edges
w.add(multi([case(1, 2, 3), case(1, 2, MAX), case(MAX - 2, MAX - 1, MAX)]))
# small exhaustive
w.add(multi([case(a, b, c) for a in range(1, 9) for b in range(a + 1, 10)
             for c in range(b + 1, 11)]))
# YES-heavy tests
for _ in range(3):
    w.add(multi([yes_case() for _ in range(1000)]))
w.add(multi([yes_case(100) for _ in range(1000)]))
# randoms (mostly NO for big ranges, mixed for small)
for _ in range(6):
    w.add(multi([rand_case() for _ in range(1000)]))
for hi in (10, 30, 100, 1000):
    w.add(multi([rand_case(1, hi) for _ in range(1000)]))
# mixed + max-size t = 10^4
for _ in range(2):
    w.add(multi([yes_case() if rng.random() < 0.5 else rand_case(1, 50)
                 for _ in range(10**4)]))
w.add(multi([yes_case() if rng.random() < 0.3 else rand_case()
             for _ in range(10**4)]))
