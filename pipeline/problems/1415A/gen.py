import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

MAX = 10 ** 9
rng = random.Random(1415)
w = Writer(sys.argv[1])


def case(n, m, r, c):
    assert 1 <= r <= n <= MAX and 1 <= c <= m <= MAX
    return f"{n} {m} {r} {c}"


def rand_case(hi=MAX):
    n = rng.randint(1, hi)
    m = rng.randint(1, hi)
    return case(n, m, rng.randint(1, n), rng.randint(1, m))


# edges
w.add(multi([case(1, 1, 1, 1), case(MAX, MAX, 1, 1), case(MAX, MAX, MAX, MAX),
             case(MAX, MAX, MAX // 2, MAX // 2), case(1, MAX, 1, 1),
             case(MAX, 1, MAX, 1), case(2, 2, 1, 2), case(1, 1000000000, 1, 500000000)]))
# exhaustive small grids
small = [case(n, m, r, c) for n in range(1, 6) for m in range(1, 6)
         for r in range(1, n + 1) for c in range(1, m + 1)]
w.add(multi(small))
# random small / medium / large
for hi in (10, 1000, 10 ** 6, MAX):
    for _ in range(2):
        w.add(multi([rand_case(hi) for _ in range(10 ** 4)]))
# corners on huge grids
def corner():
    n, m = MAX, MAX
    r = rng.choice([1, n, n // 2, n // 2 + 1])
    c = rng.choice([1, m, m // 2, m // 2 + 1])
    return case(n, m, r, c)


w.add(multi([corner() for _ in range(10 ** 4)]))
w.add(multi([case(MAX, MAX, 1, 1) for _ in range(10 ** 4)]))
