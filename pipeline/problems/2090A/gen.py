import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

MAX = 10**9
rng = random.Random(2090)
w = Writer(sys.argv[1])


def case(x, y, a):
    return f"{x} {y} {a}"


# edge cases
w.add(multi([case(1, 1, 1)]))
w.add(multi([case(MAX, MAX, MAX), case(1, MAX, MAX), case(MAX, 1, MAX),
             case(1, 1, MAX), case(MAX, MAX, 1)]))
# boundary: x exactly reaches / just misses the remainder
w.add(multi([case(5, 3, 8 * k + 5) for k in range(100)] +
            [case(5, 3, 8 * k + 4) for k in range(100)]))

# small exhaustive-ish
w.add(multi([case(x, y, a) for x in range(1, 6) for y in range(1, 6)
             for a in range(1, 11)]))

# random smalls
for _ in range(6):
    w.add(multi([case(rng.randint(1, 100), rng.randint(1, 100), rng.randint(1, 1000))
                 for _ in range(rng.randint(50, 200))]))

# random large
for _ in range(8):
    w.add(multi([case(rng.randint(1, MAX), rng.randint(1, MAX), rng.randint(1, MAX))
                 for _ in range(rng.randint(200, 1000))]))

# max-size: t = 1000, all values near max
w.add(multi([case(rng.randint(MAX - 100, MAX), rng.randint(MAX - 100, MAX),
                  rng.randint(MAX - 100, MAX)) for _ in range(1000)]))
w.add(multi([case(rng.randint(1, MAX), rng.randint(1, MAX), rng.randint(1, MAX))
             for _ in range(1000)]))
