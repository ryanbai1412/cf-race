import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

M = 10**9


def main(outdir):
    rnd = random.Random(1716)
    w = Writer(outdir)
    # all small values
    w.add(multi([str(n) for n in range(1, 101)]))
    # boundary values around multiples of 3 near max
    w.add(multi([str(M), str(M - 1), str(M - 2), str(M - 3), "1", "2", "3", "4"]))
    # random
    for _ in range(4):
        w.add(multi([str(rnd.randint(1, M)) for _ in range(5000)]))
    # max-size test
    w.add(multi([str(rnd.randint(M - 100, M)) for _ in range(10**4)]))


if __name__ == "__main__":
    main(sys.argv[1])
