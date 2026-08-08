import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402


def case(grid):
    return f"{len(grid)}\n" + "\n".join(grid) + "\n"


def main(outdir):
    rnd = random.Random(1106)
    w = Writer(outdir)
    # n too small for any cross
    w.add(case(["X"]))
    w.add(case(["."]))
    w.add(case(["XX", "XX"]))
    # all X, maximum n -> (n-2)^2 crosses
    n = 500
    w.add(case(["X" * n] * n))
    # all dots, maximum n
    w.add(case(["." * n] * n))
    # single cross in the middle of a big empty grid
    g = [["."] * n for _ in range(n)]
    for di, dj in ((0, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)):
        g[250 + di][250 + dj] = "X"
    w.add(case(["".join(r) for r in g]))
    # checkerboard patterns (dense crosses on one parity)
    w.add(case(["".join("X" if (i + j) % 2 == 0 else "." for j in range(n))
                for i in range(n)]))
    w.add(case(["".join("X" if (i + j) % 2 == 1 else "." for j in range(n))
                for i in range(n)]))
    # borders only: X ring, no crosses
    g = [["." for _ in range(n)] for _ in range(n)]
    for i in range(n):
        g[0][i] = g[n - 1][i] = g[i][0] = g[i][n - 1] = "X"
    w.add(case(["".join(r) for r in g]))
    # random densities, small and large
    for m in (3, 4, 5, 10):
        for _ in range(2):
            w.add(case(["".join(rnd.choice("X.") for _ in range(m))
                        for _ in range(m)]))
    for p in (0.5, 0.8, 0.95):
        m = 500
        w.add(case(["".join("X" if rnd.random() < p else "." for _ in range(m))
                    for _ in range(m)]))


if __name__ == "__main__":
    main(sys.argv[1])
