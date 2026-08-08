import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1173)
    w = Writer(outdir)
    fixed = [(0, 0, 0), (100, 100, 100), (0, 0, 100), (100, 0, 0), (0, 100, 0),
             (5, 5, 1), (5, 4, 1), (5, 3, 1), (50, 51, 1), (100, 99, 1), (1, 0, 1), (0, 1, 1)]
    for x, y, z in fixed:
        w.add(f"{x} {y} {z}")
    for _ in range(8):
        w.add(f"{rnd.randint(0, 100)} {rnd.randint(0, 100)} {rnd.randint(0, 100)}")


if __name__ == "__main__":
    main(sys.argv[1])
