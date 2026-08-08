"""Random small-input generator for stress-testing ref.py against brute.py."""
import random
import sys

rnd = random.Random(int(sys.argv[1]))
t = rnd.randint(1, 15)
print(t)
for _ in range(t):
    n = rnd.randint(1, 10)
    print(n)
    print("".join(rnd.choice("01") for _ in range(n)))
