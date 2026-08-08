"""Random tiny-input generator for stress-testing ref.py against brute.py.
Sizes stay tiny because brute.py enumerates wall subsets."""
import random
import sys

rnd = random.Random(int(sys.argv[1]))
pairs = [(1, 1), (1, 2), (2, 1), (1, 3), (3, 1), (2, 2), (1, 4), (4, 1), (2, 3), (3, 2)]
t = rnd.randint(1, 4)
print(t)
for _ in range(t):
    a, b = rnd.choice(pairs)
    print(a, b)
