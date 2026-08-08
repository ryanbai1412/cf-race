import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer

MAXV = 10**9
rng = random.Random(9121)
w = Writer(sys.argv[1])


def case(a, b, x, y, z):
    return f"{a} {b}\n{x} {y} {z}"


# edges
w.add(case(0, 0, 0, 0, 0))
w.add(case(MAXV, MAXV, 0, 0, 0))
w.add(case(0, 0, MAXV, MAXV, MAXV))
w.add(case(MAXV, MAXV, MAXV, MAXV, MAXV))
w.add(case(0, 0, 1, 0, 0))
w.add(case(0, 0, 0, 1, 0))
w.add(case(0, 0, 0, 0, 1))
w.add(case(2, 0, 1, 0, 0))
w.add(case(1, 1, 0, 1, 0))
w.add(case(0, 3, 0, 0, 1))
w.add(case(MAXV, 0, 0, MAXV, 0))
w.add(case(0, MAXV, 0, MAXV, 0))

# randoms
for hi in (3, 10, 10**5, MAXV):
    for _ in range(2):
        w.add(case(rng.randint(0, hi), rng.randint(0, hi),
                   rng.randint(0, hi), rng.randint(0, hi), rng.randint(0, hi)))
