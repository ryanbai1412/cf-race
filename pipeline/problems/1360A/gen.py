import os
import random
import sys

out_dir = sys.argv[1]
rnd = random.Random(1360)
tests = []

# edge cases
cs = []
for a, b in [(1, 1), (1, 100), (100, 1), (100, 100), (99, 100), (100, 99),
             (2, 1), (1, 2), (50, 100), (100, 50), (51, 100), (100, 51),
             (49, 100), (100, 49), (2, 2), (3, 3), (1, 3), (3, 1), (99, 99)]:
    cs.append(f"{a} {b}")
tests.append(f"{len(cs)}\n" + "\n".join(cs) + "\n")

# exhaustive: all 100 x 100 pairs, split across two tests (t <= 10000)
pairs = [(a, b) for a in range(1, 101) for b in range(1, 101)]
tests.append(f"{len(pairs)}\n" + "\n".join(f"{a} {b}" for a, b in pairs) + "\n")

# squares and near-squares
cs = []
for a in range(1, 101):
    for d in (-1, 0, 1):
        b = a + d
        if 1 <= b <= 100:
            cs.append(f"{a} {b}")
tests.append(f"{len(cs)}\n" + "\n".join(cs) + "\n")

# 2:1 ratio boundary cases
cs = []
for a in range(1, 101):
    for b in (2 * a - 1, 2 * a, 2 * a + 1):
        if 1 <= b <= 100:
            cs.append(f"{a} {b}")
            cs.append(f"{b} {a}")
tests.append(f"{len(cs)}\n" + "\n".join(cs) + "\n")

# random, max t
for _ in range(5):
    cs = [f"{rnd.randint(1, 100)} {rnd.randint(1, 100)}" for _ in range(10000)]
    tests.append(f"{len(cs)}\n" + "\n".join(cs) + "\n")

# max t of maximal values
cs = ["100 100"] * 10000
tests.append(f"{len(cs)}\n" + "\n".join(cs) + "\n")

for i, body in enumerate(tests, 1):
    with open(os.path.join(out_dir, f"{i:02d}.in"), "w") as f:
        f.write(body)
