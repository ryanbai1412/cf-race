import os
import random
import sys

out = sys.argv[1]
random.seed(1028)


def make(n, m, k, r0, c0):
    """n x m grid with a k x k black square whose top-left is (r0, c0), 0-based."""
    g = [["W"] * m for _ in range(n)]
    for r in range(r0, r0 + k):
        for c in range(c0, c0 + k):
            g[r][c] = "B"
    return g


cases = []
cases.append(make(1, 1, 1, 0, 0))            # minimal
cases.append(make(115, 115, 115, 0, 0))      # whole max grid black
cases.append(make(115, 115, 1, 0, 0))        # single cell, corner
cases.append(make(115, 115, 1, 114, 114))    # single cell, far corner
cases.append(make(115, 1, 1, 57, 0))         # thin column
cases.append(make(1, 115, 1, 0, 80))         # thin row
for _ in range(8):
    n = random.randint(1, 115)
    m = random.randint(1, 115)
    kmax = min(n, m)
    k = random.randrange(1, kmax + 1, 2)
    r0 = random.randint(0, n - k)
    c0 = random.randint(0, m - k)
    cases.append(make(n, m, k, r0, c0))

for i, g in enumerate(cases, 1):
    with open(os.path.join(out, f"{i:02d}.in"), "w") as f:
        f.write(f"{len(g)} {len(g[0])}\n")
        for row in g:
            f.write("".join(row) + "\n")
