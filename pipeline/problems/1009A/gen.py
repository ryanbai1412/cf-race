import os
import random
import sys

out = sys.argv[1]
random.seed(1009)

cases = []
cases.append(([1], [1]))                              # buys exactly one
cases.append(([1000], [999]))                         # cannot afford
cases.append(([1] * 1000, [1000] * 1000))             # max, buys everything
cases.append(([1000] * 1000, [1] * 1000))             # max, buys nothing
cases.append(([2, 4, 5, 2, 4], [5, 3, 4, 6]))         # statement example
cases.append(([1] * 1000, [1]))                       # wallet empties early
for _ in range(7):
    n = random.randint(1, 1000)
    m = random.randint(1, 1000)
    hi = random.choice([3, 10, 1000])
    c = [random.randint(1, hi) for _ in range(n)]
    a = [random.randint(1, hi) for _ in range(m)]
    cases.append((c, a))

for i, (c, a) in enumerate(cases, 1):
    with open(os.path.join(out, f"{i:02d}.in"), "w") as f:
        f.write(f"{len(c)} {len(a)}\n")
        f.write(" ".join(map(str, c)) + "\n")
        f.write(" ".join(map(str, a)) + "\n")
