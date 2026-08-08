import os
import random
import sys

out = sys.argv[1]
random.seed(1013)

cases = []
cases.append(([0], [0]))                          # both empty
cases.append(([0], [1]))                          # impossible
cases.append(([1000] * 50, [1000] * 50))          # max equal
cases.append(([1000] * 50, [0] * 50))             # all taken
cases.append(([0] * 50, [1000] * 50))             # impossible max
cases.append(([1, 2, 3], [3, 2, 1]))              # rearranged
for _ in range(8):
    n = random.randint(1, 50)
    x = [random.randint(0, 1000) for _ in range(n)]
    if random.random() < 0.5:
        # y is a redistribution of a (possibly reduced) total: always "Yes"
        total = sum(x) - random.randint(0, min(sum(x), 20))
        y = [0] * n
        for _ in range(total):
            y[random.randrange(n)] += 1
        y = [min(v, 1000) for v in y]
    else:
        y = [random.randint(0, 1000) for _ in range(n)]
    cases.append((x, y))

for i, (x, y) in enumerate(cases, 1):
    with open(os.path.join(out, f"{i:02d}.in"), "w") as f:
        f.write(f"{len(x)}\n")
        f.write(" ".join(map(str, x)) + "\n")
        f.write(" ".join(map(str, y)) + "\n")
