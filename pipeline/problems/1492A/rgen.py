"""Random small-input generator for stress-testing ref.py against brute.py."""
import random
import sys

rnd = random.Random(int(sys.argv[1]))
t = rnd.randint(1, 30)
print(t)
for _ in range(t):
    print(rnd.randint(1, 60), rnd.randint(1, 20), rnd.randint(1, 20), rnd.randint(1, 20))
