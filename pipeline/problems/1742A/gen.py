import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1742)
    w = Writer(outdir)
    # exhaustive: all 21^3 = 9261 triples (t max)
    w.add(multi([f"{a} {b} {c}" for a in range(21) for b in range(21) for c in range(21)]))
    # edges
    w.add(multi(["0 0 0", "20 20 20", "0 0 20", "20 0 20", "0 20 20", "10 10 20"]))
    # random
    for _ in range(6):
        t = rnd.randint(1, 200)
        w.add(multi([f"{rnd.randint(0, 20)} {rnd.randint(0, 20)} {rnd.randint(0, 20)}" for _ in range(t)]))


if __name__ == "__main__":
    main(sys.argv[1])
