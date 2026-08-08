import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(1556)
w = Writer(sys.argv[1])
MAXT = 10000
MAXV = 10 ** 9


def case(c, d):
    return f"{c} {d}"


# all tiny pairs
w.add(multi([case(c, d) for c in range(6) for d in range(6)]))
# extremes: zeros and maxima in every combination
ex = [0, 1, 2, MAXV - 1, MAXV]
w.add(multi([case(c, d) for c in ex for d in ex]))
# max t fully random
w.add(multi([case(rng.randint(0, MAXV), rng.randint(0, MAXV))
             for _ in range(MAXT)]))
# max t equal pairs (answer 1, except 0 0)
w.add(multi([case(v, v) for v in [rng.randint(0, MAXV) for _ in range(MAXT)]]))
# max t same parity, distinct (answer 2)
cases = []
while len(cases) < MAXT:
    c = rng.randint(0, MAXV)
    d = rng.randint(0, MAXV)
    if (c + d) % 2 == 0 and c != d:
        cases.append(case(c, d))
w.add(multi(cases))
# max t opposite parity (answer -1)
cases = []
while len(cases) < MAXT:
    c = rng.randint(0, MAXV)
    d = rng.randint(0, MAXV)
    if (c + d) % 2 == 1:
        cases.append(case(c, d))
w.add(multi(cases))
# max t with one of the values zero
w.add(multi([case(0, rng.randint(0, MAXV)) if rng.random() < 0.5
             else case(rng.randint(0, MAXV), 0) for _ in range(MAXT)]))
# max t small values
w.add(multi([case(rng.randint(0, 4), rng.randint(0, 4)) for _ in range(MAXT)]))
# mixed magnitudes
for _ in range(2):
    w.add(multi([case(rng.randint(0, 10 ** rng.randint(0, 9)),
                      rng.randint(0, 10 ** rng.randint(0, 9)))
                 for _ in range(MAXT)]))
# single cases
w.add("1\n0 0\n")
w.add(f"1\n{MAXV} {MAXV}\n")
