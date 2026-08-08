import os
import random
import sys

out = sys.argv[1]
random.seed(964)

cases = [1, 2, 3, 4, 999999999, 1000000000]
cases += [random.randint(5, 10**9) for _ in range(8)]

for i, n in enumerate(cases, 1):
    with open(os.path.join(out, f"{i:02d}.in"), "w") as f:
        f.write(f"{n}\n")
