import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(1562)
w = Writer(sys.argv[1])
MAXT = 10000
MAXV = 10 ** 9


def case(l, r):
    return f"{l} {r}"


def rand_pair(hi):
    l = rng.randint(1, hi)
    r = rng.randint(l, hi)
    return case(l, r)


# all tiny pairs
w.add(multi([case(l, r) for l in range(1, 13) for r in range(l, 13)]))
# extremes
ex = [1, 2, 3, MAXV // 2 - 1, MAXV // 2, MAXV // 2 + 1, MAXV - 1, MAXV]
w.add(multi([case(l, r) for l in ex for r in ex if l <= r]))
# max t random over the whole range
w.add(multi([rand_pair(MAXV) for _ in range(MAXT)]))
# max t with l == r
w.add(multi([case(v, v) for v in [rng.randint(1, MAXV) for _ in range(MAXT)]]))
# max t right at the r = 2l / r = 2l+1 boundary
cases = []
for _ in range(MAXT):
    l = rng.randint(1, MAXV // 2 - 1)
    r = min(MAXV, 2 * l + rng.choice([-1, 0, 1, 2]))
    cases.append(case(l, min(max(r, l), MAXV)))
w.add(multi(cases))
# max t with r much larger than l (answer (r-1)//2)
w.add(multi([case(rng.randint(1, 1000), rng.randint(MAXV // 2, MAXV))
             for _ in range(MAXT)]))
# max t with r close to l (answer r-l)
cases = []
for _ in range(MAXT):
    l = rng.randint(MAXV // 2, MAXV)
    r = min(MAXV, l + rng.randint(0, 5))
    cases.append(case(l, r))
w.add(multi(cases))
# max t small values
w.add(multi([rand_pair(30) for _ in range(MAXT)]))
# mixed magnitudes
for _ in range(2):
    w.add(multi([rand_pair(10 ** rng.randint(1, 9)) for _ in range(MAXT)]))
# single cases
w.add("1\n1 1\n")
w.add(f"1\n1 {MAXV}\n")
w.add(f"1\n{MAXV} {MAXV}\n")
