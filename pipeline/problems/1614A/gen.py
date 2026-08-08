import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

M = 10 ** 9


def case(rnd, n, vmax, kmax):
    l = rnd.randint(1, vmax)
    r = rnd.randint(l, vmax)
    k = rnd.randint(1, kmax)
    a = [rnd.randint(1, vmax) for _ in range(n)]
    return f"{n} {l} {r} {k}\n" + " ".join(map(str, a))


def main(outdir):
    rnd = random.Random(1614)
    w = Writer(outdir)
    # edges: single item, all too cheap/expensive, exact budget
    w.add(multi([
        "1 1 1 1\n1",
        f"1 1 {M} {M}\n{M}",
        "3 5 10 100\n1 2 4",
        "3 1 4 100\n5 6 7",
        "4 2 5 7\n2 2 3 5",
        f"2 1 {M} 1\n{M} {M}",
        f"100 1 {M} {M}\n" + " ".join(["1"] * 100),
    ]))
    # random small values
    for _ in range(4):
        w.add(multi([case(rnd, rnd.randint(1, 10), 10, 20)
                     for _ in range(100)]))
    # random large
    for _ in range(4):
        w.add(multi([case(rnd, rnd.randint(1, 100), M, M)
                     for _ in range(100)]))
    # max size
    w.add(multi([case(rnd, 100, M, M) for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
