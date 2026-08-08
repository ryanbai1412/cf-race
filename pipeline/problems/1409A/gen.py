import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

MAX = 10 ** 9
rng = random.Random(1409)
w = Writer(sys.argv[1])


def case(a, b):
    return f"{a} {b}"


# edges
w.add(multi([case(1, 1), case(1, MAX), case(MAX, 1), case(MAX, MAX),
             case(1, 11), case(11, 1), case(1, 10), case(10, 1),
             case(5, 5), case(1, 2)]))
# exhaustive small
w.add(multi([case(a, b) for a in range(1, 41) for b in range(1, 41)]))
# random small
for hi in (20, 100, 1000):
    w.add(multi([case(rng.randint(1, hi), rng.randint(1, hi))
                 for _ in range(2000)]))
# differences that are exact multiples of 10 / off by one
def aligned():
    a = rng.randint(1, MAX // 2)
    d = 10 * rng.randint(0, 10 ** 7) + rng.choice([-1, 0, 1])
    b = max(1, min(MAX, a + d))
    return case(a, b)


for _ in range(2):
    w.add(multi([aligned() for _ in range(2 * 10 ** 4)]))
# random big
for _ in range(3):
    w.add(multi([case(rng.randint(1, MAX), rng.randint(1, MAX))
                 for _ in range(2 * 10 ** 4)]))
# max size extremes
w.add(multi([case(1, MAX) for _ in range(2 * 10 ** 4)]))
