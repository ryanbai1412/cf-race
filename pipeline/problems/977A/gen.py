import os
import random
import sys

out = sys.argv[1]
random.seed(977)


def result_positive(n, k):
    for _ in range(k):
        if n % 10 == 0:
            n //= 10
        else:
            n -= 1
        if n <= 0:
            return False
    return True


cases = [(2, 1), (10**9, 9), (10**9, 50), (1000000, 50), (101, 2), (11, 10)]
while len(cases) < 16:
    n = random.randint(2, 10**9)
    k = random.randint(1, 50)
    if result_positive(n, k):
        cases.append((n, k))

for i, (n, k) in enumerate(cases, 1):
    with open(os.path.join(out, f"{i:02d}.in"), "w") as f:
        f.write(f"{n} {k}\n")
