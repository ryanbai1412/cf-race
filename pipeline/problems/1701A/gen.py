import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(1701)
w = Writer(sys.argv[1])


def case(a, b, c, d):
    return f"{a} {b}\n{c} {d}"


# all 16 possible fields (t <= 16)
allc = [case((k >> 3) & 1, (k >> 2) & 1, (k >> 1) & 1, k & 1) for k in range(16)]
w.add(multi(allc))
# each edge count separately
w.add(multi([case(0, 0, 0, 0), case(1, 1, 1, 1)]))
w.add(multi([case(1, 0, 0, 0), case(0, 1, 0, 0), case(0, 0, 1, 0), case(0, 0, 0, 1)]))
w.add(multi([case(1, 1, 0, 0), case(1, 0, 1, 0), case(1, 0, 0, 1),
             case(0, 1, 1, 0), case(0, 1, 0, 1), case(0, 0, 1, 1)]))
w.add(multi([case(1, 1, 1, 0), case(1, 1, 0, 1), case(1, 0, 1, 1), case(0, 1, 1, 1)]))
# random max-t
for _ in range(3):
    w.add(multi([allc[rng.randrange(16)] for _ in range(16)]))
