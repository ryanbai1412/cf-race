import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1525)
    w = Writer(outdir)
    # all possible k values (k = 1..100), max t = 100
    w.add(multi([str(k) for k in range(1, 101)]))
    # edges
    w.add(multi(["1", "100", "50", "99", "97"]))
    # random
    for _ in range(3):
        w.add(multi([str(rnd.randint(1, 100)) for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
