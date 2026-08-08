import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402


def case(a):
    return f"{len(a)}\n" + " ".join(map(str, a)) + "\n"


def main(outdir):
    rnd = random.Random(1092)
    w = Writer(outdir)
    # minimum n
    w.add(case([1, 1]))
    w.add(case([1, 100]))
    w.add(case([100, 100]))
    # max n, all equal (answer 0)
    w.add(case([7] * 100))
    # max n, worst spread
    w.add(case([1] * 50 + [100] * 50))
    # max n, all distinct-ish increasing
    w.add(case([i % 100 + 1 for i in range(100)]))
    # already-paired duplicates
    w.add(case([v for v in range(1, 51) for _ in (0, 1)]))
    for n in (2, 4, 10, 50, 100):
        for _ in range(2):
            w.add(case([rnd.randint(1, 100) for _ in range(n)]))
    for _ in range(3):
        w.add(case([rnd.randint(1, 5) for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
