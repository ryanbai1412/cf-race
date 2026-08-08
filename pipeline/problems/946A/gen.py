import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402


def case(a):
    return f"{len(a)}\n{' '.join(map(str, a))}"


def main(outdir):
    rnd = random.Random(946)
    w = Writer(outdir)
    # edge: single element
    w.add(case([0]))
    w.add(case([-100]))
    w.add(case([100]))
    # all negative / all positive / all zero
    w.add(case([-100] * 100))
    w.add(case([100] * 100))
    w.add(case([0] * 100))
    # mixed extremes
    w.add(case([-100, 100] * 50))
    # random tests of varying size
    for _ in range(8):
        n = rnd.randint(1, 100)
        w.add(case([rnd.randint(-100, 100) for _ in range(n)]))
    # small values around zero
    for _ in range(3):
        n = rnd.randint(1, 100)
        w.add(case([rnd.randint(-2, 2) for _ in range(n)]))


if __name__ == "__main__":
    main(sys.argv[1])
