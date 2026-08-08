import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer

MAXA = 1000
MAXN = 100
rng = random.Random(17691)
w = Writer(sys.argv[1])


def case(a):
    return f"{len(a)}\n" + "\n".join(map(str, a))


def rand_case(n, hi=MAXA):
    return sorted(rng.sample(range(1, hi + 1), n))


# edges
w.add(case([1]))
w.add(case([MAXA]))
w.add(case(list(range(1, MAXN + 1))))            # tight column, everyone blocked
w.add(case([i for i in range(MAXA - MAXN + 1, MAXA + 1)]))  # tight column, far away
w.add(case([1, 1000]))
w.add(case([100 * i for i in range(1, 11)]))     # nobody blocked
w.add(case([1, 2]))
w.add(case([MAXA - 1, MAXA]))

# partially tight: blocks form clusters
for _ in range(4):
    n = rng.randint(2, MAXN)
    a = []
    cur = rng.randint(1, 50)
    for _ in range(n):
        a.append(cur)
        cur += rng.choice([1, 1, 1, 2, 3, rng.randint(1, 9)])
    a = [min(v, MAXA) for v in a]
    # keep strictly increasing
    fixed = []
    prev = 0
    for v in a:
        prev = max(v, prev + 1)
        if prev > MAXA:
            break
        fixed.append(prev)
    w.add(case(fixed))

# randoms of assorted sizes
for n in (2, 5, 17, 50, 99, MAXN):
    w.add(case(rand_case(n)))

# max size with the smallest possible values
w.add(case(list(range(1, MAXN + 1))))
w.add(case(rand_case(MAXN, 200)))
