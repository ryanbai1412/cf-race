import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(1702)
w = Writer(sys.argv[1])

# edge: powers of 10, off-by-one around them, 1, 10^9
edge = []
p = 1
while p <= 10**9:
    edge += [p]
    if p > 1:
        edge += [p - 1, p + 1]
    p *= 10
edge += [10**9, 2, 9, 11, 99, 101]
w.add(multi([str(x) for x in edge if 1 <= x <= 10**9]))
# small exhaustive
w.add(multi([str(x) for x in range(1, 1001)]))
# random per digit-length
for d in range(1, 10):
    w.add(multi([str(rng.randint(10 ** (d - 1), min(10**d - 1, 10**9))) for _ in range(1000)]))
# max t random
for _ in range(2):
    w.add(multi([str(rng.randint(1, 10**9)) for _ in range(10000)]))
