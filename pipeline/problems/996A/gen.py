import os
import random
import sys

out = sys.argv[1]
random.seed(996)

cases = [1, 4, 5, 19, 99, 100, 1000000000, 999999999]
cases += [random.randint(1, 10**9) for _ in range(8)]

for i, n in enumerate(cases, 1):
    with open(os.path.join(out, f"{i:02d}.in"), "w") as f:
        f.write(f"{n}\n")
