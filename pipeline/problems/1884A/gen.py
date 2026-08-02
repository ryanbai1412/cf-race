import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

MAX = 10**9
rng = random.Random(1884)
w = Writer(sys.argv[1])


def case(x, k):
    return f"{x} {k}"


# edges
w.add(multi([case(1, 1), case(1, 10), case(MAX, 10), case(MAX, 1),
             case(999999999, 10), case(10**9 - 10**5, 10)]))
# 10^k - 1 style digit-sum cliffs
w.add(multi([case(10**p - d, k) for p in range(1, 10) for d in (0, 1, 2)
             for k in (7, 9, 10)]))
# small exhaustive
w.add(multi([case(x, k) for x in range(1, 201) for k in range(1, 11)]))
# randoms
for _ in range(8):
    w.add(multi([case(rng.randint(1, 10**4), rng.randint(1, 10))
                 for _ in range(1000)]))
for _ in range(6):
    w.add(multi([case(rng.randint(1, MAX), rng.randint(1, 10))
                 for _ in range(1000)]))
# max-size: t = 10^4, worst k
w.add(multi([case(rng.randint(1, MAX), 10) for _ in range(10**4)]))
w.add(multi([case(rng.randint(1, MAX), rng.randint(1, 10)) for _ in range(10**4)]))
w.add(multi([case(999999999, 10)] * 10**4))
