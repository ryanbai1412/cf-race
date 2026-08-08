import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1647)
    w = Writer(outdir)
    # exhaustive small values and boundary values
    w.add(multi([str(n) for n in range(1, 101)]))
    w.add(multi(["998", "999", "1000", "1", "2", "3"]))
    # full range, max t
    vals = list(range(1, 1001))
    rnd.shuffle(vals)
    w.add(multi([str(v) for v in vals[:1000]]))


if __name__ == "__main__":
    main(sys.argv[1])
