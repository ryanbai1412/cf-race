import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1283)
    w = Writer(outdir)
    allc = [f"{h} {m}" for h in range(24) for m in range(60) if h or m]
    # all 1439 possible times
    w.add(multi(allc))
    w.add(multi(["0 1"]))
    w.add(multi(["23 59"]))
    w.add(multi(["1 0"]))
    for _ in range(6):
        t = rnd.randint(1, 1439)
        w.add(multi([rnd.choice(allc) for _ in range(t)]))


if __name__ == "__main__":
    main(sys.argv[1])
