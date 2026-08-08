import os
import random
import sys

out_dir = sys.argv[1]
rnd = random.Random(1374)
N = 10 ** 9
tests = []


def make(cases):
    return f"{len(cases)}\n" + "".join(f"{x} {y} {n}\n" for x, y, n in cases)


# edge cases
edge = [(2, 0, 0), (2, 1, 1), (2, 0, N), (2, 1, N), (N, 0, N), (N, N - 1, N),
        (N, 0, 0), (7, 5, 12345), (5, 0, 4), (10, 5, 15), (17, 8, 54321),
        (499999993, 9, N), (10, 5, 187), (2, 0, 999999999),
        (N, N - 1, N - 1), (3, 2, 2), (1000000000, 1, 1)]
tests.append(make(edge))

# exhaustive small: every x in 2..30, every y < x, every n in y..60
cs = [(x, y, n) for x in range(2, 31) for y in range(x)
      for n in range(y, min(y + 40, 61))]
for chunk in range(0, len(cs), 20000):
    tests.append(make(cs[chunk:chunk + 20000]))

# random, max t = 5e4
for _ in range(5):
    cs = []
    for _ in range(20000):
        x = rnd.randint(2, N)
        y = rnd.randint(0, x - 1)
        n = rnd.randint(y, N)
        cs.append((x, y, n))
    tests.append(make(cs))

# k = n exactly (answer is n itself)
cs = []
for _ in range(20000):
    x = rnd.randint(2, N)
    n = rnd.randint(0, N)
    cs.append((x, n % x, n))
tests.append(make(cs))

# answer forced to y (n < y + x)
cs = []
for _ in range(20000):
    x = rnd.randint(2, N)
    y = rnd.randint(0, x - 1)
    n = rnd.randint(y, min(N, y + x - 1))
    cs.append((x, y, n))
tests.append(make(cs))

for i, body in enumerate(tests, 1):
    with open(os.path.join(out_dir, f"{i:02d}.in"), "w") as f:
        f.write(body)
