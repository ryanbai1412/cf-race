import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1186)
    w = Writer(outdir)
    fixed = [(5, 8, 6), (3, 9, 3), (8, 5, 20), (1, 1, 1), (100, 100, 100),
             (100, 99, 100), (100, 100, 99), (1, 100, 100), (100, 1, 1), (2, 2, 1)]
    for t in fixed:
        w.add(" ".join(map(str, t)))
    for _ in range(10):
        w.add(" ".join(str(rnd.randint(1, 100)) for _ in range(3)))


if __name__ == "__main__":
    main(sys.argv[1])
