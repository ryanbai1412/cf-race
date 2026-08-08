import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer

MAXN = 100
MAXV = 600
rng = random.Random(9371)
w = Writer(sys.argv[1])


def case(a):
    return f"{len(a)}\n" + " ".join(map(str, a))


# edges
w.add(case([1]))
w.add(case([MAXV]))
w.add(case([0, 1]))
w.add(case([1, 0]))
w.add(case([0] * 99 + [MAXV]))
w.add(case([MAXV] * MAXN))
w.add(case(list(range(0, MAXN))))
w.add(case([1] * 50 + [0] * 50))
w.add(case(sorted(rng.sample(range(1, MAXV + 1), MAXN), reverse=True)))

# randoms with varying numbers of zeros / duplicates
for hi in (1, 2, 5, 50, MAXV):
    for _ in range(2):
        n = rng.randint(1, MAXN)
        a = [rng.randint(0, hi) for _ in range(n)]
        if not any(a):
            a[rng.randrange(n)] = max(1, hi)
        w.add(case(a))
