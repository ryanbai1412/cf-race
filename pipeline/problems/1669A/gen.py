import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1669)
    w = Writer(outdir)
    # all boundary ratings
    w.add(multi(list(map(str, [
        -5000, 0, 1398, 1399, 1400, 1401, 1598, 1599, 1600, 1601,
        1898, 1899, 1900, 1901, 5000,
    ]))))
    # dense sweep around each boundary
    w.add(multi([str(x) for b in (1400, 1600, 1900) for x in range(b - 20, b + 21)]))
    # random full range
    for _ in range(3):
        w.add(multi([str(rnd.randint(-5000, 5000)) for _ in range(2000)]))
    # max t
    w.add(multi([str(rnd.randint(-5000, 5000)) for _ in range(10000)]))


if __name__ == "__main__":
    main(sys.argv[1])
