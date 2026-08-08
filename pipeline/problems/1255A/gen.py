import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAXV = 10**9


def case(a, b):
    return f"{a} {b}"


def main(outdir):
    rnd = random.Random(1255)
    w = Writer(outdir)
    # zero difference, extremes, and the two directions of the max difference
    w.add(multi([case(0, 0), case(MAXV, MAXV), case(0, MAXV), case(MAXV, 0),
                 case(0, 1), case(1, 0), case(4, 0), case(0, 4)]))
    # every difference 0..60 in both directions (covers all 5/2/1 remainders)
    cs = [case(0, d) for d in range(61)] + [case(d, 0) for d in range(40)]
    w.add(multi(cs[:1000]))
    # differences near multiples of 5 at large magnitudes
    cs = []
    for k in (1, 2, 3, 10**8, 2 * 10**8):
        for r in range(5):
            cs.append(case(0, 5 * k + r))
            cs.append(case(5 * k + r, 0))
    w.add(multi(cs))
    # max T with max-magnitude random values
    w.add(multi([case(rnd.randint(0, MAXV), rnd.randint(0, MAXV))
                 for _ in range(1000)]))
    # small random values (dense coverage of tiny differences)
    for _ in range(7):
        t = rnd.randint(1, 1000)
        w.add(multi([case(rnd.randint(0, 20), rnd.randint(0, 20))
                     for _ in range(t)]))
    # mixed magnitudes
    for _ in range(6):
        t = rnd.randint(1, 1000)
        cs = []
        for _ in range(t):
            hi = rnd.choice([10, 1000, 10**6, MAXV])
            cs.append(case(rnd.randint(0, hi), rnd.randint(0, hi)))
        w.add(multi(cs))


if __name__ == "__main__":
    main(sys.argv[1])
