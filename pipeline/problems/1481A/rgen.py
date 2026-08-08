"""Random small-input generator for stress-testing ref.py against brute.py."""
import random
import sys

rnd = random.Random(int(sys.argv[1]))
t = rnd.randint(1, 20)
print(t)
for _ in range(t):
    s = "".join(rnd.choice("UDLR") for _ in range(rnd.randint(1, 9)))
    px = rnd.randint(-4, 4)
    py = rnd.randint(-4, 4)
    if (px, py) == (0, 0):
        px = 1
    print(px, py)
    print(s)
