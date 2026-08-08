import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402


def main(outdir):
    rnd = random.Random(1091)
    w = Writer(outdir)
    # extremes and boundary cases (each bound binding in turn)
    w.add("1 2 3")
    w.add("100 100 100")
    w.add("1 100 100")
    w.add("100 2 100")
    w.add("100 100 3")
    w.add("50 51 52")
    w.add("50 100 100")
    w.add("100 51 100")
    w.add("100 100 52")
    w.add("99 100 100")
    for _ in range(8):
        y = rnd.randint(1, 100)
        b = rnd.randint(2, 100)
        r = rnd.randint(3, 100)
        w.add(f"{y} {b} {r}")


if __name__ == "__main__":
    main(sys.argv[1])
