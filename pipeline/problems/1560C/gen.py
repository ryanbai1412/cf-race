import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(15603)
w = Writer(sys.argv[1])
MAXT = 100
MAXK = 10 ** 9

# first 100 numbers
w.add(multi([str(k) for k in range(1, MAXT + 1)]))
# perfect squares and their neighbours (layer boundaries / corners)
edge = set()
for m in list(range(1, 12)) + [31621, 31622, 31623, 31624]:
    for d in (-2, -1, 0, 1, 2):
        v = m * m + d
        if 1 <= v <= MAXK:
            edge.add(v)
edge.update([1, 2, 3, MAXK, MAXK - 1, 999950884, 999950885, 1000000000])
edge = sorted(edge)[:MAXT]
w.add(multi([str(v) for v in edge]))
# diagonal-ish: k = m*m - m + 1 (end of the downward run)
w.add(multi([str(m * m - m + 1) for m in range(1, MAXT + 1)]))
# k = m*m - m (just before) and k = m*m (row end)
w.add(multi([str(max(1, m * m - m)) for m in range(1, MAXT + 1)]))
w.add(multi([str(m * m) for m in range(1, MAXT + 1)]))
# random full-size batches over the whole range
for _ in range(5):
    w.add(multi([str(rng.randint(1, MAXK)) for _ in range(MAXT)]))
# random magnitudes
for _ in range(3):
    w.add(multi([str(rng.randint(1, 10 ** rng.randint(1, 9)))
                 for _ in range(MAXT)]))
# large values near the maximum
w.add(multi([str(rng.randint(MAXK - 1000, MAXK)) for _ in range(MAXT)]))
# single cases
w.add("1\n1\n")
w.add(f"1\n{MAXK}\n")
