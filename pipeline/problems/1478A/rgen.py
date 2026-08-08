"""Random small-input generator for stress-testing ref.py against brute.py."""
import random
import sys

rnd = random.Random(int(sys.argv[1]))
t = rnd.randint(1, 20)
print(t)
for _ in range(t):
    n = rnd.randint(1, 10)
    print(n)
    print(*sorted(rnd.randint(1, n) for _ in range(n)))
