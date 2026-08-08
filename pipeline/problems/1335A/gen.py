import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1335)
    w = Writer(outdir)
    M = 2 * 10 ** 9
    # edges
    w.add(multi(["1", "2", "3", "4", str(M), str(M - 1)]))
    # all small values
    w.add(multi([str(n) for n in range(1, 201)]))
    # random
    for _ in range(3):
        w.add(multi([str(rnd.randint(1, 100)) for _ in range(5000)]))
    for _ in range(3):
        w.add(multi([str(rnd.randint(1, M)) for _ in range(10000)]))


if __name__ == "__main__":
    main(sys.argv[1])
