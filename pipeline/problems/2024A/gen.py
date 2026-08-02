import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

MAX = 10**9
rng = random.Random(2024)
w = Writer(sys.argv[1])


def case(a, b):
    return f"{a} {b}"


# edges
w.add(multi([case(1, 1), case(1, MAX), case(MAX, 1), case(MAX, MAX)]))
# boundaries around 2a = b
w.add(multi([case(a, 2 * a + d) for a in (1, 5, 10**5, MAX // 2)
             for d in (-2, -1, 0, 1, 2) if 1 <= 2 * a + d <= MAX]))
# small exhaustive
w.add(multi([case(a, b) for a in range(1, 26) for b in range(1, 26)]))
# randoms
for _ in range(8):
    w.add(multi([case(rng.randint(1, 1000), rng.randint(1, 1000))
                 for _ in range(rng.randint(100, 1000))]))
for _ in range(5):
    w.add(multi([case(rng.randint(1, MAX), rng.randint(1, MAX))
                 for _ in range(1000)]))
# a close to b
w.add(multi([case(v := rng.randint(1, MAX - 10), max(1, v + rng.randint(-5, 5)))
             for _ in range(1000)]))
# max-size t = 10^4
w.add(multi([case(rng.randint(1, MAX), rng.randint(1, MAX))
             for _ in range(10**4)]))
w.add(multi([case(rng.randint(MAX // 2, MAX), rng.randint(MAX // 2, MAX))
             for _ in range(10**4)]))
