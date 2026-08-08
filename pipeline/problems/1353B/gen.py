import os
import random
import sys

out_dir = sys.argv[1]
rnd = random.Random(1353)
tests = []


def case(n, k, a, b):
    return f"{n} {k}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n"


# tiny edge cases
edge = []
edge.append(case(1, 0, [1], [30]))
edge.append(case(1, 1, [1], [30]))
edge.append(case(1, 1, [30], [1]))
edge.append(case(2, 2, [1, 1], [30, 30]))
edge.append(case(3, 0, [5, 5, 5], [30, 30, 30]))
edge.append(case(4, 2, [1, 1, 30, 30], [2, 2, 1, 1]))
edge.append(case(5, 5, [30] * 5, [1] * 5))
edge.append(case(5, 5, [1] * 5, [30] * 5))
edge.append(case(5, 3, [1, 2, 3, 4, 5], [5, 4, 3, 2, 1]))
tests.append("".join([f"{len(edge)}\n"] + edge))

# all-equal / extreme uniform values
uni = []
for n in (1, 2, 15, 30):
    for k in (0, n // 2, n):
        uni.append(case(n, k, [1] * n, [1] * n))
        uni.append(case(n, k, [30] * n, [30] * n))
tests.append("".join([f"{len(uni)}\n"] + uni))

# random small values (lots of ties)
for seed in range(4):
    cs = []
    for _ in range(200):
        n = rnd.randint(1, 30)
        k = rnd.randint(0, n)
        hi = rnd.choice([2, 3, 5, 30])
        cs.append(case(n, k,
                       [rnd.randint(1, hi) for _ in range(n)],
                       [rnd.randint(1, hi) for _ in range(n)]))
    tests.append("".join([f"{len(cs)}\n"] + cs))

# max size: t=200, n=30 uniform random
for seed in range(3):
    cs = []
    for _ in range(200):
        n = 30
        k = rnd.randint(0, n)
        cs.append(case(n, k,
                       [rnd.randint(1, 30) for _ in range(n)],
                       [rnd.randint(1, 30) for _ in range(n)]))
    tests.append("".join([f"{len(cs)}\n"] + cs))

# k = n always, b much bigger / smaller
cs = []
for _ in range(200):
    n = rnd.randint(1, 30)
    cs.append(case(n, n,
                   [rnd.randint(1, 10) for _ in range(n)],
                   [rnd.randint(20, 30) for _ in range(n)]))
tests.append("".join([f"{len(cs)}\n"] + cs))
cs = []
for _ in range(200):
    n = rnd.randint(1, 30)
    cs.append(case(n, n,
                   [rnd.randint(20, 30) for _ in range(n)],
                   [rnd.randint(1, 10) for _ in range(n)]))
tests.append("".join([f"{len(cs)}\n"] + cs))

for i, body in enumerate(tests, 1):
    with open(os.path.join(out_dir, f"{i:02d}.in"), "w") as f:
        f.write(body)
