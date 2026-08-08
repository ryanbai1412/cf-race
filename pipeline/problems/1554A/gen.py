import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(1554)
w = Writer(sys.argv[1])
SUMN = 300000
MAXA = 10 ** 6


def case(a):
    return f"{len(a)}\n" + " ".join(map(str, a))


def rand_case(n, lo=1, hi=MAXA):
    return case([rng.randint(lo, hi) for _ in range(n)])


# minimal sizes and extremes
w.add(multi([case([1, 1]), case([MAXA, MAXA]), case([1, MAXA]), case([MAXA, 1]),
             case([1, 1, 1]), case([MAXA] * 3), case([1, MAXA, 1]),
             case([MAXA, 1, MAXA])]))
# one big single case, all maximum
w.add(multi([case([MAXA] * 100000)]))
# strictly increasing / decreasing single big cases
w.add(multi([case(list(range(1, 100001)))]))
w.add(multi([case(list(range(100000, 0, -1)))]))
# alternating tiny/huge: best pair is a neighbouring pair, not the two maxima
w.add(multi([case([MAXA if i % 2 == 0 else 1 for i in range(100000)])]))
# two big values far apart, everything else small
a = [1] * 100000
a[0] = MAXA
a[-1] = MAXA
a[50000] = MAXA - 1
w.add(multi([case(a)]))
# random big cases (sum n <= 3e5)
w.add(multi([rand_case(100000), rand_case(100000), rand_case(100000)]))
w.add(multi([rand_case(150000, 1, 10), rand_case(150000, MAXA - 5, MAXA)]))
# many small random cases
for _ in range(4):
    cases = []
    left = SUMN
    while left >= 2 and len(cases) < 10000:
        n = rng.randint(2, min(20, left))
        cases.append(rand_case(n, 1, rng.choice([3, 100, MAXA])))
        left -= n
    w.add(multi(cases))
# max t with n=2 each
w.add(multi([rand_case(2) for _ in range(10000)]))
# medium random cases
for _ in range(2):
    cases = []
    left = SUMN
    while left >= 2 and len(cases) < 300:
        n = rng.randint(2, min(1000, left))
        cases.append(rand_case(n))
        left -= n
    w.add(multi(cases))
