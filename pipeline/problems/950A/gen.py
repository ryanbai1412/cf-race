import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402


def main(outdir):
    rnd = random.Random(950)
    w = Writer(outdir)
    # edges
    w.add("0 0 0")
    w.add("100 100 100")
    w.add("0 0 100")
    w.add("100 0 0")
    w.add("0 100 0")
    w.add("0 0 1")
    w.add("100 0 100")
    w.add("0 100 99")
    w.add("1 100 0")
    # random
    for _ in range(6):
        w.add(f"{rnd.randint(0, 100)} {rnd.randint(0, 100)} {rnd.randint(0, 100)}")
    # small values
    for _ in range(2):
        w.add(f"{rnd.randint(0, 3)} {rnd.randint(0, 3)} {rnd.randint(0, 3)}")


if __name__ == "__main__":
    main(sys.argv[1])
