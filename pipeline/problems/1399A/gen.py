import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(1399)
w = Writer(sys.argv[1])


def case(a):
    return f"{len(a)}\n" + " ".join(map(str, a))


def rand_case(n=None, lo=1, hi=100):
    n = n or rng.randint(1, 50)
    return case([rng.randint(lo, hi) for _ in range(n)])


def yes_case(n=None):
    n = n or rng.randint(1, 50)
    start = rng.randint(1, 100 - 3)
    a = [start]
    for _ in range(n - 1):
        a.append(min(100, a[-1] + rng.randint(0, 1)))
    rng.shuffle(a)
    return case(a)


# edges
w.add(multi([case([1]), case([100]), case([1, 100]), case([1, 2]),
             case([50, 50]), case([1] * 50), case(list(range(1, 51))),
             case(list(range(51, 101))), case([1, 3]), case([100, 99])]))
# small dense random (many duplicates -> mixed answers)
for hi in (2, 3, 4, 5, 10):
    w.add(multi([rand_case(rng.randint(1, 6), 1, hi) for _ in range(1000)]))
# yes-heavy
for _ in range(3):
    w.add(multi([yes_case() for _ in range(1000)]))
# random
for _ in range(4):
    w.add(multi([rand_case() for _ in range(1000)]))
# near-yes: consecutive run with one gap
def near():
    n = rng.randint(2, 50)
    a = list(range(1, n + 1))
    if rng.random() < 0.5:
        i = rng.randrange(n)
        a[i] = min(100, a[i] + 2)
    rng.shuffle(a)
    return case(a)


w.add(multi([near() for _ in range(1000)]))
# max size: t = 1000, n = 50 each
w.add(multi([rand_case(50) for _ in range(1000)]))
w.add(multi([yes_case(50) for _ in range(1000)]))
