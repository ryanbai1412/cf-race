import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

MAX = 5000
rng = random.Random(1550)
w = Writer(sys.argv[1])

# edge: smallest / largest
w.add(multi(["1", "2", "3", str(MAX), str(MAX - 1)]))
# perfect squares and their neighbours
cases = []
for k in range(1, 71):
    for d in (-1, 0, 1):
        v = k * k + d
        if 1 <= v <= MAX:
            cases.append(str(v))
w.add(multi(cases))
# every value 1..5000 split across a few tests (t <= 5000)
w.add(multi([str(v) for v in range(1, MAX + 1)]))
w.add(multi([str(v) for v in range(MAX, 0, -1)]))
# random
for _ in range(6):
    w.add(multi([str(rng.randint(1, MAX)) for _ in range(rng.randint(1, 5000))]))
# small values only
w.add(multi([str(rng.randint(1, 10)) for _ in range(5000)]))
# max values only
w.add(multi([str(rng.randint(MAX - 10, MAX)) for _ in range(5000)]))
