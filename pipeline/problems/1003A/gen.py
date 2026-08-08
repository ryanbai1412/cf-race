import os
import random
import sys

out = sys.argv[1]
random.seed(1003)

cases = []
cases.append([1])                      # single coin
cases.append([100] * 100)              # all same, max n
cases.append(list(range(1, 101)))      # all distinct, max n
cases.append([1, 1])                   # tiny duplicate
cases.append([7] * 50 + [3] * 50)      # two heavy groups
for _ in range(8):
    n = random.randint(1, 100)
    hi = random.choice([2, 5, 10, 100])
    cases.append([random.randint(1, hi) for _ in range(n)])
# max n, small value range (high multiplicity)
cases.append([random.randint(1, 3) for _ in range(100)])

for i, a in enumerate(cases, 1):
    with open(os.path.join(out, f"{i:02d}.in"), "w") as f:
        f.write(f"{len(a)}\n")
        f.write(" ".join(map(str, a)) + "\n")
