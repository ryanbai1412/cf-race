"""Random small-input generator for stress-testing ref.py against brute.py."""
import random
import sys

rnd = random.Random(int(sys.argv[1]))
n = rnd.randint(1, 8)
q = rnd.randint(1, 20)
qs = []
for _ in range(q):
    qs.append((rnd.randint(1, 2), rnd.randint(1, n)))
if all(t == 1 for t, _ in qs):
    qs.append((2, rnd.randint(1, n)))
print(n, len(qs))
print(*[rnd.randint(0, 1) for _ in range(n)])
for t, v in qs:
    print(t, v)
