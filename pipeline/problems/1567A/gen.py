import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def rand_row(rnd, n, p_vert):
    """Build a valid row of a 2xn domino tiling and return it."""
    row = []
    i = 0
    while i < n:
        if i + 1 < n and rnd.random() >= p_vert:
            row += ["L", "R"]
            i += 2
        else:
            row.append(rnd.choice("UD"))
            i += 1
    return "".join(row)


def case(s):
    return f"{len(s)}\n{s}"


def main(outdir):
    rnd = random.Random(1567)
    w = Writer(outdir)

    # edges: n=1, n=2, all-vertical, all-horizontal
    w.add(multi([case("U"), case("D"), case("LR"), case("UU"), case("DD"), case("UD")]))
    w.add(multi([case("LR" * 50), case("U" * 100), case("D" * 100),
                 case("".join(rnd.choice("UD") for _ in range(99)))]))
    # random mixes
    for p in (0.1, 0.5, 0.9):
        w.add(multi([case(rand_row(rnd, rnd.randint(1, 100), p)) for _ in range(200)]))
    # max: t=5000, n=100
    w.add(multi([case(rand_row(rnd, 100, rnd.random())) for _ in range(5000)]))


if __name__ == "__main__":
    main(sys.argv[1])
