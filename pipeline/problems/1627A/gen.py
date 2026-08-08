import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(n, m, r, c, grid):
    return f"{n} {m} {r} {c}\n" + "\n".join(grid)


def rand_grid(rnd, n, m, pb):
    return ["".join("B" if rnd.random() < pb else "W" for _ in range(m)) for _ in range(n)]


def rand_case(rnd, nmax, mmax, pb=None):
    n = rnd.randint(1, nmax)
    m = rnd.randint(1, mmax)
    if pb is None:
        pb = rnd.choice([0.0, 0.02, 0.1, 0.5, 0.9, 1.0])
    return case(n, m, rnd.randint(1, n), rnd.randint(1, m), rand_grid(rnd, n, m, pb))


def main(outdir):
    rnd = random.Random(1627)
    w = Writer(outdir)

    # edges: 1x1 both colors, all white, all black, single B far away
    g = ["W" * 50 for _ in range(50)]
    far = ["W" * 50] * 49 + ["W" * 49 + "B"]
    onerow = ["W" * 25 + "B" + "W" * 24]
    w.add(
        multi(
            [
                case(1, 1, 1, 1, ["B"]),
                case(1, 1, 1, 1, ["W"]),
                case(50, 50, 25, 25, g),
                case(50, 50, 1, 1, ["B" * 50 for _ in range(50)]),
                case(50, 50, 1, 1, far),
                case(1, 50, 1, 1, onerow),
                case(50, 1, 1, 1, ["W"] * 49 + ["B"]),
                case(2, 2, 1, 1, ["WB", "WW"]),
                case(2, 2, 1, 1, ["WW", "WB"]),
                case(2, 2, 1, 1, ["WW", "BW"]),
            ]
        )
    )

    # tiny grids, dense coverage of all answer classes
    for _ in range(2):
        w.add(multi([rand_case(rnd, 3, 3) for _ in range(100)]))
    # small
    w.add(multi([rand_case(rnd, 6, 6) for _ in range(100)]))
    # sparse large grids (answers 1/2/-1 likely)
    w.add(multi([rand_case(rnd, 50, 50, 0.002) for _ in range(100)]))
    # general max-size
    w.add(multi([rand_case(rnd, 50, 50) for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
