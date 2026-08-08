import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(n, m, rb, cb, rd, cd):
    return f"{n} {m} {rb} {cb} {rd} {cd}"


def rand_case(rnd, nmax, mmax):
    n = rnd.randint(1, nmax)
    m = rnd.randint(1, mmax)
    return case(n, m, rnd.randint(1, n), rnd.randint(1, m), rnd.randint(1, n), rnd.randint(1, m))


def main(outdir):
    rnd = random.Random(1623)
    w = Writer(outdir)

    # edges: 1x1, 1xm, nx1, corners, same cell, max sizes
    w.add(
        multi(
            [
                case(1, 1, 1, 1, 1, 1),
                case(1, 100, 1, 1, 1, 100),
                case(100, 1, 100, 1, 1, 1),
                case(100, 100, 1, 1, 100, 100),
                case(100, 100, 100, 100, 1, 1),
                case(100, 100, 50, 50, 50, 50),
                case(2, 2, 1, 1, 2, 2),
                case(2, 100, 2, 1, 1, 100),
                case(100, 99, 1, 99, 100, 1),
                case(99, 100, 99, 1, 1, 2),
            ]
        )
    )

    # small rooms, dense coverage
    for _ in range(3):
        w.add(multi([rand_case(rnd, 5, 5) for _ in range(3000)]))
    # medium
    w.add(multi([rand_case(rnd, 20, 20) for _ in range(5000)]))
    # large / max t
    w.add(multi([rand_case(rnd, 100, 100) for _ in range(10**4)]))
    # skinny rooms
    w.add(
        multi(
            [rand_case(rnd, 1, 100) for _ in range(2000)]
            + [rand_case(rnd, 100, 1) for _ in range(2000)]
            + [rand_case(rnd, 2, 100) for _ in range(2000)]
            + [rand_case(rnd, 100, 2) for _ in range(2000)]
        )
    )


if __name__ == "__main__":
    main(sys.argv[1])
