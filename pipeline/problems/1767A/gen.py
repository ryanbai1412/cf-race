import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

MAXC = 10**8
rng = random.Random(17671)
w = Writer(sys.argv[1])


def case(pts):
    # each test case is preceded by an empty line (per the statement)
    return "\n" + "\n".join(f"{x} {y}" for x, y in pts)


def nondegenerate(p):
    (x1, y1), (x2, y2), (x3, y3) = p
    return (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1) != 0


def rand_tri(lo=1, hi=MAXC):
    while True:
        p = [(rng.randint(lo, hi), rng.randint(lo, hi)) for _ in range(3)]
        if nondegenerate(p):
            return p


def axis_right(lo=1, hi=MAXC):
    """Right triangle with axis-aligned legs -> both coords have a duplicate -> NO."""
    while True:
        x1, x2 = rng.randint(lo, hi), rng.randint(lo, hi)
        y1, y2 = rng.randint(lo, hi), rng.randint(lo, hi)
        if x1 != x2 and y1 != y2:
            p = [(x1, y1), (x1, y2), (x2, y2)]
            rng.shuffle(p)
            return p


def dup_x_only(lo=1, hi=MAXC):
    """Two equal x, all y distinct -> YES via horizontal cut."""
    while True:
        x1, x2 = rng.randint(lo, hi), rng.randint(lo, hi)
        ys = rng.sample(range(lo, hi + 1), 3)
        if x1 != x2:
            p = [(x1, ys[0]), (x1, ys[1]), (x2, ys[2])]
            rng.shuffle(p)
            if nondegenerate(p):
                return p


# hand edges: extreme coordinates, both answers
w.add(multi([
    case([(1, 1), (1, MAXC), (MAXC, MAXC)]),          # NO
    case([(1, 1), (1, MAXC), (MAXC, 1)]),             # NO
    case([(1, 1), (2, 3), (3, 2)]),                   # YES
    case([(1, 1), (MAXC, MAXC), (1, MAXC)]),          # NO
    case([(1, 2), (2, 1), (3, 3)]),                   # YES
    case([(1, 1), (1, 2), (2, 3)]),                   # YES (y distinct)
    case([(1, 1), (2, 1), (3, 2)]),                   # YES (x distinct)
    case([(MAXC, MAXC), (MAXC, 1), (1, MAXC)]),       # NO
    case([(MAXC - 1, MAXC), (MAXC, MAXC - 1), (1, 1)]),  # YES
    case([(5, 5), (5, 6), (6, 5)]),                   # NO
]))

# small coordinate range: many duplicates by chance
for hi in (2, 3, 5, 10):
    for _ in range(2):
        w.add(multi([case(rand_tri(1, hi)) for _ in range(min(400, hi ** 6))]))

# structured mixes
for _ in range(3):
    cases = []
    for _ in range(2000):
        r = rng.random()
        if r < 0.35:
            cases.append(case(axis_right()))
        elif r < 0.7:
            cases.append(case(dup_x_only()))
        else:
            cases.append(case(rand_tri()))
    w.add(multi(cases))

# max size: t = 10^4, large coordinates
w.add(multi([case(rand_tri()) for _ in range(10000)]))
w.add(multi([case(axis_right()) for _ in range(10000)]))
w.add(multi([case(rand_tri(1, 4)) for _ in range(10000)]))
