import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAXV = 10**9


def case(n, m):
    return f"{n} {m}"


def main(outdir):
    rnd = random.Random(1668)
    w = Writer(outdir)
    # all tiny grids (covers 1x1, 1x2, 1xK impossible, both orientations)
    w.add(multi([case(n, m) for n in range(1, 7) for m in range(1, 7)]))
    # extremes
    w.add(multi([
        case(1, 1), case(1, 2), case(2, 1), case(1, MAXV), case(MAXV, 1),
        case(MAXV, MAXV), case(2, MAXV), case(MAXV, 2),
        case(MAXV - 1, MAXV), case(MAXV, MAXV - 1),
    ]))
    # parity of the excess matters: n fixed, m sweeps
    w.add(multi([case(5, m) for m in range(1, 41)]))
    # random small
    w.add(multi([case(rnd.randint(1, 50), rnd.randint(1, 50)) for _ in range(500)]))
    # random huge
    for _ in range(3):
        w.add(multi([case(rnd.randint(1, MAXV), rnd.randint(1, MAXV)) for _ in range(300)]))
    # max t
    w.add(multi([case(rnd.randint(1, MAXV), rnd.randint(1, MAXV)) for _ in range(1000)]))


if __name__ == "__main__":
    main(sys.argv[1])
