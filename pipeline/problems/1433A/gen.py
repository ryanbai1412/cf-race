import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

ALL = [str(d) * L for d in range(1, 10) for L in range(1, 5)]


def case(x):
    return str(x)


def main(outdir):
    rnd = random.Random(1433)
    w = Writer(outdir)
    # every boring apartment, one per test case (t = 36 = max)
    w.add(multi([case(x) for x in ALL]))
    # minimum: single smallest / single largest
    w.add(multi(["1"]))
    w.add(multi(["9999"]))
    # single-digit only and 4-digit only
    w.add(multi([str(d) for d in range(1, 10)]))
    w.add(multi([str(d) * 4 for d in range(1, 10)]))
    # random selections
    for _ in range(10):
        t = rnd.randint(1, 36)
        w.add(multi([case(rnd.choice(ALL)) for _ in range(t)]))


if __name__ == "__main__":
    main(sys.argv[1])
