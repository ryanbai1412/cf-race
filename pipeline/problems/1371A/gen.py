import os
import random
import sys

out_dir = sys.argv[1]
rnd = random.Random(1371)
N = 10 ** 9
tests = []


def make(vals):
    return f"{len(vals)}\n" + "\n".join(map(str, vals)) + "\n"


# edge cases
tests.append(make([1, 2, 3, 4, 5, 6, 7, N, N - 1, N - 2, 10, 11,
                   999999999, 1000000000, 8, 9]))

# all n from 1 to 1000
tests.append(make(list(range(1, 1001))))

# random, max t = 1000
for _ in range(5):
    tests.append(make([rnd.randint(1, N) for _ in range(1000)]))

# random small
for _ in range(2):
    tests.append(make([rnd.randint(1, 20) for _ in range(1000)]))

# max t of maximum n / of n = 1
tests.append(make([N] * 1000))
tests.append(make([1] * 1000))

# powers of two and neighbours
vals = []
for k in range(30):
    for d in (-1, 0, 1):
        v = (1 << k) + d
        if 1 <= v <= N:
            vals.append(v)
tests.append(make(vals))

for i, body in enumerate(tests, 1):
    with open(os.path.join(out_dir, f"{i:02d}.in"), "w") as f:
        f.write(body)
