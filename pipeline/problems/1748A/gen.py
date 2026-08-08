import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1748)
    w = Writer(outdir)
    # all small n
    w.add(multi([str(n) for n in range(1, 51)]))
    # extremes and parity edges near 1e9
    w.add(multi(["1", "2", "999999999", "1000000000", "999999998"]))
    # max t=1e4 random
    w.add(multi([str(rnd.randint(1, 10**9)) for _ in range(10**4)]))
    for _ in range(4):
        w.add(multi([str(rnd.randint(1, 10**9)) for _ in range(rnd.randint(1, 100))]))


if __name__ == "__main__":
    main(sys.argv[1])
