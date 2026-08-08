import os
import random
import sys

out = sys.argv[1]
random.seed(1006)

cases = []
cases.append([1])
cases.append([10**9])
cases.append([10**9 - 1])
cases.append([1, 2, 4, 5, 10])
cases.append([2] * 1000)               # max n, all even
cases.append([10**9 - 1] * 1000)       # max n, all max odd
for _ in range(7):
    n = random.randint(1, 1000)
    cases.append([random.randint(1, 10**9) for _ in range(n)])
cases.append([random.randint(1, 10) for _ in range(1000)])

for i, a in enumerate(cases, 1):
    with open(os.path.join(out, f"{i:02d}.in"), "w") as f:
        f.write(f"{len(a)}\n")
        f.write(" ".join(map(str, a)) + "\n")
