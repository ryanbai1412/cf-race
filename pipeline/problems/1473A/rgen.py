"""Random small-input generator for stress-testing ref.py against brute.py."""
import random
import sys

rnd = random.Random(int(sys.argv[1]))
t = rnd.randint(1, 30)
print(t)
for _ in range(t):
    n = rnd.randint(3, 7)
    v = rnd.randint(2, 15)
    print(n, rnd.randint(1, v * 2))
    print(*[rnd.randint(1, v) for _ in range(n)])
