import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1223)
    w = Writer(outdir)
    # all small values + extremes
    w.add(multi([str(n) for n in range(2, 22)]))
    w.add(multi(["2"]))
    w.add(multi(["3"]))
    w.add(multi([str(10**9), str(10**9 - 1)]))
    # randoms, max q=100
    for _ in range(4):
        w.add(multi([str(rnd.randint(2, 10**9)) for _ in range(100)]))
    w.add(multi([str(rnd.randint(2, 50)) for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
