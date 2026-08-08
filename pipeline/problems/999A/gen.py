import os
import random
import sys

out = sys.argv[1]
random.seed(999)

cases = [
    (100, [1] * 100),          # solves everything
    (1, [100]),                # solves nothing
    (50, [100] * 98 + [1, 1]),
    (50, [1, 1] + [100] * 98),
    (1, [1]),
]
for _ in range(10):
    n = random.randint(1, 100)
    k = random.randint(1, 100)
    cases.append((k, [random.randint(1, 100) for _ in range(n)]))

for i, (k, a) in enumerate(cases, 1):
    with open(os.path.join(out, f"{i:02d}.in"), "w") as f:
        f.write(f"{len(a)} {k}\n" + " ".join(map(str, a)) + "\n")
