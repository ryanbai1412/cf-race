import os
import random
import sys

out = sys.argv[1]
random.seed(1017)

cases = []
cases.append([[0, 0, 0, 0]])                                # single student
cases.append([[100, 100, 100, 100]] * 1000)                 # max n, all tied
cases.append([[0, 0, 0, 0]] + [[100, 100, 100, 100]] * 999) # Thomas last
cases.append([[100, 100, 100, 100]] + [[0, 0, 0, 0]] * 999) # Thomas first
for _ in range(9):
    n = random.randint(1, 1000)
    hi = random.choice([1, 5, 100])
    cases.append([[random.randint(0, hi) for _ in range(4)] for _ in range(n)])

for i, rows in enumerate(cases, 1):
    with open(os.path.join(out, f"{i:02d}.in"), "w") as f:
        f.write(f"{len(rows)}\n")
        for r in rows:
            f.write(" ".join(map(str, r)) + "\n")
