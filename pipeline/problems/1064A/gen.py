import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(v):
    return " ".join(map(str, v))


def main(outdir):
    rnd = random.Random(1064)
    w = Writer(outdir)
    w.add(case([1, 1, 1]))
    w.add(case([1, 1, 100]))
    w.add(case([100, 1, 1]))
    w.add(case([100, 100, 100]))
    w.add(case([1, 2, 3]))       # degenerate, needs 1
    w.add(case([3, 1, 2]))
    w.add(case([50, 50, 100]))
    w.add(case([50, 100, 50]))
    w.add(case([1, 50, 100]))
    w.add(case([2, 2, 3]))
    for _ in range(6):
        w.add(case([rnd.randint(1, 5) for _ in range(3)]))
    for _ in range(4):
        w.add(case([rnd.randint(1, 100) for _ in range(3)]))


if __name__ == "__main__":
    main(sys.argv[1])
