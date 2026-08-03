import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

MAXV = 10**5
rng = random.Random(2053)
w = Writer(sys.argv[1])


def case(a):
    return f"{len(a)}\n{' '.join(map(str, a))}"


# edges: pairs on the 2*min > max boundary
w.add(multi([case([1, 1]), case([1, 2]), case([2, 1]), case([1, MAXV]),
             case([MAXV, MAXV]), case([2, 3]), case([3, 2])] +
            [case([k, 2 * k]) for k in (1, 2, 50, 50000)] +
            [case([k, 2 * k - 1]) for k in (1, 2, 50, 50000)]))
# small exhaustive pairs
w.add(multi([case([a, b]) for a in range(1, 11) for b in range(1, 11)]))
# geometric growth (all NO) and near-equal (YES)
w.add(multi([case([2**i for i in range(17)]),
             case([v for v in range(100, 300)]),
             case([1] * 200)]))
# randoms
for hi in (3, 10, 100, MAXV):
    for _ in range(3):
        w.add(multi([case([rng.randint(1, hi) for _ in range(rng.randint(2, 200))])
                     for _ in range(rng.randint(20, 200))]))
# max-size: t = 200, n = 200
w.add(multi([case([rng.randint(1, MAXV) for _ in range(200)]) for _ in range(200)]))
w.add(multi([case([rng.choice([1, 3, 9, 27, 81]) for _ in range(200)])
             for _ in range(200)]))
w.add(multi([case(sorted(rng.randint(1, MAXV) for _ in range(200))) for _ in range(200)]))
# adversarial for quadratic DPs: no stable segment longer than 1, so
# O(n^2) scans never break early — alternating huge/small values
w.add(multi([case([MAXV if i % 2 == 0 else 1 for i in range(200)]) for _ in range(200)]))
w.add(multi([case([(MAXV if i % 2 == 0 else 1 + (i % 3)) for i in range(200)]) for _ in range(200)]))
