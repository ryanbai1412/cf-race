import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

NMAX = 10**9


def main(outdir):
    rnd = random.Random(1393)
    w = Writer(outdir)

    # single smallest / largest
    w.add(multi(["1"]))
    w.add(multi([str(NMAX)]))
    # all small n
    w.add(multi([str(n) for n in range(1, 101)]))
    # extremes and parity boundaries, max T
    edge = [1, 2, 3, 4, 5, NMAX, NMAX - 1, 999999999, 1000000000, 2, 1]
    w.add(multi([str(edge[i % len(edge)]) for i in range(100)]))
    # powers of two and of ten
    vals = [2**k for k in range(30)] + [10**k for k in range(10)]
    w.add(multi([str(v) for v in vals[:100]]))
    # random tests
    for _ in range(12):
        t = rnd.randint(1, 100)
        w.add(multi([str(rnd.randint(1, NMAX)) for _ in range(t)]))


if __name__ == "__main__":
    main(sys.argv[1])
