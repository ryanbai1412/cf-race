import os
import random
import sys

out = sys.argv[1]
random.seed(992)

M = 10**5
cases = [
    [0],
    [0] * 10,
    [M, -M, 0],
    [7] * 100,
    list(range(-50, 51)),
]
for _ in range(8):
    n = random.randint(1, M)
    cases.append([random.randint(-M, M) for _ in range(n)])
cases.append([random.randint(-M, M) for _ in range(M)])
cases.append([random.choice([0, 1, -1, 2]) for _ in range(M)])

for i, a in enumerate(cases, 1):
    with open(os.path.join(out, f"{i:02d}.in"), "w") as f:
        f.write(f"{len(a)}\n" + " ".join(map(str, a)) + "\n")
