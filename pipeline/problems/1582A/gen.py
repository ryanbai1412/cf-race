import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAXV = 10 ** 9


def case(a, b, c):
    return f"{a} {b} {c}"


def main(outdir):
    rnd = random.Random(1582)
    w = Writer(outdir)

    # edges: all parity combos at the minimum, and at the max bound
    w.add(multi([case(a, b, c) for a in (1, 2) for b in (1, 2) for c in (1, 2)]))
    w.add(multi([case(a, b, c) for a in (1, MAXV) for b in (1, MAXV)
                 for c in (1, MAXV)]))
    w.add(multi([case(MAXV, MAXV, MAXV), case(MAXV - 1, MAXV, MAXV),
                 case(MAXV, MAXV - 1, MAXV), case(MAXV, MAXV, MAXV - 1)]))
    # random small and random huge
    w.add(multi([case(rnd.randint(1, 10), rnd.randint(1, 10), rnd.randint(1, 10))
                 for _ in range(500)]))
    # max t
    w.add(multi([case(rnd.randint(1, MAXV), rnd.randint(1, MAXV),
                      rnd.randint(1, MAXV)) for _ in range(1000)]))


if __name__ == "__main__":
    main(sys.argv[1])
