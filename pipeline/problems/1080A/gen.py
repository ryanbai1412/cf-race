import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


M = 10 ** 8


def case(n, k):
    return f"{n} {k}"


def main(outdir):
    rnd = random.Random(1080)
    w = Writer(outdir)
    w.add(case(1, 1))
    w.add(case(1, M))
    w.add(case(M, 1))
    w.add(case(M, M))
    w.add(case(M, 2))
    w.add(case(M, 5))
    w.add(case(M, 8))
    w.add(case(M, M - 1))
    w.add(case(1, 2))
    w.add(case(1, 8))
    w.add(case(3, 6))
    w.add(case(4, 8))
    w.add(case(M - 1, M))
    for _ in range(7):
        w.add(case(rnd.randint(1, M), rnd.randint(1, M)))


if __name__ == "__main__":
    main(sys.argv[1])
