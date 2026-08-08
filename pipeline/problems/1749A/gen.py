import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(n, rooks):
    return f"{n} {len(rooks)}\n" + "\n".join(f"{x} {y}" for x, y in rooks)


def rand_case(rnd, n, m):
    rows = rnd.sample(range(1, n + 1), m)
    cols = rnd.sample(range(1, n + 1), m)
    return case(n, list(zip(rows, cols)))


def main(outdir):
    rnd = random.Random(1749)
    w = Writer(outdir)
    # edges: 1x1 board full; n=8 full diagonal; single rook cases
    w.add(multi([case(1, [(1, 1)]),
                 case(8, [(i, i) for i in range(1, 9)]),
                 case(8, [(i, 9 - i) for i in range(1, 9)]),
                 case(8, [(4, 5)]),
                 case(2, [(1, 1), (2, 2)])]))
    # all (n, m) combos with 1 <= m <= n <= 8
    combos = []
    for n in range(1, 9):
        for m in range(1, n + 1):
            combos.append(rand_case(rnd, n, m))
    w.add(multi(combos))
    # max t=2000 random
    def rc():
        n = rnd.randint(1, 8)
        return rand_case(rnd, n, rnd.randint(1, n))
    w.add(multi([rc() for _ in range(2000)]))
    for _ in range(5):
        w.add(multi([rc() for _ in range(rnd.randint(1, 50))]))


if __name__ == "__main__":
    main(sys.argv[1])
