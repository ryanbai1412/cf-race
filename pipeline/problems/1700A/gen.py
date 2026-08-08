import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(1700)
w = Writer(sys.argv[1])


def case(n, m):
    return f"{n} {m}"


# edge: 1x1, 1xM, Nx1, 2x2
w.add(multi([case(1, 1), case(1, 10000), case(10000, 1), case(2, 2), case(2, 3)]))
# small exhaustive-ish
w.add(multi([case(n, m) for n in range(1, 11) for m in range(1, 11)]))
# random small
for _ in range(3):
    w.add(multi([case(rng.randint(1, 100), rng.randint(1, 100)) for _ in range(1000)]))
# random large
for _ in range(3):
    w.add(multi([case(rng.randint(1, 10000), rng.randint(1, 10000)) for _ in range(1000)]))
# max values
w.add(multi([case(10000, 10000), case(9999, 10000), case(10000, 9999), case(1, 9999)]))
# max t with max sizes
w.add(multi([case(rng.choice([1, 2, 9999, 10000]), rng.choice([1, 2, 9999, 10000])) for _ in range(1000)]))
