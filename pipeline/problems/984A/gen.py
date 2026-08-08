import os
import random
import sys

out = sys.argv[1]
random.seed(984)

cases = [
    [1],
    [1000000],
    [1, 1000000],
    [5, 5, 5, 5],
    list(range(1, 1001)),
    [1000000] * 1000,
]
for _ in range(8):
    n = random.randint(1, 1000)
    cases.append([random.randint(1, 10**6) for _ in range(n)])
big = [random.randint(1, 10**6) for _ in range(1000)]
cases.append(big)

for i, a in enumerate(cases, 1):
    with open(os.path.join(out, f"{i:02d}.in"), "w") as f:
        f.write(f"{len(a)}\n" + " ".join(map(str, a)) + "\n")
