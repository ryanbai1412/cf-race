import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

MAX = 10**9
MAXT = 10000
rng = random.Random(1551)
w = Writer(sys.argv[1])

# edge: smallest values and all residues mod 3
w.add(multi([str(v) for v in range(1, 31)]))
# near max, all residues
w.add(multi([str(MAX - d) for d in range(0, 10)] + [str(MAX)]))
# every residue class at various magnitudes
cases = []
for mag in (10, 100, 1000, 10**5, 10**7, 10**9):
    for d in (-2, -1, 0):
        v = mag + d
        if v >= 1:
            cases.append(str(v))
w.add(multi(cases))
# random small
for _ in range(3):
    w.add(multi([str(rng.randint(1, 100)) for _ in range(MAXT)]))
# random full range
for _ in range(6):
    w.add(multi([str(rng.randint(1, MAX)) for _ in range(MAXT)]))
# max size, values near max
w.add(multi([str(rng.randint(MAX - 100, MAX)) for _ in range(MAXT)]))
# multiples of 3 only / off by one
w.add(multi([str(3 * rng.randint(1, MAX // 3)) for _ in range(MAXT)]))
w.add(multi([str(3 * rng.randint(1, MAX // 3) + rng.choice((1, 2)))
             for _ in range(MAXT)]))
