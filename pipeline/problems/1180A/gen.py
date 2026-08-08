import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def main(outdir):
    rnd = random.Random(1180)
    w = Writer(outdir)
    for n in (1, 2, 3, 4, 5, 10, 50, 99, 100):
        w.add(str(n))
    for _ in range(10):
        w.add(str(rnd.randint(1, 100)))


if __name__ == "__main__":
    main(sys.argv[1])
