import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1348)
    w = Writer(outdir)
    # all possible values of n
    w.add(multi([str(n) for n in range(2, 31, 2)]))
    # edges
    w.add(multi(["2", "30"]))
    # random max-size
    for _ in range(4):
        w.add(multi([str(2 * rnd.randint(1, 15)) for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
