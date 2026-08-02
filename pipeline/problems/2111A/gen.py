import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

MAX = 10**9
rng = random.Random(2111)
w = Writer(sys.argv[1])

# edges: 1, powers of two and neighbours, max
pow2 = []
p = 1
while p <= MAX:
    for v in (p - 1, p, p + 1):
        if 1 <= v <= MAX:
            pow2.append(str(v))
    p *= 2
w.add(multi(pow2))
w.add(multi(["1", str(MAX), str(MAX - 1), "536870912", "536870911"]))

# small exhaustive
w.add(multi([str(v) for v in range(1, 1001)]))

# randoms
for _ in range(12):
    w.add(multi([str(rng.randint(1, MAX)) for _ in range(rng.randint(100, 2000))]))
for lo, hi in ((1, 100), (10**6, 10**7), (MAX // 2, MAX)):
    w.add(multi([str(rng.randint(lo, hi)) for _ in range(1000)]))

# max-size: t = 10^4
w.add(multi([str(rng.randint(1, MAX)) for _ in range(10**4)]))
w.add(multi([str(MAX)] * 10**4))
