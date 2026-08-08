import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1714)
    w = Writer(outdir)
    # every possible s in one max test (t=45)
    w.add(multi([str(s) for s in range(1, 46)]))
    # extremes alone
    w.add(multi(["1"]))
    w.add(multi(["45"]))
    w.add(multi(["44"]))
    # random subsets
    for _ in range(4):
        vals = rnd.sample(range(1, 46), rnd.randint(1, 45))
        w.add(multi([str(v) for v in vals]))


if __name__ == "__main__":
    main(sys.argv[1])
