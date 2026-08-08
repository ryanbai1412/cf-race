import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer

MAXN = 10**5
rng = random.Random(9351)
w = Writer(sys.argv[1])

# edges and highly-composite / prime values
for n in (2, 3, 4, 6, 12, 97, 1024, 65536, 83160, 99991, 99999, MAXN):
    w.add(str(n))

# randoms
for _ in range(8):
    w.add(str(rng.randint(2, MAXN)))
