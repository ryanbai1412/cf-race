import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(1553)
w = Writer(sys.argv[1])
MAXT = 1000
MAXN = 10 ** 9

# smallest values
w.add(multi([str(n) for n in range(1, 61)]))
# boundaries: powers of ten and neighbours, values around multiples of 10
edge = set()
for p in range(0, 10):
    for d in (-2, -1, 0, 1, 2):
        v = 10 ** p + d
        if 1 <= v <= MAXN:
            edge.add(v)
for v in (9, 10, 19, 20, 99, 100, 999999999, 1000000000, 999999990, 888888888):
    edge.add(v)
w.add(multi([str(v) for v in sorted(edge)]))
# max t random large
w.add(multi([str(rng.randint(1, MAXN)) for _ in range(MAXT)]))
# max t all maximal
w.add(multi([str(MAXN) for _ in range(MAXT)]))
# max t random small
w.add(multi([str(rng.randint(1, 100)) for _ in range(MAXT)]))
# max t multiples of 10 and predecessors
w.add(multi([str(rng.randrange(10, MAXN + 1, 10) - rng.choice([0, 1]))
             for _ in range(MAXT)]))
# random magnitudes
for _ in range(3):
    w.add(multi([str(rng.randint(1, 10 ** rng.randint(1, 9)))
                 for _ in range(MAXT)]))
# single cases
w.add("1\n1\n")
w.add(f"1\n{MAXN}\n")
