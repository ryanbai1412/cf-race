import os
import random
import sys

out = sys.argv[1]
random.seed(965)

M = 10**4
cases = [
    (1, 1, 1, 1),
    (M, M, 1, 1),
    (M, 1, M, M),
    (1, M, M, 1),
    (M, M, M, M),
    (7, 9999, 2, 13),
]
for _ in range(10):
    cases.append(tuple(random.randint(1, M) for _ in range(4)))

for i, c in enumerate(cases, 1):
    with open(os.path.join(out, f"{i:02d}.in"), "w") as f:
        f.write(" ".join(map(str, c)) + "\n")
