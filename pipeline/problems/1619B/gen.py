import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

M = 10 ** 9


def main(outdir):
    rnd = random.Random(16192)
    w = Writer(outdir)
    # edges: 1, max, perfect powers and neighbors
    w.add(multi(["1", "2", "3", "4", "8", "9", str(M)]))
    boundary = []
    for b in [10 ** 9, 999950884, 999970029, 998244353, 64, 729, 46656]:
        for d in (-1, 0, 1):
            v = b + d
            if 1 <= v <= M:
                boundary.append(str(v))
    w.add(multi(boundary[:20]))
    # squares/cubes/sixth powers +- 1
    vals = []
    for x in [2, 3, 10, 100, 1000, 31622, 31623]:
        vals.append(str(x * x))
        vals.append(str(x * x - 1))
    for x in [2, 3, 10, 100, 1000]:
        vals.append(str(x ** 3))
        vals.append(str(x ** 3 + 1))
    w.add(multi(vals[:20]))
    # random small
    w.add(multi([str(rnd.randint(1, 1000)) for _ in range(20)]))
    # random large, max t
    for _ in range(3):
        w.add(multi([str(rnd.randint(1, M)) for _ in range(20)]))


if __name__ == "__main__":
    main(sys.argv[1])
