import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(n, s):
    return f"{n} {s}"


def main(outdir):
    rnd = random.Random(1061)
    w = Writer(outdir)
    w.add(case(1, 1))
    w.add(case(1, 10 ** 9))
    w.add(case(100000, 1))
    w.add(case(100000, 10 ** 9))
    w.add(case(100000, 100000))
    w.add(case(100000, 100001))
    w.add(case(99999, 10 ** 9))
    w.add(case(2, 10 ** 9))
    w.add(case(3, 10 ** 9))
    w.add(case(7, 7))
    w.add(case(7, 8))
    w.add(case(10 ** 5, 10 ** 9 - 1))
    for _ in range(6):
        w.add(case(rnd.randint(1, 100000), rnd.randint(1, 10 ** 9)))


if __name__ == "__main__":
    main(sys.argv[1])
