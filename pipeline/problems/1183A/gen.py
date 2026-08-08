import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1183)
    w = Writer(outdir)
    for a in (1, 2, 3, 4, 8, 99, 100, 997, 998, 999, 1000, 432, 237, 42):
        w.add(str(a))
    for _ in range(6):
        w.add(str(rnd.randint(1, 1000)))


if __name__ == "__main__":
    main(sys.argv[1])
