import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(n, m, grid):
    lines = [f"{n} {m}"] + [" ".join(map(str, row)) for row in grid]
    return "\n".join(lines)


def rand_case(rnd, n, m, lo=-10**9, hi=10**9):
    vals = rnd.sample(range(lo, hi), n * m) if hi - lo > n * m * 2 else None
    if vals is None:
        vals = rnd.sample(range(-(n * m * 3), n * m * 3), n * m)
    grid = [vals[i * m:(i + 1) * m] for i in range(n)]
    return case(n, m, grid)


def max_at(rnd, n, m, i, j):
    """Grid with the maximum forced at cell (i, j) (0-indexed)."""
    vals = rnd.sample(range(-10**9, 10**9 - 10), n * m - 1)
    grid = []
    it = iter(vals)
    for r in range(n):
        row = []
        for c in range(m):
            row.append(10**9 if (r, c) == (i, j) else next(it))
        grid.append(row)
    return case(n, m, grid)


def main(outdir):
    rnd = random.Random(16951)
    w = Writer(outdir)
    # edges: 1x1, 1xm, nx1, max in every corner / center
    edge = [
        case(1, 1, [[-1000000000]]),
        case(1, 1, [[1000000000]]),
        rand_case(rnd, 1, 40),
        rand_case(rnd, 40, 1),
        max_at(rnd, 3, 3, 1, 1),
        max_at(rnd, 40, 40, 0, 0),
        max_at(rnd, 40, 40, 39, 39),
        max_at(rnd, 40, 40, 0, 39),
        max_at(rnd, 40, 40, 39, 0),
        max_at(rnd, 40, 40, 20, 20),
        max_at(rnd, 39, 40, 19, 20),
        case(2, 2, [[1, 2], [3, 4]]),
    ]
    w.add(multi(edge[:12]))
    # small random grids
    for _ in range(4):
        cases = [rand_case(rnd, rnd.randint(1, 6), rnd.randint(1, 6))
                 for _ in range(20)]
        w.add(multi(cases))
    # random max positions on larger grids
    for _ in range(3):
        cases = []
        for _ in range(20):
            n, m = rnd.randint(1, 40), rnd.randint(1, 40)
            cases.append(max_at(rnd, n, m, rnd.randrange(n), rnd.randrange(m)))
        w.add(multi(cases))
    # max-size: t = 20 grids of 40x40
    cases = [rand_case(rnd, 40, 40) for _ in range(20)]
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
