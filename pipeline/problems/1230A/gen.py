import itertools
import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402


def case(a):
    return " ".join(map(str, a)) + "\n"


def main(outdir):
    rnd = random.Random(1230)
    w = Writer(outdir)
    w.add(case([1, 1, 1, 1]))
    w.add(case([100, 100, 100, 100]))
    w.add(case([1, 1, 1, 3]))       # YES: 3 vs 1+1+1
    w.add(case([1, 2, 3, 100]))     # NO
    w.add(case([100, 1, 1, 98]))    # YES: 100 vs 1+1+98
    w.add(case([1, 1, 2, 100]))
    w.add(case([2, 3, 4, 5]))       # YES: 2+5 vs 3+4
    # exhaustive-ish small randoms
    for _ in range(8):
        w.add(case([rnd.randint(1, 6) for _ in range(4)]))
    for _ in range(5):
        w.add(case([rnd.randint(1, 100) for _ in range(4)]))


if __name__ == "__main__":
    main(sys.argv[1])
