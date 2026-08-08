import os
import random
import sys

out = sys.argv[1]
random.seed(994)

cases = [
    ([0], [1]),                       # empty result
    ([5], [5]),
    (list(range(10)), list(range(10))),
    ([9, 8, 7, 6, 5, 4, 3, 2, 1, 0], [0, 9]),
]
for _ in range(10):
    n = random.randint(1, 10)
    m = random.randint(1, 10)
    x = random.sample(range(10), n)
    y = random.sample(range(10), m)
    cases.append((x, y))

for i, (x, y) in enumerate(cases, 1):
    with open(os.path.join(out, f"{i:02d}.in"), "w") as f:
        f.write(f"{len(x)} {len(y)}\n")
        f.write(" ".join(map(str, x)) + "\n")
        f.write(" ".join(map(str, y)) + "\n")
