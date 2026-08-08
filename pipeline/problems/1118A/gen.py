import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

NMAX = 10**12
CMAX = 1000


def case(n, a, b):
    return f"{n} {a} {b}"


def main(outdir):
    rnd = random.Random(1118)
    w = Writer(outdir)
    # edges: min/max n, min/max costs, 2-liter worth it or not
    w.add(multi([
        case(1, 1, 1), case(1, 1000, 1), case(1, 1, 1000),
        case(2, 1000, 1), case(2, 1, 1000),
        case(NMAX, 1000, 1000), case(NMAX, 1000, 1),
        case(NMAX, 1, 1000), case(NMAX - 1, 999, 1000),
        case(NMAX - 1, 500, 1000), case(NMAX, 500, 1000),
        case(3, 5, 10), case(3, 5, 11), case(3, 5, 9),
    ]))
    # single query, max everything
    w.add(multi([case(NMAX, 1000, 1)]))
    # all small n exhaustive-ish
    w.add(multi([case(n, a, b) for n in range(1, 11) for a in (1, 2, 3) for b in (1, 2, 3, 4, 5, 6)][:500]))
    # random small
    w.add(multi([case(rnd.randint(1, 20), rnd.randint(1, 10), rnd.randint(1, 20))
                 for _ in range(500)]))
    # random full range, max queries
    w.add(multi([case(rnd.randint(1, NMAX), rnd.randint(1, CMAX), rnd.randint(1, CMAX))
                 for _ in range(500)]))
    # b exactly 2a boundary
    w.add(multi([case(rnd.randint(1, NMAX), a, 2 * a) for a in range(1, 500)]))


if __name__ == "__main__":
    main(sys.argv[1])
