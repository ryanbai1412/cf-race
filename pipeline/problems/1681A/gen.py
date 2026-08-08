import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(rnd, n, m, lo=1, hi=50):
    a = [rnd.randint(lo, hi) for _ in range(n)]
    b = [rnd.randint(lo, hi) for _ in range(m)]
    return f"{n}\n{' '.join(map(str, a))}\n{m}\n{' '.join(map(str, b))}"


def main(outdir):
    rnd = random.Random(1681)
    w = Writer(outdir)
    # edge: minimal sizes, equal/unequal values
    w.add(multi(["1\n1\n1\n1", "1\n1\n1\n50", "1\n50\n1\n1", "1\n50\n1\n50"]))
    # equal maxima cases
    w.add(multi([case(rnd, rnd.randint(1, 50), rnd.randint(1, 50)) for _ in range(200)]))
    # small values to force many ties
    w.add(multi([case(rnd, rnd.randint(1, 10), rnd.randint(1, 10), 1, 3) for _ in range(300)]))
    for _ in range(5):
        w.add(multi([case(rnd, rnd.randint(1, 50), rnd.randint(1, 50)) for _ in range(rnd.randint(1, 100))]))
    # max size: t=1000 full-size cases
    w.add(multi([case(rnd, 50, 50) for _ in range(1000)]))


if __name__ == "__main__":
    main(sys.argv[1])
