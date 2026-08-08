import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAXV = 10**9


def case(rnd, n, lo=1, hi=MAXV):
    a = [rnd.randint(lo, hi) for _ in range(n)]
    b = [rnd.randint(lo, hi) for _ in range(n)]
    return f"{n}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}"


def main(outdir):
    rnd = random.Random(1661)
    w = Writer(outdir)
    # minimum n, extreme values
    w.add(multi(["2\n1 1000000000\n1000000000 1"]))
    w.add(multi(["2\n1 1\n1 1", "2\n1000000000 1000000000\n1000000000 1000000000"]))
    # already-balanced (swap makes sum 0)
    w.add(multi(["4\n3 3 10 10\n10 10 3 3"]))
    # small random values (forces ties / equal elements)
    w.add(multi([case(rnd, rnd.randint(2, 25), 1, 3) for _ in range(200)]))
    w.add(multi([case(rnd, rnd.randint(2, 25), 1, 10) for _ in range(200)]))
    # random full-range
    for _ in range(4):
        w.add(multi([case(rnd, rnd.randint(2, 25)) for _ in range(100)]))
    # max size: t=4000, all n=25
    w.add(multi([case(rnd, 25) for _ in range(4000)]))
    # max size, small values
    w.add(multi([case(rnd, 25, 1, 2) for _ in range(4000)]))


if __name__ == "__main__":
    main(sys.argv[1])
