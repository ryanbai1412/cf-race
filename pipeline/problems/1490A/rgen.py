"""Random small-input generator for stress-testing ref.py against brute.py."""
import random
import sys

rnd = random.Random(int(sys.argv[1]))
t = rnd.randint(1, 8)
print(t)
for _ in range(t):
    n = rnd.randint(2, 5)
    print(n)
    print(*[rnd.randint(1, 50) for _ in range(n)])
