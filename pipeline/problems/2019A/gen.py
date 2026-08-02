import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

MAXV = 1000
rng = random.Random(2019)
w = Writer(sys.argv[1])


def case(a):
    return f"{len(a)}\n{' '.join(map(str, a))}"


# edges
w.add(multi([case([1]), case([MAXV]), case([1, MAXV]), case([MAXV, 1]),
             case([MAXV] * 100), case([1] * 100)]))
# max at every position of a short array
w.add(multi([case([1] * i + [MAXV] + [1] * (7 - i)) for i in range(8)]))
# small exhaustive-ish: all arrays of length <= 3 over {1,2,3}
vals = (1, 2, 3)
cases = [case([a]) for a in vals]
cases += [case([a, b]) for a in vals for b in vals]
cases += [case([a, b, c]) for a in vals for b in vals for c in vals]
w.add(multi(cases))
# randoms
for hi in (2, 10, MAXV):
    for _ in range(4):
        w.add(multi([case([rng.randint(1, hi) for _ in range(rng.randint(1, 100))])
                     for _ in range(rng.randint(50, 500))]))
# max-size: t = 500, n = 100
for _ in range(3):
    w.add(multi([case([rng.randint(1, MAXV) for _ in range(100)])
                 for _ in range(500)]))
w.add(multi([case(sorted(rng.randint(1, MAXV) for _ in range(100)))
             for _ in range(500)]))
