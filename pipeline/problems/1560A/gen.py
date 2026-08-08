import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(1560)
w = Writer(sys.argv[1])
MAXT = 100
MAXK = 1000

# first 100 values
w.add(multi([str(k) for k in range(1, MAXT + 1)]))
# last 100 values
w.add(multi([str(k) for k in range(MAXK - MAXT + 1, MAXK + 1)]))
# extremes
w.add(multi([str(k) for k in [1, 2, 3, 999, 1000] + [1] * 95]))
# random full-size batches
for _ in range(6):
    w.add(multi([str(rng.randint(1, MAXK)) for _ in range(MAXT)]))
# repeated same value batches
for k in (1, 500, 1000):
    w.add(multi([str(k) for _ in range(MAXT)]))
# small-value batches
w.add(multi([str(rng.randint(1, 20)) for _ in range(MAXT)]))
# single cases
w.add("1\n1\n")
w.add(f"1\n{MAXK}\n")
