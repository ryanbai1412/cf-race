import os
import random
import sys

out_dir = sys.argv[1]
rnd = random.Random(1368)
N = 10 ** 9
tests = []


def make(cases):
    return f"{len(cases)}\n" + "".join(f"{a} {b} {n}\n" for a, b, n in cases)


# edge cases
edge = [(1, 1, 1), (1, 1, 2), (1, 1, N), (N, N, N), (1, N, N), (N, 1, N),
        (1, 2, 3), (5, 4, 100), (1, 1, 3), (2, 1, 2), (1, 2, 2),
        (N - 1, 1, N), (1, N - 1, N), (499999999, 500000000, N),
        (2, 3, N), (3, 2, N)]
tests.append(make(edge))

# tiny exhaustive: all a, b, n with n <= 12
cs = [(a, b, n) for n in range(1, 13) for a in range(1, n + 1)
      for b in range(1, n + 1)]
for chunk in range(0, len(cs), 100):
    tests.append(make(cs[chunk:chunk + 100]))

# random small n
cs = []
for _ in range(100):
    n = rnd.randint(1, 1000)
    cs.append((rnd.randint(1, n), rnd.randint(1, n), n))
tests.append(make(cs))

# random large n
for _ in range(3):
    cs = []
    for _ in range(100):
        n = rnd.randint(1, N)
        cs.append((rnd.randint(1, n), rnd.randint(1, n), n))
    tests.append(make(cs))

# worst case: a = b = 1, n near max (longest chains)
cs = [(1, 1, rnd.randint(N - 1000, N)) for _ in range(100)]
tests.append(make(cs))

# a or b already close to n
cs = []
for _ in range(100):
    n = rnd.randint(2, N)
    cs.append((n, rnd.randint(1, n), n))
tests.append(make(cs))

for i, body in enumerate(tests, 1):
    with open(os.path.join(out_dir, f"{i:02d}.in"), "w") as f:
        f.write(body)
