import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402

LIMIT = 2 * 10 ** 9


def main(outdir):
    rnd = random.Random(1102)
    w = Writer(outdir)
    # smallest values cover all four residues of n mod 4
    for n in range(1, 9):
        w.add(str(n))
    # upper bound and its neighbourhood
    for n in (LIMIT, LIMIT - 1, LIMIT - 2, LIMIT - 3):
        w.add(str(n))
    # 64-bit overflow bait: n*(n+1)/2 ~ 2e18
    w.add(str(1999999999))
    for _ in range(6):
        w.add(str(rnd.randint(1, LIMIT)))


if __name__ == "__main__":
    main(sys.argv[1])
