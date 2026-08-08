import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1766)
    w = Writer(outdir)
    # edges: powers of ten and neighbors, min/max
    edge = ["1", "9", "10", "11", "99", "100", "101", "999", "1000", "9999",
            "10000", "99999", "100000", "500000", "999998", "999999"]
    w.add(multi(edge))
    # every extremely round number and its +-1 neighbors
    er = [d * 10**k for d in range(1, 10) for k in range(6) if d * 10**k <= 999999]
    vals = sorted({v for x in er for v in (x - 1, x, x + 1) if 1 <= x + 1 and 1 <= v <= 999999})
    w.add(multi([str(v) for v in vals]))
    # random, max t
    for _ in range(3):
        w.add(multi([str(rnd.randint(1, 999999)) for _ in range(10000)]))
    w.add(multi([str(rnd.randint(1, 999)) for _ in range(10000)]))


if __name__ == "__main__":
    main(sys.argv[1])
