import itertools
import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(grid):
    return f"{len(grid)} {len(grid[0])}\n" + "\n".join(grid)


def rand_grid(rnd, n, m, p):
    while True:
        g = [
            "".join("R" if rnd.random() < p else "E" for _ in range(m))
            for _ in range(n)
        ]
        if any("R" in row for row in g):
            return g


def main(outdir):
    rnd = random.Random(16802)
    w = Writer(outdir)
    # edges: 1x1, single row/col, corner robot, full grid
    edge = [
        case(["R"]),
        case(["ER" + "E" * 3]),
        case(["E", "E", "E", "E", "R"]),
        case(["R" * 5] * 5),
        case(["EEEEE", "EEEEE", "EEEEE", "EEEEE", "EEEER"]),
        case(["EREEE", "REEEE", "EEEEE", "EEEEE", "EEEEE"]),
    ]
    w.add(multi(edge))
    # exhaustive: all non-empty 2x2 grids and all non-empty 1xM (m<=3) grids
    cs = []
    for bits in itertools.product("ER", repeat=4):
        if "R" in bits:
            cs.append(case(["".join(bits[:2]), "".join(bits[2:])]))
    for m in (1, 2, 3):
        for bits in itertools.product("ER", repeat=m):
            if "R" in bits:
                cs.append(case(["".join(bits)]))
                cs.append(case(list(bits)))
    w.add(multi(cs))
    # random sparse and dense
    for p in (0.1, 0.3, 0.6, 0.9):
        cs = []
        for _ in range(1000):
            n, m = rnd.randint(1, 5), rnd.randint(1, 5)
            cs.append(case(rand_grid(rnd, n, m, p)))
        w.add(multi(cs))
    # max t
    cs = []
    for _ in range(5000):
        n, m = rnd.randint(1, 5), rnd.randint(1, 5)
        cs.append(case(rand_grid(rnd, n, m, rnd.random())))
    w.add(multi(cs))


if __name__ == "__main__":
    main(sys.argv[1])
