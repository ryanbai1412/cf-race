import os
import random
import sys

out = sys.argv[1]
random.seed(1041)


def sample_distinct(lo, hi, n):
    return random.sample(range(lo, hi + 1), n)


cases = []
cases.append([1])                                    # single keyboard
cases.append([10**9])                                # single max value
cases.append([1, 10**9])                             # max possible gap
cases.append(list(range(500, 1500)))                 # max n, contiguous (answer 0)
cases.append(sample_distinct(1, 10**9, 1000))        # max n, huge spread
for _ in range(8):
    n = random.randint(1, 1000)
    span = random.choice([n, n * 3, 10**6, 10**9])
    lo = random.randint(1, 10**9 - span + 1)
    cases.append(sample_distinct(lo, lo + span - 1, n))

for i, a in enumerate(cases, 1):
    random.shuffle(a)
    with open(os.path.join(out, f"{i:02d}.in"), "w") as f:
        f.write(f"{len(a)}\n")
        f.write(" ".join(map(str, a)) + "\n")
