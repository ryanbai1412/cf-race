import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(16582)
    w = Writer(outdir)
    # every n from 1..100
    w.add(multi([str(n) for n in range(1, 101)]))
    # edges
    w.add(multi(["1", "2", "999", "1000"]))
    # random n, max t
    for _ in range(2):
        w.add(multi([str(rnd.randint(1, 1000)) for _ in range(1000)]))
    # all large even/odd
    w.add(multi([str(n) for n in range(901, 1001)]))


if __name__ == "__main__":
    main(sys.argv[1])
